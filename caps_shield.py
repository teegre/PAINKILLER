# caps_shield.py
# basic shield
from capsule import Capsule
from common import *

class Shield(Capsule):
    """basic shield."""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'shield'
        self.d_target = 'self'
        self.description = 'block incoming attack'
        self.icon_path = None
    def use(self, target):
        """block (part of) incoming attack"""
        log.write(f'{self.owner} use shield')
        for result in self.owner.capsule_trigger('shield'):
            if self.owner.hp == 0: return F_DEAD
        _, shield = self.owner.roll(self.owner.sides, self.owner.defense * self.owner.def_mul)
        self.owner.shield += shield
        log.write(f'{self.owner} +{shield} shield')
        return shield
