import math


def is_coprime(a, b):
    """
    return if a and b are coprimes
    """
    return math.gcd(a, b) == 1


def gcdExtended(a, b):
    if a == 0:
        return b, 0, 1
    GCD, x1, y1 = gcdExtended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return GCD, x, y
