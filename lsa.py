from typing import Tuple
import numpy as np
from key_gen_verbose import is_coprime, gcdExtended
from key_gen import KeyGen
import string

CHARS = string.ascii_letters + string.digits + string.punctuation + " \n"
CHARS_DICT = {char: i for i, char in enumerate(CHARS)}
START_C = 32


def encrypt(key_gen: KeyGen, text: str) -> Tuple[np.array, np.array]:
    """encrypt text with keys from key_gen"""
    len_text = len(text)
    z_vals = np.zeros(len_text, dtype=int)
    sigmas = np.zeros(len_text, dtype=np.uint8)
    for idx, char in enumerate(text):
        key = next(key_gen)
        char_index = CHARS_DICT[char]
        z_vals[idx], sigmas[idx] = get_cipher(key, char_index)
    return z_vals, sigmas


def get_cipher(key: int, char_idx: int) -> Tuple[int, int]:
    """get cipher from key and char_index"""
    c = 1
    stop_idx = 0
    run_prod_mod = np.zeros(char_idx + 1, dtype=int)
    for n in range(START_C, key, 1):
        if not is_coprime(key, n):
            continue
        c = c * n % key
        run_prod_mod[stop_idx] = c
        if stop_idx == char_idx:
            _, z, _ = gcdExtended(c, key)
            cong = z * run_prod_mod % key
            if z < 0:
                z += key
            return (z, np.sum(cong == 1))
        stop_idx += 1


def decrypt(key_gen: KeyGen, z_vals: np.array, sigmas: np.array) -> np.array:
    """decrypt z_vals and sigmas with keys from key_gen"""
    text = np.empty(len(z_vals), dtype=str)
    for idx, (z, sigma) in enumerate(zip(z_vals, sigmas)):
        key = next(key_gen)
        char_idx = decipher(key, z, sigma)
        text[idx] = CHARS[char_idx]
    return text


def decipher(key: int, z: int, sigma: int) -> int:
    """decipher z and sigma with key"""
    c = z
    char_idx = 0
    for n in range(START_C, key, 1):
        if not is_coprime(key, n):
            continue
        c = c * n % key
        if c == 1:
            sigma -= 1
            if sigma == 0:
                return char_idx
        char_idx += 1


if __name__ == '__main__':
    key_gen_alice = KeyGen()
    key_gen_bob = KeyGen()
    text = 'aaaaaaaaaaaaaaaaaaaa!'
    print("Encrypting:", text)
    z_vals, sigmas = encrypt(key_gen_alice, text)
    text = decrypt(key_gen_bob, z_vals, sigmas)
    print("Decrypted:", text)
