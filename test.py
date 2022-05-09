import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from tqdm import tqdm
from key_gen import KeyGen
from lsa import *

key_gen_alice = KeyGen()
key_gen_bob = KeyGen()
with open("text.txt", "r") as f:
    text = f.read()
len_text = len(text)
# text = "Z" * len_text
z_vals = np.zeros(len_text, dtype=int)
for idx, char in tqdm(enumerate(text)):
    key = next(key_gen_alice)
    try:
        char_index = CHARS_DICT[char]
        z_vals[idx] = get_cipher(key, char_index)[0]
    except KeyError:
        continue

plt.figure(figsize=(7, 5))
plt.title(f"Distribution of z values of encrypting {len_text} characters")
# plt.title(f"Distribution of z values for encrypting a single character {len_text} times")
plt.xlabel("z values")
plt.ylabel("Count")
plt.grid()
sns.histplot(z_vals, bins=95)
plt.savefig("z_dist.png")
