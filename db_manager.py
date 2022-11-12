from tinydb import TinyDB

def save_data(table_name: str, serialized: dict):
    db = TinyDB('db.json', indent=4, default=str)
    table = db.table(table_name)
    table.insert(serialized)

def save_all_data(table_name: str, serialized: list[dict]):
    db = TinyDB('db.json', indent=4, default=str)
    table = db.table(table_name)
    table.truncate()
    table.insert_multiple(serialized)

def import_all_data(table_name: str, Object: object):
    db = TinyDB('db.json', indent = 4)
    table = db.table(table_name)
    objects = table.all()
    
    created = []
    for object in objects:
        created.append(Object(object))
    return created

def serialize_object(object: object):
    return object.__dict__

def serialize(created: list[object]):
    return [object.__dict__ for object in created]

# if __name__ == '__main__':
#     Tournoi1 = Tournoi('tournoi1')
#     t = [Tournoi1.__dict__]
#     save_all_data('tournaments_table', t)
#     import_all_data('tournaments_table')
