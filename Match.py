'''
Un match unique doit être stocké sous la forme d'un tuple contenant deux listes, 
chacune contenant deux éléments : une référence à une instance de joueur et un score. 
'''



from Joueur import Joueur


class Match:
    def __init__(self, players: list[Joueur], score_1: float):
        self.player_index_1 = players[0]
        self.player_index_2 = players[1]
        self.score1 = score_1
        self.score2 = 1- score_1
    
    def get_match(self):
        return ([self.player_index_1, self.score1], [self.player_index_2, self.score2])

if __name__ == '__main__':
    pass
    # Ronde1= Ronde(Tournoi1)
    # Match1 = Match(1, 1, 2, 0)


'''
- Ajouter une gestion des erreurs pour vérifier que la somme des 2 scores = 1 et que ils sont bien égal à 1, 1/2 ou 0
'''