from datetime import datetime

from Match import Match

now = lambda: datetime.now()


class Ronde: 
    def __init__(self, name: str, start: datetime = now(), end: datetime = now(), matchs: list = []):
        if isinstance(name, int):
            self.name = f"Round {name}"
        else:
            self.name = name
        self.start = start
        self.end = end
        self.matchs = matchs

    def __str__(self):
        return self.name
    
    def add_match(self, match: Match):
        self.matchs.append(match.get_match())
        return self

    def end_round(self):
        self.end = now()

'''
- Faire en sorte que le compteur de Round pour le nommage dépende du tournoi (si tournoi 1 a 3 rounds, recommencer le tournoi 2 avec le nom Round1 et non Round4)
'''

# if __name__ == '__main__':
#     Ronde1 = Ronde(1)
#     Ronde1.end_round()
#     Ronde2 = Ronde(4)
#     match1 = Match({1,0},1)
#     Ronde2.add_match(match1)
#     print(Ronde1.__dict__)
#     print(Ronde2.__dict__)