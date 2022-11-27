from Model.Joueur import Joueur
from Model.Tournoi import Tournoi
from Controler.util import serialize_object

NewTournament = Tournoi()
serializedNewTournament = serialize_object(NewTournament)
Tournoi.Table.save_data(serializedNewTournament)

NewPlayer = Joueur()
serializedNewPlayer = serialize_object(NewPlayer)
Joueur.Table.save_data(serializedNewPlayer)
