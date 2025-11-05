def encrypt_scytale(plaintext, n):
    """
    Функция записывает строку в виде матрицы и переписывает ее в порядке,
    соответствующем методу шифрования Скитла
    """
    matrix = []
    j = 0
    while j < len(plaintext):
        temporary_row = []
        for i in range(n):
            if (i + j) < len(plaintext):
                if plaintext[i + j] == " ":
                    temporary_row.append("_")
                else:
                    temporary_row.append(plaintext[i + j])
            else:
                temporary_row.append("*")
        matrix.append(temporary_row)
        j += n
    ciphertext = []
    for k in range(n):
        for m in range(len(matrix)):
            ciphertext.append(matrix[m][k])
    ciphertext = "".join(ciphertext)
    return ciphertext


def decrypt_scytale(ciphertext, n):
    """
    Функция записывает зашифрованную строку в виде матрицы так,
    чтобы при прямом чтении матрицы получалось декодированное сообщение
    """
    matrix = []
    j = 0
    if len(ciphertext) % n == 0:
        m = len(ciphertext) // n
    else:
        m = (len(ciphertext) // n) + 1
    while j < m:
        temporary_row = []
        for i in range(n):
            if (i * (n - 1) + j) < len(ciphertext):
                if ciphertext[i * (n - 1) + j] == " ":
                    temporary_row.append("_")
                else:
                    temporary_row.append(ciphertext[i * (n - 1) + j])
            else:
                temporary_row.append("*")
        matrix.append(temporary_row)
        j += 1
    plaintext = []
    for k in range(len(matrix)):
        for m in range(n):
            if (matrix[k][m]) == "_":
                plaintext.append(" ")
            elif (matrix[k][m]) == "*":
                continue
            else:
                plaintext.append(matrix[k][m])
    plaintext = "".join(plaintext)
    return plaintext
