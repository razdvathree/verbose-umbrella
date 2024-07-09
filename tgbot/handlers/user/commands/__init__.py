from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from tgbot.utils.database import create_note, get_all_notes, delete_note, get_note, edit_note
from tgbot.utils.downloader_photo import download_photo_from_url
from tgbot.utils.generate_image import add_text_to_image_with_brightness
from tgbot.utils.keyboard import menu_note, menu_list_notes


async def command_new_handler(message: Message, command: CommandObject, state: FSMContext):
    # get command args
    note_content: str = command.args
    if note_content:
        # add new note and send menu with settings
        note_id = create_note(note_content)
        await message.answer(f"Заметка #{note_id} создана!\nВыберите действие для данной заметки!",
                             reply_markup=menu_note())
        await state.update_data(note_id=note_id)
    else:
        await message.answer("Вы не указали текст для новой заметки!")


async def command_list_handler(message: Message):
    # send keyboard with all notes
    notes = get_all_notes()
    await message.answer(f"Все заметки⬇️",
                         reply_markup=menu_list_notes(notes))


async def command_delete_handler(message: Message, command: CommandObject):
    # get command args
    try:
        note_id: int = int(command.args)
        if note_id:
            # delete note
            delete_note(note_id)
            await message.answer(f"Заметка #{note_id} удалена!")
        else:
            await message.answer("Вы не указали ID для удаления заметки!")
    except TypeError:
        await message.answer("Вы не указали ID для удаления заметки!")


async def command_note_handler(message: Message, command: CommandObject):
    # get command args
    try:
        note_id: int = int(command.args)
        if note_id:
            # get note
            note = get_note(note_id)
            await message.answer(f"Заметка #{note_id}:\n\n{note}")
        else:
            await message.answer("Вы не указали ID для вывода заметки!")
    except TypeError:
        await message.answer("Вы не указали ID для вывода заметки!")


async def command_edit_handler(message: Message, command: CommandObject):
    # get command args
    args: str = command.args
    if args is not None:
        # check amount words in args and is int first element or not
        list_words_args = args.split()
        if len(list_words_args) >= 2:
            try:
                note_id: int = int(list_words_args[0])
                # collect all words after first element
                note_content: str = " ".join(list_words_args[1:])
                print(note_id, note_content)
                if note_id and note_content:
                    # edit note
                    note = edit_note(note_id, note_content)
                    if note:
                        await message.answer(f"Заметка #{note_id} отредактирована!")
                    else:
                        await message.answer("Данной заметки не существует!")
                else:
                    await message.answer("Вы не указали ID для редактирования заметки!")
            except TypeError:
                await message.answer("Вы не указали ID для редактирования заметки!")
        else:
            await message.answer("Вы не указали ID или текст для редактирования заметки!")
    else:
        await message.answer("Вы не указали ID для редактирования заметки!")


async def command_start_handler(message: Message, state: FSMContext):
    # Reset FSMContext
    await state.clear()
    await message.answer(f"Привет {message.from_user.first_name}, это бот для заметок! У вас появилось меню слева от"
                         f" поля ввода, творите!\n\nКоманды доступные вам:\n"
                         f"/new - (/new [текст]) - создать новую заметку\n"
                         f"/start - Перезапуск бота\n"
                         f"/note - (/note [номер]) - вывести заметку по номеру\n"
                         f"/delete - (/delete [номер]) - удалить заметку по номеру\n"
                         f"/edit - (/edit [номер] [новый текст]) - редактировать заметку по номеру\n"
                         f"/list - вывести список всех заметок\n"
                         f"/generate - (/generate [номер заметки] [url]) - сгенерировать изображение с заметкой",
                         parse_mode="HTML")


async def command_generate_handler(message: Message, command: CommandObject):
    # get command args
    args: str = command.args
    if args is not None:
        # check amount elements in args
        elements = args.split()
        if len(elements) == 2:
            try:
                note_id: int = int(elements[0])
                url: str = elements[1]
                if note_id and url:
                    # generate image
                    path_to_photo = download_photo_from_url(url)
                    if path_to_photo:
                        add_text_to_image_with_brightness(image_path=path_to_photo,
                                                          text=get_note(note_id),
                                                          save_path=path_to_photo)
                        photo = FSInputFile(path_to_photo)
                        await message.answer_photo(photo=photo, caption="Сгенерированное изображение с вашей заметкой!")
                    else:
                        await message.answer("Вернитесь к /start")
            except TypeError:
                await message.answer("Номер заметки не число!")
        else:
            await message.answer("Слишком много аргументов...")
    else:
        await message.answer("Аргументы не указаны...")
