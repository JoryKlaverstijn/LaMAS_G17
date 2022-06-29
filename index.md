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

The Werewolves of Millers Hollow is a social deduction game with multiple different player roles, in which the players attempt to figure out the roles of the other players. The role of each player is hidden from the other players and can only be revealed through a couple of game mechanics. The roles are divided up into wolves and villagers. The wolves attempt to kill off all the villagers to win the game, whereas the villagers attempt to kill all the wolves to win the game. Each day, a single game cycle takes place in which all phases of the game cycle are ran through. There are two voting moments in the game cycle: One moment at night at which only the wolves can vote who to kill, and a moment during the day at which everyone can vote who to kill.

This report has the following structure: First the simplified version of the Werewolves of Millers Hollow that we used in our simulations is explained. This includes an explanation of the simplifications we introduced as well as explanations of all the player roles that we used. Afterwards The Kripke model formalization of the game is explained thoroughly along with the amount of possible worlds. The game cycle is then explained, leading into a short explanation of the graphical user interface, the results and finally a discussion.

## Index

- [Roles](#roles)
    - [Werewolves](#werewolves)
    - [Seer](#seer)
    - [Little girl](#little-girl)
    - [Hunter](#hunter)
    - [Villager](#villager)
- [Simplifications](#simplifications)
    - [Role and player reduction](#role-and-player-reduction)
    - [Perceived role reduction](#perceived-role-reduction)
    - [Communication](#communication)
- [General Kripke model implementation](#general-kripke-model-implementation)
- [Kripke Model Formalization](#kripke-model-formalization)
    - [Possible worlds and relations](#possible-worlds-and-relations)
- [Game cycle](#game-cycle)
    - [Start](#start)
    - [Wolves identify each other](#wolves-identify-each-other)
    - [Seer identifies a chosen person](#seer-identifies-a-chosen-person)
    - [Little girl peeks](#little-girl-peeks)
    - [Little girl gets caught](#little-girl-gets-caught)
    - [Wolves vote for someone to die](#wolves-vote-for-someone-to-die)
    - [Dead persons identity is revealed](#dead-persons-identity-is-revealed)
    - [Dead person is a hunter](#dead-person-is-a-hunter)
    - [Players discuss](#players-discuss)
    - [Everyone gets to vote](#everyone-gets-to-vote)
- [Graphical User Interface](#graphical-user-interface)
- [Results and experimental setups](#results-and-experimental-setups)
    - [Different role distributions](#different-role-distributions)
    - [Differentiating information exchange](#differentiating-information-exchange)
    - [Results analysis](#results-analysis)
- [Discussion and conclusion](#discussion-and-conclusion)
- [References](#references)

## Roles

There are several different roles in the game. In the game there are multiple roles that are not used in our simplified version of the game, these include: The thief, cupid, the lovers the witch and the mayor mechanic. Note that all roles are referred to as villagers, except the werewolves.

### Werewolves

The werewolves attempt to kill off all the villagers. Each night, they wake up to vote on who they want to kill.

![Wolf Card](https://user-images.githubusercontent.com/63637256/175937346-ae7f6958-664e-4f1b-81be-b00c25e7bb6c.jpg "Wolf Card")

### Seer

The seer can view the role card of another player each night. The seer is a specialized villager.

![Seer Card](https://user-images.githubusercontent.com/63637256/175937378-e6d67781-fa29-4467-97c0-392f6424fd86.jpg "Seer Card")

### Little girl

The little girl is allowed to spy on the werewolves during the werewolf phase. However, she must be careful to avoid the werewolves detecting her. The little girl is a specialized villager.

![Little Girl Card](https://user-images.githubusercontent.com/63637256/175937430-35bb2a8a-45ae-409d-ad66-7cb1e215ed17.jpg "Little Girl Card")

### Hunter

When the hunter is killed, they are allowed to kill one other player of their choosing. The hunter is a specialized villager.

![Hunter Card](https://user-images.githubusercontent.com/63637256/175937455-f6081ee2-158a-4d6f-92bd-4baa699530cd.jpg "Hunter Card")

### Villager

The ordinary villager has no extra actions that it can take, the only impact it has on the game is voting and discussing.

![Villager Card](https://user-images.githubusercontent.com/63637256/175937478-b5b236fb-b033-489e-a66a-be2edddf59c9.jpg "Villager Card")

## Simplifications

Due to the complexity of the game, some simplifications were made to the original game.

### Role and player reduction

The primary simplification is related to the fact that there are too many roles in the original game to represent it in a Kripke model without the amount of possible worlds and relations exploding in numbers. Therefore, we decided to remove some of the roles and reduce the amount of players in the game. The maximum amount of players that can be used in the game is 8 instead of the possible 18, with there being 5 different roles instead of the original 8. We also decided to remove the mayor and lovers mechanic. The amount of roles and the roles that can be taken by the players is dynamic, with different combinations being possible.

### Perceived role reduction

Another related simplification that was introduced, was the roles that each player assigns to itself and the other players (its perceived state of reality). Normally this would include all the roles that are in the game, but since this makes the amount of possible worlds and relations in the Kripke models explode into the millions, we decided to approach it from a different angle. For the villagers, it is sufficient to know if a person is a wolf or not, since they only care about removing wolves from the game. For the wolves, it is important that they know who the villagers are, but also what type of villagers they are; they are more interested in removing some role types from the game earlier than other role types. These role types include the little girl and the seer. However, they only focus on the little girl, since she is capable of revealing all of the wolves if she decides to peek. We decided to not include a perceived seer and hunter role, since that came with more added complexity of the game. To sum up, there are two facts that each player uses to determine the roles of other players, "is wolf" and "is little girl". For a wolf, the former is true, but the latter is false. For a little girl the former is false, but the latter is true. For any other role, both facts are false. It is not possible for both facts to be true for a player. This means that there are 3 possible perceived roles for a player.

### Communication

A third simplification that we introduced is the inability of each player to manually deduce the roles of other players through the other players actions. Any player in the game is only able to receive information on the role of another player by explicitly receiving that information through a public announcement. In the game, players are also able to share information by public announcement with their fellow players, with those announcements always being truthful, e.g. the players can not lie. An announcement is always a player revealing the role of another player: players cannot reveal their own role, as this would make the game too simple for the villagers. A player can only reveal the role of another player when they know the role of the other player.

## General Kripke model implementation

To be able to model the knowledge of all the players, we have chosen to create a separate Kripke model for each player. Each Kripke model reflects the knowledge of a single player on the knowledge of all players, including their own knowledge. Each Kripke model has a set of possible worlds, where each world models a different possible permutation of the roles in the game. For example, one world  might model the situation in which player 1 and player 2 are wolves, and the rest are villagers, and another world might model the situation in which player 3 and player 5 are wolves and the rest are villagers. Then in each Kripke model, the relations between the worlds for each player are modeled. The relations of the player that the model belongs to reflect the knowledge of the player on the game state. The relations of other player in the Kripke model reflect what the player thinks that the other players know. This way we are able to use higher-order knowledge, and we are able to use public announcements to separately change the knowledge of players on other players' knowledge.

## Kripke Model Formalization

In our version of the game, each player keeps track of its own knowledge, having its own Kripke model. The explanation that follows here are the Kripke models, such as each player keeps track of by itself. The model described here is based on having the following roles: 2 wolves, 1 little girl, 1 seer, 1 hunter and 3 villagers; it shows how any combination of roles in a game can be defined by using this model as an example. Before the model can be defined, the players and the predicates used in the model need to be defined first:

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

The amount of possible worlds depends on the amount of players and the different roles that the players have. The total amount of worlds depends on the amount of permutations that are possible over the perceived roles in the game. If the total amount of worlds $$w$$ is known, the amount of players $$p$$ can be used to calculate the amount of relations for the Kripke models that each player has. At the start of the game, every world is connected to every other world, resulting in $$w^{2}$$ amount of relations for each player in the model. Since every player is modeled in one Kripke model, the amount of relations for all players in one Kripke model is $$w^{2} * p$$. There are as many models as there are players, resulting in a total of  $$w^{2} * p^{2}$$ relations over all Kripke models.

To exemplify the amount of possible worlds, we will take the example of having 2 wolves, 1 little girl, 1 seer, 1 hunter and 3 villagers in a game. At the start of the game, after having been told their own identity, every player has the same amount of possible worlds, with relations to each other possible world. In our example this means that there are 168 different worlds in every players' own Kripke model; a world for every possible permutation of having 5 perceived villager roles, one perceived little girl role and 2 wolf roles. The amount of relations in one Kripke model for one player is $$168^{2}$$ = 28224. The amount of relations in one Kripke model for all players is $$168^{2} * 8$$ = 225792. There are then 8 of these models in the game, resulting in a total of $$168^{2} * 8^{2}$$ = 1806336 total relations. View [Figure 1](#possible-worlds-1) to see one of the eight Kripke models present at the start of the game, the player the model belongs to is a wolf called Joann.

<figure>
    <img id="possible-worlds-1" src="https://user-images.githubusercontent.com/63637256/175941808-aaf77ca9-a8a9-47f3-832a-c093a3cd6a2e.png" />
    <figcaption>Figure 1: Possible Worlds - Case 1</figcaption>
</figure>

In [this figure](#possible-worlds-1), all the possible worlds are shown, with the relations of Joann. It can be seen that in the real world, player 1 and 2 are wolves, and player 7 is the little girl. The amount of relations drastically reduces over the course of the game, eventually resulting in a lot fewer options for the players. For example, after Joann has been informed of the role of the other wolf immediately after being informed of her own role, the amount of possible worlds turns into only a few. View [Figure 2](#possible-worlds-2)  for an example.

<figure>
    <img id="possible-worlds-2" src="https://user-images.githubusercontent.com/63637256/175941881-1ee89090-1e5e-4bc9-8c8f-e407a05f54ea.png" />
    <figcaption>Figure 2: Possible Worlds - Case 2</figcaption>
</figure>

## Game cycle

<figure>
    <img id="flowchart-stages" src="https://user-images.githubusercontent.com/63637256/175819749-4d057d47-68aa-476f-8f77-e0a5d448948f.jpeg" />
    <figcaption>Figure 3: Flowchart of Game Stages</figcaption>
</figure>

### Start

When the game starts, none of the players have any knowledge about their own role, or other players' roles. Each player gets notified of their own identity using a public announcement. After this notification, the amount of relations of the player in their Kripke model decreases, and the amount of accessible worlds from the real world is limited to the worlds in which their own role is equal to their announced role.

### Wolves identify each other

After the players know their own role, the wolves are allowed to know who the other wolves are. This is done by a public announcement in the Kripke model of all wolves. An announcement is made to tell the player that they now know the role of the other wolves, and an announcement is made to tell the player that the other wolves also know their role.

### Seer identifies a chosen person

At this stage of the game, the seer is allowed to choose a person to identify. To choose who to identify, the seer uses their own Kripke model to choose a person that they want to know valuable identity information of. The seer iterates through all other players, and checks for each player if the seer knows they are a wolf and if the seer knows they are not a wolf. If neither is true, that means the seer still suspects the player to be a wolf, and wants to reveal this player's identity. If the seer does not suspect anyone, then it could still be useful to find out if there is another player of which the seer does not know the role. That way the seer gets to know who has a specialized good role, to be able to communicate it to other players later.

### Little girl peeks

The little girl can decide to peek or not to peek before the wolves vote. By default, she has a 50% chance to peek at night to discover the identity of the wolves. If it turns out the girl has decided to peek, then a public announcement is made in her Kripke model, telling her that she knows who the wolves are.

### Little girl gets caught

If the little girl has decided to peek, then afterwards there is a 50% chance that she will get caught. If she does get caught, that means the wolves will now know that she knows that they are the wolf. The wolves will also now know that she is the little girl. This means that in the upcoming voting round for the wolves, the little girl will surely get killed by the wolves.

### Wolves vote for someone to die

After the little girl has or has not peeked, the wolves get to vote to kill one person. The voting strategy of the wolf is based on their knowledge modeled in their Kripke model. First they iterate through every other player, and check in their Kripke model if they know that the other player knows they are a wolf, and that they know that the other player is not a wolf. They base this most important option on the higher order knowledge present in their Kripke model. If this is the case, they have been caught by a non-wolf player and that player must be voted out immediately. If this is not the case, they instead vote out anyone that they know is a little girl, which may be known through deduction of knowing other players' roles. Finally, if no information about the little girl is known either, the wolves will kill anyone that they know is not a wolf.

### Dead persons identity is revealed

When a person has died, everyone gets to know the identity of this person. An announcement in every players' Kripke model is made informing everyone of the role of the killed person. In doing so, the amount of relations in each Kripke model rapidly decreases as the game goes on. 

### Dead person is a hunter

In the case that a hunter has died, the hunter is allowed to kill another player. The choice of who the hunter wants to kill is explained in the [everyone gets to vote](#everyone-gets-to-vote) section.

### Players discuss

Now that players have died, the little girl has maybe seen who the wolves are and the seer has identified a role, the players are allowed to discuss. The discussion works in turns and every non-wolf player is able to use their own Kripke model to decide if they have any useful information to reveal. The first thing that a player checks in their Kripke model is if they know for some player if they are the wolf and if they know that any of the other players does not know this information. If this is the case, they reveal the identity of the wolf. Second, a player checks if they know who is a little girl, and if anyone does not know this information. Finally, they check if they know who is good, and if anyone does not know this information. If none of these apply, the player stays quiet. The reason to reveal the role of a good player is so that other players know that they should not vote this player out.

### Everyone gets to vote

After the discussion, all the players are allowed to vote someone out. The voting behavior of the wolves is the same as in the [wolves vote for someone to die](#wolves-vote-for-someone-to-die) section. The non-wolf players check in their Kripke model if they know if someone is a wolf, in which case they vote for that person. Second, each non-wolf player votes for anyone who they still do not know to not be a wolf, who are still suspected of being a wolf. There should always be someone who they know is the wolf, or who they suspect to be a wolf. After all the players have voted a single player out, the dead person's identity is again revealed, and the cycle is started over again, with a seer identifying someone's role. Note that the voting behavior of the non-wolf players is also used for the hunter to determine who to bring down when they are killed.

## Graphical User Interface

The graphical user interface (GUI) consists of the players, each with their roles revealed, a reset button, a next step button, a console to view the game progression and buttons numbering from 1 to the amount of players. View [Figure 4](#gui) for an overview.

<figure>
    <img id="gui" src="https://user-images.githubusercontent.com/63637256/175936223-09cc176f-87d9-4b66-8eaf-3a8cc9137b7d.png" />
    <figcaption>Figure 4: Graphical User Interface of Game</figcaption>
</figure>

In the overview, a day voting process is visible for a game with 2 wolves, 1 little girl, 1 seer, 1 hunter and 3 villagers. Lyla, Rogelio and Kendra are shown to have one vote each. The purple lining is added to players that already voted. The little girl player Porsha is already dead; the console shows that she was killed after she peeked during the night voting phase, after which the wolves detected and killed her. The reset button will create a new game with new players, while the next step button will take the game into the next stage. The buttons numbered 1 to 8 can be used to view the Kripke models of each player, refer back to the [possible worlds and relations section](#possible-worlds-and-relations) for an explanation of the Kripke models.

## Results and experimental setups
To test the knowledge types in our version of the game, we tested a few different scenarios to see how it would affect win percentages for the villagers and the wolves. We also recorded the day voting metrics of every game, with a correct vote being counted as a vote on a wolf by a villager.

### Different role distributions
To test if the types of roles have an effect on the win percentages and the amount of correct votes, a couple of different game setups with different role distributions were simulated. The role distributions are defined as follows:
- Default: 2 wolves, 1 little girl, 1 seer, 1 hunter and 3 villagers.
- More Seers: 2 wolves, 1 little girl, 2 seer, 1 hunter and 2 villagers.
- More Hunters: 2 wolves, 1 little girl, 1 seer, 2 hunter and 2 villagers.
- More Wolves: 3 wolves, 1 little girl, 3 seer, 1 hunter and 0 villagers.

A 1000 games were ran for each role distribtion setup, resulting in the following [(Figure 5)](#total_bar_graph_1000_iterations) win percentages. The amount of total, correct and % correct votes are also visible in the table below.

<figure>
    <img id="total_bar_graph_1000_iterations" src="https://user-images.githubusercontent.com/63637256/176162322-5710a1aa-f917-4486-b98c-e42e9e207f34.png" class = "center"/>
    <figcaption>Figure 5: Different role distributions results over 1000 game iterations</figcaption>
</figure>

<center>
    <table>
        <tr>
            <th>Distribution</th>
            <th>Total votes</th>
            <th>Correct votes</th>
            <th>% Correct</th>
        </tr>
        <tr>
            <td>Default</td>
            <td>8658</td>
            <td>5672</td>
            <td>65.51</td>
        </tr>
        <tr>
            <td>More Seers</td>
            <td>8593</td>
            <td>6556</td>
            <td>76.29</td>
        </tr>
        <tr>
            <td>More Hunters</td>
            <td>7656</td>
            <td>4841</td>
            <td>63.23</td>
        </tr>
        <tr>
            <td>More Wolves</td>
            <td>7456</td>
            <td>7062</td>
            <td>94.72</td>
        </tr>
    </table>
</center>

### Differentiating information exchange
We were also interested in finding out what effect of communication was on the win percentage. With our default setup, the agents reveal the identity of any wolves they know, and if they do not know any wolves, they reveal the identity of any good player they know. For this experiment we also tried only revealing the identity of wolves, only revealing the identity of good players, or not revealing any information. 1000 Games were simulated for each configuration, and the results are shown in [Figure 6](#Communication_results) with the table below containing the voting information.

<figure>
    <img id="Communication_results" src="https://user-images.githubusercontent.com/63673224/176284536-2f3c0f40-eabc-4f06-a21d-6536bfd5f4d0.png" class = "center"/>
    <figcaption>Figure 6: Villager wins over different little girl detection tresholds.</figcaption>
</figure>

<center>
    <table>
        <tr>
            <th>Configuration</th>
            <th>Total votes</th>
            <th>Correct votes</th>
            <th>% Correct</th>
        </tr>
        <tr>
            <td>Reveal wolf</td>
            <td>5772</td>
            <td>8610</td>
            <td>67.04</td>
        </tr>
        <tr>
            <td>Reveal good</td>
            <td>5545</td>
            <td>8601</td>
            <td>64.47</td>
        </tr>
        <tr>
            <td>Reveal neither</td>
            <td>4359</td>
            <td>8560</td>
            <td>50.92</td>
        </tr>
        <tr>
            <td>Reveal both</td>
            <td>4082</td>
            <td>8545</td>
            <td>47.77</td>
        </tr>
    </table>
</center>

### Results analysis

From the experiment with different role distributions, we can conclude that more seers drastically increases the win chance of the villagers, whereas adding more hunters does not seem to change the win rate by much. Adding more wolves while also adding more seers balances out the game more, giving similar results to the default setup. However, doing so does lead to a simpler game for the villagers, as they have a higher chance of voting correctly. Therefore, we can conclude that seers, and their role of revealing the roles of wolf and non-wolf players, is very important for the villagers to win.

From the experiment with all, partial, or no communication it can be concluded that revealing the identity of wolves has a large impact on the win rate of the villagers compared to not revealing any information. It is interesting to see that only revealing who is good also improves the win rate compared to not revealing any information. This means that revealing good roles helps the players in deducing who the wolves are, and is more helpful to the good players trying to deduce who the wolves are, than it is helpful for the wolves finding out who the little girl is. Overall, the communication of roles plays a big part in the success of the villagers.

## Discussion and conclusion

In this project, we have discovered how to implement the knowledge of a player using a Kripke model. We have found out how to update the knowledge of the players such that they have separate views of the game state. We have also learned how to use the knowledge stored in the Kripke models to let the players make decisions. The project has presented us with some difficulties when trying to implement higher-order knowledge, which was solved by implementing multiple Kripke models. If we were to continue on this project, we would be interested in trying to implement the knowledge in a different way, such as storing all the knowledge in a single Kripke model. We would also look into how we could model the knowledge of more players without having the amount of player relations explode into the millions. The model we implemented only uses first- and second-order knowledge, but it would be interesting to use even higher order knowledge for decision-making. In conclusion, this project was successful in modeling the game of "Wolves of Miller Hollow", but there are still some improvements to be made, such as using a single Kripke model instead of one for each agent.

<!-- why does this not work -->

## References
- The Banner image was taken from: <a href="https://coolwallpapers.me/xfsearch/alt/werewolf/">here</a>
- BOK unit 1 and BOK unit 2 from the course materials.
- Van Ditmarsch, H., van Der Hoek, W., & Kooi, B. (2007). Dynamic epistemic logic (Vol. 337). Springer Science & Business Media.

<a href="#index" class="float">To Index</a>
