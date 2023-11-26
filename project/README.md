# Ranger
#### Video Demo:  https://youtu.be/fMA_cJDqOxM
#### Pathfinder 2e Rules:   https://2e.aonprd.com/
## What is Pathfinder 2e?
Pathfinder 2e (PF2e) is a table-top pen-and-paper RPG game (think Dungeons and Dragons). Without delving too deeply into the history, Pathfinder is based on Dungeons and Dragons 3.5 edition. PF2e is the sequel to Pathfinder and has some significant changes. Being descended form D&D, Pathfinder naturally plays similarly.
## Description:
This program, "Ranger" is a simple turn-based battle based on Pathfinder Second Edition rules. It was created as the final project for the Harvard CS50's Introduction to Programming with Python. The basic premise is a battle between a slime and a player over a desired object, "The MacGuffin Muffin." The writing is a bit tongue-in-cheek and should amuse those familiar with tabletop RPG games. Those who are not familiar may find that the humor is lost on them.
The game is text-based with some simple ASCII art for the title and menus. Generally, the game will prompt you for input. If given a menu, you can choose an option by typing it (case insensitive).
The slime enemy uses the statblock for a giant amoeba and the player character is a stripped down level 1 ranger. Being only single battle, it plays more like a visual novel... without the visuals. While there was originally a plan to include some simple spritework and cut-ins during the battle, I pretty quickly decided that coding took precedence over art design (given that coding is the focus of the assignment anyway). There is a single art asset in this folder leftover from this earlier concept (Slime.gif).
Those familiar with Pathfinder 2e or any TTRPG system may notice certain elements missing. Many of these are described below, but the most notable one is the lack of any movement. Movement is a core element of Pathfinder and it is rare to stand toe-to-toe with an opponent without moving whatsoever. This is doubly true with this particular enemy, which is notably slower than most player characters. Kiting it and using hit-and-run tactics would be the go-to strategy. For the purposes of this assignment, I have deemed it an acceptable to leave out - plenty of RPG games restrict all movement once engaged in battle (Final Fantasy, Dragon Quest, and Earthbound are examples of this design). Time constraints were naturally a significant factor.

## Files:
### project.py
This is the main project file for running the game. Requires creatures.py to function properly.

### creatures.py
This contains three basic stat blocks in the form of class objects. It also has a main function that was used for testing functionality.

#### Creature:
This is the basic statblock that could be used to generate any type of creature. It has its own statistics, can take and deal damage, and is able to make a basic strike with proper tracking of the multiple attack penalty (in accordance with Pathfinder 2e rules). They are also able to roll their own dice. In hindsight it might have been better put dice in a separate class, perhaps called "dice cup" which would make it easier to make other types of rolls if the game were to be expanded. It is also notable that when creating a new creature, proficiencies must be set manually as there is not a current function for adding a proficiency bonus. If you guessed that it was cut for time, you would be right!
Due to the limited scope of the project, there are some features that are absent. Status effects are not built into the creature class and instead are part of the main project file. If this project were to be expanded, it would be better to have status effects be an inherent part of the creature class so they could be more easily tracked. It would also make sense for creatures to track their own initiative, making them easier to place in an initiative order for larger battles. As mentioned before, creatures are not able to move so their speed is not tracked. It would also be useful for creatures to be able to perform maneuvers such as grappling and special actions like demoralizing or feinting.
In terms of moving forward, working the above would go a long way towards making creatures more useful and dynamic for placement in future projects. One final feature that would be useful for the class would be an equipment system which would allow armor and items to be tracked and modify statistics.

#### Slime:
The slime inherits most of its features from the creature class (as it should) and also has some attacks unique to it. In the project, it works mostly as it would in PF2e, and I am satisfied with how it turned out.

#### Ranger:
The Ranger, as mentioned, is a stripped down level 1 ranger. Notably, the class is missing the Hunt Prey ability and, by extension, the Hunter's Edge (intended to be Flurry). It is also missing a first-level feat (intended to be Twin Takedown which doesn't function without Hunt Prey). As mentioned before, maneuvers such as trip are absent, as are actions like demoralize. The ranger is hard coded to be equipped with a breastplate, a metal shield (material isn't important as the character doesn't have shield block), and a shortsword. Despite missing a number of class features, the battle seems to be in the ranger's favor in my own playtesting. This is in large part because the slime is vulnerable to slashing damage from the shortsword. Speaking of which, recalling knowledge on a creature is also notably absent, so the player would have difficulty knowing this without referencing the rules separately (amusingly, this is common of older RPG games that have rules and mechanics tucked away in the instruction booklet so... ¯\_(ツ)_/¯).

### test_project.py
This is a quick test of a few functions in project.py. Required for the assignment.

### Slime.gif
This is a leftover art asset from earlier in development.

### requirements.txt
What is says on the tin. A list of libraries required to run the program.
