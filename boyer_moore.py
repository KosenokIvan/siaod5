from collections import defaultdict


def boyer_moore(string, substring, case_sensitive=True):
    if not case_sensitive:
        string = string.lower()
        substring = substring.lower()
    if len(substring) > len(string):
        return -1
    offset_table = defaultdict(lambda: len(substring))
    for i in range(len(substring) - 1):
        offset_table[substring[i]] = len(substring) - i - 1
    i = len(substring) - 1
    j = k = i
    while j >= 0 and i <= len(string) - 1:
        j = len(substring) - 1
        k = i
        while j >= 0 and string[k] == substring[j]:
            k -= 1
            j -= 1
        i += offset_table[string[i]]
    if k >= len(string) - len(substring):
        return -1
    return k + 1


if __name__ == '__main__':
    print(boyer_moore("abcabcABcDefabCabCabc", "def"))
    print(boyer_moore("abcabcABcDefabCabCabc", "def", False))
    print(boyer_moore("abcabcABcdefabCabCabc", "def"))
