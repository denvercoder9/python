"""
This problem was asked by Twitter.

Implement an autocomplete system. That is, given a query string s and a set of 
all possible query strings, return all strings in the set that have s as a prefix.

For example, given the query string de and the set of strings [dog, deer, deal]
return [deer, deal].

Hint: Try preprocessing the dictionary into a more efficient data structure to speed up queries.
"""


def autocomplete(s, dictionary):
    return [word for word in dictionary if word.startswith(s)]


class Autocomplete(object):  # "optimized"
    def __init__(self, dictionary):
        from collections import defaultdict
        self.dictionary = defaultdict(list)
        for word in dictionary:
            self.dictionary[word[0]].append(word)

    def autocomplete(self, s):
        return [word for word in self.dictionary[s[0]] if word.startswith(s)]


assert autocomplete('de', ['dog', 'deer', 'deal']) == ['deer', 'deal']
assert Autocomplete(['dog', 'deer', 'deal']).autocomplete('de') == ['deer', 'deal']
