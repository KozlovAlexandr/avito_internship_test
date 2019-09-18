import sqlite3
import os
import json
from datetime import datetime

DB_PATH = 'server_db.db'

is_db_exists = os.path.isfile(DB_PATH)
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute('PRAGMA foreign_keys = 1;')

if not is_db_exists:
    cur.executescript(open('db.sql').read())


def add_chat(body):

    body = json.loads(body)
    name = body['name']
    date = datetime.now().strftime('%Y-%m-%d %H:%M')
    if not body['users']:
        raise
    try:
        cur.execute("INSERT INTO Chat_Info VALUES(NULL, '{0}', '{1}');".format(name, date))

        cur_chat_id = cur.execute("SELECT MAX(id) FROM Chat_Info;").fetchall()[0][0];

        for uid in body['users']:
            cur.execute("INSERT INTO Chat_Users VALUES('{0}', '{1}');".format(str(cur_chat_id), uid))
    except:
        conn.rollback()
        raise

    conn.commit()

    return cur_chat_id


def add_user(body):

    body = json.loads(body)
    uname = body['username']
    date = datetime.now().strftime('%Y-%m-%d %H:%M')
    try:
        cur.execute("INSERT INTO User VALUES(NULL, '{0}', '{1}');".format(uname, date))
        cur_user_id = cur.execute("SELECT MAX(id) FROM User;").fetchall()[0][0]
    except:
        conn.rollback()
        raise

    conn.commit()

    return cur_user_id


def add_message(body):

    body = json.loads(body)
    uid = body['author']
    cid = body['chat']
    txt = body['text']
    date = datetime.now().strftime('%Y-%m-%d %H:%M')
    try:
        cur.execute("INSERT INTO Message VALUES(NULL, '{0}', '{1}', '{2}', '{3}');".format(cid, uid, txt, date))
        msg_id = cur.execute("SELECT MAX(id) FROM Message;").fetchall()[0][0]
    except:
        conn.rollback()
        raise
    conn.commit()

    return msg_id


def get_messages(body):

    body = json.loads(body)
    cid = body['chat']

    chats = cur.execute("SELECT * FROM Chat_Info WHERE id='{0}';".format(cid)).fetchall()
    if not chats:
        raise

    q_res = cur.execute("SELECT * FROM Message WHERE chat_id='{0}' ORDER BY created_at;".format(cid)).fetchall()

    return q_res


def get_chat(body):

    body = json.loads(body)
    uid = body['user']

    try:
        q_res = cur.execute("""SELECT * FROM Chat_Info 
                       WHERE id IN
                       (SELECT chat_id FROM Chat_Users 
                       WHERE user_id = {0}) ORDER BY created_at DESC;""".format(uid)).fetchall()
        if not q_res:
            raise
        q_res = list(q_res)
        new_q_res = []
        for chat in q_res:
            cid = chat[0]
            users_in_chat = cur.execute("""SELECT username FROM User
                            WHERE id in (SELECT user_id 
                            FROM Chat_Users WHERE chat_id = {0});""".format(cid)).fetchall()
            users_in_chat = [user[0] for user in users_in_chat]
            new_q_res.append(tuple(list(chat)+[users_in_chat]))
    except:
        conn.rollback()
        raise

    conn.commit()
    return new_q_res


