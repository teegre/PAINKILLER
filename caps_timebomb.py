# caps_timebomb.py
# sacrifices all remaining hp in a desperate last attack
# when countdown reaches zero
from capsule import Capsule
from common import *

class TimeBomb(Capsule):
    """
    when countdown reaches zero, sacrifices all remaining hp in a desperate last attack.
    (for enemies only)
    """
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'timebomb'
        self.d_target = 'self'
        self.description = 'the final countdown.'
        self.countdown = 0
    def use(self, target):
        self.target = target
        self.countdown = self.owner.sides * 2
        log.write(f'{self.owner} use {self}')
        self.attach()
        self.active = False
        return self.countdown
    def effect(self, action, *args):
        self.countdown -= 1
        if self.countdown == 0:
            hit = self.owner.hp
            self.target.hurt(self.owner, hit)
            self.owner.shield = 0
            self.owner.hurt(self.owner, hit)
            return hit
        else: return F_NOFX
    def reset(self):
        self.countdown = 0
    @property
    def display(self):
        if self.countdown:
            return f'{self.name}-{self.countdown}'
        else: return self.name

