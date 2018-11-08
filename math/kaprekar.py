import sys

"""

Step 1: Take any four-digit number, using at least two different digits
        (Leading zeros are allowed.)

Step 2: Arrange the digits in descending and then in ascending order to
        get two four-digit numbers, adding leading zeros if necessary.

Step 3: Subtract the smaller number from the bigger number.

"""


KAPREKAR = 6174


def get_user_input():
    """Step 1: Take any four-digit number, using at least two different digits
    (Leading zeros are allowed.)
    """

    query = ('Take any four-digit number, using at least two different digits.'
             '(Leading zeros are allowed.): ')
    indata = raw_input(query)

    if len(indata) > 4:
        raise ValueError('Maximum 4 digits')
    if len(set(indata)) < 2:
        raise ValueError('Minimum of two different digits')
    try:
        int(indata)
    except Exception:
        raise ValueError('Only digits allowed')

    return indata


def process(indata):
    """Step 2: Arrange the digits in descending and then in ascending order to
    get two four-digit numbers, adding leading zeros if necessary.

    Step 3: Subtract the smaller number from the bigger number.
    """

    n1 = '{:0>4}'.format(''.join(sorted(indata, key=int)))
    n2 = n1[::-1]

    smaller, larger = list(sorted(map(int, [n1, n2])))
    diff = larger - smaller
    print '{:0>4} - {:0>4} = {:0>4}'.format(larger, smaller, diff)
    return diff


def main():
    diff = process(get_user_input())
    count = 1
    while diff != KAPREKAR:
        diff = process(str(diff))
        count += 1

    print "Number of iterations need to reach Kaprekar's constant:", count


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        sys.exit(e)
