from Model.Joueur import Joueur


class Match:
    def __init__(self, players: list[Joueur], score_1: float):
        self.player_index_1 = players[0]
        self.player_index_2 = players[1]
        self.score1 = score_1
        self.score2 = 1 - score_1

    def get_match(self):
        return ([self.player_index_1, self.score1], [self.player_index_2, self.score2])


if __name__ == "__main__":
    pass
