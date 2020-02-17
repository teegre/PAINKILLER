from common import *
from capsules import CAPSULES
from random import randint

class Character():
    """base class for game characters."""
    def __init__(self, name, ttype=None, hp=50, level=1, strength=1, defense=1, agility=1):
        # characteristics
        self.name = name
        self.type = ttype
        self.level = level
        self.maxhp = hp
        self.hp = hp
        self.strength = strength # dice count.
        self.defense = defense # dice count.
        self.agility = agility # ability to hit the opponent.
        self.self_healing = 10 # ability to heal after easing the pain.
        self.immunity = [] # immune to some capsules?
        self.str_mul = 1 # strength multiplier
        self.def_mul = 1 # defense multiplier
        # state
        self.shield = 0 # blocked damage.
        self.pain = 0 # damage taken.
        self.p_pain = 0 # percentage of damage taken / actual hp.
        # owned capsules
        self.capsules = {}
        # capsules used against character
        self.active_c = []
        # some stats
        self.damage_taken = 0
        self.damage_done = 0

        log.write(f'{self} created')

    def roll(self, s=6, n=1):
        """roll the dice."""
        result = [randint(1, s) for i in range(n)]
        log.write(f'{self} dice roll: {result}')
        return tuple(result), sum(result)

    def success(self, target):
        """determine action success"""
        log.write(f'will {self} succeed?')
        S = T = 0
        while S == T:
            #determine success
            S = self.roll(self.sides, n=2)[1] + self.agility
            T = target.roll(target.sides)[1] + target.agility
            if S == T: log.write('** try again **')
        return S > T

    def lucky(self, target):
        """try character's luck"""
        log.write(f'{self} takes a chance...')
        S = T = 0
        while S == T:
            S = self.roll(self.sides, n=2)[1] + self.roll(n=1)[1]
            T = target.roll(target.sides, n=2)[1] + target.roll(n=1)[1]
            if S == T: log.write('** draw **')
        return S > T

    @property
    def sides(self):
        """dice side count"""
        return self.level + 5

    @property
    def is_in_pain(self):
        """is character in pain?"""
        return self.p_pain >= 100

    def __action_keys(self, action_list):
        keys = []
        for action in action_list:
            added = False
            idx = 0
            while not added:
                if not action[idx] in keys:
                    keys.append(action[idx])
                    added = True
                elif not action[idx].upper() in keys:
                    keys.append(action[idx].upper())
                    added = True
                else: idx += 1
                if idx > len(action) - 1:
                    log.write('[ERROR] cannot add key!')
                    break
        return keys

    @property
    def actions(self):
        """character's available actions."""
        if self.hp == 0: return None
        actions = []
        for capsule in self.capsules.values():
            if capsule.active and not capsule.name == 'relieve':
                actions.append(capsule.name)
        if not actions: return F_NOCS
        if self.is_in_pain:
            actions.append('relieve')
            self.activate_capsule('relieve')
        else:
            self.deactivate_capsule('relieve')
        return actions, self.__action_keys([a for a in actions])

    @property
    def stats(self):
        stat1 = f'{self.name} L{self.level} | HP:{self.hp}/{self.maxhp} SH:{self.shield} PN:{self.p_pain}%'
        stat2 = f'STR:{self.strength*self.str_mul}x{self.sides} DEF:{self.defense*self.def_mul}x{self.sides} AGI:{self.agility} HEA:{self.self_healing}%'
        stat3 = f'CPS:[{" ".join([c.display for c in self.active_c])}]'
        return stat1, stat2, stat3

    def can_kill(self, target):
        if self.is_capsule_attached('berserk'): mul = 2
        else: mul = 1
        maxhit = self.strength * self.str_mul * self.sides * mul
        if maxhit >= target.hp + target.shield:
            return True
        else:
            maxhit *= self.p_pain // 100 * mul
            if maxhit >= target.hp + target.shield:
                return True
            else: return False

    def is_immune(self, capsname):
        """return true if character is immune to the capsule"""
        return capsname in self.immunity

    def add_immunity(self, *capsnames):
        for capsname in capsnames:
            self.immunity.append(capsname)

    def activate_capsules(self, but=()):
        for capsule in self.capsules.values():
            if not capsule.name in but:
                capsule.activate()

    def deactivate_capsules(self, but=()):
        for capsule in self.capsules.values():
            if not capsule.name in but:
                capsule.deactivate()

    def activate_capsule(self, capsname):
            capsule = self.get_capsule(capsname)
            if capsule != F_NOCS:
                capsule.activate()
                return 0
            else: return F_NOCS

    def deactivate_capsule(self, capsname):
        capsule = self.get_capsule(capsname)
        if capsule != F_NOCS:
            capsule.deactivate()
            return 0
        else: return F_NOCS

    def get_capsule(self, capsname):
        try:
            return self.capsules[capsname]
        except KeyError:
            log.write(f'{self}: cannot get → no such capsule: {capsname}')
            return F_NOCS

    def heal(self, value=None):
        if self.hp < self.maxhp and self.hp > 0:
            if value is not None: heal = value
            else: heal = self.maxhp * self.self_healing // 100
            self.hp += int(heal)
            if self.hp > self.maxhp: self.hp = self.maxhp
            log.write(f'{self} heals {int(heal)} HP.')

    def has_capsule(self, capsname):
        if capsname in self.capsules.keys():
            return True
        else: return False

    def is_capsule_attached(self, capsname):
        for capsule in self.active_c:
            if capsule.name == capsname: return True
        return False

    def is_capsule_active(self, capsname):
        if not self.has_capsule(capsname):
            return False
        else:
            capsule = self.get_capsule(capsname)
            if capsule != F_NOCS:
                return capsule.active
            else: return False

    def add_capsule(self, *capsnames):
        """add a capsule to the inventory"""
        nocs = []
        for capsname in capsnames:
            try:
                capsule_obj = CAPSULES[capsname]
                capsule = capsule_obj(self)
                self.capsules[capsname] = capsule
                log.write(f'{self} got a new capsule: {capsule.name}')
            except KeyError:
                nocs.append(capsname)
                log.write(f'{self}: cannot add → no such capsule: {capsname}')
                continue
        if nocs: return len(nocs)
        else: return 0

    def use_capsule(self, capsname, target=None):
        """use a capsule for amazing effects!"""
        capsule = self.get_capsule(capsname)
        if capsule != F_NOCS: return capsule.use(target)
        else:
            log.write(f'{self}: cannot use → no such capsule: {capsname}')
            return F_NOCS

    def get_caps_df(self, capsname):
        """get capsule default target"""
        capsule = self.get_capsule(capsname)
        if capsule != F_NOCS: return capsule.d_target
        else: return F_NOCS

    def get_caps_desc(self, capsname):
        """get capsule description"""
        capsule = self.get_capsule(capsname)
        if capsule != F_NOCS: return capsule.description
        else: return F_NOCS


    def drop_capsule(self, capsname):
        """drop a capsule from inventory."""
        if capsname in self.capsules.keys():
            log.write(f'{self} drops {capsname}')
            capsule = self.capsules.pop(capsname)
            del capsule
            return 0
        else: return 1

    def drop_capsules(self, but=()):
        """drop all capsules"""
        for capsname in self.capsules.keys():
            if capsname not in but:
                self.drop_capsule(capsname)


    def attach_capsule(self, capsule, high_priority=False):
        """attach a capsule to character"""
        if high_priority: self.active_c.insert(0, capsule)
        else: self.active_c.append(capsule)

    def detach_capsule(self, capsule):
        """detach a capsule from character"""
        self.active_c.remove(capsule)
        log.write(f'{self}: {capsule.name} is no longer active.')
        capsule.reset()

    def detach_capsules(self):
        """detach all capsules"""
        for capsule in self.active_c:
            capsule.detach()
            capsule.reset()
        self.active_c.clear()

    def capsule_trigger(self, action, *args):
        """triggers capsule effect."""
        if self.active_c:
            for capsule in self.active_c:
                result = capsule.effect(action, *args)
                log.write(f'[TRIGGER] {self}: {capsule.name} {args} → {result}')
                yield result
        else: yield F_NOCS

    def hurt(self, attacker, hit):
        """take damage... feel the pain..."""
        # missed attack
        if hit <= 0: log.write(f'{self} doesn\'t hurt')
        if hit <= 0: return F_NOFX

        result = F_NOCS

        for result in self.capsule_trigger('hurt', attacker, hit):
            if result == F_MISS: hit = 0
            elif result > 0: hit = result

        # attack totally blocked
        if self.shield == hit: self.shield = 0; hit = 0
        elif self.shield > hit: self.shield -= hit; hit = 0
        # attack partially blocked
        elif self.shield < hit: hit -= self.shield; self.shield = 0

        # actual damage taken
        self.hp -= hit
        log.write(f'{self} takes {hit} damage')

        self.damage_taken += hit
        attacker.damage_done += hit

        # still alive?
        if self.hp <= 0: log.write(f'{self} is dead')
        if self.hp <= 0: self.hp = 0; return F_DEAD

        if result != F_NOPN:
            # increase pain gauge
            self.pain += hit
            self.p_pain = self.pain * 100 // self.hp
            log.write(f'{self} pain ({self.pain}) is now {self.p_pain}%')
            #if self.p_pain < 0: self.p_pain = 0
        return hit

    def hpup(self, value):
        log.write(f'{self} HP up +{value}!')
        hp = (self.hp * (self.maxhp + value)) // self.maxhp
        self.maxhp += value
        self.hp = hp

    def levelup(self):
        log.write(f'{self} level up')
        self.maxhp += 50
        self.hp = self.maxhp
        self.level += 1
        self.strength += 1
        self.defense += 1
        self.agility += 1
        self.self_healing += 5
        self.pain = 0
        self.p_pain = 0
        for capsule in self.capsules.values():
            capsule.upgrade()

    def reset(self):
        log.write(f'{self} reset')
        self.hp = hp
        self.detach_capsules()
        self.drop_capsules()

    def __repr__(self):
        return self.name
