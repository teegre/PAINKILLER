# caps_morphine.py
# opponent doesn't feel pain when hit
from capsule import Capsule
from common import *

class Morphine(Capsule):
    """opponent's pain doesn't increase next time damage is taken."""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'morphine'
        self.description = 'did you hit me?'
        self.d_target = 'other'
    def use(self, target):
        if target.is_immune(self.name):
            return F_IMMU
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self}')
        self.target = target
        self.attach()
        self.active = False
        return F_NOFX
    def effect(self, action, attacker=None, hit=0):
        if action == 'hurt' and hit > 0:
            log.write(f'{self.target} doesn\'t feel the pain.')
            self.detach()
            self.active = True
            return F_NOPN;
        else: return F_NOFX

