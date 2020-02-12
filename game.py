#! /usr/bin/env python
# ⚀ ⚁ ⚂ ⚃ ⚄ ⚅
# ─┌┐│└┘
import random
from time import sleep
import sys
from common import  *
from objects import *
from capsule import *

def choose(text, *choices, default=0):
    keywords = []
    string = text + ' ['

    for index, item in enumerate(choices):
        if index == default and index == len(choices) - 1:
            string += f'<{item}>'
        elif index == default:
            string += f'<{item}>/'
        elif index == len(choices) - 1:
            string += f'{item}'
        else:
            string += f'{item}/'
        keywords.append(item)

    string += ']:'
    keywords = tuple(keywords)
    answer = ''

    while answer not in keywords and answer not in [char[0] for char in keywords]:
        answer = input(f'{string} ')
        if not answer: return default
        if answer.lower() in [char[0] for char in keywords]:
            for key in keywords:
                if key[0] == answer:
                    return keywords.index(key)
    return keywords.index(answer)

class Enemy(Character):
    def action(self, target):
        # too difficult
        #if self.is_in_pain:
        #    # if a pain attack can kill the opponent, give it a try!
        #    pain = self.sides * self.strength
        #    hit = pain * self.p_pain // 100
        #    if hit >= player.hp:
        #        action = self.get_capsule('attack')
        #        result = action.release(player)
        #        return 'release', result

        if self.actions == F_NOCS:
            log.write(f'{self} cannot move')
            return None, F_NOCS

        actions, _ = self.actions
        idx = randint(0, len(actions) - 1)
        capsname = actions[idx]
        d_target = self.get_caps_df(capsname)
        if d_target == 'self': target = self
        else: target = player
        result = self.use_capsule(capsname, target)
        return capsname, result
    def upgrade(self):
        #self.level += 1
        self.maxhp += self.sides * 4
        self.hp = self.maxhp
        self.strength += 1
        self.defense = self.strength - 1
        if self.defense == 0: self.defense = 1
        self.name = f'ENEMY{self.strength}'
        self.pain = 0
        self.p_pain = 0
        self.shield = 0
        self.damage_taken = 0
        self.damage_done = 0
        self.detach_all_capsules()
        self.drop_all_capsules(but=('attack', 'shield', 'timebomb'))

class Boss(Enemy):
    pass

player = Character(name='PLAYER', hp=100, strength=2, agility=2)
enemy = Enemy(name='ENEMY', hp=0, level=1, strength=0, defense=0)
player.add_capsule('attack', 'shield')
enemy.add_capsule('attack', 'shield')
#enemy.add_capsule(Kamikaze(enemy))

print('\x1b[2J\x1b[H')
print(f'-- PAINKILLER (dev) -- {SEED}')
try:
    choose('hit enter to start', 's')
except (KeyboardInterrupt, EOFError):
    sys.exit()

fight = 1

capsules = [c for c in capsules_dict.keys() if c not in ('attack', 'shield')]

while player.hp > 0:
    turn = 1
    played = 0
    player.detach_all_capsules()
    capsule = capsules[random.randint(0, len(capsules) -1)]
    player.add_capsule(capsule)
    capsdesc = player.get_caps_desc(capsule)
    print('\x1b[2J\x1b[H')
    print(f'** you got a capsule → {capsule}: {capsdesc} **')
    sleep(3)
    enemy.upgrade()
    enemy.activate_capsules()
    player.activate_capsules()
    player.shield = 0
    try:
        toggle = random.randint(0, 1)
        while (player.hp > 0) and (enemy.hp > 0):
            if played == 2: turn += 1; played = 0
            if toggle == 0: name = player.name
            else: name = enemy.name
            if player.can_kill(enemy): PKE = '[!]'
            else: PKE = '[ ]'
            if enemy.can_kill(player): EKP = '[!]'
            else: EKP = '[ ]'
            log.write(f'*** FIGHT {fight}: {name.upper()} TURN {turn} ***')
            print('\x1b[2J\x1b[H')
            print(f'[FIGHT {fight} TURN {turn}]')
            log.write(player.stats[0])
            log.write(player.stats[1])
            log.write(f'{PKE} {player.stats[2]}')
            log.write(enemy.stats[0])
            log.write(enemy.stats[1])
            log.write(f'{EKP} {enemy.stats[2]}')
            print(player.stats[0])
            print(player.stats[1])
            print(f'{PKE} {player.stats[2]}')
            print(enemy.stats[0])
            print(enemy.stats[1])
            print(f'{EKP} {enemy.stats[2]}')
            if toggle == 0:
                print('your turn')
                actions, keys = player.actions
                idx = choose(' '.join(actions), *keys)
                capsname = actions[idx]
                d_target = player.get_caps_df(capsname)
                if d_target == 'self': target = player
                else: target = enemy
                result = player.use_capsule(capsname, target)
                print(f'{player} use {capsname}!')
                if capsname == 'attack':
                    if result == F_MISS:
                        print(f'{player} miss...')
                    elif result != F_NOFX:
                        print(f'{player} does {result} damage!')
                elif capsname == 'shield':
                    print(f'{player} +{result} shield')
                elif d_target == 'other':
                    if result == F_MISS:
                        print(f'{player} miss...')
                    elif result == F_NOFX:
                        print(f'{player} ok')
                    else:
                        print(f'{player} does {result} damage!')
                sleep(1)
                toggle = 1
                played += 1
            else:
                print('ENEMY TURN')
                sleep(1)
                capsname, result = enemy.action(player)
                if capsname is None:
                    print(f'{enemy.name} cannot move!')
                else:
                    print(f'{enemy.name} use {capsname}')
                    if capsname == 'attack':
                        if result == F_MISS:
                            print(f'{enemy.name} MISS...')
                        else:
                            print(f'{enemy.name} does {result} damage!')
                    elif capsname == 'shield':
                        print(f'{enemy.name} blocks +{result}')
                    elif capsname ==  'release':
                        if result == F_MISS:
                            print(f'{enemy.name} miss...')
                        else:
                            print(f'{enemy.name} does {result} damage...')
                    elif result == F_MISS:
                        print(f'{enemy.name} miss...')
                    else:
                        print(f'{enemy.name} does {result} damage!')
                sleep(1.5)
                toggle = 0
                played += 1

        print('\x1b[2J\x1b[H')
        print(player.stats[0])
        print(player.stats[1])
        print(player.stats[2])
        print(enemy.stats[0])
        print(enemy.stats[1])
        print(enemy.stats[2])
        if player.hp > 0:
            print('>> victory achieved <<')
            sleep(3)
            if (enemy.strength % 5) == 0:
                player.levelup()
                print(f'** level up **')
            if enemy.strength % 10 == 0:
                enemy.levelup()
                enemy.agility += 2

            sleep(1.5)

            print('choose an upgrade...')
            while True:
                action = choose(f'(f)ull health (h)p up (d)amage up (s)hield up (k)eep {capsule}', 'f', 'h', 'd', 's', 'k')
                if action == 0:
                    if player.hp == player.maxhp:
                        print('you are full health already')
                        print('choose another upgrade:')
                        continue
                    print('full health!')
                    player.hp = player.maxhp
                elif action == 1:
                    print('hp up!')
                    player.hpup(25)
                elif action == 2:
                    print('damage up')
                    player.strength += 1
                elif action == 3:
                    print('shield up')
                    player.defense += 1
                elif action == 4:
                    capsules.remove(capsule)
                    print(f'keep {capsule} capsule')
                if action != 4: player.drop_capsule(capsule)
                print('amen!')
                fight += 1
                break
        else:
            print(f'-- you died --')
        sleep(3)

    except (KeyboardInterrupt, EOFError):
        print('\nbye !')
        break

print(f'SEED: {SEED}')
print(f'total damage taken: {player.damage_taken}')
print(f'damage done: {player.damage_done}')
print('** GAME OVER **')