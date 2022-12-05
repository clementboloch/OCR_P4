from tinydb import TinyDB

db = TinyDB('db.json', indent=4, default=str)
table = db.table('players_table')
table.truncate()

table = db.table('tournaments_table')
table.truncate()
