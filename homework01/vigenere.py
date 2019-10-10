def encrypt_vigenere(plaintext: str, key: str) -> str:
    key = ''.join([key[i % len(key)] for i in range(len(plaintext))])
    shifts = [ord(char) - 65 if ord(char) in range(65, 91) else ord(char) - 97 for char in key]
    ciphertext = ''
    for index, char in enumerate(plaintext):
        code = ord(char)
        if code in range(65, 91):
            code += shifts[index] - 26 if code + shifts[index] > 90 else shifts[index]
        elif code in range(97, 123):
            code += shifts[index] - 26 if code + shifts[index] > 122 else shifts[index]
        ciphertext += chr(code)
    print([ord(char) for char in ciphertext])
    return ciphertext


def decrypt_vigenere(ciphertext: str, key: str) -> str:
    key = ''.join([key[i % len(key)] for i in range(len(ciphertext))])
    shifts = [ord(char) - 65 if ord(char) in range(65, 91) else ord(char) - 97 for char in key]
    plaintext = ''
    for index, char in enumerate(ciphertext):
        code = ord(char)
        if code in range(65, 91):
            code -= shifts[index] - 26 if code - shifts[index] < 65 else shifts[index]
        elif code in range(97, 123):
            code -= shifts[index] - 26 if code - shifts[index] < 97 else shifts[index]
        plaintext += chr(code)
    return plaintext
