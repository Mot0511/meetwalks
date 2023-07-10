import sqlite3 as sq

def useSql(q):
    conn = sq.connect('db.db')
    cur = conn.cursor()
    cur.execute(q)
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data