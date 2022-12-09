from datetime import date
from faker import Faker

from Model.db_manager import Table
from Controler.util import input_date, serialize_object
from Model.Ronde import Ronde
from Model.Joueur import Joueur
import View.view_text as view_text

f = Faker(locale="fr_FR")

today = date.today()


class Tournoi:
    Table = Table('db.json', 'tournaments_table')

    scenario = {
        'tournament_name': [{'type': input, 'text': view_text.sc_tournament_name}],
        'tournament_location': [{'type': input, 'text': view_text.sc_tournament_location}],
        'tournament_start_date': [{'type': print, 'text': view_text.sc_tournament_start_date}],
        'tournament_end_date': [{'type': input_date, 'text': view_text.sc_tournament_end_date}],
        'tournament_nb_round': [{'type': input, 'text': view_text.sc_tournament_nb_round}],
        'tournament_time_control': [{'type': input, 'text': view_text.sc_tournament_time_control,
                                     'answers': view_text.rep_time_control}],
        'tournament_description': [{'type': input, 'text': view_text.sc_tournament_description}],
    }

    step = ['tournament_name', 'tournament_location', 'tournament_start_date', 'tournament_end_date',
            'tournament_time_control', 'tournament_description']

    # TODO: check if still usefull
    @classmethod
    def import_tournoi_from_id(cls, tournament_id):
        return cls.Table.import_data_from_id(cls, tournament_id)

    def __init__(self, id: int = -1, tournament_name: str = f.word(), tournament_location: str = f.address(),
                 tournament_start_date: date = today, tournament_end_date: date = today,
                 tournament_nb_round: int = 0, tournament_rounds: list[dict] = [],
                 tournament_players: list[int] = [], tournament_time_control: str = 'non renseigné',
                 tournament_description: str = 'non renseignée', _step: int = 0, _pairs: list = [],
                 _played_pairs: list = []):
        self.id = Tournoi.Table.ask_size() + 1 if id == -1 else id
        self.tournament_name = tournament_name
        self.tournament_location = tournament_location
        self.tournament_start_date = tournament_start_date
        self.tournament_end_date = tournament_end_date
        self.tournament_nb_round = tournament_nb_round
        self.tournament_rounds = tournament_rounds if tournament_rounds != [] else []
        self.tournament_players = tournament_players if tournament_players != [] else []
        self.tournament_time_control = tournament_time_control
        self.tournament_description = tournament_description
        self._step = _step
        self._pairs = _pairs
        self._played_pairs = _played_pairs

    def __str__(self):
        return f"{self.tournament_name}, le {self.tournament_start_date}"

    def add_round(self, round: Ronde):
        serializedRound = serialize_object(round)
        self.tournament_rounds.append(serializedRound)
        self.tournament_nb_round += 1
        serializedTournament = serialize_object(self)
        Tournoi.Table.update_data(serializedTournament)

    def add_player(self, player_id: int):
        self.tournament_players.append(player_id)

    def list_players(self):
        return [Joueur.import_player_from_id(player_id) for player_id in self.tournament_players]


if __name__ == "__main__":
    pass
