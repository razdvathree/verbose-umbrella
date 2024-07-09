from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from tgbot.utils.database import Notes


def menu_note() -> InlineKeyboardMarkup:
    """
    Create menu for note
    :return: InlineKeyboardMarkup
    """
    kb = InlineKeyboardBuilder()
    kb.button(text="Просмотр заметки", callback_data="view-note")
    kb.button(text="Изменение заметки", callback_data="edit-note")
    kb.button(text="Удаление заметки", callback_data="delete-note")
    kb.button(text="Генерация изображения", callback_data="generate-image")
    kb.button(text="Запостить на Telegraph", callback_data="upload-to-telegraph")
    return kb.adjust(1).as_markup()


def menu_list_notes(notes: list[Notes]) -> InlineKeyboardMarkup:
    """
    Create menu for list notes
    :param notes:
    :return: InlineKeyboardMarkup
    """
    kb = InlineKeyboardBuilder()
    if len(notes) == 0:
        kb.button(text="Заметок нет(", callback_data="None!!_+")
    for note in notes:
        kb.button(text=f"Заметка №{note.id}", callback_data=f"note_{note.id}")
    return kb.adjust(1).as_markup()
