import sqlite3

conn = sqlite3.connect('db.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS pokemons
                  (id INTEGER PRIMARY KEY, name TEXT, cp INTEGER, hp INTEGER, attack INTEGER, defense INTEGER, health INTEGER, level INTEGER DEFAULT 0, stat_prod REAL DEFAULT 0.00)''')

conn.commit()