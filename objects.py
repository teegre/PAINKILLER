from random import randint
from common import *
from capsule import capsules_dict as CAPSULES

class Character():
    """base class for game characters."""
    def __init__(self, name, hp=50, level=1, strength=1, defense=1, agility=1):
        # characteristics
        self.name = name
        self.level = level
        self.maxhp = hp
        self.hp = hp
        self.strength = strength # dice count.
        self.defense = defense # dice count.
        self.agility = agility # ability to hit the opponent.
        self.self_healing = 10 # ability to heal after easing the pain.
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

    @property
    def sides(self):
        """dice sides."""
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
            if capsule.active:
                actions.append(capsule.name)
        if not actions: return F_NOCS
        if self.is_in_pain: actions.append('release')
        return actions, self.__action_keys([a for a in actions])

    @property
    def stats(self):
        stat1 = f'{self.name} L{self.level} | HP:{self.hp}/{self.maxhp} SH:{self.shield} PN:{self.p_pain}%'
        stat2 = f'STR:{self.strength}x{self.sides} DEF:{self.defense}x{self.sides} AGI:{self.agility} HEA:{self.self_healing}%'
        stat3 = f'CPS:[{" ".join([c.display for c in self.active_c])}]'
        return stat1, stat2, stat3

    def can_kill(self, target):
        if self.is_capsule_active('berserk'): mul = 2
        else: mul = 1
        maxhit = self.strength * self.sides * mul
        if maxhit >= target.hp + target.shield:
            return True
        else:
            maxhit *= self.p_pain // 100 * mul
            if maxhit >= target.hp + target.shield:
                return True
            else: return False


    def activate_capsules(self):
        for capsule in self.capsules.values():
            capsule.active = True

    def deactivate_capsules(self, but=()):
        for capsname in self.capsules.keys():
            if not capsname in but:
                self.capsules[capsname].active = False

    def get_capsule(self, capsname):
        try:
            return self.capsules[capsname]
        except KeyError:
            log.write(f'{self}: cannot get → no such capsule: {capsname}')
            return F_NOCS

    def ease_the_pain(self, target):
        capsule = self.get_capsule('attack')
        if capsule:
            return capsule.use(target, ease=True)
        else: return F_NOFX

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
        if nocs: return F_NOCS
        else: return 0

    def use_capsule(self, capsname, target=None):
        """use a capsule for amazing effects!"""
        try:
            if capsname == 'release':
                return self.ease_the_pain(target)
            else:
                capsule = self.capsules[capsname]
                return capsule.use(target)
        except KeyError:
            log.write(f'{self}: cannot use → no such capsule: {capsname}')
            return F_NOCS

    def get_caps_df(self, capsname):
        """get capsule default target"""
        try:
            if capsname == 'release': return 'other'
            else:
                capsule = self.get_capsule(capsname)
                return capsule.d_target
        except:
            return F_NOCS

    def get_caps_desc(self, capsname):
        try:
            if capsname == 'release': return 'release the pain.'
            else:
                capsule = self.get_capsule(capsname)
                return capsule.description
        except:
            return F_NOCS


    def drop_capsule(self, capsname):
        """drop a capsule from inventory."""
        if capsname in self.capsules.keys():
            log.write(f'{self} drops {capsname}')
            capsule = self.capsules.pop(capsname)
            del capsule

    def drop_all_capsules(self, but=()):
        for capsname in self.capsules.keys():
            if capsname not in but:
                self.drop_capsule(capsname)


    def attach_capsule(self, capsule, high_priority=False):
        """attach a capsule to the character."""
        if high_priority: self.active_c.insert(0, capsule)
        else: self.active_c.append(capsule)

    def detach_capsule(self, capsule):
        self.active_c.remove(capsule)
        log.write(f'{self}: {capsule.name} is no longer active.')
        capsule.reset()

    def detach_all_capsules(self):
        for capsule in self.active_c:
            log.write(f'{self}: {capsule.name} is no longer active.')
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
        #return F_NOFX

    def hurt(self, attacker, hit):
        """feel the pain..."""
        # missed attack
        if hit <= 0: log.write(f'{self} doesn\'t hurt')
        if hit <= 0: return F_NOFX

        # attack totally blocked
        if self.shield == hit: self.shield = 0; hit = 0
        elif self.shield > hit: self.shield -= hit; hit = 0
        # attack partially blocked
        elif self.shield < hit: hit -= self.shield; self.shield = 0

        result = F_NOCS

        for result in self.capsule_trigger('hurt', attacker, hit):
            if result == F_MISS: hit = 0
            elif result > 0: hit = result

        # actual damage taken
        self.hp -= hit
        log.write(f'{self} takes {hit} damage')

        self.damage_taken += hit
        attacker.damage_done += hit

        # still alive?
        if self.hp <= 0: log.write(f'{self} is dead')
        if self.hp <= 0: self.hp = 0; return 0
        else:
            # increase pain gauge
            if result != F_NOPN:
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

    def __repr__(self):
        return self.name
