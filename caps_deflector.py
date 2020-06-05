# caps_deflector.py
# block incoming attack and return it to the sender
from capsule import Capsule
from common import *

class Deflector(Capsule):
    """return attack to sender."""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'deflector'
        self.d_target = 'self'
        self.description = 'return it'
        self.icon_path = ''
    def use(self, target):
        self.target = target
        self.attach(True)
        self.active = False
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self.name}!')
        return F_ATTX
    def effect(self, action, attacker=None, hit=None):
        if action == 'hurt':
            log.write(f'{self.owner} returns {attacker}\'s attack!')
            self.detach()
            attacker.hurt(attacker, hit)
            self.active = True
            return F_MISS
        else: return F_NOFX
