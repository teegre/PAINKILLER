# caps_shell.py
# invincible if standstill
# grant 'pass' capsule
from capsule import Capsule
from common import *

class Shell(Capsule):
    """
    invicibility as long as no action is performed.
    activates 'pass' capsule
    """
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'shell'
        self.description = 'indestructible unless you take action.'
        self.d_target = 'self'
    def use(self, target):
        self.target = self.owner
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self}')
        self.owner.add_capsule('pass')
        self.attach()
        self.active = False
        return F_NOFX
    def effect(self, action, *args):
        if action == 'hurt':
            log.write(f'{self.owner} is indestructible!')
            return F_MISS
        elif action != 'pass':
            self.detach()
            self.owner.drop_capsule('pass')
            self.active = True
            return F_NOFX
    def on_deactivate(self):
        self.owner.drop_capsule('pass')
        return 0

