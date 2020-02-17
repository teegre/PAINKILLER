# capsule.py
# base class for a capsule

from common import *

class Capsule():
    """base class for capsule."""
    def __init__(self, owner):
        self.name = 'capsule'
        self.description = 'empty capsule.'
        self.d_target = None # default target: should be either self or other.
        self.icon_path = None
        self.active = True # if False, the capsule cannot be used.
        self.owner = owner
        self.target = None
    def use(self, target, *args):
        """use a capsule."""
        pass
    def attach(self, high_priority=False):
        """attach capsule to target."""
        if not self.target: raise Exception(f'{self}: no specified target')
        if not self in self.target.active_c:
            self.on_attach()
            self.target.attach_capsule(self, high_priority)
    def detach(self):
        """detach capsule from target."""
        if not self.target: raise Exception(f'{self}: no specified target')
        if self in self.target.active_c:
            self.on_detach()
            self.target.detach_capsule(self)
    def activate(self):
        self.active = True
        self.on_activate()
        return 0
    def deactivate(self):
        self.on_deactivate()
        self.active = False
        return 0
    def on_activate(self):
        pass
    def on_deactivate(self):
        pass
    def on_attach(self):
        pass
    def on_detach(self):
        pass
    def effect(self, action=None, *args):
        self.owner.capsule_trigger(action, *args)
        return F_NOFX
    def upgrade(self):
        """upgrade capsule."""
        pass
    def reset(self):
        """reset capsule."""
        pass
    @property
    def display(self):
        return self.name
    def __repr__(self):
        return self.name
