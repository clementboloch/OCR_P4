from operator import attrgetter

from Model.Joueur import Joueur


def visible(players: list[Joueur]):
    return [player.player_ranking for player in players]


def sort_score(players: list[Joueur]):
    return sorted(players, key=attrgetter('_player_score'), reverse=True)


def sort_rank(players: list[Joueur]):
    return sorted(players, key=attrgetter('player_ranking'))


def sort(players: list[Joueur]):
    return sort_score(sort_rank(players))


def suisse_first(players: list[Joueur]):
    for player in players:
        player._player_score = 0
    nb_players = len(players)
    sorted_list = sort(players)
    first_pairs = [sort_rank([sorted_list[i], sorted_list[int(nb_players/2) + i]]) for i in range(int(nb_players / 2))]
    played_pairs = first_pairs.copy()
    return first_pairs, played_pairs


def suisse_then(players: list[Joueur], played_pairs: list):
    nb_players = len(players)
    sorted_list = sort(players)
    pairs = []
    attributed_players = []
    try:
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
    except Exception:
        return False


if __name__ == "__main__":
    pass
