from operator import attrgetter

from util import input_date
from Tournoi import Tournoi
from Ronde import Ronde
from Match import Match
from Joueur import Joueur
from datetime import date
from algo_suisse import suisse_first, suisse_then, sort
from db_manager import import_all_data, save_all_data, serialize
import project_const as const

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
        score = float(input('score du joueur ' + str(pair[0]) + ' : '))
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
    Tournament = create_instance(Tournoi)
    potential_players = Joueur.created.copy()
    print(f"Ajouter les {const.nb_player} joueurs pour ce tournoi")
    for _ in range(const.nb_player):
        print("Joueurs disponibles :")
        for index, player in enumerate(potential_players):
            print(f"{index + 1} - {player}")
        index = validate_int('num joueur : ', 1, len(potential_players)) - 1
        Tournament.add_player(potential_players.pop(index))
        print('joueur ajouté \n')
    print(Tournament.__dict__)

    # A remplacer par la suite, pour le moment gérer avec les instances, et pas avec les indices dans la base
    players = Tournament.tournament_players
    pairs, played_pairs = suisse_first(players)
    print('Voilà les paires : ', pairs)
    
    for i in range(Tournament.tournament_nb_round - 1):
        Round = Ronde(i + 1)
        ask_score(Round, pairs)
        Tournament.add_round(Round)
        pairs, played_pairs = suisse_then(players, played_pairs)
        print('Voilà les paires : ', pairs)
    
    # Affichage des résultats
    sorted_players = sort(players)
    print("\n Resultats :")
    for i in range(len(players)):
        print(f"{i + 1} - {sorted_players[i]}")

    # Mise à jour des classements
    for player in sorted_players:
        new_rank = input(f"Nouveau classement du joueur {player} : ")
        player.player_ranking = int(new_rank)
    

import_all_data('players_table', Joueur)
import_all_data('tournaments_table', Tournoi)

print(Joueur.created)
# import fake data
import fake_data

print(Joueur.created)

menu = '''\nQue voulez vous faire ? \n
    1 - Créer un tournoi\n
    2 - Ajouter un joueur\n
    3 - Changer le classement d'un joueur\n
    4 - Liste de tous les joueurs (alpha ou classement)\n
    5 - Liste des tournois\n
    6 - Liste des joueurs d'un tournoi\n
    7 - Liste des tours d'un tournoi\n
    8 - Liste des matchs d'un tournoi\n
    9 - Sauvegarder et quitter le porgramme\n'''
    
while True:
    answer = validate_int(menu, 1, 9)

    if answer == 1:
        new_tournament()

    elif answer == 2:
        create_instance(Joueur)
    
    elif answer == 3:
        players = Joueur.created
        print("De quel joueur voulez-vous changer le classement ?")
        for index, player in enumerate(players):
            print(f"{index + 1} - {player}")
        index = validate_int("", 1, len(players))
        player = players[index - 1]
        new_rank = input(f"Nouveau classement du joueur {player} : ")
        player.player_ranking = int(new_rank)
        print(player.player_ranking)
    
    elif answer == 4:
        players = Joueur.created
        sort = validate_int("1 - Par classement \n2 - Par ordre alphabétique", 1, 2)
        if sort == 1:
            sorted_players = sorted(players, key=attrgetter('player_ranking', 'player_lastname', 'player_firstname'))
        else:
            sorted_players = sorted(players, key=attrgetter('player_lastname', 'player_firstname', 'player_ranking'))
        
        for index, player in enumerate(sorted_players):
            print(f"{index + 1} - {player}")
    
    elif answer == 5:
        for index, tournament in enumerate(Tournoi.created):
            print(f"{index + 1} - {tournament}")

    elif answer in [6, 7, 8]:
        search_key = {6: 'joueurs', 7: 'tours', 8: 'match'}
        tournaments = Tournoi.created
        print(f"De quel tournoi voulez-vous lister les {search_key[answer]} ?")
        for index, tournament in enumerate(tournaments):
            print(f"{index + 1} - {tournament}")
        index = validate_int("", 1, len(tournaments))
        tournament = tournaments[index - 1]
        print(f"Liste des {search_key[answer]} du tournoi {tournament.tournament_name}")
        if answer == 6:
            sort = validate_int("1 - Par classement \n2 - Par ordre alphabétique", 1, 2)
            if sort == 1:
                sorted_players = sorted(tournament.tournament_players, key=attrgetter('player_ranking', 'player_lastname', 'player_firstname'))
            else:
                sorted_players = sorted(tournament.tournament_players, key=attrgetter('player_lastname', 'player_firstname', 'player_ranking'))            
            for index, player in enumerate(sorted_players):
                print(f"{index + 1} - {player}")
        elif answer == 7:
            for index, round in enumerate(tournament.tournament_rounds):
                print(f"{index + 1} - {round.matchs}")
        else:
            for index, round in enumerate(tournament.tournament_rounds):
                print(f"{index + 1} - {round}")
                for index, match in enumerate(round.matchs):
                    print(f"      {index + 1} - {match}")
    
    elif answer == 9:
        save_all_data('players_table', serialize(Joueur.created))
        save_all_data('tournaments_table', serialize(Tournoi.created))
        print('Sauvegardé !')
        print('Au revoir')
        break







# create_tournament()
# create_instance(Tournoi)

# new_tournament()

# Tournoi1 = Tournoi('tournoi1')
# ask_date(Tournoi1.start_date)
# ask(Tournoi1, 'tournament_name')
# print(Tournoi1.__dict__)
