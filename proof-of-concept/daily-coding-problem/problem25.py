"""
This problem was asked by Facebook.

Implement regular expression matching with the following special characters:

    . (period) which matches any single character
    * (asterisk) which matches zero or more of the preceding element

That is, implement a function that takes in a string and a valid regular 
expression and returns whether or not the string matches the regular expression.

For example, given the regular expression "ra." and the string "ray", your 
function should return true. The same regular expression on the string "raymond"
should return false.

Given the regular expression ".*at" and the string "chat", your function 
should return true. The same regular expression on the string "chats" should 
return false.

"""

class State(object):

    NOT_STARTED = 0
    STARTED = 1
    MATCH_UNTIL = 2
    ENDED = 3

    def __init__(self, exp):
        self.exp = iter(exp)
        self.state = State.NOT_STARTED

        self.match_until = False
        self.result = None
        self.last = None

    def update_result(self, result):
        if self.result is None:
            self.result = result
        else:
            self.result = self.result and result

    def update(self, c):
        if self.state == State.NOT_STARTED:
            self.state = State.STARTED
            self.read_char(c)

        elif self.state == State.STARTED:
            self.read_char(c)

        elif self.state == State.MATCH_UNTIL:
            if c == self.match_until:
                self.state = State.STARTED
    
        elif self.state == State.ENDED:
            if self.last != '*':
                self.update_result(False)

    def read_char(self, c):
        expect = next(self.exp, None)
        if expect is None:
            self.update_result(self.last == '*')

        if expect == '*':
            self.state = State.MATCH_UNTIL
            self.match_until = next(self.exp, None)
            if self.match_until is None:
                self.update_result(True)
                self.state = State.ENDED
        else:
            self.update_result(expect in [c, '.'])

        self.last = expect

    def match(self, s):
        map(self.update, s)
        return self.result


def match(expression, string):
    return State(expression).match(string)


assert match('ra.', 'ray')
assert match('ra.', 'raymond') is False
assert match('.*at', 'chat')
assert match('.*at', 'chats') is False
