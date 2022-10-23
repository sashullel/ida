from collections import defaultdict


def find_anagrams(s: str, p: str):
    s = list(s.lower().strip().replace(' ', ''))
    p = list(p.lower().strip().replace(' ', ''))

    chars_s = defaultdict(int, {char_s: s.count(char_s) for char_s in s})
    chars_p = {char_p: p.count(char_p) for char_p in p}

    indices = set()

    for char_p, freq_p in chars_p.items():
        if chars_s[char_p] >= freq_p:

            start_idx = 0
            end_idx = len(p)
            while end_idx <= len(s):

                if sorted(p) == sorted(s[start_idx:end_idx]):
                    indices.add(start_idx)

                start_idx += 1
                end_idx += 1

    print(list(indices) if indices else 'no anagrams :(')


find_anagrams('qrwetyqoiwuy', 'cvm')
find_anagrams('cbaebabacd', 'abc')
find_anagrams('dEBIt  cArd', 'BAD credit    ')