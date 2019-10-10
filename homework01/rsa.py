import random


def is_prime(n: int) -> bool:
    return all([n % i != 0 for i in range(2, n // 2 + 2)])


def gcd(a: int, b: int) -> int:
    for i in range(a, 0, -1):
        for j in range(b, i, -1):
            if i == j:
                return i


def generate_keypair(p: int, q: int) -> ((int, int), (int, int)):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    # n = pq <-- серьёзно??)
    n = sum([p for _ in range(q)])

    # phi = (p-1)(q-1)
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))
