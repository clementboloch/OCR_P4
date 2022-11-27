import datetime
from faker import Faker

# from project_const import no_date

from db_manager import Table
# TODO: utiliser player_birthday -> attention, voir comment gérer la date pour l'aniversaire : texte, objet date ?
# from util import input_date

f = Faker(locale="fr_FR")


class Joueur:
    Table = Table('db.json', 'players_table')

    scenario = {
        'player_firstname': [{'type': input, 'text': "\n\nfirst name : \n"}],
        'player_lastname': [{'type': input, 'text': "\n\nlast name : \n"}],
        # 'player_birthday': [{'type': input_date, 'text': "\n\nbirthday : \n"}],
        'player_birthday': [{'type': input, 'text': "\n\nbirthday : \n"}],
        'player_gender': [{'type': input, 'text': "\n\ngender : \n"}],
        'player_ranking': [{'type': input, 'text': "\n\nranking : \n"}],
    }

    step = ['player_firstname', 'player_lastname', 'player_birthday', 'player_gender', 'player_ranking']

    @classmethod
    def import_player_from_id(cls, player_id):
        return cls.Table.import_data_from_id(cls, player_id)

    # def __init__(self, player_firstname: str = 'non renseigné', player_lastname: str = 'non renseigné',
    #              player_birthday: datetime.date = no_date, player_gender: str = '',
    #              player_ranking: int = -1, _player_score: float = 0):
    def __init__(self, player_firstname: str = f.first_name(), player_lastname: str = f.last_name(),
                 player_birthday: datetime.date = f.date(), player_gender: str = '',
                 player_ranking: int = int(Faker().numerify(text="#%")), _player_score: float = 0):
        self.player_firstname = player_firstname
        self.player_lastname = player_lastname
        self.player_birthday = player_birthday
        self.player_gender = player_gender
        self.player_ranking = player_ranking
        self._player_score = _player_score

    def __repr__(self):
        return str(self.player_firstname) + " " + str(self.player_lastname)

    def __str__(self):
        return str(self.player_firstname) + " " + str(self.player_lastname)


if __name__ == "__main__":
    pass
