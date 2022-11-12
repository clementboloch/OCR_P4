from Joueur import Joueur
from Tournoi import Tournoi
from db_manager import save_data, serialize_object

for _ in range(5):
    NewTournament = Tournoi()
    serializedNewTournament = serialize_object(NewTournament)
    save_data('tournaments_table', serializedNewTournament)

    NewPlayer = Joueur()
    serializedNewPlayer = serialize_object(NewPlayer)
    save_data('players_table', serializedNewPlayer)