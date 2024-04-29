from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/working_hours')
b2 = KeyboardButton('/contacts')
b3 = KeyboardButton('/menu')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.add(b1).row(b2, b3)

