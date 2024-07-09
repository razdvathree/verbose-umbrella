from aiogram.fsm.state import State, StatesGroup


class EditNote(StatesGroup):
    note_content = State()


class DownloadPhoto(StatesGroup):
    url_to_photo = State()
