from operator import attrgetter

from util import input_date
from Tournoi import Tournoi
from Ronde import Ronde
from Match import Match
from Joueur import Joueur
from datetime import date
from algo_suisse import suisse_first, suisse_then, sort
from db_manager import Table, serialize_object
import project_const as const

PlayersTable = Table('db.json', 'players_table')
TournamentTable = Table('db.json', 'tournaments_table')


def ask_date(obj: object, param: str):
    #si que des dates demandées, ^plus besoin de mettre l'argument param, qui ne sert que pour le test sur l'instance date
    # if isinstance(param, datetime.date):
    day = int(input('jour'))
    mounth = int(input('mois'))
    year = int(input('année'))
    new_date =  date(year, mounth, day)
    obj.__dict__[param] = new_date
# to use it : ask_date(tournament, 'start_date')

def confirmation(type):
    if type == print:
        return 0
    repeat = 1
    while repeat:
        inp = input('\n Confirmez-vous votre saisie ? \n"y" ou "entrer" pour confirmer, "n" pour modifier \n')
        if inp in ['y', ''] :
            return 0
        elif inp == 'n': 
            return 1
        else:
            print("\nJe n'ai pas compris, merci de recommencer.")

def validate_int(text: str, min: int, max: int):
    answer = input(text)
    while not answer.isdigit():
        print("Ceci n'est pas un nombre entier")
        answer = input(text)
    while (float(answer) < min or float(answer) > max):
        print(f"Ceci n'est pas un nombre entier compris entre {min} et {max}")
        answer = input(text)
    return int(answer)

def ask(obj: object, param: str):
    text = obj.scenario
    for step in text[param]:
        try:
            [type, txt, answers] = step.values()
        except:
            [type, txt] = step.values()
            answers = None
        conf = 1
        while conf:
            if answers:
                print(txt)
                for i in range(len(answers)):
                    print(f"{i+1} -  {answers[i]}")
                inp = validate_int("", 1, len(answers))
                inp = answers[inp - 1]
            else:
                inp = type(txt + 'present value: ' + str(obj.__dict__[param]) + '\n')
            if type != print and inp != '':
                obj.__dict__[param] = inp
            conf = confirmation(type)

def ask_score(Round: Ronde, pairs: list[list[Joueur]]):
    for pair in pairs:
        score = float(input('score de ' + str(pair[0]) + ' : '))
        pair[0]._player_score += score
        pair[1]._player_score += 1 - score
        match = Match(pair, score)
        Round.add_match(match)


                
tournament_step = ['tournament_name', 'tournament_location', 'tournament_start_date', 'tournament_end_date', 'tournament_nb_round', 'tournament_rounds', 'tournament_players', 'tournament_time_control', 'tournament_description']
player_step = ['player_firstname', 'player_lastname', 'player_birthday', 'player_gender', 'player_ranking']

def create_instance(obj):
    Instance = obj()
    for param in Instance.step:
        ask(Instance, param)
    print(Instance.__dict__)
    return Instance

def new_tournament():
    nb_potential_players = PlayersTable.ask_size()
    potential_players_id = list(range(1, nb_potential_players + 1))
    if nb_potential_players < const.nb_player:
        print(f"Il faut un minmum de {const.nb_player} joueurs pour créer le tournoi. \nMerci de bien vouloir ajouter au moins {const.nb_player - nb_potential_players} joueurs.")
        return False
    Tournament = create_instance(Tournoi)
    print(f"Ajouter les {const.nb_player} joueurs pour ce tournoi")
    for _ in range(const.nb_player):
        print("Joueurs disponibles :")
        for index, player_id in enumerate(potential_players_id):
            player = PlayersTable.import_data_from_id(Joueur, player_id)
            print(f"{index + 1} - {player}")
        index = validate_int('num joueur : ', 1, len(potential_players_id))
        id = potential_players_id.pop(index - 1)
        Tournament.add_player(id)

        playerAdded = PlayersTable.import_data_from_id(Joueur, id)
        if playerAdded.player_gender == 'F':
            print(f'{playerAdded} a bien été ajoutée au tournoi \n')
        else:
            print(f'{playerAdded} a bien été ajouté au tournoi \n')
    print(Tournament.__dict__)

    players_id = Tournament.tournament_players
    players = [PlayersTable.import_data_from_id(Joueur, player_id) for player_id in players_id]
    pairs, played_pairs = suisse_first(players)
    print('Voilà les paires : ', pairs)
    
    for i in range(Tournament.tournament_nb_round - 1):
        Round = Ronde(i + 1)
        ask_score(Round, pairs)
        Round.end_round()
        Tournament.add_round(Round)
        pairs, played_pairs = suisse_then(players, played_pairs)
        print('Voilà les paires : ', pairs)
    
    # Affichage des résultats
    sorted_players = sort(players)
    print("\n Resultats :")
    for i in range(len(players)):
        print(f"{i + 1} - {sorted_players[i]}")

    # Mise à jour des classements
    for player_id in Tournament.tournament_players:
        player = PlayersTable.import_data_from_id(Joueur, player_id)
        new_rank = input(f"Nouveau classement du joueur {player} : ")
        PlayersTable.update_data(player_id, {'player_ranking': int(new_rank)})
    
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
            TournamentTable.save_data(serializedNewTournament)

    elif answer == 2:
        NewPlayer = create_instance(Joueur)
        serializedNewPlayer = serialize_object(NewPlayer)
        PlayersTable.save_data(serializedNewPlayer)
    
    elif answer == 3:
        players = PlayersTable.import_all_data(Joueur)
        print("De quel joueur voulez-vous changer le classement ?")
        for index, player in enumerate(players):
            print(f"{index + 1} - {player}")
        index = validate_int("", 1, len(players))
        Player = players[index - 1]
        print(f"Ancien classement du joueur {Player} : {Player.player_ranking}")
        new_rank = input(f"Nouveau classement du joueur {Player} : ")
        PlayersTable.update_data(index, {'player_ranking': int(new_rank)})
    
    elif answer == 4:
        players = PlayersTable.import_all_data(Joueur)
        sort = validate_int("1 - Par classement \n2 - Par ordre alphabétique\n", 1, 2)
        if sort == 1:
            sorted_players = sorted(players, key=attrgetter('player_ranking', 'player_lastname', 'player_firstname'))
        else:
            sorted_players = sorted(players, key=attrgetter('player_lastname', 'player_firstname', 'player_ranking'))
        
        for index, player in enumerate(sorted_players):
            print(f"{index + 1} - {player} (classement : {player.player_ranking})")
    
    elif answer == 5:
        tournaments = TournamentTable.import_all_data(Tournoi)
        for index, tournament in enumerate(tournaments):
            print(f"{index + 1} - {tournament}")

    elif answer in [6, 7, 8]:
        search_key = {6: 'joueurs', 7: 'tours', 8: 'match'}
        tournaments = TournamentTable.import_all_data(Tournoi)
        print(f"De quel tournoi voulez-vous lister les {search_key[answer]} ?")
        for index, tournament in enumerate(tournaments):
            print(f"{index + 1} - {tournament}")
        index = validate_int("", 1, len(tournaments))
        tournament = tournaments[index - 1]
        print(f"Liste des {search_key[answer]} du tournoi {tournament.tournament_name}")
        if answer == 6:
            sort = validate_int("1 - Par classement \n2 - Par ordre alphabétique \n", 1, 2)
            # TODO : méthode d'instance de Tournoi : lister ses joueurs
            players = [PlayersTable.import_data_from_id(Joueur, player_id) for player_id in tournament.tournament_players]
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







# create_tournament()
# create_instance(Tournoi)

# new_tournament()

# Tournoi1 = Tournoi('tournoi1')
# ask_date(Tournoi1.start_date)
# ask(Tournoi1, 'tournament_name')
# print(Tournoi1.__dict__)
