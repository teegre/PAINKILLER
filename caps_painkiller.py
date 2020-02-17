# caps_painkiller.py
# reduce opponent's pain to zero
from capsule import Capsule
from common import *

class PainKiller(Capsule):
    """reduce opponent's pain to zero"""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'painkiller'
        self.d_target = 'other'
        self.description = 'ease the pain. not its cause.'
    def use(self, target):
        log.write(f'{self.owner}→{target}: {self.owner} use {self.name}!')
        if target.pain > 0:
            target.pain = 0
            target.p_pain = 0
            log.write(f'{target}\'s pain is soothed...')
            self.active = False
        else: self.active = True
        return F_NOFX

