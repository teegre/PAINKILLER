# caps_empathy.py
# increase pain when doing damage to opponent
from capsule import Capsule
from common import *

class Empathy(Capsule):
    """pain increase also when attacking the enemy"""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'empathy'
        self.d_target = 'other'
        self.description = 'feel your opponent\'s pain.'
    def use(self, target):
        self.target = target
        self.attach()
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self.name}')
        self.active = False
        return F_NOFX
    def effect(self, action, attacker=None, hit=None):
        if action == 'hurt':
            log.write(f'{self.owner} feels {self.target}\'s pain...')
            self.owner.pain += hit // 2
            self.owner.p_pain = self.owner.pain * 100 // self.owner.hp
        return F_NOFX

