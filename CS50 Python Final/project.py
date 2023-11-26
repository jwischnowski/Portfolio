import time
import os
import sys
import re
# pip install pyfiglet
from pyfiglet import figlet_format
# pip install py-getch
import getch

from creatures import Slime
from creatures import Ranger
slime = Slime()
ranger = Ranger()

def main():
    # Title screen
    os.system('cls||clear')
    print(figlet_format("Ranger", font="larry3d", justify="center"))
    getch.pause()

    # Opening Crawl
    os.system('cls||clear')
    #string = str(
    #"""You are walking in the woods. There is no one around and your phone is dead. Out of the corner of your eye
    #you spot him. Shia LaBeouf\n"""
    #)
    slowprint(
        """You trudge through the Ancient Forest. The old crone told you that what you sought is deep in this
uncharted place. Though it is midday, the forest floor is cloaked in shadow as the dense canopy filters
all but a few rays of sunlight. All is quiet as you mask your footfalls and slowly creep forward.
Suddenly, something lunges from behind a bush, narrowly flying over your sholder and landing behind you.
You whirl about to face your attacker and unsheathe your blade. Before you is a glistening, blue slime
and within it, the very object you seek - a hunk of the MacGuffin Muffin!\n\n"""
)
    getch.pause()
    os.system('cls||clear')

    # Opening Choice
    choicesmenu = (
        f"""
        ┌──────────────────────────────┐
        │ What will you do?            │▒
        ╞══════════════════════════════╡▒
        │ Fight!                       │▒
        │ Seduce                       │▒
        │ Run Away                     │▒
        └──────────────────────────────┘▒
         ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        \n""")
    while True:
        choice = input(choicesmenu).strip().casefold()
        if re.search(r"^fight!?$", choice):
            os.system('cls||clear')
            print(choice)
            slowprint("You decide to engage the slime the old fashioned way!\n\n")
            time.sleep(1)
            getch.pause()
            break
        elif choice == "seduce":
            os.system('cls||clear')
            print(choice)
            slowprint(
"""You've heard tales of bards convincing dragons to leave their hoards with a well-executed seduction.
You muster up every ounce of charisma and attempt to seduce the slime with a smooth pickup line…
Unfortunately, you forgot that you were a ranger, not a bard and you dumped your charisma stat because you
wanted more constitution. The slime is thoroughly unimpressed.\n\n"""
                )
            time.sleep(1)
            getch.pause()
            break
        elif choice == "run away":
            os.system('cls||clear')
            print(choice)
            slowprint(
"""This battle seems dangerous and, besides, railroading is lame. The whole situation is contrived and silly
so you decide to leave. You spend the rest of the campaign dodging progressively more absurd plot hooks thrown
at you by an increasingly frustrated DM.

“Sorry! I don't want any adventures, thank you. Not Today. Good morning! But please come to tea -any time you
like! Why not tomorrow? Good bye!”
J.R.R. Tolkien, The Hobbit"""
            )
            getch.pause("\n\nYou got the Hobbitism ending! Press any key to exit.")
            sys.exit()
        else:
            os.system('cls||clear')
            print("Input not recognized. Try typing one of the options in the menu.")
            continue

    # Battle Initiative
    os.system('cls||clear')
    slowprint("Roll for initiative!\n")
    time.sleep(1)
    slimespeed = slime.initiative()
    rangerspeed = ranger.initiative()
    print(f"You rolled {rangerspeed}. Slime rolled {slimespeed}.")
    time.sleep(1)
    if slimespeed > rangerspeed:
        player_phase = False
        print("The Slime makes its move first!")
    else:
        player_phase = True
        print("You move first!")
        time.sleep(.5)

    # Battle flow
    ranger_grabbed = False
    ranger_engulfed = False
    ranger_medicine = True
    engulf_can_damage = True
    while ranger.hp > 0 and slime.hp > 0:

        # Flat footed condition
        if ranger_grabbed == True:
            ranger.ac = ranger_flat_footed(True)
        else:
            ranger.ac = ranger_flat_footed(False)

        # Engulfed condition
        if ranger_engulfed == True:
            slime.ac = slime_flat_footed(True)
        else:
            slime.ac = slime_flat_footed(False)

        # Player phase
        # Battle Menu
        hp = "{:02d}".format(ranger.hp)
        maxhp = "{:02d}".format(ranger.maxhp)
        menu = (
            f"""
            ┌──────────────────────────────┐
            │ HP: {hp}/{maxhp}                    │▒
            │ Actions: {ranger.actions}                   │▒
            ╞══════════════════════════════╡▒
            │ Slash (Shortsword)           │▒
            │ Stab  (Shortsword)           │▒
            │ Bash  (Shield)               │▒
            │ Battle Medicine              │▒
            │ Struggle                     │▒
            │ Wait                         │▒
            └──────────────────────────────┘▒
             ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
            """)

        if player_phase == True and ranger.hp > 0:
            # Damage at the start of the turn if engulfed by the slime
            if ranger_engulfed == True and engulf_can_damage == True:
                engulf_can_damage = False
                attack = slime.engulfed()
                time.sleep(1)
                print("\nYou are still engulfed by the Slime!")
                time.sleep(.5)
                if attack["dc"] >= ranger.saves["fort"] + 20:
                    # Double damage
                    print("CRITICAL!!")
                    ranger.damage(attack["damage"][0]*2)
                    print(f"You take {attack["damage"][0]*2} {attack["damage"][1]} damage!")
                elif attack["dc"] >= ranger.saves["fort"] + 10:
                    # Normal damage
                    ranger.damage(attack["damage"][0])
                    print(f"You take {attack["damage"][0]} {attack["damage"][1]} damage!")
                elif attack["dc"] > ranger.saves["fort"]:
                    # Half damage
                    print("You manage to resist its attack!")
                    ranger.damage(attack["damage"][0]/2)
                    print(f"You take {attack["damage"][0]/2} {attack["damage"][1]} damage!")
                else:
                    # No damage
                    print("You manage to steel yourself and take no damage!")

            move = input(f"\n{menu}\n\nWhat will you do?\n").strip().casefold()

            # Wait
            if move == "wait":
                print("You wait for the Slime to make a move.")
                ranger.actions = 0
                time.sleep(1)

            # Escape
            elif move == "struggle":
                if ranger_grabbed == True:
                    time.sleep(.3)
                    print("You attempt to struggle free...")
                    time.sleep(.5)
                    # A bit of fudgery. For this assignment, the ranger's athletics and attack bonus are the
                    # same. Since shield bash already adds to the multiple attack penalty, takes an action, and
                    # rolls a DC, I am using it instead of building a new escape function for the class.
                    roll = ranger.strike_shield_bash()
                    if roll["dc"] >= 17:
                        ranger_grabbed = False
                        ranger_engulfed = False
                        print("You successfully escape the Slime!")
                    else:
                        print("You struggle but fail to break the slime's grasp!")
                else:
                    print("You wiggle around a bit in your armor. Since you're not grabbed, there is nothing to escape from.")

            # Sword slash
            elif move == "slash":
                attack = ranger.strike_shortsword_slash()
                time.sleep(.3)
                print("You slash with your shortsword...")
                time.sleep(.5)
                if attack["dc"] >= slime.ac:
                    slime.damage(attack["damage"]+5)
                    if attack["dc"] >= slime.ac + 10:
                        print("CRITICAL!!")
                    if ranger_engulfed == True and attack["damage"] >= 3:
                        print("You damage the Slime enough to break free and are no longer engulfed!")
                    print(f"The Slime takes {attack['damage']+5} {attack['type']} damage!")
                    if slime.hp < (slime.maxhp/2):
                        print(f"The Slime is looking rough!")
                else:
                    print("Your attack missed!")

            # Sword stab
            elif move == "stab":
                attack = ranger.strike_shortsword_pierce()
                time.sleep(.3)
                print("You stab with your shortsword...")
                time.sleep(.5)
                if attack["dc"] >= slime.ac:
                    slime.damage(attack["damage"])
                    if attack["dc"] >= slime.ac + 10:
                        print("CRITICAL!!")
                    if ranger_engulfed == True and attack["damage"] >= 3:
                        print("You damage the Slime enough to break free and are no longer engulfed!")
                    print(f"The Slime takes {attack['damage']} {attack['type']} damage!")
                    if slime.hp < (slime.maxhp/2):
                        print(f"The Slime is looking rough!")
                else:
                    print("Your attack missed!")

            # Shield bash
            elif move == "shield bash" or move == "bash":
                if ranger_engulfed == False:
                    attack = ranger.strike_shield_bash()
                    time.sleep(.3)
                    print("You strike with your shield...")
                    time.sleep(.5)
                    if attack["dc"] >= slime.ac:
                        if attack["dc"] >= slime.ac + 10:
                            print("CRITICAL!!")
                        slime.damage(attack["damage"])
                        print(f"The Slime takes {attack['damage']} {attack['type']} damage!")
                        if slime.hp < (slime.maxhp/2):
                            print(f"The Slime is looking rough!")
                    else:
                        print("Your attack missed!")
                else:
                    print("Your shield is too bulky to swing while engulfed!")

            # Battle medicine
            elif move == "battle medicine":
                flat_check = 20
                if ranger_grabbed == True:
                    flat_check = ranger.d(20)
                if flat_check[0] < 5:
                    time.sleep(.3)
                    ranger.actions -= 1
                    print("The Slime's grapple interferes with your attempt and the action is wasted!")
                else:
                    healing = ranger.battle_medicine()
                    time.sleep(.3)
                    if ranger_medicine == True:
                        ranger_medicine = False
                        print("You attempt to patch yourself up...")
                        if healing["success"] == "critical success":
                            print(f"Critical success! You heal {healing["amount"]} HP!")
                        elif healing["success"] == "success":
                            print(f"Success! You heal {healing["amount"]} HP!")
                        elif healing["success"] == "failure":
                            print("Failure! You don't manage to heal yourself!")
                        else:
                            print(f"Critical failure! Your attempt goes so poorly that you manage to deal {healing["amount"]} damage to yourself!")
                    else:
                        print("Can't attempt to treat wounds for another hour!")

            else:
                print("Can't do that now! Try another move!")

            # End of turn
            if ranger.actions == 0:
                player_phase = False
                ranger.refresh_actions()
                if ranger_engulfed == True:
                    ranger.actions -= 1
                engulf_can_damage = True

        # Enemy phase
        if player_phase == False and slime.hp > 0:
            if slime.actions == 3:
                print("\nSlime's turn!")
            time.sleep(1)
            # Pseudopod attack
            if ranger_grabbed == False:
                attack = slime.pseudopod()
                print("\nThe Slime extends a pseudopod to attack!")
                time.sleep(1)
                if attack["dc"] >= ranger.ac:
                    ranger.damage(attack["damage"][0])
                    # Double damage on a critical. Not baked into the Slime class yet
                    if attack["dc"] >= ranger.ac + 10:
                        ranger.damage(attack["damage"][0])
                        print("CRITICAL!!")
                    print(f"You take {attack['damage'][0]} {attack['damage'][1]} damage!")
                    ranger_grabbed = True
                    print("You were grabbed by the Slime!")
                else:
                    print("The Slime misses it's attack!")

            # Engulf
            if ranger_grabbed == True and slime.actions == 3 and ranger_engulfed == False:
                attack = slime.envelop()
                print("\nThe Slime attempts to engulf you!")
                time.sleep(1)
                if attack["dc"] >= ranger.saves["fort"] + 10:
                    ranger_engulfed = True
                    print("You are engulfed by the slime!")
                    if attack["dc"] >= ranger.saves["fort"] + 20:
                        # Double damage
                        print("CRITICAL!!")
                        ranger.damage(attack["damage"][0]*2)
                        print(f"You take {attack["damage"][0]*2} {attack["damage"][1]} damage!")
                    elif attack["dc"] >= ranger.saves["fort"] + 10:
                        # Normal damage
                        ranger.damage(attack["damage"][0])
                        print(f"You take {attack["damage"][0]} {attack["damage"][1]} damage!")
                    elif attack["dc"] > ranger.saves["fort"]:
                        # Half damage
                        print("You manage to resist its attack!")
                        ranger.damage(attack["damage"][0]/2)
                        print(f"You take {attack["damage"][0]/2} {attack["damage"][1]} damage!")
                    else:
                        # No damage
                        print("You manage to steel yourself and take no damage!")
                else:
                    print("The slime fails to engulf you!")

            # Constrict
            elif ranger_grabbed == True:
                attack = slime.constrict()
                print("\nThe Slime attempts to constrict you!")
                time.sleep(1)
                if attack["dc"] >= ranger.saves["fort"] + 20:
                    # Double damage
                    print("CRITICAL!!")
                    ranger.damage(attack["damage"][0]*2)
                    ranger.damage(attack["damage"][2]*2)
                    print(f"You take {attack["damage"][0]*2} {attack["damage"][1]} and {attack["damage"][2]*2} {attack["damage"][3]} damage!")
                elif attack["dc"] >= ranger.saves["fort"] + 10:
                    # Normal damage
                    ranger.damage(attack["damage"][0])
                    ranger.damage(attack["damage"][2])
                    print(f"You take {attack["damage"][0]} {attack["damage"][1]} and {attack["damage"][2]} {attack["damage"][3]} damage!")
                elif attack["dc"] > ranger.saves["fort"]:
                    # Half damage
                    print("You manage to resist its attack!")
                    ranger.damage(attack["damage"][0]/2)
                    ranger.damage(attack["damage"][2]/2)
                    print(f"You take {attack["damage"][0]/2} {attack["damage"][1]} and {attack["damage"][2]/2} {attack["damage"][3]} damage!")
                else:
                    # No damage
                    print("You manage to shrug off its attack and take no damage!")


            if slime.actions == 0:
                player_phase = True
                slime.refresh_actions()

    if slime.hp <= 0:
        ranger_grabbed = False
        ranger_engulfed = False
        time.sleep(1)
        os.system('cls||clear')
        slowprint(
"""Through your wit and skill, you managed to best the slime and claim the chunk of the MacGuffin Muffin
for yourself!\n"""
        )
        getch.pause("You defeated the slime! Gained 100 XP! Press any key to exit.")
        sys.exit()

    if ranger.hp <= 0:
        time.sleep(1)
        os.system('cls||clear')
        slowprint(
"""You black out... When you awake, you somehow find yourself at the last inn you visited... also, half
of your Gold is missing!\n"""
        )
        getch.pause("You were defeated! Press any key to exit.")
        sys.exit()

def slowprint(s, speed=.025):
    string = str(s)
    for char in string:
        print(char, end="", flush=True)
        time.sleep(speed)

def ranger_flat_footed(n):
        # Flat-footed condition. Should be in creature class but isn't due to time constraints
        if n == True:
            return ranger.base_ac - 2
        elif n == False:
            return ranger.base_ac
        else:
            raise ValueError("Function only accepts 'True' or 'False' as arguments")

def slime_flat_footed(n):
        if n == True:
            return slime.base_ac - 2
        elif n == False:
            return slime.base_ac
        else:
            raise ValueError("Function only accepts 'True' or 'False' as inputs")

if __name__ == "__main__":
    main()
