from collections import defaultdict


def find_anagrams(s: str, p: str):
    s = s.lower().strip().replace(' ', '')
    p = p.lower().strip().replace(' ', '')

    chars_p = defaultdict(int, {char_p: p.count(char_p) for char_p in p})

    indices = []
    i, j = 0, len(p)
    while j <= len(s):
        if all(char_p in s[i:j] for char_p in p) and all(s[i:j].count(char_s) >= chars_p[char_s] for char_s in s[i:j]):
            indices.append(i)
        i += 1
        j += 1

    print(indices if indices else 'no anagrams :(')


find_anagrams('qrwetyqoiwuy', 'cvm')  # no anagrams :(
find_anagrams('cbaebabacd', 'abc')  # [0, 6]
find_anagrams('cbaebabacd', 'abcc')  # no anagrams :(
find_anagrams('dEBIt  cArd', 'BAD credit    ')  # [0]
