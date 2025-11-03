"""
Модуль для выполнение RSA шифрования: функции шифрования и расшифровки
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
