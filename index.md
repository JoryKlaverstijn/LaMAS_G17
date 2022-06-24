### The Werewolves of Millers Hollow

The Werewolves of Millers Hollow is a social deduction game with multiple different player roles, in which the players attempt to figure out the roles of the other players. The role of each player is hidden from the other players and can only be revealed through a couple of game mechanics. The roles are divided up into wolves and villagers. The wolves attempt to kill off all the villagers to win the game, while the villagers attempt to kill all of the wolves to win the game. Each day a single game cycle takes place in which all phases of the game cycle are ran through. There are two voting moments in the game cycle: only the werewolves can vote on who they want to kill at night and all of the players can vote on who they want to kill during the day.

This report is structured by first explaining the specific game details of The Werewolves of Millers Hollow, after which simplifications we introduced are discussed, leading into kripke model formalizations of the simulations and results from running the simulations.

## Roles
There are several different roles in the game. Note that all roles are villagers, except the werewolves.

# Werewolves
The werewolves attempt to kill off all the villagers. Each night they wake up to share information and to vote on who they want to kill.

# Thief
The thief is allowed to switch its own role. After having seen its own role, the thief is allowed to switch its role card with one of two randomly drawn cards from the role deck on the first night.

# Cupid
Cupid can appoint two other players to be lovers, but only on the first night.

# Lovers
Lovers become aware that they are each other's lovers after cupid has made them so on the first night. If one lover dies, the other lover dies as well and lovers can not vote against one another. If either of the lovers is a werewolf while the other is not, then they need to eliminate all other players to win.

# Seer
The seer can view the role card of another player each night.

# Witch
The witch has two potions, one potion that can save a werewolf victim and one potion that can kill another player, she can use both potions only once. The witch is capable of saving herself if the werewolves attempted to kill her.

# Little girl
The little girl is allowed to spy on the werewolves during the werewolf phase. However she must be careful to avoid the werewolves detecting her.

# Hunter
When the hunter is killed, he is allowed to kill one other player of their choosing.

# Mayor
The mayor is an additional role card that can be given to any of the players. The players can vote on who gets to be the mayor. The mayor gets two votes instead of one.

## Game cycle & Discussions
The game starts by each player being given a role card and each player realising their own role. The first night then commences in which several players can take special first night actions, these include: The thief, cupid and the lovers. Afterwards the other players also perform their nightly actions. The werewolves are allowed to exchange information and to vote on who they want to kill, while the little girl will want to spy on them. The seer and witch will also take their actions after. After the night is over, the players should vote on who they want to make the mayor of the village. Afterwards they can exchange information and can vote on who they want to kill. The game then progresses into the night again, with the thief, cupid and the lovers now taking no more action.

## Simplifications
Due to the complexity of the game there were some simplifications introduced. The primary simplification is related to the fact that there are too many roles in the original game to represent it in a kripke model. Therefore we decided to remove some of the roles and reduce the amount of players in the game. The amount of players therefore is 8 with 3 of those being ordinary villagers, 2 being werewolves, 1 being the little girl and 2 being seers. Another related simplification that was introduced was the roles that each player assigns to itself and the other players (its perceived state of reality). Normally this would include all the roles that are in the game, but since the villager roles are not important to know for other villagers it is sufficient for the villagers to know if a player is a wolf or not. For the wolves this is slighlty different as they would benefit more from killing off players that have a higher chance of killing them such as the little girl or the seer. Therefore there are three roles that are perceived by the players in the game: wolf, not a wolf or other. Other includes anything that is not an ordinary villager and a wolf.

## Kripke Model Formalization
Explanation of the individual kripke models for each player, also explanation of how each player is capable of higher order knowledge. Include state figures here!

## Simple example game Kripke model analysis
Milan?

## Experiments & Results

## Results analysis

### GitHub PAGES INSTRUCTIONS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

## Welcome to GitHub Pages

You can use the [editor on GitHub](https://github.com/JoryKlaverstijn/LaMAS_G17/edit/gh-pages/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/JoryKlaverstijn/LaMAS_G17/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
