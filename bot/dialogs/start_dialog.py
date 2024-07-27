from aiogram_dialog import Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.window import Window

from bot.states.start_sg import StartSg

start_window = Window(
    Const("Приветствую в боте!\nВыберите что сделать:"),
    Button(Const("Присоединиться к сессии"), "connect_to_session"),
    Button(Const("Создать сессию"), "create_session"),
    Button(Const("Посмотреть ваши сессии"), "watch_session"),
    state=StartSg.start,
)

start_dialog = Dialog(start_window)
