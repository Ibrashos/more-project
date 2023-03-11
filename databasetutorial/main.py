import sqlite3 as sq

with sq.connect("kaopan.db") as con:
    cur = con.cursor()

    # cur.execute("DROP TABLE IF EXISTS users")
    # cur.execute("""CREATE TABLE IF NOT EXISTS users (
    #     user_id INTEGER PRIMARY KEY,
    #     name TEXT,
    #     sex INTEGER,
    #     old INTEGER,
    #     score INTEGER
    #     )""")

    cur.execute("SELECT * FROM users WHERE old IN(12,24) AND score <= 1000 or sex = 1 ORDER BY old ASC")
    print(cur.fetchall())
    for result in cur:
        print(result)