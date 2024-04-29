from aiogram import executor
from create_bot import dp
from handlers import client_handlers, admin_handlers, common_handlers
from db import start_db

async def on_startup(_):
    print('Your bot is online')
    start_db()


client_handlers.register_client_handlers(dp)
admin_handlers.register_admin_handlers(dp)
common_handlers.register_common_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
