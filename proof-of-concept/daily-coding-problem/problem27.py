"""
This problem was asked by Facebook.

Given a string of round, curly, and square open and closing brackets, return 
whether the brackets are balanced (well-formed).

For example, given the string "([])[]({})", you should return true.

Given the string "([)]" or "((()", you should return false.

"""

def check(string):
    pairs = {
        '(': ')',
        '[': ']',
        '{': '}',
    }
    stack = []

    for c in string:
        if c in pairs.keys():
            stack.append(c)
        elif c in pairs.values():
            expected = pairs[stack.pop()]
            if c != expected:
                return False

    return len(stack) == 0


assert check('([])[]({})')
assert check('([)]') is False
assert check('((()') is False
