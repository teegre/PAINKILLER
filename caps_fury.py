# caps_fury.py
# increase pain the first time damage are taken
from capsule import Capsule
from common import *

class Fury(Capsule):
    """increase pain"""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'fury'
        self.d_target = 'self'
        self.description = 'it\'s gonna hurt...'
        self.icon_path = 'sprites/fury.gif'
    def use(self, target):
        self.target = self.owner
        self.attach()
        self.active = False
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self.name}!')
    def effect(self, action, attacker=None, hit=0):
        if action == 'hurt' and hit > 0:
            if self.owner.has_capsule('berserk'): mul = 100
            else: mul = 200
            if self.owner.pain == 0: self.owner.pain = self.owner.maxhp * mul // 100
            else: self.owner.pain += self.owner.maxhp * mul // 100
            log.write(f'{self.owner} get furious!')
            self.detach()
            return 0
        else: return F_NOFX

