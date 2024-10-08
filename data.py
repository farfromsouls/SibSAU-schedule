async def create(conn, cursor, tg_id, link):
    import sqlite3

    link_id = link.split("/")
    link_id = f'{link_id[-2]}/{link_id[-1]}'
    data = (tg_id, link_id)

    try:
        cursor.execute('INSERT INTO users (tg_id, link) VALUES(?, ?)', data)
    except:
        cursor.execute('''UPDATE  users SET link = ? WHERE tg_id = ?''', data[::-1])

    conn.commit()
