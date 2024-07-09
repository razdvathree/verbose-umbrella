from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from tgbot.utils.data.states import EditNote, DownloadPhoto
from tgbot.utils.database import get_note, delete_note, edit_note
from tgbot.utils.downloader_photo import download_photo_from_url
from tgbot.utils.generate_image import add_text_to_image_with_brightness
from tgbot.utils.keyboard import menu_note
from tgbot.utils.telegraph_uploader import telegraph_uploader


async def view_note_handler(callback: CallbackQuery, state: FSMContext):
    data: dict = await state.get_data()
    note_id: int = data.get("note_id")
    if note_id is None:
        await callback.message.answer("Вернитесь к /start")
    else:
        note = get_note(note_id)
        await callback.message.edit_text(f"Заметка #{note_id}:\n\n{note}", reply_markup=menu_note())


async def delete_note_handler(callback: CallbackQuery, state: FSMContext):
    data: dict = await state.get_data()
    note_id: int = data.get("note_id")
    if note_id is None:
        await callback.message.answer("Вернитесь к /start")
    else:
        delete_note(note_id)
        await callback.message.delete()
        await callback.message.answer("Заметка удалена!")


async def edit_note_handler(callback: CallbackQuery, state: FSMContext):
    data: dict = await state.get_data()
    note_id: int = data.get("note_id")
    if note_id is None:
        await callback.message.answer("Вернитесь к /start")
    else:
        await callback.message.delete()
        await callback.message.answer("Внимание, прошлая заметка будет затерта!\nОтправьте новую заметку.")
        await state.set_state(EditNote.note_content)


async def fsm_edit_note_handler(message: Message, state: FSMContext):
    note_content: str = message.text
    data: dict = await state.get_data()
    note_id: int = data.get("note_id")
    edit_note(note_id, note_content)
    await message.answer("Заметка отредактирована!")
    await state.clear()


async def generate_image_handler(callback: CallbackQuery, state: FSMContext):
    data: dict = await state.get_data()
    note_id: int = data.get("note_id")
    if note_id is None:
        await callback.message.answer("Вернитесь к /start")
    else:
        await callback.message.edit_text("Отправьте ссылку на фоновое фото для загрузки.")
        await state.set_state(DownloadPhoto.url_to_photo)


async def open_note_handler(callback: CallbackQuery, state: FSMContext):
    note_id: int = int(callback.data.split("_")[1])
    await state.update_data(note_id=note_id)
    await callback.message.edit_text(f"Выберите действия для данной заметки⬇️", reply_markup=menu_note())


async def download_photo_handler(message: Message, state: FSMContext):
    url_to_photo: str = message.text
    data: dict = await state.get_data()
    note_id: int = data.get("note_id")
    path_to_photo = download_photo_from_url(url_to_photo)
    if path_to_photo:
        add_text_to_image_with_brightness(image_path=path_to_photo,
                                          text=get_note(note_id),
                                          save_path=path_to_photo)
        photo = FSInputFile(path_to_photo)
        await message.answer_photo(photo=photo, caption="Сгенерированное изображение с вашей заметкой!")
        await state.clear()
    else:
        await message.answer("Вернитесь к /start")
        return


async def upload_to_telegraph_handler(callback: CallbackQuery, state: FSMContext):
    data: dict = await state.get_data()
    note_id: int = data.get("note_id")
    note_content = get_note(note_id)
    url_tele = await telegraph_uploader(note_content, note_id)
    if note_id is not None and url_tele is not None:
        await callback.message.edit_text(f"Ссылка на заметку:\n{url_tele}", reply_markup=menu_note())
    else:
        await callback.message.edit_text("Вернитесь к /start")
