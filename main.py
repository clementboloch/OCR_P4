from operator import attrgetter

from util import serialize_object, validate_int, create_instance
from Tournoi import Tournoi
from Ronde import Ronde
from Joueur import Joueur
from algo_suisse import suisse_first, suisse_then, sort
from project_const import nb_player


def new_tournament():
    nb_potential_players = Joueur.Table.ask_size()
    potential_players_id = list(range(1, nb_potential_players + 1))
    if nb_potential_players < nb_player:
        print(f"Il faut un minmum de {nb_player} joueurs pour créer le tournoi. \nMerci de bien vouloir ajouter au moins {nb_player - nb_potential_players} joueurs.")
        return False
    Tournament = create_instance(Tournoi)
    print(f"Ajouter les {nb_player} joueurs pour ce tournoi")
    for _ in range(nb_player):
        print("Joueurs disponibles :")
        for index, player_id in enumerate(potential_players_id):
            player = Joueur.import_player_from_id(player_id)
            print(f"{index + 1} - {player}")
        index = validate_int('num joueur : ', 1, len(potential_players_id))
        id = potential_players_id.pop(index - 1)
        Tournament.add_player(id)

        playerAdded = Joueur.import_player_from_id(id)
        if playerAdded.player_gender == 'F':
            print(f'{playerAdded} a bien été ajoutée au tournoi \n')
        else:
            print(f'{playerAdded} a bien été ajouté au tournoi \n')
    print(Tournament.__dict__)

    players = Tournament.list_players()
    pairs, played_pairs = suisse_first(players)
    print('Voilà les paires : ', pairs)
    
    for i in range(Tournament.tournament_nb_round - 1):
        Round = Ronde(str(i + 1))
        Round.ask_score(pairs)
        Round.end_round()
        Tournament.add_round(Round)
        pairs, played_pairs = suisse_then(players, played_pairs)
        print('Voilà les paires : ', pairs)
    
    # Affichage des résultats
    # TODO: transformer en classe
    sorted_players = sort(players)
    print("\n Resultats :")
    for i in range(len(players)):
        print(f"{i + 1} - {sorted_players[i]}")

    # Mise à jour des classements
    # TODO: transformer en classe
    for player_id in Tournament.tournament_players:
        player = Joueur.import_player_from_id(player_id)
        new_rank = input(f"Nouveau classement du joueur {player} : ")
        Joueur.Table.update_data(player_id, {'player_ranking': int(new_rank)})
    
    return Tournament
    


menu = '''\nQue voulez vous faire ? \n
    1 - Créer un tournoi\n
    2 - Ajouter un joueur\n
    3 - Changer le classement d'un joueur\n
    4 - Liste de tous les joueurs\n
    5 - Liste des tournois\n
    6 - Liste des joueurs d'un tournoi\n
    7 - Liste des tours d'un tournoi\n
    8 - Liste des matchs d'un tournoi\n
    9 - Quitter le porgramme\n'''
    
while True:
    answer = validate_int(menu, 1, 9)

    if answer == 1:
        NewTournament = new_tournament()
        if NewTournament:
            serializedNewTournament = serialize_object(NewTournament)
            Tournoi.Table.save_data(serializedNewTournament)

    elif answer == 2:
        NewPlayer = create_instance(Joueur)
        serializedNewPlayer = serialize_object(NewPlayer)
        Joueur.Table.save_data(serializedNewPlayer)
    
    elif answer == 3:
        players = Joueur.Table.import_all_data(Joueur)
        print("De quel joueur voulez-vous changer le classement ?")
        for index, player in enumerate(players):
            print(f"{index + 1} - {player}")
        index = validate_int("", 1, len(players))
        Player = players[index - 1]
        print(f"Ancien classement du joueur {Player} : {Player.player_ranking}")
        new_rank = input(f"Nouveau classement du joueur {Player} : ")
        Joueur.Table.update_data(index, {'player_ranking': int(new_rank)})
    
    elif answer == 4:
        players = Joueur.Table.import_all_data(Joueur)
        sort = validate_int("1 - Par classement \n2 - Par ordre alphabétique\n", 1, 2)
        if sort == 1:
            sorted_players = sorted(players, key=attrgetter('player_ranking', 'player_lastname', 'player_firstname'))
        else:
            sorted_players = sorted(players, key=attrgetter('player_lastname', 'player_firstname', 'player_ranking'))
        
        for index, player in enumerate(sorted_players):
            print(f"{index + 1} - {player} (classement : {player.player_ranking})")
    
    elif answer == 5:
        tournaments = Tournoi.Table.import_all_data(Tournoi)
        for index, tournament in enumerate(tournaments):
            print(f"{index + 1} - {tournament}")

    elif answer in [6, 7, 8]:
        search_key = {6: 'joueurs', 7: 'tours', 8: 'match'}
        tournaments = Tournoi.Table.import_all_data(Tournoi)
        print(f"De quel tournoi voulez-vous lister les {search_key[answer]} ?")
        for index, tournament in enumerate(tournaments):
            print(f"{index + 1} - {tournament}")
        index = validate_int("", 1, len(tournaments))
        tournament = tournaments[index - 1]
        print(f"Liste des {search_key[answer]} du tournoi {tournament.tournament_name}")
        if answer == 6:
            sort = validate_int("1 - Par classement \n2 - Par ordre alphabétique \n", 1, 2)
            players = tournament.list_players()
            if sort == 1:
                sorted_players = sorted(players, key=attrgetter('player_ranking', 'player_lastname', 'player_firstname'))
            else:
                sorted_players = sorted(players, key=attrgetter('player_lastname', 'player_firstname', 'player_ranking'))            
            for index, player in enumerate(sorted_players):
                print(f"{index + 1} - {player} (classement : {player.player_ranking})")
        elif answer == 7:
            for index, round in enumerate(tournament.tournament_rounds):
                print(f"{index + 1} - {round['name']}")
        else:
            for index, round in enumerate(tournament.tournament_rounds):
                Round = Ronde(**round)
                print(f"{index + 1} - {Round}")
                for index, match in enumerate(Round.matchs):
                    print(f"      {index + 1} - {match}")
    
    elif answer == 9:
        print('Au revoir !')
        break
