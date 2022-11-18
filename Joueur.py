'''    
Classement --> doit être positif
'''

import datetime
from faker import Faker

from util import input_date

f = Faker(locale = "fr_FR")
no_date = datetime.date(1, 1, 1)

class Joueur:
    created = []

    scenario = {
        'player_firstname': [{'type': input, 'text': "\n\nfirst name : \n"}],
        'player_lastname': [{'type': input, 'text': "\n\nlast name : \n"}],
        # 'player_birthday': [{'type': input_date, 'text': "\n\nbirthday : \n"}],
        'player_birthday': [{'type': input, 'text': "\n\nbirthday : \n"}],
        'player_gender': [{'type': input, 'text': "\n\ngender : \n"}],
        'player_ranking': [{'type': input, 'text': "\n\nranking : \n"}],
    }

    step = ['player_firstname', 'player_lastname', 'player_birthday', 'player_gender', 'player_ranking']


    # def __init__(self, player_firstname: str = 'non renseigné', player_lastname: str = 'non renseigné', player_birthday: datetime.date = no_date, player_gender: str = '', player_ranking: int = -1, _player_score: float = 0):
    def __init__(self, player_firstname: str = f.first_name(), player_lastname: str = f.last_name(), player_birthday: datetime.date = f.date(), player_gender: str = '', player_ranking: int = int(Faker().numerify(text="#%")), _player_score: float = 0):
        self.player_firstname = player_firstname
        self.player_lastname = player_lastname
        self.player_birthday = player_birthday
        self.player_gender = player_gender
        self.player_ranking = player_ranking
        self._player_score = _player_score
    
    def __repr__(self):
        return str(self.player_firstname)

    def __str__(self):
        return str(self.player_firstname) + " " + str(self.player_lastname)

# joueur1 = Joueur('a', 'A', no_date, 'M', 1)
# joueur2 = Joueur('z', 'Z', no_date, 'M', 2)
# joueur3 = Joueur('e', 'E', no_date, 'M', 3)
# joueur4 = Joueur('r', 'R', no_date, 'M', 4)
# joueur5 = Joueur('t', 'T', no_date, 'M', 5)
# joueur6 = Joueur('y', 'Y', no_date, 'M', 6)
# joueur7 = Joueur('u', 'U', no_date, 'M', 7)
# joueur8 = Joueur('i', 'I', no_date, 'M', 8)
# joueurs = [joueur1, joueur2, joueur3, joueur4, joueur5, joueur6, joueur7, joueur8]

if __name__ == "__main__":
    # print(f.gender())
    pass

'''
- attention, voir comment gérer la date pour l'aniversaire : texte, objet date ?
'''