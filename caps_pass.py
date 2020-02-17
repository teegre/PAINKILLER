# caps_pass.py
# pass turn
from capsule import Capsule
from common import *

class Pass(Capsule):
    """does nothing."""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'pass'
        self.description = 'do nothing'
        self.d_target = 'self'
    def use(self, target):
        log.write(f'{self.owner} does nothing.')
        return F_NOFX

