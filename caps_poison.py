# caps_poison.py
# poison capsule
from capsule import Capsule
from common import *

class Poison(Capsule):
    """inflict poison damage."""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'poison'
        self.d_target = 'other'
        self.description = 'poison.'
        self.icon_path = 'sprites/poison.gif'
        self.value = 0
    def use(self, target):
        if target.is_immune(self.name):
            return F_IMMU
        self.target = target
        self.value += self.owner.roll(self.owner.sides, self.owner.strength)[1]
        self.attach()
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self.name}!')
        return self.value
    def effect(self, action, *args):
        if action == 'hurt': return F_NOFX
        log.write(f'{self.target} get {self.value} poison damage!')
        self.target.hp -= self.value
        self.target.pain += self.value
        self.value -= 1
        if self.value <= 0: self.detach()
        if self.target.hp <= 0:
            self.target.hp = 0
            self.target.pain = 0
            self.detach()
        return F_NOFX
    def reset(self):
        self.value = 0
    @property
    def display(self):
        if self.value: return f'{self.name}-{self.value}'
        else: return self.name
