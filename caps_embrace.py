# caps_embrace.py
# user fully healed
# opponent self-healed
# reset shield and pain
# cure poison
from capsule import Capsule
from common import *

class Embrace(Capsule):
    """
    user is fully healed and opponent heals according to its self-healing ability.
    shield and pain are resetted for both characters.
    cure poison
    """
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'embrace'
        self.d_target = 'other'
        self.description = 'love thy neighbour.'
    def use(self, target):
        log.write(f'{self.owner}→{target}: {self.owner} use {self}')
        target.pain = 0
        target.shield = 0
        log.write(f'{target} pain is relieved...')
        target.heal()
        self.owner.pain = 0
        self.owner.shield = 0
        self.owner.hp = self.owner.maxhp
        log.write(f'{self.owner} is healed!')
        if self.owner.is_capsule_attached('poison'):
            capsule = self.owner.get_active_capsule('poison')
            capsule.detach()
            log.write(f'{self.owner}: poison cured')
        self.active = False
        return 0

