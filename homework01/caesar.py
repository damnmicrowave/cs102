def encrypt_caesar(plaintext: str, shift: int) -> str:
    """
        >>> encrypt_caesar("PYTHON", 3)
        'SBWKRQ'
        >>> encrypt_caesar("python", 3)
        'sbwkrq'
        >>> encrypt_caesar("Python3.6", 3)
        'Sbwkrq3.6'
        >>> encrypt_caesar("", 3)
        ''
    """
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
    """
        >>> decrypt_caesar("SBWKRQ", 3)
        'PYTHON'
        >>> decrypt_caesar("sbwkrq", 3)
        'python'
        >>> decrypt_caesar("Sbwkrq3.6", 3)
        'Python3.6'
        >>> decrypt_caesar("", 3)
        ''
    """
    plaintext = ''
    for char in ciphertext:
        code = ord(char)
        if code in range(65, 91):
            code -= shift - 26 if code - shift < 65 else shift
        elif code in range(97, 123):
            code -= shift - 26 if code - shift < 97 else shift
        plaintext += chr(code)
    return plaintext
