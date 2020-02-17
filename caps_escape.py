# caps_escape.py
# escape from a fight
from capsule import Capsule
from common import *

class Escape(Capsule):
    """allow escaping from a fight"""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'escape'
        self.description = 'run away'
        self.d_target = 'other'
        self.active = False
    def use(self, target):
        log.write(f'{self.owner} tries to escape...')
        if self.owner.lucky(target): return F_ESCP
        else: return F_MISS

