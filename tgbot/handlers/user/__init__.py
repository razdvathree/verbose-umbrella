from aiogram import Router, F
from aiogram.filters import Command

from tgbot.handlers.user.commands import command_list_handler, command_note_handler, command_delete_handler, \
    command_edit_handler, command_new_handler, command_start_handler, command_generate_handler
from tgbot.handlers.user.callback import view_note_handler, generate_image_handler, delete_note_handler, \
    edit_note_handler, fsm_edit_note_handler, open_note_handler, download_photo_handler
from tgbot.utils.data.states import EditNote, DownloadPhoto

router = Router()

# message register
router.message.register(command_start_handler, Command(commands=["start"]))
router.message.register(command_list_handler, Command(commands=["list"]))
router.message.register(command_note_handler, Command(commands=["note"]))
router.message.register(command_delete_handler, Command(commands=["delete"]))
router.message.register(command_edit_handler, Command(commands=["edit"]))
router.message.register(command_new_handler, Command(commands=["new"]))
router.message.register(command_generate_handler, Command(commands=["generate"]))
router.message.register(fsm_edit_note_handler, EditNote.note_content)
router.message.register(download_photo_handler, DownloadPhoto.url_to_photo)
# callback register
router.callback_query.register(view_note_handler, F.data == "view-note")
router.callback_query.register(generate_image_handler, F.data == "generate-image")
router.callback_query.register(delete_note_handler, F.data == "delete-note")
router.callback_query.register(edit_note_handler, F.data == "edit-note")
router.callback_query.register(open_note_handler, F.data.startswith("note_"))
