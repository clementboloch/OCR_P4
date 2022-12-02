from datetime import datetime

from Model.Match import Match
from Model.Joueur import Joueur
from Controler.util import validate_value, now
from Controler.project_const import no_datetime


class Ronde:
    def __init__(self, name: str, matchs: list = [], start: datetime = no_datetime, end: datetime = no_datetime):
        self.name = f"Round {name}" if name.isdigit() else name
        self.matchs = matchs if matchs != [] else []
        self.start = now() if start == no_datetime else start
        self.end = now() if end == no_datetime else end

    def __str__(self):
        return self.name

    def add_match(self, match: Match):
        self.matchs.append(match.get_match())

    def end_round(self):
        self.end = now()

    def ask_score(self, pairs: list[list[Joueur]]):
        for pair in pairs:
            score = validate_value('score de ' + str(pair[0]) + ' : ', [0, 0.5, 1])
            pair[0]._player_score += score
            pair[1]._player_score += 1 - score
            match = Match(pair, score)
            self.add_match(match)


if __name__ == '__main__':
    pass
