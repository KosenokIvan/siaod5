def prefix_function(string):
    res = [0] * len(string)
    for i in range(1, len(string)):
        k = res[i - 1]
        while k > 0 and string[k] != string[i]:
            k = res[k - 1]
        if string[k] == string[i]:
            k += 1
        res[i] = k
    return res


def knuth_morris_pratt(string, substring, case_sensitive=True):
    if not case_sensitive:
        string = string.lower()
        substring = substring.lower()
    index = -1
    prefix = prefix_function(substring)
    k = 0
    for i in range(len(string)):
        while k > 0 and substring[k] != string[i]:
            k = prefix[k - 1]
        if substring[k] == string[i]:
            k += 1
        if k == len(substring):
            index = i - len(substring) + 1
            break
    return index


if __name__ == '__main__':
    print(knuth_morris_pratt("abcabcABcDefabCabCabc", "def"))
    print(knuth_morris_pratt("abcabcABcDefabCabCabc", "def", False))
    print(knuth_morris_pratt("abcabcABcdefabCabCabc", "def"))
