import sqlite3 as sq

from aiogram import types

from create_bot import bot

db = sq.connect('botopizza.db')
cur = db.cursor()


def start_db():
    if db:
        print('DB connected successfully')
    db.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    db.commit()


async def add_to_db(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES(?, ?, ?, ?)', tuple(data.values()))
        db.commit()


async def get_menu(message: types.Message):
    for ret in cur.execute('select * from menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nDescription: {ret[2]}\nPrice: {ret[-1]}')


async def read_all_from_db():
    return cur.execute('select * from menu').fetchall()


async def delete_db_item(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    db.commit()
