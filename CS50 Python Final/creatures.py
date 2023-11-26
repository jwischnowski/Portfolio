import random
import math

# Need a function to update skills and HP based on level and proficiency


class Creature:
    def __init__(self, str=0, dex=0, con=0, int=0, wis=0, cha=0):
        self.level = 0
        self.actions = 3
        self.penalty = 0
        self.shield = 0

        # Ability scores
        self.str = str
        self.dex = dex
        self.con = con
        self.int = int
        self.wis = wis
        self.cha = cha

        # Ability modifiers
        self.strmod = math.floor((self.str - 10) / 2)
        self.dexmod = math.floor((self.dex - 10) / 2)
        self.conmod = math.floor((self.con - 10) / 2)
        self.intmod = math.floor((self.int - 10) / 2)
        self.wismod = math.floor((self.wis - 10) / 2)
        self.chamod = math.floor((self.cha - 10) / 2)

        # Stats based on ability mods
        # Hitpoints
        self.maxhp = self.conmod
        self.hp = self.maxhp
        # HP should be conmod + racebonus + level * classhp
        self.ac = 10 + self.dexmod
        self.base_ac = self.ac
        self.saves = {
            "fort": (self.conmod),
            "ref": (self.dexmod),
            "will": (self.wismod),
        }
        self.perception = self.wismod
        self.skills = {
            "acrobatics": self.dexmod,
            "arcana": self.intmod,
            "athletics": self.strmod,
            "crafting": self.intmod,
            "deception": self.chamod,
            "diplomacy": self.chamod,
            "intimidation": self.chamod,
            "lores": {"General Lore": self.intmod},
            "medicine": self.wismod,
            "nature": self.wismod,
            "occultism": self.intmod,
            "performance": self.chamod,
            "religion": self.wismod,
            "society": self.intmod,
            "stealth": self.dexmod,
            "survival": self.wismod,
            "thievery": self.dexmod,
        }

    # Healing from damage/increasing HP
    def heal(self, n):
        self.hp = self.hp + n
        if self.hp > self.maxhp:
            self.hp = self.maxhp
        return self.hp

    # Taking damage/decreasing HP
    def damage(self, n):
        self.hp = self.hp - n
        return self.hp

    @property
    def maxhp(self):
        return self._maxhp

    @maxhp.setter
    def maxhp(self, maxhp):
        if maxhp < 0:
            maxhp = 0
        self._maxhp = maxhp

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, hp):
        self._hp = hp

    # Dice. "s" is sides, "n" is number of dice. Each creature can roll it's own dice!
    def d(self, s=20, n=1):
        dice = []
        for _ in range(n):
            dice.append(random.randint(1, s))
        return dice

    def take_action(self, n=0):
        self.actions = self.actions - n
        return self.actions

    def refresh_actions(self):
        self.actions = 3
        self.penalty = 0
        self.shield = 0
        return self.actions

    def attack_penalty(self, n):
        # n is the penalty multiplier
        self.penalty = self.penalty + n
        if self.penalty > 2:
            self.penalty = 2
        return self.penalty

    def initiative(self):
        initiative = self.d(20)[0] + self.perception
        return initiative

    # The basic strike function
    def strike(
        self, attack_bonus=0, penalty_mod=5, dice=0, sides=0, damage_bonus=0, type=None
    ):
        roll = self.d(20)[0]
        damage = 0
        for _ in range(dice):
            damage += self.d(sides)[0]
        attack = {
            "dc": (roll + attack_bonus) - (self.penalty * penalty_mod),
            "damage": damage + damage_bonus,
            "type": str(type),
            "critical": False,
        }
        if roll == 20:
            attack["critical"] = True
            attack["damage"] *= 2
            attack["dc"] += 10
        self.take_action(1)
        self.attack_penalty(1)
        return attack


# Slime enemy
class Slime(Creature):
    def __init__(self, str=0, dex=0, con=0, int=0, wis=0, cha=0):
        super().__init__(str=16, dex=14, con=14, int=0, wis=10, cha=0)
        self.recall_occult = 15
        self.maxhp = 45
        self.hp = self.maxhp
        self.ac = 8
        self.base_ac = self.ac
        self.saves = {"fort": 7, "ref": 3, "will": 5}
        self.perception = 4
        self.skills["athletics"] = 6
        self.skills["stealth"] = 3

    def pseudopod(self):
        d20 = self.d(20, 2)
        attack = {
            "dc": (d20[0] + 8) - (self.penalty * 5),
            "damage": [self.d(6)[0], "acid"],
            "grab": d20[1] + self.skills["athletics"],
        }
        self.take_action(1)
        self.attack_penalty(1)
        return attack

    def constrict(self):
        # Against Fortitude save
        attack = {
            "dc": 17,
            "damage": [self.d(4)[0], "bludgeoning", self.d(4)[0], "acid"],
        }
        self.take_action(1)
        self.attack_penalty(1)
        return attack

    def envelop(self):
        # Against Fortitude save
        attack = {"dc": 17, "damage": [self.d(6)[0], "acid"], "rupture": 3}
        self.take_action(3)
        return attack

    def engulfed(self):
        attack = {"dc": 17, "damage": [self.d(6)[0], "acid"], "rupture": 3}
        return attack


# Ranger Character
class Ranger(Creature):
    def __init__(self, str=0, dex=0, con=0, int=0, wis=0, cha=0):
        super().__init__(str=18, dex=12, con=14, int=12, wis=12, cha=10)
        self.maxhp = 20
        self.hp = self.maxhp
        self.ac = 18
        self.base_ac = self.ac
        self.prey = None
        self.saves = {"fort": 7, "ref": 6, "will": 4}
        self.perception = 6
        self.skills["athletics"] = 7
        self.skills["crafting"] = 4
        self.skills["diplomacy"] = 3
        self.skills["lores"]["forest terrain"] = 4
        self.skills["medicine"] = 4
        self.skills["nature"] = 4
        self.skills["occultism"] = 4
        self.skills["stealth"] = 4
        self.skills["survival"] = 4

    def hunt_prey(self, n):
        self.prey = str(n)
        self.take_action(1)
        return self.prey

    # Agile is a cumulative -4 penalty
    # Flurry is a cumulative -3
    # Flurry with agile is a cumulative -2

    def strike_shortsword_pierce(self):
        attack = self.strike(
            attack_bonus=7,
            penalty_mod=4,
            dice=1,
            sides=6,
            damage_bonus=4,
            type="piercing",
        )
        return attack

    def strike_shortsword_slash(self):
        attack = self.strike(
            attack_bonus=7,
            penalty_mod=4,
            dice=1,
            sides=6,
            damage_bonus=4,
            type="slashing",
        )
        return attack

    def strike_shield_bash(self):
        attack = self.strike(
            attack_bonus=7, dice=1, sides=6, damage_bonus=4, type="bludgeoning"
        )
        return attack

    def twin_takedown(self, x, y):
        self.actions += 1
        attack = x, y
        return attack

    def grapple(self):
        attack = self.strike(attack_bonus=7)
        return attack

    def trip(self):
        attack = self.strike(attack_bonus=7)
        return attack

    def battle_medicine(self):
        attack = self.d(20)[0] + 7
        if attack > 25:
            healing = {
                "amount": (self.d(6)[0] + self.d(6)[0]) * 2,
                "success": "critical success",
            }
        elif attack > 14:
            healing = {"amount": self.d(6)[0] + self.d(6)[0], "success": "success"}
        elif 8 < attack < 15:
            healing = {"amount": 0, "success": "failure"}
        elif attack == 8:
            healing = {"amount": -(self.d(6)[0]), "success": "critical failure"}
        self.take_action(1)
        self.heal(healing["amount"])
        return healing


# Testing portion
def main():
    slime = Slime()
    print(slime.constrict()["damage"][0])
    print(slime.actions)
    ranger = Ranger()
    print(ranger.strike_shortsword_pierce())
    print(ranger.penalty)
    print(ranger.strike_shortsword_pierce())
    print(ranger.penalty)
    print(ranger.strike_shortsword_pierce())
    print(ranger.penalty)
    print(ranger.strike_shortsword_pierce())
    print(ranger.penalty)
    ranger.refresh_actions()
    print(ranger.strike_shortsword_pierce())
    print(ranger.penalty)
    print(ranger.battle_medicine())
    print(ranger.trip())


if __name__ == "__main__":
    main()
