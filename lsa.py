from utils import is_coprime, gcdExtended
import numpy as np


def get_cipher_lsa(key: int, char_idx: int, start: int = 30) -> int:
    """get cipher from key and char_index"""
    c = 1
    stop_idx = 0
    # run_prod_mod = np.zeros(char_idx + 1, dtype=int)
    for n in range(start, key, 1):
        if not key % 2 and not n % 2:
            continue
        if not is_coprime(key, n):
            continue
        c = c * n % key
        # run_prod_mod[stop_idx] = c
        if stop_idx == char_idx:
            _, z, _ = gcdExtended(c, key)
            # cong = z * run_prod_mod % key
            if z < 0:
                z += key
            # return (z, np.sum(cong == 1))
            return z
        stop_idx += 1


def get_cipher_lsa_bw(key: int, char_idx: int, end=30) -> int:
    """get cipher from key and char_index, starting backwards"""
    c = 1
    stop_idx = 0
    # run_prod_mod = np.zeros(char_idx + 1, dtype=int)
    for n in range(key - 1 - end, 0, -1):
        if not key % 2 and not n % 2:
            continue
        if not is_coprime(key, n):
            continue
        c = c * n % key
        # run_prod_mod[stop_idx] = c
        if stop_idx == char_idx:
            _, z, _ = gcdExtended(c, key)
            # cong = z * run_prod_mod % key
            if z < 0:
                z += key
            # return (z, np.sum(cong == 1))
            return z
        stop_idx += 1


def get_cipher_xor(key: int, char_idx: int) -> int:
    return key ^ char_idx
