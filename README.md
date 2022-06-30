![example_game_image](https://user-images.githubusercontent.com/63673224/175604435-8988f655-de08-4108-8807-48e137f28f32.png)

# Setup
1) Install all required libraries (`pip install numpy`, `pip install pygame`, `pip install matplotlib`)
2) Take a look at the [Game rules](https://www.ultraboardgames.com/the-werewolves-of-millers-hollow/game-rules.php)
3) Change the amount of players per role in `gameloop.py` (Optional)
3) Run `python gameloop.py`

# General game explanation
In this game there are multiple roles. The wolves' goal is to kill all villagers.
The villagers' goal is to kill all wolves. The wolves are generally outnumbered
by villagers, but they know who the other wolves are, whereas the villagers do not know who the wolves are.
By means of voting, the villagers must try and kill all wolves, before the wolves
kill every villager during the night. The villagers can have various special sub-roles, like
a seer who can reveal someone's identity, or a little girl who can peek while
the wolves are killing someone.

# Logic explanation
Each agent's knowledge is modeled by a separate Kripke model. In each model, the relations of all agents between the worlds are modeled.
Only when an agent finds information out, or finds out that someone else knows something, their Kripke model is updated.
The good players are allowed to discuss knowledge, and make a voting decision based on their knowledge.
 
# Controls
* `Step` or space-bar: Progresses the game by 1 step
* `Reset` or backspace: Restarts the game and initializes new players
* `^` or arrow-up key: Scrolls the text chat upwards (if possible)
* `v` or arrow-down key: Scrolls the text chat downwards (if possible)
* `1-8`: Buttons for displaying the Kripke model of player 1-8

# Code structure
* `images/` A folder containing player card images
* `PlayerClasses/`: A folder containing all the player implementations
* `mlsolver/`: Module containing the logic for kripke model, including the model definition
* `Button.py`: Class for general clickable buttons
* `Colors.py`: A file containing some often-used RGB colors
* `Game.py`: Class containing the main game logic and state
* `gameloop.py`: The main driver of the program
* `gameloop_novisual.py`: Runs the game without gui (for experiments)
* `names.cvs`: Contains some randomly generated names using the [names](https://pypi.org/project/names/) library
* `TextChat.py`: Class for the in-game chat showing messages and events
* `Controller.py`: Class for handling any key/mouse events
* `View.py`: Handles the drawing of all the game components
