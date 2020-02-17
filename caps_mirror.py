# caps_mirror.py
# block incoming attack and return it to the sender
from capsule import Capsule
from common import *

class Mirror(Capsule):
    """return attack to sender."""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'mirror'
        self.d_target = 'self'
        self.description = 'what do you see?'
        self.icon_path = 'sprites/mirror.gif'
    def use(self, target):
        self.target = target
        self.attach(True)
        self.active = False
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self.name}!')
    def effect(self, action, attacker=None, hit=None):
        if action == 'hurt':
            log.write(f'{self.owner} returns {attacker}\'s attack!')
            attacker.hurt(attacker, hit)
            self.detach()
            self.active = True
            return F_MISS
        else: return F_NOFX

