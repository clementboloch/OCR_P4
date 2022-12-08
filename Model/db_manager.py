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

    def import_data_from_id(self, Object, id: int):
        data = self.table.get(doc_id=id)
        Obj = Object(**data)
        return Obj

    def update_data(self, updated: dict):
        self.table.update(updated, doc_ids=[updated['id']])

    def import_all_data(self, Object):
        objects = self.table.all()
        created = []
        for object in objects:
            created.append(Object(**object))
        return created


if __name__ == "__main__":
    pass
