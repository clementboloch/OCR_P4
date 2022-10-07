'''    
Classement --> doit être positif
'''

from datetime import date
no_date = date(1, 1, 1)

class Joueur:
    def __init__(self, name: str, surname: str, birthday: date = no_date, gender: str = '', ranking: int = -1):
        self.name = name
        self.surname = surname
        self.birthday = birthday
        self.gender = gender
        self.ranking = ranking

    

if __name__ == "__main__":
    joueur1 = Joueur('Boloch', 'Clément')
    print(joueur1.__dict__)