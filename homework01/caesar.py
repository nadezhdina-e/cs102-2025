def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """

    abc_length = 26
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            if char.isupper():
                start = ord('A')
            else:
                start = ord('a')
            ciphertext += chr((ord(char) - start + shift) % abc_length + start)
        else:
            ciphertext += char
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ''
    abc_length = 26
    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                start = ord('A')
            else:
                start = ord('a')
            plaintext += chr((ord(char) - start - shift) % abc_length + start)
        else:
            plaintext += char
    return plaintext

print(decrypt_caesar("sbwkrq"))
