# The Werewolves of Millers Hollow
![example_game_image](https://user-images.githubusercontent.com/63673224/175807188-43e3595d-a05a-43f4-8b30-dd6a8869e262.png)

The Werewolves of Millers Hollow is a social deduction game with multiple different player roles, in which the players attempt to figure out the roles of the other players. The role of each player is hidden from the other players and can only be revealed through a couple of game mechanics. The roles are divided up into wolves and villagers. The wolves attempt to kill off all the villagers to win the game, while the villagers attempt to kill all of the wolves to win the game. Each day a single game cycle takes place in which all phases of the game cycle are ran through. There are two voting moments in the game cycle: only the werewolves can vote on who they want to kill at night and all of the players can vote on who they want to kill during the day.

This report has the following structure: First the simplified version of the Werewolves of Millers Hollow that we used in our simulations is explained, afterwards, kripke model formalizations of the simulations and results from running the simulations are shown.

## Roles
There are several different roles in the game. In the game there are multiple roles that are not used in our simplified version of the game, these include: The thief, cupid, the lovers the witch and the mayor mechanic. Note that all roles are villagers, except the werewolves.

### Werewolves
The werewolves attempt to kill off all the villagers. Each night they wake up to share information and to vote on who they want to kill.

### Seer
The seer can view the role card of another player each night.

### Little girl
The little girl is allowed to spy on the werewolves during the werewolf phase. However she must be careful to avoid the werewolves detecting her.

### Hunter
When the hunter is killed, he is allowed to kill one other player of their choosing.

### Villager
The ordinary villager has no extra actions that it can take, the only decisions it can make are related to voting during the day time.

## Simplifications
Due to the complexity of the game some simplifications were made to the original game. The primary simplification is related to the fact that there are too many roles in the original game to represent it in a kripke model without the amount of possible worlds and relations exploding in complexity. Therefore we decided to remove some of the roles and reduce the amount of players in the game. The maximum amount of players that can be used in the game is 8, with there being 5 different roles instead of the original 8. We also decided to remove the mayor and lovers mechanic. The amount of roles and the roles that can be taken by the players is dynamic, with different combinations being possible.

Another related simplification that was introduced was the roles that each player assigns to itself and the other players (its perceived state of reality). Normally this would include all the roles that are in the game, but since this makes the amount of possible worlds in the kripke models explode into the millions, we decided to approach it from a different angle. For the villagers it is sufficient to know if a person is a wolf or not, since they only care about removing wolves from the game. For the wolves it is important that they know who the villagers are, but also what type of villagers they are; they are more interested in removing some role types from the game earlier than other role types. These role types include the little girl and the seer. However, they only focus on the little girl since she is capable of revealing both of the wolves if she decides to peek. We decided to not include a perceived seer role since that came with more added complexity to the game. To sum up, there are two base roles that each player uses to determine the roles of other players, wolf or not wolf and little girl and not little girl. Combining these two options results in four possible combinations which the players used to determine the perceived roles of each player, with one of those being impossible (wolf and little girl).

## Kripke Model Formalization
In our version of the game, each player keeps track of its own knowledge, having its own kripke model. The explanation that follows here are the kripke models such as each player keeps track of by itself. Before the model can be defined the agents and the predicates used in the model need to be defined first, the model consists of:
![kripke_model_formalization](https://user-images.githubusercontent.com/63637256/175820743-d28e81a9-7c2a-4bee-9b2a-fd1c14ffd51d.png)

### Possible worlds
There are as many possible worlds as there are possible permutations of the roles in the game.

## Game cycle
<!--
- Flowchart should be used here
- Different voting methods for different players should be explained here
-->
![Flowchart stages](https://user-images.githubusercontent.com/63637256/175819749-4d057d47-68aa-476f-8f77-e0a5d448948f.jpeg)
### Start
When the game starts, each player gets notified of their own identity. Next, stages start in which communication between the agents is possible, which always happens through thruthful public announcements to the kripke model of the agent receiving information. Each wolf gets sent a public announcement about the other wolves, entailing that each wolf now knows about all other wolves.

### Night
The seer identifies a person to view the role of, again being sent a public announcement. The wolf voting stage then starts, in which the little girl has the option to peek or not, which the wolves have a chance of detecting if she does. If the little girl decides to peek, she figures out the identity of both of the wolves. If the little girl is also caught by the wolves, the wolves figure out the identity of the little girl and the little girl knows that the wolves know that she is the little girl. If the little girl does not decide to peek then no information is shared between the little girl and the wolves. Regardless of what happens, afterwards the wolves vote on who they want to kill, with a public announcement on who they killed being sent to all other players. If the dead persons turns out to be a hunter, then the hunter has to shoot another player; the process can cycle if there are multiple hunters in the game. 

### Day and continuation
Next the day voting stage starts, which starts with each player sharing aquired and not yet shared information. The little girl and the seer can share one piece of identity information, which they tell to the other players through public announcements. Next each player gets to vote on who they want to kill. Once again, a hunter killing cycle can occur based on who was killed. The dead player(s) identity is revealed and all other players are made aware of it. Afterwards, the next night starts, which begins with the seer picking a person to identify again.

## Voting stages

### Wolves

### Seer

### Voting during the day

### Hunter


## Simple example game Kripke model analysis
Milan?

## Experiments & Results

## Results analysis

<!--
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
-->