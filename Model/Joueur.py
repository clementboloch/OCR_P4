import datetime
from faker import Faker

from Controler.util import input_date, serialize_object
from Model.db_manager import Table
import View.view_text as view_text

f = Faker(locale="fr_FR")


class Joueur:
    Table = Table('db.json', 'players_table')

    scenario = {
        'player_firstname': [{'type': input, 'text': view_text.sc_player_firstname}],
        'player_lastname': [{'type': input, 'text': view_text.sc_player_lastname}],
        'player_birthday': [{'type': input_date, 'text': view_text.sc_player_birthday}],
        'player_gender': [{'type': input, 'text': view_text.sc_player_gender}],
        'player_ranking': [{'type': input, 'text': view_text.sc_player_ranking}],
    }

    step = ['player_firstname', 'player_lastname', 'player_birthday', 'player_gender', 'player_ranking']

    # TODO: check if still usefull
    @classmethod
    def import_player_from_id(cls, player_id):
        return cls.Table.import_data_from_id(cls, player_id)

    @classmethod
    def ids_to_players(cls, ids: list[int]):
        return [cls.import_player_from_id(id) for id in ids]

    @classmethod
    def players_to_ids(cls, players: list):
        return [Player.id for Player in players]

    # def __init__(self, player_firstname: str = 'non renseigné', player_lastname: str = 'non renseigné',
    #              player_birthday: datetime.date = no_date, player_gender: str = '',
    #              player_ranking: int = -1, _player_score: float = 0):
    def __init__(self, id: int = -1, player_firstname: str = f.first_name(), player_lastname: str = f.last_name(),
                 player_birthday: datetime.date = f.date(), player_gender: str = '',
                 player_ranking: int = int(Faker().numerify(text="#%")), _player_score: float = 0):
        self.id = Joueur.Table.ask_size() + 1 if id == -1 else id
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

    def update_rank(self, new_rank: int):
        serialized = serialize_object(self)
        serialized['player_ranking'] = new_rank
        return serialized


if __name__ == "__main__":
    pass
