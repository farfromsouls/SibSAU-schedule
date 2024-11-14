import sqlite3

# connecting to db
db_path = 'cfg/data.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


async def crt_upd(tg_id, link):

    # getting "(group/professor)/(number)""
    link_id = link.split("/")
    link_id = f'{link_id[-2]}/{link_id[-1]}'
    data_insert = (tg_id, link_id, 0)
    data_update = (link_id, tg_id)

    # adding/updating link in db
    try:
        cursor.execute('INSERT INTO users (tg_id, link, mailing) VALUES(?, ?, ?)', data_insert)
    except:
        cursor.execute('UPDATE users SET link = ? WHERE tg_id = ?', data_update)
    conn.commit()

async def getLink(tg_id):
    # searching link in db using user tg_id
    cursor.execute('SELECT link FROM Users WHERE tg_id = ?', (tg_id,))
    link = cursor.fetchone()[0]
    return link

async def getMailingStatus(tg_id):
    cursor.execute('SELECT mailing FROM Users WHERE tg_id = ?', (tg_id,))
    mailingStatus = cursor.fetchone()[0]
    return mailingStatus

async def updateMailingStatus(tg_id, mailing):
    data = (mailing, tg_id)
    cursor.execute('UPDATE users SET mailing = ? WHERE tg_id = ?', data)
    conn.commit()
    return "Успешно!"

async def getMailingUsers():
    cursor.execute('SELECT tg_id FROM Users WHERE mailing = 1')
    mailingUsers = cursor.fetchall()
    return mailingUsers