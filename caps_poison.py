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
        self.efficiency = 1 # dice count
        self.value = 0
    def use(self, target):
        if target.is_immune(self.name):
            return F_IMMU
        self.target = target
        self.value += self.owner.roll(self.owner.sides, self.efficiency)[1]
        self.attach()
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self.name}!')
        return self.value
    def effect(self, action, *args):
        if self.owner.hp == 0:
            self.value = 0
            return 0
        if self.target and self.value and action in ('attack', 'shield'):
            log.write(f'{self.target} get {self.value} poison damage!')
            shield = self.target.shield
            self.target.shield = 0
            self.target.hurt(self.owner, self.value)
            self.target.shield = shield
            self.value -= 1
            if self.value <= 0 or self.target.hp == 0:
                self.detach()
                self.target = None
            return F_NOFX
        elif self.target.hp == 0:
            self.value = 0
            self.detach()
            return F_NOFX
        else: return F_NOFX
    def upgrade(self):
        self.efficiency += 1
    def reset(self):
        self.value = 0
    @property
    def display(self):
        if self.value: return f'{self.name}-{self.value}'
        else: return self.name

