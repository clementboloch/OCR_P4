from datetime import date

from Ronde import Ronde

today = date.today()
no_date = date(1, 1, 1)

class Tournoi:
    def __init__(self, name: str, location: str = 'non renseignée', start_date: date = today, end_date: date = today, nb_round: int = 4, rounds: list = [], players: list = [], time_control: str = 'non renseigné', description: str = 'non renseignée'):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.nb_round = nb_round # pourquoi def à 4 de base, vu qu'on en ajoute au fur et à mesure, pourquoi pas regarder taille de liste ?
        self.rounds = rounds
        self.players = players
        self.time_control = time_control
        self.description = description

    def modif_date(self, start_date: date, end_date: date = no_date):
        self.start_date = start_date
        self.end_date = end_date
        return "message de confirmation"
    
    def add_round(self, round: Ronde):
        self.rounds.append(round)
        # self.nb_round += 1
        return self
    
    def add_player(self, player_index):
        if player_index not in self.players:
            self.players.append(player_index)
            return "message de confirmation"
        else:
            return "Le joueur est déjà inscrit au tournoi"

    def del_player(self, player_index):
        if player_index in self.players:
            self.players.remove(player_index)
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
    print(Tournoi1.__dict__)


'''
préciser dans la console que la date est définie automatiquement à la date du jour
Faire des return quel que soit l'alternatif ? 

'''

'''
• Tournées
    ◦ La liste des instances rondes.
    '''