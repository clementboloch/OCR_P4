import datetime

def input_date(text: str):
    print(text)
    day = int(input('jour'))
    mounth = int(input('mois'))
    year = int(input('année'))
    new_date =  datetime.date(year, mounth, day)
    return new_date