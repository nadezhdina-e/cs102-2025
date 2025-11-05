def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    abc_length = 26
    for i, char in enumerate(plaintext):
        element_defining_shift = i % len(keyword)
        shift = 0
        if keyword[element_defining_shift].isalpha():
            if keyword[element_defining_shift].isupper():
                shift = ord(keyword[element_defining_shift]) - ord("A")
            else:
                shift = ord(keyword[element_defining_shift]) - ord("a")
        if char.isalpha():
            if char.isupper():
                start = ord("A")
            else:
                start = ord("a")
            ciphertext += chr((ord(char) - start + shift) % abc_length + start)
        else:
            ciphertext += char
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    abc_length = 26
    for i, char in enumerate(ciphertext):
        element_defining_shift = i % len(keyword)
        shift = 0
        if keyword[element_defining_shift].isalpha():
            if keyword[element_defining_shift].isupper():
                shift = ord(keyword[element_defining_shift]) - ord("A")
            else:
                shift = ord(keyword[element_defining_shift]) - ord("a")
        if char.isalpha():
            if char.isupper():
                start = ord("A")
            else:
                start = ord("a")
            plaintext += chr((ord(char) - start - shift) % abc_length + start)
        else:
            plaintext += char
    return plaintext
