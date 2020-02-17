# caps_attack.py
# basic attack class
from capsule import Capsule
from common import *

class Attack(Capsule):
    """basic attack."""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'attack'
        self.description = 'the least you can do.'
        self.d_target = 'other'
        self.icon_path = None
    def use(self, target):
        """attack a target / ease the pain."""
        log.write(f'{self.owner} attacks')

        # will attack succeed?
        success = self.owner.success(target)
        if not success: log.write(f'{self.owner} misses')
        else: log.write(f'{self.owner} succeed!')
        if not success: hit = F_MISS
        else:
            # normal attack
            _, hit = self.owner.roll(self.owner.sides, self.owner.strength * self.owner.str_mul)

        for result in self.owner.capsule_trigger('attack', hit):
            if result not in (F_NOCS, F_NOFX): hit = result
            if success: log.write(f'{self.owner} damage={hit}')
            if self.owner.hp == 0: return F_DEAD
        if success: target.hurt(attacker=self.owner, hit=hit)
        return hit

