from aiogram import Bot, Dispatcher
import asyncio

from aiogram.types import BotCommand

import config
from tgbot.handlers import user
from tgbot.utils.database import init_db


async def start_bot() -> None:
    """
    Starting bot on polling
    :return: None
    """
    print('[+] Бот запущен.')
    bot = Bot(token=config.TOKEN)
    # Add Menu button with commands
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Перезапустить бота"),
            BotCommand(command="new", description="Создать новую заметку"),
            BotCommand(command="note", description="Вывести заметку по номеру"),
            BotCommand(command="delete", description="Удалить заметку по номеру"),
            BotCommand(command="edit", description="Редактировать заметку по номеру"),
            BotCommand(command="list", description="Вывод всех заметок"),
        ]
    )
    dp = Dispatcher()

    # Include routers
    dp.include_routers(
        user.router
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    init_db()
    loop.create_task(start_bot())
    loop.run_forever()

