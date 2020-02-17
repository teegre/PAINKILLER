# caps_paralysis.py
# opponent cannot move until he takes damage
from capsule import Capsule
from common import *

class Paralysis(Capsule):
    """opponent cannot move until he takes damage"""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'paralysis'
        self.description = 'nothing to do'
        self.d_target = 'other'
    def use(self, target):
        if target.is_immune(self.name):
            return F_IMMU
        self.target = target
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self}')
        self.attach()
        self.target.deactivate_capsules()
        self.active = False
        return F_NOFX
    def effect(self, action, attacker=None, hit=0):
        log.write(f'{self.target} cannot move!')
        if action == 'hurt' and hit > 0:
            self.target.activate_capsules()
            self.detach()
            self.active = True
            return hit
        return F_NOFX

