"""
This problem was asked by Palantir.

Write an algorithm to justify text. Given a sequence of words and an integer 
line length k, return a list of strings which represents each line, fully justified.

More specifically, you should have as many words as possible in each line. 
There should be at least one space between each word. Pad extra spaces when 
necessary so that each line has exactly length k. Spaces should be distributed 
as equally as possible, with the extra spaces, if any, distributed starting from the left.

If you can only fit one word on a line, then you should pad the right-hand side with spaces.

Each word is guaranteed not to be longer than k.

For example, given the list of words ["the", "quick", "brown", "fox", "jumps", 
"over", "the", "lazy", "dog"] and k = 16, you should return the following:

["the  quick brown", # 1 extra space on the left
"fox  jumps  over", # 2 extra spaces distributed evenly
"the   lazy   dog"] # 4 extra spaces distributed evenly
"""

from itertools import chain, izip_longest


def split(words, k):
    total = 0
    saved_words = []
    for word in words:
        if len(word) + total + len(saved_words) > k:
            yield total, saved_words
            total = 0
            saved_words = []
            
        total += len(word)
        saved_words.append(word)
    
    yield total, saved_words 


def get_spaces(left, spaces):
    width, rest = divmod(left, spaces)
    return [' ' * (width + rest)] + ([' ' * width] * (spaces - 1))


def mix(first, second):
    return chain.from_iterable( 
        izip_longest(first, second, fillvalue=''))


def justify(words, k):
    for length, saved_words in split(words, k):
        spaces = len(saved_words) - 1
        left = k - length
        if spaces == 0:
            yield saved_words[0] + ' ' * left
        else:
            yield ''.join(mix(saved_words, get_spaces(left, spaces)))
            


data = ["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]
k = 16

data2 = ['verylongword', 'and', 'then', 'some', 'whatevers']
k2 = 14

assert list(justify(data, k)) == ["the  quick brown", "fox  jumps  over", "the   lazy   dog"]
assert list(justify(data2, k2)) == ['verylongword  ', 'and  then some', 'whatevers     ']
