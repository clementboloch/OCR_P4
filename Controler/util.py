from datetime import date, datetime


def create_instance(obj):
    Instance = obj()
    for param in Instance.step:
        ask(Instance, param)
    print(Instance.__dict__)
    return Instance


def input_date(text: str):
    inp = input(text)
    if inp in ['', 'y']:
        return inp
    day = validate_int('Jour : ', 1, 31)
    mounth = validate_int('Mois : ', 1, 12)
    year = validate_int('Année : ', 1900, 2100)
    new_date = date(year, mounth, day)
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
        if inp in ['y', '']:
            return 0
        elif inp == 'n':
            return 1
        else:
            print("\nJe n'ai pas compris, merci de recommencer.")


def validate_int(text: str, min: int, max=-1):
    answer = input(text)
    condition = False
    while condition is False:
        if not answer.isdigit():
            print("Ceci n'est pas un nombre entier")
            answer = input(text)
            continue
        if max in [-1, "l'infini"]:
            max_condition = False
            max = "l'infini"
        else:
            max_condition = float(answer) > float(max)
        if (float(answer) < min or max_condition):
            print(f"Ceci n'est pas un nombre entier compris entre {min} et {max}")
            answer = input(text)
            continue
        else:
            condition = True
    return int(answer)


def validate_value(text: str, values: list):
    str_values = [str(value) for value in values]
    first_str_values = str_values.copy()
    last_str_value = first_str_values.pop()
    answer = input(text)
    while answer not in str_values:
        print(f"La valeur doit être {', '.join(first_str_values)} ou {last_str_value}")
        answer = input(text)
    return float(answer)


def ask(obj, param: str):
    text = obj.scenario
    for step in text[param]:
        try:
            [type, txt, answers] = step.values()
        except Exception:
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


def now():
    return datetime.now()


if __name__ == "__main__":
    pass
