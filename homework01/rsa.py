def is_prime(n: int) -> bool:
    return all([n % i != 0 for i in range(2, n // 2 + 2)])
