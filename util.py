import datetime

def input_date(text: str):
    print(text)
    day = int(input('jour'))
    mounth = int(input('mois'))
    year = int(input('année'))
    new_date =  datetime.date(year, mounth, day)
    return new_date

def serialize_object(object: object):
    return object.__dict__

def serialize(created: list[object]):
    return [object.__dict__ for object in created]

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