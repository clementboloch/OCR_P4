from datetime import date
from faker import Faker

from Model.db_manager import Table
from Controler.util import input_date, serialize_object
from Model.Ronde import Ronde
from Model.Joueur import Joueur
from Controler.project_const import nb_round

f = Faker(locale="fr_FR")

today = date.today()
no_date = date(1, 1, 1)


class Tournoi:
    Table = Table('app/db.json', 'tournaments_table')

    scenario = {
        'tournament_name': [{'type': input, 'text': "\n\nVeuillez saisir le nom de l'événement : \n"}],
        'tournament_location': [{'type': input, 'text': "\n\nlocalisation : \n"}],
        'tournament_start_date': [{
            'type': print,
            'text': '\n\nLa date de début du tournoi est définie à la date du jour.\n'
        }],
        'tournament_end_date': [{
            'type': input_date,
            'text': '\n\n\nPour avoir la date du jour comme date de fin du tournoi saisir "y" ou "entrer"\n'
        }],
        'tournament_nb_round': [{'type': input, 'text': "\n\nnb round : \n"}],
        'tournament_rounds': [{'type': input, 'text': "\n\nround : \n"}],
        'tournament_players': [{'type': input, 'text': "\n\nplayers : \n"}],
        'tournament_time_control': [{'type': input, 'text': "\n\ntime control : \n",
                                    'answers': ['bullet', 'blitz', 'coup rapide']}],
        'tournament_description': [{'type': input, 'text': "\n\ndescription : \n"}],
    }

    step = ['tournament_name', 'tournament_location', 'tournament_start_date', 'tournament_end_date',
            'tournament_time_control', 'tournament_description']

    def __init__(self, tournament_name: str = f.word(), tournament_location: str = f.address(),
                 tournament_start_date: date = today, tournament_end_date: date = today,
                 tournament_nb_round: int = nb_round, tournament_rounds: list[dict] = [],
                 tournament_players: list[int] = [], tournament_time_control: str = 'non renseigné',
                 tournament_description: str = 'non renseignée'):
        self.tournament_name = tournament_name
        self.tournament_location = tournament_location
        self.tournament_start_date = tournament_start_date
        self.tournament_end_date = tournament_end_date
        self.tournament_nb_round = tournament_nb_round
        self.tournament_rounds = tournament_rounds if tournament_rounds != [] else []
        self.tournament_players = tournament_players if tournament_players != [] else []
        self.tournament_time_control = tournament_time_control
        self.tournament_description = tournament_description

    def __str__(self):
        return f"{self.tournament_name}, le {self.tournament_start_date}"

    def add_round(self, round: Ronde):
        serializedRound = serialize_object(round)
        self.tournament_rounds.append(serializedRound)

    def add_player(self, player_id: int):
        self.tournament_players.append(player_id)

    def list_players(self):
        return [Joueur.import_player_from_id(player_id) for player_id in self.tournament_players]


if __name__ == '__main__':
    Tournoi1 = Tournoi('tournoi1')
    # print(type(Tournoi1.tournament_rounds))
    # print(Tournoi1.__dict__)
    print(f.word())
