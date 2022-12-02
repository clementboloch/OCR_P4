from datetime import date, datetime

import View.view_text as view_text


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
        inp = input(view_text.confirmer_saisie)
        if inp in view_text.rep_confirmation:
            return 0
        elif inp in view_text.rep_annulation:
            return 1
        else:
            print(view_text.saisie_incorrecte)


def validate_int(text: str, min: int, max=-1):
    answer = input(text)
    condition = False
    while condition is False:
        if not answer.isdigit():
            print(view_text.pas_entier)
            answer = input(text)
            continue
        if max in [-1, "l'infini"]:
            max_condition = False
            max = "l'infini"
        else:
            max_condition = float(answer) > float(max)
        if (float(answer) < min or max_condition):
            print(view_text.pas_interval.format(min, max))
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
        print(view_text.pas_defaut.format(', '.join(first_str_values), last_str_value))
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
                inp = type(txt + view_text.valeure_actuelle.format(str(obj.__dict__[param])))
            if type != print and inp != '':
                obj.__dict__[param] = inp
            conf = confirmation(type)


def now():
    return datetime.now()


if __name__ == "__main__":
    pass
