# caps_berserk.py
# double damage, no pain
from capsule import Capsule
from common import *

class Berserk(Capsule):
    """character damage is doubled. no pain."""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'berserk'
        self.d_target = 'self'
        self.description = 'powerful and painless.'
    def use(self, target):
        self.target = target
        log.write(f'{self.owner}→{target}: {self.owner} use {self}')
        self.attach()
        self.active = False
    def effect(self, action, hit=None, *args):
        if action == 'attack':
            if hit <= 0: return hit 
            log.write(f'{self.owner} attack is doubled {hit}→{hit*2}')
            return hit * 2
        elif action == 'hurt':
            log.write(f'{self.owner} feel no pain.')
            return F_NOPN
        else: return F_NOFX

