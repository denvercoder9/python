"""
Small script to run when forgetting what the different combinatoric functions
in itertools mean ;-)

"""

import itertools

print "permutations"
for n in range(1, 6):
    print n, "->", len(list(itertools.permutations(range(n))))

print "product repeat=n"
for n in range(1, 6):
    print n, "->", len(list(itertools.product(range(n), repeat=n)))

print 'combiations'
for n in range(1, 6):
    print n, "->", len(list(itertools.combinations(range(n), n)))

print 'combiations with replacement'
for n in range(1, 6):
    print n, "->", len(list(itertools.combinations_with_replacement(range(n), n)))
