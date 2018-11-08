"""
Run-length encoding is a fast and simple method of encoding strings. The basic 
idea is to represent repeated successive characters as a single count and 
character. For example, the string "AAAABBBCCDAA" would be encoded as "4A3B2C1D2A".

Implement run-length encoding and decoding. You can assume the string to be 
encoded have no digits and consists solely of alphabetic characters. You can 
assume the string to be decoded is valid.
"""

from itertools import chain, groupby


def encode(string):
    return ''.join(chain.from_iterable(
        (str(len(list(grouper))), char) for char, grouper in groupby(string)))


def decode(string):
    return ''.join(char * int(count) for count, char in zip(*[iter(string)]*2))



assert encode("AAAABBBCCDAA") == "4A3B2C1D2A"
assert decode("4A3B2C1D2A") == "AAAABBBCCDAA"
