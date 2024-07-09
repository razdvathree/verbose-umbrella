from tgbot.utils.database.models import Notes, db


def init_db() -> None:
    """
    Create Tables if not exists in database

    :return: None
    """
    print("[+] Создаем таблицы, если они еще не были созданы.")
    db.create_tables([Notes])


def create_note(note_content: str) -> int:
    """
    Create new note in database

    :param note_content: text of note
    :return: ID Note
    """
    note: Notes = Notes.create(note_content=note_content)
    return note.id


def get_note(note_id: int) -> str:
    """
    Get note by ID

    :param note_id: ID note
    :return: text of note
    """
    print(note_id)
    note: Notes = Notes.get(Notes.id == note_id)
    return note.note_content


def delete_note(note_id: int) -> None:
    """
    Delete note by ID

    :param note_id: ID note
    :return: None
    """
    Notes.delete().where(Notes.id == note_id).execute()


def edit_note(note_id: int, note_content: str) -> bool:
    """
    Edit note by ID

    :param note_id: ID note
    :param note_content: text of note
    :return: None
    """
    note = Notes.get_or_none(Notes.id == note_id)
    if note is None:
        return False
    else:
        Notes.update(note_content=note_content).where(Notes.id == note_id).execute()
        return True


def get_all_notes() -> list[Notes]:
    """
    Get all notes from database

    :return: list of notes
    """
    notes: list[Notes] = Notes.select()
    return notes
