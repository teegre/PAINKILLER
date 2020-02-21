# caps_relieve.py
# special attack
from capsule import Capsule
from common import *

class Relieve(Capsule):
    """special attack"""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'relieve'
        self.description = 'relieve the pain'
        self.d_target = 'other'
        self.active = False
    def use(self, target):
        """special attack"""
        log.write(f'{self.owner} relieves the pain!')

        #will attack succeed?
        success = self.owner.success(target)
        if not success: log.write(f'{self.owner} misses')
        else: log.write(f'{self.owner} succeed!')
        if not success: hit = F_MISS
        if success:
            #relieve the pain
            _, pain = self.owner.roll(self.owner.sides, self.owner.strength * self.owner.str_mul)
            if pain == self.owner.sides * self.owner.strength * self.owner.str_mul:
                pain *= 2
                log.write(f'{self.owner} LUCKY HIT! ({pain})')
            hit = pain * self.owner.p_pain // 100
            self.owner.pain = 0
            self.owner.heal()

        for result in self.owner.capsule_trigger('attack', hit):
            if result not in (F_NOCS, F_NOFX): hit = result
            if self.owner.hp == 0: return F_DEAD
        if success: target.hurt(attacker=self.owner, hit=hit)
        self.active = False
        return hit

