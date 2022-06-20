from mlsolver.kripke import KripkeStructure, World
from mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star
from PlayerClasses.Roles import Role
from itertools import permutations
import numpy as np
import matplotlib.pyplot as plt


class MillerHollowModel:
    """
    The kripke model definition of the Wolves of Miller Hollow game
    Large parts of this class are modified versions/inspired by:
    https://github.com/MaxVinValk/AmongUsLAMAS/blob/main/mlsolver/model.py#L99
    """
    def __init__(self, players):
        self.setup(players)

    def setup(self, players):
        self.n_players = len(players)
        self.worlds = []
        # We make the worlds with each permutation of wolves little_girls and other
        simplified_roles = []
        for player in players:
            if player.role == Role.WOLF:
                simplified_roles.append(Role.WOLF)
            elif player.role == Role.LITTLE_GIRL:
                simplified_roles.append(Role.LITTLE_GIRL)
            else:
                simplified_roles.append(Role.VILLAGER)

        # Only unique permutations
        perms = set(permutations(simplified_roles))

        # Go through every possible unique permutation
        self.worlds_roles = []
        for perm in perms:
            wolf_indices = [idx for idx, role in enumerate(perm) if role == Role.WOLF]
            girl_indices = [idx for idx, role in enumerate(perm) if role == Role.LITTLE_GIRL]
            other_indices = list(set(range(len(perm))) - set(wolf_indices) - set(girl_indices))
            w_roles = {}
            w_roles[Role.WOLF] = wolf_indices
            w_roles[Role.LITTLE_GIRL] = girl_indices
            self.worlds_roles.append(w_roles)

            world_truths = {}
            for idx in wolf_indices:
                world_truths[f'IsWolf:{idx}'] = True
                world_truths[f'IsGirl:{idx}'] = False

            for idx in girl_indices:
                world_truths[f'IsWolf:{idx}'] = False
                world_truths[f'IsGirl:{idx}'] = True

            for idx in other_indices:
                world_truths[f'IsWolf:{idx}'] = False
                world_truths[f'IsGirl:{idx}'] = False

            world_name = 'Wolf' + '_'.join(map(str, wolf_indices)) + ',Girl' + '_'.join(map(str, girl_indices))
            self.worlds.append(World(world_name, world_truths))

        # Create the relationships for each agent
        self.relations = {}
        for agent_idx, player in enumerate(players):
            agent_rels = set()
            for w_roles1, world1 in zip(self.worlds_roles, self.worlds):
                for w_roles2, world2 in zip(self.worlds_roles, self.worlds):
                    # The wolves start by only knowing their own role
                    if player.role == Role.WOLF:
                        if agent_idx in w_roles1[Role.WOLF] and agent_idx in w_roles2[Role.WOLF]:
                            agent_rels.add((world1.name, world2.name))
                    # Little girls only know their own role (other worlds are not acessible)
                    elif player.role == Role.LITTLE_GIRL:
                        if agent_idx in w_roles1[Role.LITTLE_GIRL] and agent_idx in w_roles2[Role.LITTLE_GIRL]:
                            agent_rels.add((world1.name, world2.name))
                    else:
                    # Villagers and other "good" roles also only know they are good
                        if agent_idx not in w_roles1[Role.LITTLE_GIRL] + w_roles1[Role.WOLF] \
                                + w_roles2[Role.LITTLE_GIRL] + w_roles2[Role.WOLF]:
                            agent_rels.add((world1.name, world2.name))
            self.relations[str(agent_idx)] = agent_rels

        self.relations.update(self.add_symmetric_edges(self.relations))
        self.relations.update(self.add_reflexive_edges(self.worlds, self.relations))
        self.kripke_structure = KripkeStructure(self.worlds, self.relations)

        wolf_indices = [idx for idx, role in enumerate(simplified_roles) if role == Role.WOLF]
        girl_indices = [idx for idx, role in enumerate(simplified_roles) if role == Role.LITTLE_GIRL]
        self.real_world = 'Wolf' + '_'.join(map(str, wolf_indices)) + ',Girl' + '_'.join(map(str, girl_indices))

    def kripke_structure_solve_a(self, agent, formula):
        """
        This function is a small change to mlsolver taken from the code of The Ship at
        https://github.com/JohnRoyale/MAS2018/blob/master/mlsolver/kripke.py#L36
        """

        nodes_to_remove = self.kripke_structure.nodes_not_follow_formula(formula)
        if len(nodes_to_remove) == 0:
            return self.kripke_structure

        relations_to_remove = []

        for relation in self.kripke_structure.relations[str(agent)]:
            for node in nodes_to_remove:
                if node in relation:
                    relations_to_remove.append(relation)
                    break

        self.kripke_structure.relations[str(agent)] = self.kripke_structure.relations[str(agent)] \
                                                      - set(relations_to_remove)

    @staticmethod
    def add_reflexive_edges(worlds, relations):
        """Routine adds reflexive edges to Kripke frame
        """
        result = {}
        for agent, agents_relations in relations.items():
            result_agents = agents_relations.copy()
            for world in worlds:
                result_agents.add((world.name, world.name))
                result[agent] = result_agents
        return result

    @staticmethod
    def add_symmetric_edges(relations):
        """Routine adds symmetric edges to Kripke frame
        """
        result = {}
        for agent, agents_relations in relations.items():
            result_agents = agents_relations.copy()
            for r in agents_relations:
                x, y = r[1], r[0]
                result_agents.add((x, y))
            result[agent] = result_agents
        return result

    def plot_model(self, player=None):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(10, 10)
        r = 20
        world_angles = np.linspace(0, np.pi * 2, len(self.worlds) + 1)[:-1]
        world_positions = [(r * np.cos(theta), r * np.sin(theta)) for theta in world_angles]
        world_idx = {world.name: idx for idx, world in enumerate(self.worlds)}

        # Plot the relations
        for agent, relations in self.kripke_structure.relations.items():
            if player is not None and agent != player:
                continue
            for start, end in relations:
                if start == end:
                    continue

                x1, y1 = world_positions[world_idx[start]]
                x2, y2 = world_positions[world_idx[end]]
                plt.plot((x1, x2), (y1, y2), color='black')

        # Plot the worlds
        plt.scatter(*zip(*world_positions))
        plt.scatter(*world_positions[world_idx[self.real_world]], color='lime', s=100, zorder=10)

        plt.show()

    def suspects(self, observer, observee):
        # Observer does not know that the observee is not a wolf
        sentence = Not(Box_a(str(observer), Not(Atom(f'IsWolf:{observee}'))))
        return sentence.semantic(self.kripke_structure, self.real_world)

    def knows_wolf(self, observer, observee):
        # Observer knows the observee is a wolf
        sentence = Box_a(str(observer), Atom(f'IsWolf:{observee}'))
        return sentence.semantic(self.kripke_structure, self.real_world)

    def knows_little_girl(self, observer, observee):
        # Observer knows the observee is a seer
        sentence = Box_a(str(observer), Atom(f'IsGirl:{observee}'))
        return sentence.semantic(self.kripke_structure, self.real_world)

    def knows_good(self, observer, observee):
        # Observer knows the observee is not a wolf
        sentence = Box_a(str(observer), Not(Atom(f'IsWolf:{observee}')))
        return sentence.semantic(self.kripke_structure, self.real_world)

    def update_knows_wolf(self, observer, observee):
        # Updates the knowledge of the observer that observee is a wolf
        sentence = Atom(f'IsWolf:{observee}')
        self.kripke_structure_solve_a(str(observer), sentence)

    def update_knows_little_girl(self, observer, observee):
        sentence = Atom(f'IsGirl:{observee}')
        self.kripke_structure_solve_a(str(observer), sentence)

    def update_knows_good(self, observer, observee):
        # Updates the knowledge of the observer that observee is a wolf
        sentence = Not(Atom(f'IsWolf:{observee}'))
        self.kripke_structure_solve_a(str(observer), sentence)
