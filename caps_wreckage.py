# caps_wreckage.py
# break opponent's shield and perform normal attack
from capsule import Capsule
from common import *

class Wreckage(Capsule):
    """break opponent's shield and perform normal attack"""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'wreckage'
        self.d_target = 'other'
        self.description = 'break it.'
        self.icon_path = None
    def use(self, target):
        log.write(f'{self.owner} use {self}!')
        if self.owner.lucky(target):
            target.shield = 0
            return self.owner.use_capsule('attack', target)
        else: return F_MISS

