from telegraph_api import Telegraph


async def telegraph_uploader(note_content: str, note_id: int) -> str:
    telegraph = Telegraph()
    await telegraph.create_account(
        short_name="NoteBot",
        author_name="NoteBot",
    )

    page = await telegraph.create_page(title=f"Заметка #{note_id}", content_html=note_content)
    return page.url
