# from mlsolver.model import MillerHollowModel
# import random
# from PlayerClasses.Roles import Role
# from PlayerClasses.PlayerWolf import PlayerWolf
# from PlayerClasses.PlayerVillager import PlayerVillager
# from PlayerClasses.PlayerSeer import PlayerSeer
# from PlayerClasses.PlayerLittlegirl import PlayerLittlegirl
# from PlayerClasses.PlayerHunter import PlayerHunter
# from mlsolver.kripke import KripkeStructure, World
# from mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star
#
# roles = {
#     Role.WOLF: 1,
#     Role.VILLAGER: 1,
#     Role.SEER: 0,
#     Role.LITTLE_GIRL: 2,
#     Role.HUNTER: 0
# }
#
#
# role_class_mapping = {
#         Role.WOLF: PlayerWolf,
#         Role.VILLAGER: PlayerVillager,
#         Role.SEER: PlayerSeer,
#         Role.LITTLE_GIRL: PlayerLittlegirl,
#         Role.HUNTER: PlayerHunter,
#     }
#
#
# def initialize_players(roles, role_class_mapping):
#     """
#     Creates instances of players using the distribution of roles. Also gives each player a random name.
#     """
#     # Load some random names for the players
#     with open('names.csv', 'r') as f:
#         names = f.read().split('\n')
#         random.shuffle(names)
#         names = names[:sum(roles.values())]
#
#     # Initialize the players with their role, name and the role distribution
#     player_id = 0
#     players = []
#     for role, amount in roles.items():
#         for _ in range(amount):
#             player_class = role_class_mapping[role]
#             players.append(player_class(names[player_id], role, roles, player_id))
#             player_id += 1
#
#     return players
#
# players = initialize_players(roles, role_class_mapping)
# km = MillerHollowModel(players)
#
# sentence = Box_a('2', Atom('IsWolf:0'))
# print(km.check_sentence(sentence))
#
# sentence = Box_a('0', Box_a('2', Atom('IsWolf:0')))
# print(km.check_sentence(sentence))
#
# # Tell girl that wolf is a wolf
# sentence = Box_a('2', Atom('IsWolf:0'))
# km.update_sentence('2', sentence)
#
# sentence = Box_a('2', Atom('IsWolf:0'))
# print(km.check_sentence(sentence))
#
# sentence = Box_a('1', Atom('IsWolf:0'))
# print(km.check_sentence(sentence))
#
#
# km.plot_model('0')

