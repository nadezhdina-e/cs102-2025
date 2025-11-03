"""
Модуль для выполнение RSA шифрования: функции шифрования и расшифровки
"""

import random
from typing import Tuple


"""
Функция определяет, является ли число, выбранное пользователем, простым
"""


def is_prime(n: int) -> bool:
    """
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:  # для ускорения перебора в последнем уровне цикла
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


"""
Функция определяет НОД двух чисел: рандомного е на промежутке от 1 до phi и 
phi - численного значения функции эйлера для n
"""


def gcd(a: int, b: int) -> int:
    """
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    while b != 0:
        a, b = b, a % b
    return a


"""
Вычисление d такого что d*e mod phi = 1
"""


def multiplicative_inverse(e: int, phi: int) -> int:
    """
    >>> multiplicative_inverse(7, 40)
    23
    """
    original_phi = phi
    y, x = 1, 0
    while e > 1:
        q = e // phi
        e, phi = phi, e % phi
        y, x = x, y - q * x
    if y < 0:
        y += original_phi
    return y


"""
Итоговая функция генерации двойного ключа шифрования
"""


def generate_keypair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    elif p == q:
        raise ValueError("p and q cannot be equal")
    else:
        n = p * q
        phi = (p - 1) * (q - 1)
        e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = multiplicative_inverse(e, phi)
    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return (e, n), (d, n)
