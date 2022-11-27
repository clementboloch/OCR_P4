from Model.Joueur import Joueur
from Model.Tournoi import Tournoi
from util import serialize_object

NewTournament = Tournoi()
serializedNewTournament = serialize_object(NewTournament)
Joueur.Table.save_data(serializedNewTournament)

NewPlayer = Joueur()
serializedNewPlayer = serialize_object(NewPlayer)
Tournoi.Table.save_data(serializedNewPlayer)
