<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      inlineMath: [ ['$','$'], ["\\(","\\)"] ],
      processEscapes: true
    }
  });
</script>
<script
  type="text/javascript"
  charset="utf-8"
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"
>
</script>

# The Werewolves of Millers Hollow
<!--![example_game_image](https://user-images.githubusercontent.com/63673224/175807188-43e3595d-a05a-43f4-8b30-dd6a8869e262.png)-->

The Werewolves of Millers Hollow is a social deduction game with multiple different player roles, in which the players attempt to figure out the roles of the other players. The role of each player is hidden from the other players and can only be revealed through a couple of game mechanics. The roles are divided up into wolves and villagers. The wolves attempt to kill off all the villagers to win the game, while the villagers attempt to kill all of the wolves to win the game. Each day a single game cycle takes place in which all phases of the game cycle are ran through. There are two voting moments in the game cycle: only the werewolves can vote on who they want to kill at night and all of the players can vote on who they want to kill during the day.

This report has the following structure: First the simplified version of the Werewolves of Millers Hollow that we used in our simulations is explained. After that we form a kripke model formalization of the game, we then explain about the game cycle and different types of voting, leading into an experimental setup, results and an analysis.

## Roles
There are several different roles in the game. In the game there are multiple roles that are not used in our simplified version of the game, these include: The thief, cupid, the lovers the witch and the mayor mechanic. Note that all roles are villagers, except the werewolves.

### Werewolves
The werewolves attempt to kill off all the villagers. Each night they wake up to share information and to vote on who they want to kill.

![wolf_card](https://user-images.githubusercontent.com/63637256/175937346-ae7f6958-664e-4f1b-81be-b00c25e7bb6c.jpg)

### Seer
The seer can view the role card of another player each night.

![seer_card](https://user-images.githubusercontent.com/63637256/175937378-e6d67781-fa29-4467-97c0-392f6424fd86.jpg)

### Little girl
The little girl is allowed to spy on the werewolves during the werewolf phase. However she must be careful to avoid the werewolves detecting her.

![littlegirl_card](https://user-images.githubusercontent.com/63637256/175937430-35bb2a8a-45ae-409d-ad66-7cb1e215ed17.jpg)

### Hunter
When the hunter is killed, he is allowed to kill one other player of their choosing.

![hunter_card](https://user-images.githubusercontent.com/63637256/175937455-f6081ee2-158a-4d6f-92bd-4baa699530cd.jpg)

### Villager
The ordinary villager has no extra actions that it can take, the only decisions it can make are related to voting during the day time.

![villager_card](https://user-images.githubusercontent.com/63637256/175937478-b5b236fb-b033-489e-a66a-be2edddf59c9.jpg)


## Simplifications
Due to the complexity of the game some simplifications were made to the original game.

### Role and player reduction
The primary simplification is related to the fact that there are too many roles in the original game to represent it in a kripke model without the amount of possible worlds and relations exploding in complexity. Therefore we decided to remove some of the roles and reduce the amount of players in the game. The maximum amount of players that can be used in the game is 8, with there being 5 different roles instead of the original 8. We also decided to remove the mayor and lovers mechanic. The amount of roles and the roles that can be taken by the players is dynamic, with different combinations being possible.

### Perceived role reduction
Another related simplification that was introduced was the roles that each player assigns to itself and the other players (its perceived state of reality). Normally this would include all the roles that are in the game, but since this makes the amount of possible worlds in the kripke models explode into the millions, we decided to approach it from a different angle. For the villagers it is sufficient to know if a person is a wolf or not, since they only care about removing wolves from the game. For the wolves it is important that they know who the villagers are, but also what type of villagers they are; they are more interested in removing some role types from the game earlier than other role types. These role types include the little girl and the seer. However, they only focus on the little girl since she is capable of revealing both of the wolves if she decides to peek. We decided to not include a perceived seer role since that came with more added complexity to the game. To sum up, there are two base roles that each player uses to determine the roles of other players, wolf or not wolf and little girl and not little girl. Combining these two options results in four possible combinations which the players used to determine the perceived roles of each player, with one of those being impossible (wolf and little girl).

### Communication
A third simplification that we introduced is the inability of each player to manually deduce the roles of another player through their actions. Any player in the game is only able to receive information on the role of another player by explicitly receiving that information through a public announcement. In the game players are able to share information by public announcement with their fellow players, with those announcements always being truthful, e.g. the players can not lie. If this were to happen in a real world game, players would be able to deduce the roles of other players by them sharing information that is known to be truthful. For example if a player would share that they know who another player is, then that player would either be the seer or the little girl. But this type of role deduction is not present in our version of the game.

## Kripke Model Formalization
In our version of the game, each player keeps track of its own knowledge, having its own kripke model. The explanation that follows here are the kripke models such as each player keeps track of by itself. The model described here is based on having the following roles: 2 wolves, 1 little girl, 1 seer, 1 hunter and 3 villagers; it shows how any combination of roles can be defined using this model. Before the model can be defined the agents and the predicates used in the model need to be defined first:

- A set of $$m$$ players,

  $$A = \{a_{1}, a_{2}, ... , a_{m}\}$$

- A set of predicates, for each player,

  $$P = \{\{wolf_{1}, wolf_{2}, ... , wolf_{m}\}, \{girl_{1}, girl_{2}, ... , girl_{m}\} \}$$

The formal definition of the Kripke model M: $\langle S, \pi, R_{1}, ... , R_{m}\rangle$ is then as follows:

- States $$S$$:

  $$S = \{s_{wolf:i-j, girl:k} | a_{i} \in A \land a_{j} \in A \land a_{k} \in A \land i < j \land k \neq i \land k \neq j\}$$

- Evaluations $\pi$:

  $$
  \begin{align*}
  \pi (s_{wolf:i-j, girl:k})(\text{wolf}_{l}) &= t \text{ iff } l = i \lor l = j\\
  \pi (s_{wolf:i-j, girl:k})(\text{girl}_{l}) &= t \text{ iff } l = k\\
  \pi (s_{wolf:i-j, girl:k})(\text{villagers}_{l}) &= t \text{ iff } l \neq k \land l \neq i \land l \neq j
  \end{align*}
  $$

- Relations $$R$$:

    Each possible world is connected to each possible world that can still be the true world, including reflexive relations.

    $$R = \{(s_{i}, s_{j}) | s_{i} \in S \land s_{j} \in S \}$$


### Possible worlds and relations
The amount of possible worlds depends on the amount of players and the different roles that the players have. The total amount of worlds depends on the amount of permutations that are possible over the perceived roles in the game. If the total amount of worlds $$w$$ is known, the amount of players $$p$$ can be used to calculate the amount of relations for the kripke models that each player has. At the start of the game very world is connected to every other world, resulting in $$w^{2}$$ amount of relations for each player in the model. Since every player is modelled in one kripke model, the amount of relations for all players in one kripke model is $$w^{2} * p$$. There are as many models as there are players, resulting in a total of  $$w^{2} * p^{2}$$ relations over all kripke models.

To exemplify the amount of possible worlds, we will again take the example of having 2 wolves, 1 little girl, 1 seer, 1 hunter and 3 villagers. At the start of the game, after having been told their own identity, every player has the same amount of possible worlds, with relations to each other possible world. In our example this means that there are 168 different worlds in every players own kripke model; a world for every possible permutation of having 5 perceived villager roles, one perceived little girl role and 2 wolf roles. The amount of relations in one kripke model for one player is $$168^{2}$$ = 28224. The amount of relations in one kripke model for all players is $$168^{2} * 8$$ = 225792. There are then 8 of these models in the game, resulting in a total of $$168^{2} * 8^{2}$$ = 1806336 total relations. View the figure down below to see one of the eight kripke models present at the start of the game, the player the model belongs to is a wolf called Joann.

<p align="center">
  <img src="https://user-images.githubusercontent.com/63637256/175941808-aaf77ca9-a8a9-47f3-832a-c093a3cd6a2e.png" />
</p>

The amount of relations drastically reduces over the course of the game eventually resulting in a lot fewer options for the players. For example after Joann has been informed of the role of the other wolf immediately after being informed of her own role, the amount of possible worlds turns into only a few. View the figure down below for an example.

<p align="center">
  <img src="https://user-images.githubusercontent.com/63637256/175941881-1ee89090-1e5e-4bc9-8c8f-e407a05f54ea.png" />
</p>

## Game cycle
![Flowchart stages](https://user-images.githubusercontent.com/63637256/175819749-4d057d47-68aa-476f-8f77-e0a5d448948f.jpeg)
### Start
When the game starts, each player gets notified of their own identity. Next, stages start in which communication between the agents is possible, which always happens through thruthful public announcements to the kripke model of the agent receiving information. Each wolf gets sent a public announcement about the other wolves, entailing that each wolf now knows about all other wolves.

### Night
The seer identifies a person to view the role of, again being sent a public announcement. The wolf voting stage then starts, in which the little girl has the option to peek or not, which the wolves have a chance of detecting if she does. If the little girl decides to peek, she figures out the identity of both of the wolves. If the little girl is also caught by the wolves, the wolves figure out the identity of the little girl and the little girl knows that the wolves know that she is the little girl. If the little girl does not decide to peek then no information is shared between the little girl and the wolves. Regardless of what happens, afterwards the wolves vote on who they want to kill, with a public announcement on who they killed being sent to all other players. If the dead persons turns out to be a hunter, then the hunter has to shoot another player; the process can cycle if there are multiple hunters in the game.

### Day and continuation
Next the day voting stage starts, which starts with each player sharing aquired and not yet shared information. The little girl and the seer can share one piece of identity information, which they tell to the other players through public announcements. Next each player gets to vote on who they want to kill. Once again, a hunter killing cycle can occur based on who was killed. The dead player(s) identity is revealed and all other players are made aware of it. Afterwards, the next night starts, which begins with the seer picking a person to identify again.

## Selection (voting) stages
At any type of selection stage, the best player to select is based on the role of the person who is doing the selection. The seer and the hunter perform a selection action, there is day and night voting and the little girl decides to peek or not. During day and night voting there is no communication between the different players in the game to coordinate their voting; they only use the information that they have themselves. If ties occur between the most amount of votes during day and night voting a selection between the tied options is made at random.

### Night voting
The wolves get to vote at night on who they want to kill. They have three options for voting based on priority. The first option is by using higher order knowledge to select a player that knows about them being the wolves, if the wolves know about this they will want to kill them first. If that type of knowledge is not present in the model of a wolf, then the second option is elected, which is voting out the little girl player if the wolves know the role of a little girl in the game. If that option is also not present, then the wolves will elect to kill anyone who is a villager; since the wolves know about each other, they will randomly elect one of the other players to kill.

### Seer
The seer gets to reveal the role of another player. Like the wolves, the seer also has three selection options based on priority. The first option is for the seer to select a player that he does not know not to be a wolf and hence is suspected of possibly being a wolf. If such an option exists, that option will be used first. If such an option does not exist, which can happen when identities of both wolves or all villagers are known, then the seer will reveal the role of a random player that it does not know the identity of yet. If that option is also not available, then the wolf will use the third option; selecting the role of someone that was already knwon to him.

### Day voting
During the day all the players in the game can vote on someone that they want to kill. For the wolves the voting occurs the same as in the night voting phase (they make the same choices), but this time they have to comply with the votes of others as well. For the villagers there are two options for voting. The first option is when a villager knows about the identity of a wolf, they will then vote to kill the wolf. If that information is not available, the villager will use the second option; voting for a player that they do not know not to be the wolf, being suspected of being a wolf. Note that the seer, little girl and hunter all classify as villagers in the day voting stage.

### Hunter
The hunter can select to kill someone if he has been killed. This selection is the same as the vote he would make during day voting.

### Little Girl
The little girl can decide to peek or not to discover the identity of the wolves in the game. By default she has a 50% chance to peek at night to discover the wolves. There is then also a default 50% chance that the wolves will detect her peeking. If the wolves detect her she will get killed on the same night. If the little girl has peeked during the game, then she will not peek again since she already knows the identity of the wolves.

## Graphical User Interface
The graphical user interface (GUI) consists of the players, each with their roles revealed, a reset button a next step button, a console to view the game progression and buttons numbering from 1 to the amount of players. View the figure below for an overview. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/63637256/175936223-09cc176f-87d9-4b66-8eaf-3a8cc9137b7d.png" />
</p>

In the overview, the voting process is visible for a game with 2 wolves, 1 little girl, 1 seer, 1 hunter and 3 villagers. Lyla, Rogelio and Kendra are shown to have one vote each. The purple lining is added to players that already voted. The little girl player Porsha is already dead; the console shows that she was killed after she peeked during the night voting phase, after which the wolves detected and killed her. The reset button will create a new game with new players, while the next step button will take the game into the next stage. The buttons numbered 1 to 8 can be used to view the kripke models of each player, refer back to the **Possible worlds and relations** section for an explanation of the kripke models.

<!--
## Simple example game Kripke model analysis
Milan?
-->

<!--
## Experiments & Results
-->

<!--
## Results analysis
-->

