from tinydb import TinyDB

from Controler.util import ask_stop


class Table:
    def __init__(self, db_name: str, table_name: str):
        self.db_name = db_name
        self.table_name = table_name

        self.db = TinyDB(self.db_name, indent=4, default=str)
        self.table = self.db.table(self.table_name)

    def ask_size(self):
        return len(self.table)

    def save_data(self, serialized: dict, propose_stop: bool = False):
        self.table.insert(serialized)
        if propose_stop:
            return ask_stop()

    def import_data_from_prop(self, Object, prop: str, value):
        data = self.table.get(getattr(Object, prop) == value)
        Obj = Object(**data)
        return Obj

    def import_data_from_id(self, Object, id: int):
        data = self.table.get(doc_id=id)
        Obj = Object(**data)
        return Obj

    def update_data(self, updated: dict, propose_stop: bool = False):
        self.table.update(updated, doc_ids=[updated['id']])
        if propose_stop:
            return ask_stop()

    def import_all_data(self, Object):
        objects = self.table.all()
        created = []
        for object in objects:
            created.append(Object(**object))
        return created


if __name__ == "__main__":
    pass
