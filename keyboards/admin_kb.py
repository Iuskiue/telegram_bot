from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

btn_load = KeyboardButton('/upload')
btn_delete = KeyboardButton('/delete')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_admin.row(btn_load, btn_delete)
