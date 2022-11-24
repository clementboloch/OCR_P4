'''
1. Au début du premier tour, triez tous les joueurs en fonction de leur classement.
2. Divisez les joueurs en deux moitiés, une supérieure et une inférieure. Le meilleur joueur de la moitié supérieure est jumelé avec le meilleur joueur de la moitié inférieure, et ainsi de suite. Si nous avons huit joueurs triés par rang, alors le joueur 1 est jumelé avec le joueur 5, le joueur 2 est jumelé avec le joueur 6, etc.
3. Au prochain tour, triez tous les joueurs en fonction de leur nombre total de points. Si plusieurs joueurs ont le même nombre de points, triez-les en fonction de leur rang.
4. Associez le joueur 1 avec le joueur 2, le joueur 3 avec le joueur 4, et ainsi de suite. Si le joueur 1 a déjà joué contre le joueur 2, associez-le plutôt au joueur 3.
5. Répétez les étapes 3 et 4 jusqu'à ce que le tournoi soit terminé.
'''

from operator import attrgetter
import random

from Joueur import Joueur, no_date


def visible(l: list[Joueur]):
    return [player.player_ranking for player in l]

def sort_score(l: list[Joueur]):
    return sorted(l, key=attrgetter('_player_score'), reverse=True)

def sort_rank(l: list[Joueur]):
    return sorted(l, key=attrgetter('player_ranking'))

def sort(l: list[Joueur]):
    return sort_score(sort_rank(l))

def suisse_first(players: list[Joueur]):
    for player in players:
        player._player_score = 0
    nb_players = len(players)
    sorted_list = sort(players)
    first_pairs = [sort_rank([sorted_list[i], sorted_list[int(nb_players/2) + i]]) for i in range(int(nb_players / 2))]
    played_pairs = first_pairs.copy()
    return first_pairs, played_pairs

# TODO: bug, fait plus de 8 match par round !!
def suisse_then(players: list[Joueur], played_pairs: list):
    nb_players = len(players)
    sorted_list = sort(players)
    pairs = []
    attributed_players = []
    for i in range(nb_players):
        if sorted_list[i] in attributed_players:
            continue
        competitor_found = False
        j = i + 1
        while not competitor_found:
            potential_pair = sort_rank([sorted_list[i], sorted_list[j]])
            if potential_pair not in played_pairs and sorted_list[j] not in attributed_players:
                pairs.append(potential_pair)
                attributed_players.extend(potential_pair)
                competitor_found = True
            j += 1
    played_pairs.extend(pairs)
    return pairs, played_pairs


# if __name__ == "__main__":
#     def result(round):
#         for pair in round:
#             score = random.randint(0, 2) / 2
#             print(score)
#             pair[0]._player_score += score
#             pair[1]._player_score += 1 - score

#     joueur1 = Joueur('1', 'A', no_date, 'M', 1)
#     joueur2 = Joueur('2', 'Z', no_date, 'M', 2)
#     joueur3 = Joueur('3', 'E', no_date, 'M', 3)
#     joueur4 = Joueur('4', 'R', no_date, 'M', 4)
#     joueur5 = Joueur('5', 'T', no_date, 'M', 5)
#     joueur6 = Joueur('6', 'Y', no_date, 'M', 6)
#     joueur7 = Joueur('7', 'U', no_date, 'M', 7)
#     joueur8 = Joueur('8', 'I', no_date, 'M', 8)

#     joueurs = [joueur1, joueur2, joueur3, joueur4, joueur5, joueur6, joueur7, joueur8]

#     round, played_pairs = suisse_first(joueurs)
#     print(round)
#     for i in range(6):
#         result(round)
#         round, played_pairs = suisse_then(joueurs, played_pairs)
#         print(round)