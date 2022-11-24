from datetime import datetime

from Match import Match
from Joueur import Joueur
#TEST
import time

now = lambda: datetime.now()


class Ronde: 
    def __init__(self, name: str, start: datetime = now(), end: datetime = now(), matchs: list = []):
        if name.isdigit():
            self.name = f"Round {name}"
        else:
            self.name = name
        self.start = start
        self.end = end
        self.matchs = matchs
        #TEST
        print('name ', self.name)
        print('start ', self.start)
        print('end ', self.end)
        print('matchs ', self.matchs)

    def __str__(self):
        return self.name
    
    def add_match(self, match: Match):
        self.matchs.append(match.get_match())

    def end_round(self):
        self.end = now()

    def ask_score(self, pairs: list[list[Joueur]]):
        for pair in pairs:
            score = float(input('score de ' + str(pair[0]) + ' : '))
            pair[0]._player_score += score
            pair[1]._player_score += 1 - score
            match = Match(pair, score)
            self.add_match(match)

'''
- Faire en sorte que le compteur de Round pour le nommage dépende du tournoi (si tournoi 1 a 3 rounds, recommencer le tournoi 2 avec le nom Round1 et non Round4)
'''

if __name__ == '__main__':
    from Joueur import Joueur, no_date

    # Je crée un match pour l'ajouter à une de mes instances
    joueur1 = Joueur('1', 'A', no_date, 'M', 1)
    joueur2 = Joueur('2', 'Z', no_date, 'M', 2)
    match1 = Match([joueur1, joueur2],1)

    # J'instancie une première fois ma classe
    Ronde1 = Ronde("1")
    # Je lui ajoute le match1
    Ronde1.add_match(match1)
    # Je mets fin à mon round
    Ronde1.end_round()

    time.sleep(3)
    
    # J'instancie une deuxième fois ma classe
    Ronde2 = Ronde("2")
    
    # On constate ici que le match apparait dans mes deux instances, et non que dans la première.
    # Si j'avais ajouté un match à ma Ronde2, il se serait également ajouté à ma Ronde1
    print(Ronde1.__dict__)
    print(Ronde2.__dict__)