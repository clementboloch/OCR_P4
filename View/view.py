from operator import attrgetter

from Controler.util import serialize_object, validate_int, create_instance, iterate_list, ask_stop
from Controler.algo_suisse import suisse_first, suisse_then, sort
from Controler.project_const import nb_player, nb_round
from Model.Tournoi import Tournoi
from Model.Ronde import Ronde
from Model.Joueur import Joueur
import View.view_text as view_text


def new_tournament(PartialTournament=None):
    nb_potential_players = Joueur.Table.ask_size()
    potential_players_id = list(range(1, nb_potential_players + 1))
    if PartialTournament is None:
        Tournament = create_instance(Tournoi)
        serializedNewTournament = serialize_object(Tournament)
        stop = Tournoi.Table.save_data(serializedNewTournament, True)
        if stop:
            return
    else:
        Tournament = PartialTournament

    if Tournament._step == 0:
        print(f"Ajouter les {nb_player} joueurs pour ce tournoi")
        for _ in range(nb_player - len(Tournament.tournament_players)):
            print("Joueurs disponibles :")
            for index, player_id in enumerate(potential_players_id):
                player = Joueur.import_player_from_id(player_id)
                print(f"{index + 1} - {player}")
            print(f"{len(potential_players_id) + 1} - Créer un joueur (et l'ajouter)")
            index = validate_int('Choix : ', 1, len(potential_players_id) + 1)
            if index == len(potential_players_id) + 1:
                id = answer_2()
            else:
                id = potential_players_id.pop(index - 1)
            Tournament.add_player(id)

            playerAdded = Joueur.import_player_from_id(id)
            if playerAdded.player_gender == 'F':
                print(f'{playerAdded} a bien été ajoutée au tournoi \n')
            else:
                print(f'{playerAdded} a bien été ajouté au tournoi \n')
        Tournament._step = 1
        serializedNewTournament = serialize_object(Tournament)
        stop = Tournoi.Table.update_data(serializedNewTournament, True)
        if stop:
            return

    players = Tournament.list_players()
    if Tournament._step <= 1:
        if not make_rounds(Tournament, players):
            return
        Tournament._step = 2
    if Tournament._step <= 2:
        display_results(players)
        Tournament._step = 3
        if ask_stop():
            return
    if Tournament._step <= 3:
        update_ranks(Tournament)
        Tournament._step = 4

    return Tournament


def make_rounds(Tournament: Tournoi, players: list[Joueur]):
    if Tournament.tournament_nb_round == 0:
        Tournament._pairs, Tournament._played_pairs = suisse_first(players)
    print('Voilà les paires : ', iterate_list(Tournament._pairs, Joueur.ids_to_players))
    while Tournament.tournament_nb_round <= nb_round - 2:
        Round = Ronde(str(Tournament.tournament_nb_round + 1))
        then = suisse_then(players, Tournament._played_pairs)
        if then is False:
            Round.ask_score(Tournament._pairs)
            Round.end_round()
            Tournament.add_round(Round)
            print("\nNous n'avons pas pu attribuer les paires selon l'algorithme suisse.\
                   \nNous avons donc mis fin au tournoi.")
            break
        else:
            Round.ask_score(iterate_list(Tournament._pairs, Joueur.ids_to_players))
            Round.end_round()
            Tournament._pairs, Tournament._played_pairs = then
            Tournament.add_round(Round)
            if ask_stop():
                return False
            print('Voilà les paires : ', iterate_list(Tournament._pairs, Joueur.ids_to_players))
    if Tournament.tournament_nb_round == nb_round - 1:
        Round = Ronde(str(Tournament.tournament_nb_round + 1))
        Round.ask_score(iterate_list(Tournament._pairs, Joueur.ids_to_players))
        Round.end_round()
        Tournament.add_round(Round)
    return True


def display_results(players: list[Joueur]):
    sorted_players = sort(players)
    print("\n Resultats :")
    for i in range(len(players)):
        print(f"{i + 1} - {sorted_players[i]}")


def update_ranks(Tournament: Tournoi):
    for player_id in Tournament.tournament_players:
        player = Joueur.import_player_from_id(player_id)
        new_rank = validate_int(f"Nouveau classement du joueur {player} : ", 1)
        serialized_updated = player.update_rank(new_rank)
        Joueur.Table.update_data(serialized_updated)


def answer_1():
    tournaments = Tournoi.Table.import_all_data(Tournoi)
    tournaments_unfinished = [Tournoi for Tournoi in tournaments if Tournoi._step < 4]
    nb_unfinished = len(tournaments_unfinished)
    if nb_unfinished != 0:
        answer = validate_int(view_text.create_tournament, 1, 2)
        if answer == 1:
            Tournament = None
        else:
            tournaments = Tournoi.Table.import_all_data(Tournoi)
            tournaments = [Tournoi for Tournoi in tournaments if Tournoi._step < 4]
            print("Quel tournoi voulez-vous reprendre ?")
            for index, Tournament in enumerate(tournaments):
                print(f"{index + 1} - {Tournament}")
            index = validate_int("", 1, len(tournaments))
            Tournament = tournaments[index - 1]
    else:
        Tournament = None
    NewTournament = new_tournament(Tournament)
    if NewTournament:
        serializedNewTournament = serialize_object(NewTournament)
        Tournoi.Table.update_data(serializedNewTournament)


def answer_2():
    NewPlayer = create_instance(Joueur)
    serializedNewPlayer = serialize_object(NewPlayer)
    Joueur.Table.save_data(serializedNewPlayer)
    return NewPlayer.id


def answer_3():
    players = Joueur.Table.import_all_data(Joueur)
    print("De quel joueur voulez-vous changer le classement ?")
    for index, player in enumerate(players):
        print(f"{index + 1} - {player}")
    index = validate_int("", 1, len(players))
    Player = players[index - 1]
    print(f"Ancien classement du joueur {Player} : {Player.player_ranking}")
    new_rank = input(f"Nouveau classement du joueur {Player} : ")
    serialized_updated = Player.update_rank(new_rank)
    Joueur.Table.update_data(serialized_updated)


def answer_4():
    players = Joueur.Table.import_all_data(Joueur)
    sort_type = validate_int("1 - Par classement \n2 - Par ordre alphabétique\n", 1, 2)
    if sort_type == 1:
        sorted_players = sorted(players, key=attrgetter('player_ranking', 'player_lastname',
                                                        'player_firstname'))
    else:
        sorted_players = sorted(players, key=attrgetter('player_lastname', 'player_firstname',
                                                        'player_ranking'))

    for index, player in enumerate(sorted_players):
        print(f"{index + 1} - {player} (classement : {player.player_ranking})")


def answer_5():
    tournaments = Tournoi.Table.import_all_data(Tournoi)
    for index, tournament in enumerate(tournaments):
        print(f"{index + 1} - {tournament}")


def answer_678(answer):
    search_key = {6: 'joueurs', 7: 'tours', 8: 'match'}
    tournaments = Tournoi.Table.import_all_data(Tournoi)
    print(f"De quel tournoi voulez-vous lister les {search_key[answer]} ?")
    for index, tournament in enumerate(tournaments):
        print(f"{index + 1} - {tournament}")
    index = validate_int("", 1, len(tournaments))
    tournament = tournaments[index - 1]
    print(f"Liste des {search_key[answer]} du tournoi {tournament.tournament_name}")
    if answer == 6:
        sort_type = validate_int("1 - Par classement \n2 - Par ordre alphabétique \n", 1, 2)
        players = tournament.list_players()
        if sort_type == 1:
            sorted_players = sorted(players, key=attrgetter('player_ranking', 'player_lastname',
                                                            'player_firstname'))
        else:
            sorted_players = sorted(players, key=attrgetter('player_lastname', 'player_firstname',
                                                            'player_ranking'))
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


def menu():
    menu = view_text.menu

    while True:
        answer = validate_int(menu, 1, 9)
        if answer == 1:
            answer_1()
        elif answer == 2:
            answer_2()
        elif answer == 3:
            answer_3()
        elif answer == 4:
            answer_4()
        elif answer == 5:
            answer_5()
        elif answer in [6, 7, 8]:
            answer_678(answer)
        elif answer == 9:
            print('Au revoir !')
            break


if __name__ == "__main__":
    pass
