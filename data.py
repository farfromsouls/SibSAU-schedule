import sqlite3

# connecting to db
db_path = 'cfg/data.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


async def crt_upd(tg_id, link):

    # getting "(group/professor)/(number)""
    link_id = link.split("/")
    link_id = f'{link_id[-2]}/{link_id[-1]}'

    data = (tg_id, link_id)

    # adding/updating link in db
    try:
        cursor.execute('INSERT INTO users (tg_id, link) VALUES(?, ?)', data)
    except:
        cursor.execute(
            'UPDATE  users SET link = ? WHERE tg_id = ?', data[::-1])

    conn.commit()


async def getLink(tg_id):

    # searching link in db using user tg_id
    cursor.execute('SELECT link FROM Users WHERE tg_id = ?', (tg_id,))
    result = cursor.fetchone()[0]
    return result