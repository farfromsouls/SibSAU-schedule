async def crt_upd(sql, tg_id, link):

    cursor = sql[0]
    conn = sql[1]

    # getting "(group/professor)/(number)""
    link_id = link.split("/")
    link_id = f'{link_id[-2]}/{link_id[-1]}'

    data = (tg_id, link_id)

    # adding/updating link in db
    try:
        cursor.execute('INSERT INTO users (tg_id, link) VALUES(?, ?)', data)
    except:
        cursor.execute('''UPDATE  users SET link = ? WHERE tg_id = ?''', data[::-1])

    conn.commit()

async def get(sql, tg_id):
    pass