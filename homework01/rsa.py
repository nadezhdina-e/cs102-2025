"""
Модуль для выполнение RSA шифрования: функции шифрования и расшифровки
"""

import random
from typing import Tuple

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


def generate_keypair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Генерирует пару ключей (публичный и приватный) на основе двух простых чисел p и q.
    return: Кортеж из двух кортежей: публичного ключа (e, n) и приватного ключа (d, n).
    raises ValueError: Если p или q не являются простыми числами или если p равно q.
    """
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    if p == q:
        raise ValueError("p and q cannot be equal")
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
