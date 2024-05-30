import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS objects (
            key INTEGER PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')
    cursor.execute('INSERT INTO objects (key, value) VALUES (?, ?)', (1, 'value1'))
    cursor.execute('INSERT INTO objects (key, value) VALUES (?, ?)', (2, 'value2'))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
