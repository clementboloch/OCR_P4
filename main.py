import time

from Tournoi import Tournoi
from Ronde import Ronde
from Match import Match
from Joueur import Joueur

Clément = Joueur('Boloch', 'Clément')
Claire = Joueur('Dalibot', 'Claire')

Tournoi1 = Tournoi('tournoi1')

Ronde1 = Ronde(Tournoi1)
Ronde1.end_round()
Ronde2 = Ronde(Tournoi1)

Match1 = Match(Ronde1, 2, 3, 1)


print('Claire', Claire.__dict__)
print('tournoi1', Tournoi1.__dict__)
print('ronde1', Ronde1.__dict__)
print('match1', Match1.__dict__)
print(Match1.get_match())