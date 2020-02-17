# caps_prudence.py
# normal attack = shield
from capsule import Capsule
from common import *

class Prudence(Capsule):
    """normal attack + shield"""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'prudence'
        self.description = 'the best form of defence is attack'
        self.d_target = 'other'
    def use(self, target):
        log.write(f'{self.owner} uses {self}')
        result = self.owner.use_capsule('attack', target)
        if result < 0: return F_NOFX
        self.owner.shield += result
        log.write(f'{self.owner} gains +{result} shield')
        return result

