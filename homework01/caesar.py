def encrypt_caesar(plaintext: str, shift: int) -> str:
    ciphertext = ''
    for char in plaintext:
        code = ord(char)
        if code in range(65, 91):
            code += shift - 26 if code + shift > 90 else shift
        elif code in range(97, 123):
            code += shift - 26 if code + shift > 122 else shift
        ciphertext += chr(code)
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int) -> str:
    plaintext = ''
    for char in ciphertext:
        code = ord(char)
        if code in range(65, 91):
            code -= shift - 26 if code - shift < 65 else shift
        elif code in range(97, 123):
            code -= shift - 26 if code - shift < 97 else shift
        plaintext += chr(code)
    return plaintext
