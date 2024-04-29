from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import db
from create_bot import bot
from db import add_to_db, delete_db_item
from keyboards import kb_admin
from create_bot import dp

ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id

    await bot.send_message(
        message.from_user.id,
        'What do you want, oh mighty Admin?',
        reply_markup=kb_admin
    )
    await message.delete()


async def sfm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Please provide an image')


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        curr_state = await state.get_state()
        if not curr_state:
            return
        await state.finish()
        await message.reply('Ok. The process is successfully canceled')


async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id

        await FSMAdmin.next()
        await message.reply('Now provide a name')


async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text.strip()

        await FSMAdmin.next()
        await message.reply('Enter description')


async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text.strip()

        await FSMAdmin.next()
        await message.reply('Enter price')


async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text.strip())

        await add_to_db(state=state)
        await state.finish()


async def delete_cb_handler(callback: types.CallbackQuery):
    db_data_clean = callback.data.replace('del ', '')

    await db.delete_db_item(db_data_clean)
    await callback.answer(text=f'{db_data_clean} item deleted.', show_alert=True)


async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await db.read_all_from_db()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nDescription: {ret[2]}\nPrice: {ret[-1]}')
            await bot.send_message(
                message.from_user.id,
                text='^^^',
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(f'Delete {ret[1]}', callback_data=f'del {ret[1]}'),
                ),
            )


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(sfm_start, commands=['upload'], state=None)

    dp.register_message_handler(cancel_handler, state='*', commands=['cancel'])
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state='*')

    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)

    dp.register_message_handler(delete_item, commands=['delete'])
    dp.register_callback_query_handler(delete_cb_handler, lambda x: x.data.startswith('del '))

    dp.register_message_handler(make_changes_command, commands=['is_admin'], is_chat_admin=True)

