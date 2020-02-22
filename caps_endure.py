# caps_endure.py
# no damage taken but feel the pain

from capsule import Capsule
from common import *

class Endure(Capsule):
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'endure'
        self.description = 'it\'s ok, you can make it!'
        self.d_target = 'self'
    def use(self, target):
        self.target = target
        self.attach()
        self.active = False
    def effect(self, action, attacker=None, hit=0):
        if action == 'hurt':
            if self.owner.is_capsule_attached('berserk'):
                self.detach()
                return F_NOFX
            if hit > self.owner.shield and self.owner.shield >= 0:
                hit -= self.owner.shield
            elif hit < self.owner.shield:
                return hit
            self.owner.shield = 0
            self.owner.pain += hit
            self.detach()
            return F_NODM
        else: return F_NOFX


