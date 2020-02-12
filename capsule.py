from common import *
from log import Log

class Capsule():
    """Base class for capsule"""
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
            self.target.attach_capsule(self, high_priority)
    def detach(self):
        """detach capsule from target."""
        if not self.target: raise Exception(f'{self}: no specified target')
        if self in self.target.active_c:
            self.target.detach_capsule(self)
    def effect(self, action=None, *args):
        """triggered in Character class' action methods: attack, block and hurt."""
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
            _, hit = self.owner.roll(self.owner.sides, self.owner.strength)

        for result in self.owner.capsule_trigger('attack', hit):
            if result not in (F_NOCS, F_NOFX): hit = result
            if success: log.write(f'{self.owner} damage={hit}')
            if self.owner.hp == 0: return F_DEAD
        if success: target.hurt(attacker=self.owner, hit=hit)
        return hit

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
            _, pain = self.owner.roll(self.owner.sides, self.owner.strength)
            hit = pain * self.owner.p_pain // 100
            self.owner.pain = 0
            self.owner.p_pain = 0
            self.owner.heal()
            self.active = False

        for result in self.owner.capsule_trigger('attack', hit):
            if result not in (F_NOCS, F_NOFX): hit = result
            if self.owner.hp == 0: return F_DEAD
        if success: target.hurt(attacker=self.owner, hit=hit)
        return hit


class Shield(Capsule):
    """basic shield."""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'shield'
        self.d_target = 'self'
        self.description = 'block incoming attack'
        self.icon_path = None
    def use(self, target):
        """block (part of) incoming attack"""
        log.write(f'{self.owner} use shield')
        for result in self.owner.capsule_trigger('shield'):
            if self.owner.hp == 0: return F_DEAD
        _, shield = self.owner.roll(self.owner.sides, self.owner.defense)
        self.owner.shield += shield
        log.write(f'{self.owner} +{shield} shield')
        return shield

class Poison(Capsule):
    """inflict poison damage."""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'poison'
        self.d_target = 'other'
        self.description = 'poison.'
        self.icon_path = 'sprites/poison.gif'
        self.efficiency = 1 # dice count
        self.value = 0
    def use(self, target):
        self.target = target
        self.value += self.owner.roll(self.owner.sides, self.efficiency)[1]
        self.attach()
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self.name}!')
        return self.value
    def effect(self, action, *args):
        if self.owner.hp == 0:
            self.value = 0
            return 0
        if self.target and self.value and action in ('attack', 'shield'):
            log.write(f'{self.target} get {self.value} poison damage!')
            shield = self.target.shield
            self.target.shield = 0
            self.target.hurt(self.owner, self.value)
            self.target.shield = shield
            self.value -= 1
            if self.value <= 0 or self.target.hp == 0:
                self.detach()
                self.target = None
            return F_NOFX
        elif self.target.hp == 0:
            self.value = 0
            self.detach()
            return F_NOFX
        else: return F_NOFX
    def upgrade(self):
        self.efficiency += 1
    def reset(self):
        self.value = 0
    @property
    def display(self):
        if self.value: return f'{self.name}-{self.value}'
        else: return self.name

class Wall(Capsule):
    """Totally block incoming damage."""
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

class Mirror(Capsule):
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
            return F_MISS
        else: return F_NOFX

class Fury(Capsule):
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'fury'
        self.d_target = 'self'
        self.description = 'it\'s gonna hurt... way more!'
        self.icon_path = 'sprites/fury.gif'
    def use(self, target):
        self.target = self.owner
        self.attach()
        self.active = False
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self.name}!')
    def effect(self, action, *args):
        if action == 'hurt':
            if self.owner.has_capsule('berserk'): mult = 100
            else: mult = 200
            if self.owner.pain == 0: self.owner.pain = self.owner.maxhp * mult // 100
            else: self.owner.pain += self.owner.maxhp * mult // 100
            log.write(f'{self.owner} get furious!')
            self.detach()
            return 0
        else: return -3

class Wreckage(Capsule):
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'wreckage'
        self.d_target = 'other'
        self.description = 'break it.'
        self.icon_path = None
    def use(self, target):
        log.write(f'{self.owner} use {self}!')
        target.shield = 0
        return self.owner.use_capsule('attack', target)

class PainKiller(Capsule):
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

class Empathy(Capsule):
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'empathy'
        self.d_target = 'other'
        self.description = 'feel your opponent\'s pain.'
    def use(self, target):
        self.target = target
        self.attach()
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self.name}')
        self.active = False
        return F_NOFX
    def effect(self, action, attacker=None, hit=None):
        if action == 'hurt':
            log.write(f'{self.owner} feels {self.target}\'s pain...')
            self.owner.pain += hit // 2
            self.owner.p_pain = self.owner.pain * 100 // self.owner.hp
        return F_NOFX

class Embrace(Capsule):
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'embrace'
        self.d_target = 'other'
        self.description = 'love your enemy.'
    def use(self, target):
        log.write(f'{self.owner}→{target}: {self.owner} use {self}')
        target.pain = 0
        target.p_pain = 0
        target.shield = 0
        log.write(f'{target} feels no pain...')
        target.heal()
        self.owner.pain = 0
        self.owner.p_pain = 0
        self.owner.shield = 0
        self.owner.hp = self.owner.maxhp
        log.write(f'{self.owner} is healed!')
        self.active = False
        return 0

class Berserk(Capsule):
    """owner damage is doubled. no pain."""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'berserk'
        self.d_target = 'self'
        self.description = 'powerful and painless.'
    def use(self, target):
        self.target = target
        log.write(f'{self.owner}→{target}: {self.owner} use {self}')
        self.attach(True)
        self.active = False
    def effect(self, action, hit=None, *args):
        if action == 'attack':
            if hit <= 0: return hit 
            log.write(f'{self.owner} attack is doubled {hit}→{hit*2}')
            return hit * 2
        elif action == 'hurt':
            log.write(f'{self.owner} feel no pain.')
            return F_NOPN
        else: return F_NOFX

class Timebomb(Capsule):
    """for enemies..."""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'timebomb'
        self.d_target = 'self'
        self.description = 'the final countdown.'
        self.countdown = 0
    def use(self, target):
        self.target = target
        self.countdown = self.owner.sides * 2
        log.write(f'{self.owner} use {self}')
        self.attach()
        self.active = False
        return self.countdown
    def effect(self, action, *args):
        self.countdown -= 1
        if self.countdown == 0:
            hit = self.owner.hp
            target.hurt(self.owner, hit)
            self.owner.shield = 0
            self.owner.hurt(self.owner, hit)
            return hit
        else: return F_NOFX
    def reset(self):
        self.countdown = 0
    @property
    def display(self):
        if self.countdown:
            return f'{self.name}-{self.countdown}'
        else: return self.name

class Leech(Capsule):
    """drain life of the opponent"""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'leech'
        self.description = 'drain life'
        self.d_target = 'other'
    def use(self, target):
        self.target = target
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self}')
        self.attach()
        capsule = self.owner.get_capsule('attack')
        self.active = False
        return F_NOFX
    def effect(self, action, attacker=None, hit=0):
        if action == 'hurt':
            if hit > self.target.shield: hit -= self.target.shield
            elif hit < self.target.shield: hit = None
            elif hit == self.target.shield: hit = None
            if hit:
                self.owner.heal(hit)
                self.owner.pain -= hit
                if self.owner.pain < 0: self.owner.pain = 0
                self.owner.p_pain = self.owner.pain * 100 // self.owner.hp
                return 0
            else: return F_NOFX
        else: return F_NOFX

class Charity(Capsule):
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'charity'
        self.description = 'be nice!'
        self.d_target = 'other'
    def use(self, target):
        heal = self.owner.maxhp * self.owner.self_healing // 100
        self.owner.hurt(target, heal)
        target.heal(heal)
        target.pain = target.p_pain = 0
        target.shield = 0
        self.active = False
        return F_NOFX

class Paralysis(Capsule):
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'paralysis'
        self.description = 'nothing to do'
        self.d_target = 'other'
    def use(self, target):
        self.target = target
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self}')
        self.attach()
        self.target.deactivate_capsules()
        self.active = False
        return F_NOFX
    def effect(self, action, attacker=None, hit=0):
        log.write(f'{self.target} cannot move!')
        if action == 'hurt' and hit > 0:
            self.target.activate_capsules()
            self.detach()
            self.active = True
            return hit
        return F_NOFX

class Shell(Capsule):
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'shell'
        self.description = 'indestructible unless you take action.'
        self.d_target = 'self'
    def use(self, target):
        self.target = self.owner
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self}')
        self.owner.add_capsule(Pass(self.owner))
        self.attach()
        self.active = False
        return F_NOFX
    def effect(self, action, attacker=None, hit=0):
        if action == 'hurt':
            log.write(f'{self.owner} is indestructible!')
            return F_MISS
        elif action != 'pass':
            self.detach()
            self.owner.drop_capsule('pass')
            self.active = True
            return F_NOFX

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

class Morphine(Capsule):
    """opponent's pain doesn't increase next time damage is taken."""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'morphine'
        self.description = 'did you hit me?'
        self.d_target = 'other'
    def use(self, target):
        log.write(f'{self.owner}→{self.target}: {self.owner} use {self}')
        self.target = target
        self.attach()
        self.active = False
        return F_NOFX
    def effect(self, action, *args):
        if action == 'hurt':
            log.write(f'{self.target} doesn\'t feel the pain.')
            self.detach()
            self.active = True
            return F_NOPN;
        else: return F_NOFX

class Sacrifice(Capsule):
    """instant enemy kill, 1 HP left."""
    def __init__(self, owner):
        Capsule.__init__(self, owner)
        self.name = 'sacrifice'
        self.description = 'last chance.'
        self.d_target = 'other'
    def use(self, target):
        log.write(f'{self.owner}→{target}: {self.owner} use {self}')
        self.owner.hurt(self.owner, self.owner.hp + self.owner.shield - 1)
        if target.is_capsule_attached('leech'):
            target.hurt(self.owner, (target.hp // 4) + target.shield)
        else:
            target.hurt(self.owner, target.hp + target.shield)
        return F_NOFX

capsules_dict = {
        #name         #object
        'attack':     Attack,
        'shield':     Shield,
        'relieve':    Relieve,
        'poison':     Poison,
        'wall':       Wall,
        'mirror':     Mirror,
        'fury':       Fury,
        'wreckage':   Wreckage,
        'painkiller': PainKiller,
        'empathy':    Empathy,
        'embrace':    Embrace,
        'berserk':    Berserk,
        'leech':      Leech,
        'charity':    Charity,
        'paralysis':  Paralysis,
        'shell':      Shell,
        'morphine':   Morphine,
        'sacrifice':  Sacrifice,
}

