# caps_sacrifice.py
# kills the opponent
# 1 HP left
from capsule import Capsule
from common import *

class Sacrifice(Capsule):
    """instant enemy kill, 1 HP left."""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'sacrifice'
        self.description = 'last chance.'
        self.d_target = 'other'
    def use(self, target):
        if target.is_immune(self.name):
            return F_IMMU
        log.write(f'{self.owner}→{target}: {self.owner} use {self}')
        self.owner.hurt(self.owner, self.owner.hp + self.owner.shield - 1)
        if target.is_capsule_attached('leech'):
            target.hurt(self.owner, (target.hp // 4) + target.shield)
        else:
            target.hurt(self.owner, target.hp + target.shield)
        return F_NOFX

