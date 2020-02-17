# caps_steroids.py
# strength multiplied
from capsule import Capsule
from common import *

class Steroids(Capsule):
    """gain strength"""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'steroids'
        self.description = 'more strength'
        self.d_target = 'self'
        self.value = 1
        self.str_mul = self.owner.str_mul
    def use(self, target):
        log.write(f'{self.owner}→{target}: {self.owner} use {self}')
        self.target = self.owner
        self.attach(high_priority=True)
        self.owner.str_mul += self.value
        log.write(f'{self.owner} is +{self.value} stronger!')
        self.deactivate()
        return F_NOFX
    def upgrade(self):
        self.value += 1
    def on_detach(self):
        self.owner.str_mul = self.str_mul
        log.write(f'{self.owner}: {self} effect comes to an end.')

