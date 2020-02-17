# caps_wall.py
# block incoming attack
from capsule import Capsule
from common import *

class Wall(Capsule):
    """totally block incoming damage."""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'wall'
        self.d_target = 'self'
        self.description = 'safe... temporarly.'
        self.icon_path = 'sprites/wall.gif'
    def use(self, target):
        self.target = target
        self.attach()
        self.active = False
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self.name}!')
    def effect(self, action, *args):
        if action == 'hurt':
            log.write(f'{self.target} cancel opponent\'s attack')
            self.detach()
            self.active = True
            return F_MISS
        else: return F_NOFX

