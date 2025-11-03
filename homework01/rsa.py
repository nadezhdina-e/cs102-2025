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
    elif n == 2:
        return True
    elif n % 2 == 0:  # для ускорения перебора в последнем уровне цикла
        return False
    else:
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
    return True
