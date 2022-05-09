import numpy as np
import random
from typing import List, Tuple
from math import gcd as bltin_gcd
from time import perf_counter
import logging

"""
Receiver:
1. receive the dh key (d bits)
2. chop the key into equal n parts
3. wait for receiving k ciphers
4. for each cipher, determine if fake
5. if not fake, find m and add it to M.
6. chop M into parts of 5
"""


def is_coprime(a, b):
    """
    return if a and b are coprimes
    """
    return bltin_gcd(a, b) == 1


def gcdExtended(a, b):
    if a == 0:
        return b, 0, 1
    GCD, x1, y1 = gcdExtended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return GCD, x, y


class KeyGen:
    def __init__(self, dh_key: int,
                 chop_size_dh: int = 5,
                 chop_size_m: int = 5,
                 smallest_key: int = 1000,
                 outfile: str = "LOG.log"):
        """store the key as int and string, store its length"""

        self.dh_key = dh_key
        self.dh_key_str = str(dh_key)
        self.dh_key_len = len(self.dh_key_str)
        self.chop_size_dh = chop_size_dh
        self.chop_size_m = chop_size_m
        self.smallest_key = smallest_key
        self.M: str = ""  # total of all m
        self.keys = []  # store resulting keys
        self.outfile = outfile

        self.t = None

    def generate_keys(self, ciphers: List[Tuple[int, int]]):
        """generate keys by chopping the dh key into equal parts of size chunk_size"""
        logging.info("Generating keys...")

        for chunck_idx, cipher in zip(range(0, self.dh_key_len, self.chop_size_dh), ciphers):
            sub_key_str = self.dh_key_str[chunck_idx: chunck_idx +
                                          self.chop_size_dh]
            m = str(self.get_m(sub_key_str, cipher))
            self.M += m
            logging.info(f"m_{chunck_idx // self.chop_size_dh}: {m}")

        logging.info(f"LENGTH OF M KEY:{len(str(self.M))}")
        logging.info(f"M CHOP SIZE:\t{self.chop_size_m}")
        logging.info(f"M KEY:\n{self.M}")

        return self.chop_m()

    def get_m(self, dh_key_chunk: str, cipher: Tuple[int, int]) -> int:
        """get m from cipher and dh_key_chunk"""
        key = int(dh_key_chunk)
        z, sigma = cipher
        m, p = 1, z
        for n in range(1, key, 1):
            if not is_coprime(key, n):
                continue
            m *= n
            # p = p * n % key
            p = z * n % key
            if p == 1:
                sigma -= 1
                if sigma < 0:
                    return m
        return 0

    def chop_m(self):
        """chop M into parts of size chop_size_m"""
        logging.info(
            f"Choping M into chuncks of {self.chop_size_m} digits...")
        logging.info(
            f"Number of chuncks: {len(str(self.M)) // self.chop_size_m}")

        for chunck_idx in range(0, len(self.M), self.chop_size_m):
            key_str = self.M[chunck_idx: chunck_idx + self.chop_size_m]
            if int(key_str) < self.smallest_key:
                key_str = str(int(key_str) + self.smallest_key)
            self.keys.append(key_str)
            logging.info(key_str)
        return self.keys


def get_keys_from_dh_key(dh_key: int, chunck_size: int) -> List[int]:
    """get keys from dh key"""
    logging.info(
        f"Chopping the dh key into chuncks of {chunck_size} digits...")
    key_str = str(dh_key)
    keys = []
    for chunck_idx in range(0, len(key_str), chunck_size):
        sub_key_str = key_str[chunck_idx: chunck_idx + chunck_size]
        keys.append(int(sub_key_str))
    return keys


def is_coprime_with(number, other_numbers):
    """return if number is coprime with a list other_numbers"""
    for num in other_numbers:
        if not is_coprime(number, num):
            return False
    return True


def get_ciphers(key: int, num_chunks: int, chunk_size: int, n_ciphers: int) -> List[Tuple[int, int]]:
    key_str = str(key)
    key_len = len(key_str)
    keys = get_keys_from_dh_key(key, chunk_size)
    ciphers = []
    logging.info("Ciphers are:")
    for _ in range(n_ciphers):
        if len(ciphers) < num_chunks:
            # find real ciphers
            while True:
                cipher = np.random.randint(1, key_len)
                if is_coprime_with(cipher, keys):
                    logging.info(f"Real: \t {(cipher, 0)}")
                    break
        else:
            cipher = random.getrandbits(8)
            logging.info(f"Fake: \t {(cipher, 0)}")

        ciphers.append((cipher, 0))
    return ciphers


if __name__ == '__main__':
    from timeit import timeit

    outfile = "LOG.log"
    logging.basicConfig(
        filename=outfile, filemode='w', level=logging.DEBUG, force=True)

    nbit_min = 1024
    nbit_max = 2048
    DH_KEY = random.getrandbits(random.choice((nbit_min, nbit_min)))

    key_len = len(str(DH_KEY))
    chop_size_dh = 5
    num_chunks = key_len // chop_size_dh

    logging.info(f"LENGTH OF DH KEY:{key_len}")
    logging.info(f"DH CHOP SIZE:\t{chop_size_dh}")
    logging.info(f"DH KEY:\n{DH_KEY}")

    # print(f"num_chunks: {num_chunks}\n")
    ciphers = get_ciphers(DH_KEY, num_chunks, chop_size_dh, n_ciphers=122)
    key_gen = KeyGen(dh_key=DH_KEY,
                     chop_size_dh=chop_size_dh,
                     chop_size_m=5,
                     smallest_key=1000,
                     outfile="LOG.log")
    keys = key_gen.generate_keys(ciphers)
