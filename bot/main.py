import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, ErrorEvent
from aiogram_dialog import DialogManager, setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent

from bot.config_reader import Settings
from bot.dialogs.start_dialog import start_dialog
from bot.handlers.start_handler import router


async def set_bot_commands(current_bot: Bot):
    commands = [
        BotCommand(command="start", description="Начать"),
    ]
    await current_bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())


async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager, **kwargs):
    pass


async def main():
    config = Settings()
    dispatcher = Dispatcher(storage=MemoryStorage(), events_isolation=SimpleEventIsolation())
    bot = Bot(token=config.bot_token.get_secret_value())

    dispatcher.include_router(start_dialog)
    dispatcher.include_router(router)
    dispatcher.errors.register(on_unknown_intent, ExceptionTypeFilter(UnknownIntent))
    await set_bot_commands(bot)
    setup_dialogs(dispatcher)
    try:
        await dispatcher.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
