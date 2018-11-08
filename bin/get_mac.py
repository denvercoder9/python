"""Generates a new random mac address.

On a mac or any other system that still uses ifconfig you can use it like:

    sudo ifconfig en0 ether $(python get_mac.py)
"""

import random

data = hex(random.getrandbits(48))[2:-1]
print ':'.join(map(''.join, zip(*[iter(data.zfill(12))]*2)))
