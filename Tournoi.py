from datetime import date
from faker import Faker

from util import input_date
from Ronde import Ronde
from Joueur import Joueur
import project_const as const

f = Faker(locale = "fr_FR")

today = date.today()
no_date = date(1, 1, 1)

class Tournoi:
    created = []

    scenario = {
        'tournament_name': [{'type': input, 'text': "\n\nVeuillez saisir le nom de l'événement : \n"}],
        'tournament_location': [{'type': input, 'text': "\n\nlocalisation : \n"}],
        'tournament_start_date': [{'type': input_date, 'text': "\n\nstart date : \n"}],
        'tournament_end_date': [{'type': input_date, 'text': "\n\nend date : \n"}],
        'tournament_nb_round': [{'type': input, 'text': "\n\nnb round : \n"}],
        'tournament_rounds': [{'type': input, 'text': "\n\nround : \n"}],
        'tournament_players': [{'type': input, 'text': "\n\nplayers : \n"}],
        'tournament_time_control': [{'type': input, 'text': "\n\ntime control : \n", 'answers': ['bullet', 'blitz', 'coup rapide']}],
        'tournament_description': [{'type': input, 'text': "\n\ndescription : \n"}],
    }
    
    step = ['tournament_name', 'tournament_location', 'tournament_time_control', 'tournament_description']
    
    def __init__(self, tournament_name: str = f.word(), tournament_location: str = f.address(), tournament_start_date: date = today, tournament_end_date: date = today, tournament_nb_round: int = const.nb_round, tournament_rounds: list[Ronde] = [], tournament_players: list[int] = [], tournament_time_control: str = 'non renseigné', tournament_description: str = 'non renseignée'):
        self.tournament_name = tournament_name
        self.tournament_location = tournament_location
        self.tournament_start_date = tournament_start_date
        self.tournament_end_date = tournament_end_date
        self.tournament_nb_round = tournament_nb_round
        self.tournament_rounds = tournament_rounds
        self.tournament_players = tournament_players
        self.tournament_time_control = tournament_time_control
        self.tournament_description = tournament_description

    def __str__(self):
        return f"{self.tournament_name}, le {self.tournament_start_date}"
    
    def add_round(self, round: Ronde):
        self.tournament_rounds.append(round)
        return self
    
    def add_player(self, player_id: int):
        if player_id in self.tournament_players:
            return False
        else:
            self.tournament_players.append(player_id)
            return True

    def del_player(self, player: Joueur):
        if player in self.tournament_players:
            self.tournament_players.remove(player)
            return "message de confirmation"
        else:
            return "Le joueur n'était pas inscrit au tournoi"
    
    def def_time(self, time_control):
        if time_control in ["bullet", "blitz", "coup rapide"]:
            self.time_control = time_control
            return "message de confirmation"
        else:
            return "message erreur"
        # faire en sorte que le main (controler) renvoie les valeurs par défault (un bullet, un blitz ou un coup rapide)

        

if __name__ == '__main__':
    Tournoi1 = Tournoi('tournoi1')
    # print(type(Tournoi1.tournament_rounds))
    # print(Tournoi1.__dict__)
    print(f.word())

'''
préciser dans la console que la date est définie automatiquement à la date du jour
Faire des return quel que soit l'alternatif ? 

'''

'''
• Tournées
    ◦ La liste des instances rondes.
    '''