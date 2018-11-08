# -*- coding:utf-8

"""Silly script pretending to be a bad human typist."""

from __future__ import print_function
import time
import random
import string
import sys

text = """What is the good life? Religion, philosophy, and modern
self-help books grapple with the question, but the answer
is elusive. Does it mean being happy? Or is it about wealth
and professional success? What role does virtue play? Does
the good life mean being good? Does it mean helping others
and making the world a better place?
Two hundred and fifty years ago, a Scottish moral philosopher
addressed these questions in a book with the unglamorous
title The Theory of Moral Sentiments. The book
was Adam Smith’s attempt to explain where morality comes
from and why people can act with decency and virtue even
when it conflicts with their own self-interest. It’s a mix of
psychology, philosophy, and what we now call behavioral
economics, peppered with Smith’s observations on friendship,
the pursuit of wealth, the pursuit of happiness, and
virtue. Along the way, Smith tells his readers what the good
life is and how to achieve it.""".replace('\n', ' ')


def print(c):
    sys.stdout.write(c)
    sys.stdout.flush()


for c in text:
    print(c)
    if c in string.punctuation:
        time.sleep(0.4)
    else:
        time.sleep(0.1)

    if random.random() > 0.97:
        print(random.choice(string.ascii_lowercase))
        time.sleep(1)
        print('\b')
        time.sleep(0.1)
