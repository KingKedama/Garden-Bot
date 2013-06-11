import sqlite3,sys

def main(argv):
    database=argv[0]
    conn= sqlite3.connect(database)
    c=conn.cursor()
    try:
        c.execute('''ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0 NOT NULL''')
    except:
        pass
    c.execute('SELECT nick COLLATE nocase FROM users ')
    nicks=c.fetchall()
    for nick in nicks:
        nick=nick[0]
        c.execute('SELECT SUM(messages), SUM(actions) FROM users WHERE nick=? COLLATE nocase',(nick,))
        sums=c.fetchone()
        c.execute('DELETE FROM users WHERE nick=? COLLATE nocase',(nick,))
        conn.commit()
        c.execute('INSERT INTO users (nick,messages,actions) VALUES(?,?,?)',(nick.lower(),sums[0],sums[1]))
        conn.commit()
if __name__ == "__main__":
    main(sys.argv[1:])