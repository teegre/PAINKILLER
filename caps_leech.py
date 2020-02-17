# caps_leech.py
# opponent's hp are drained when attacking
# reduce owner's pain
from capsule import Capsule
from common import *

class Leech(Capsule):
    """opponent's hp are drained when performing an attack. reduce pain"""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'leech'
        self.description = 'drain life'
        self.d_target = 'other'
    def use(self, target):
        if target.is_immune(self.name):
            return F_IMMU
        self.target = target
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self}')
        self.attach()
        capsule = self.owner.get_capsule('attack')
        self.active = False
        return F_NOFX
    def effect(self, action, attacker=None, hit=0):
        if action == 'hurt':
            if hit > self.target.shield: hit -= self.target.shield
            elif hit < self.target.shield: hit = None
            elif hit == self.target.shield: hit = None
            if hit:
                self.owner.heal(hit)
                self.owner.pain -= hit
                if self.owner.pain < 0: self.owner.pain = 0
                self.owner.p_pain = self.owner.pain * 100 // self.owner.hp
                return 0
            else: return F_NOFX
        else: return F_NOFX

