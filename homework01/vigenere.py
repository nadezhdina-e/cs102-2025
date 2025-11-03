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
    for i in range(len(plaintext)):
        j = i % len(keyword)
        if keyword[j].isalpha():
            if keyword[j].isupper():
                shift = ord(keyword[j]) - ord('A')
            else:
                shift = ord(keyword[j]) - ord('a')
        if plaintext[i].isalpha():
            if plaintext[i].isupper():
                start = ord('A')
            else:
                start = ord('a')
            ciphertext += chr((ord(plaintext[i]) - start + shift) % abc_length + start)
        else:
            ciphertext += plaintext[i]
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
    for i in range(len(ciphertext)):
        j = i % len(keyword)
        if keyword[j].isalpha():
            if keyword[j].isupper():
                shift = ord(keyword[j]) - ord('A')
            else:
                shift = ord(keyword[j]) - ord('a')
        if ciphertext[i].isalpha():
            if ciphertext[i].isupper():
                start = ord('A')
            else:
                start = ord('a')
            plaintext += chr((ord(ciphertext[i]) - start - shift) % abc_length + start)
        else:
            plaintext += ciphertext[i]
    return plaintext

