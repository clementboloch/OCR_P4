from Joueur import Joueur
from Tournoi import Tournoi
from db_manager import Table
from util import serialize_object

PlayersTable = Table('db.json', 'players_table')
TournamentTable = Table('db.json', 'tournaments_table')


NewTournament = Tournoi()
serializedNewTournament = serialize_object(NewTournament)
PlayersTable.save_data(serializedNewTournament)

NewPlayer = Joueur()
serializedNewPlayer = serialize_object(NewPlayer)
TournamentTable.save_data(serializedNewPlayer)