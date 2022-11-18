from tinydb import TinyDB

class Table:
    def __init__(self, db_name: str, table_name: str):
        self.db_name = db_name
        self.table_name = table_name

        self.db = TinyDB(self.db_name, indent=4, default=str)
        self.table = self.db.table(self.table_name)

    def ask_size(self):
        return len(self.table)
    
    def save_data(self, serialized: dict):
        self.table.insert(serialized)

    def import_data_from_id(self, Object: object, id: int):
        data = self.table.get(doc_id = id)
        Obj = Object(**data)
        return Obj


    def update_data(self, id: int, updated: dict):
        self.table.update(updated, doc_ids=[id])


    def save_all_data(self, serialized: list[dict]):
        self.table.truncate()
        self.table.insert_multiple(serialized)

    def import_all_data(self, Object: object):
        objects = self.table.all()

        created = []
        for object in objects:
            created.append(Object(**object))
        return created
