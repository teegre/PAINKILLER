from random import seed, randint
import re
from log import Log

# common

# message flags
F_MISS = -1
F_DEAD = -2
F_NOFX = -3
F_NOPN = -4
F_NOCS = -5

# seed generator
def seed_gen(s=None):
    C = [chr(c) for c in range(65, 90)]
    C += [chr(n) for n in range(48 ,57)]

    if not s:
        s = ''.join([C[randint(0, len(C) - 1)] for i in range(0, 4)])
        s += '-'
        s += ''.join([C[randint(0, len(C) - 1)] for i in range(0, 4)])
    else:
        r = r'[A-Z0-9]{4}-[A-Z0-9]{4}'
        if not re.match(r, s):
            raise Exception('[ERROR] invalid seed.')
    seed(s)
    return s

SEED = seed_gen()
#SEED = seed_gen('ULBT-BTUJ')
log = Log(SEED, add_timestamp=False)
log.clear()
log.write(f'SEED: {SEED}')
