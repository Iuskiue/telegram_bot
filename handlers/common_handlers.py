import json
import string

from aiogram import types, Dispatcher


async def profanity_filter(message: types.Message):
    profanity_words_list = json.load(open('profanity_filter/profanity.json'))

    if {
        word.lower().translate(str.maketrans('', '', string.punctuation))
        for word in message.text.split(' ')
    }.intersection(set(profanity_words_list)):
        await message.reply('Profanity is forbidden!')
        await message.delete()


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(profanity_filter)
