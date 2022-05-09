import numpy as np

from key_gen_verbose import is_coprime


def is_prime(number):
    """return if number is prime"""
    for i in range(2, number):
        if not number % i:
            return False
    return True


class KeyGen:
    def __init__(self, seed=10, prime=True) -> None:
        self.rng = np.random.default_rng(seed)
        self.n = 999
        self.prime = prime

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        # return self.rng.choice(range(1000, 10_000))
        # self.n += 1
        self.n = self.rng.choice(range(1000, 1_000_000))
        while not self.prime and is_prime(self.n):
            self.n = self.rng.choice(range(1000, 1_000_000))
        return self.n


if __name__ == "__main__":
    key_gen1 = KeyGen()
    key_gen2 = KeyGen()
    for _ in range(10):
        print(next(key_gen1), next(key_gen2))
