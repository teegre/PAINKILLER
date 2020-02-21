# caps_charity.py
# opponent self-healed
# reset his pain and shield
from capsule import Capsule
from common import *

class Charity(Capsule):
    """
    give the equivalent of self-healing% hp to the opponent
    reset his pain and shield
    """
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'charity'
        self.description = 'be nice!'
        self.d_target = 'other'
    def use(self, target):
        heal = self.owner.maxhp * self.owner.self_healing // 100
        self.owner.hurt(self.owner, heal)
        target.heal(heal)
        target.pain = 0
        target.shield = 0
        self.active = False
        return F_NOFX

