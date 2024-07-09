from telegraph_api import Telegraph


async def telegraph_uploader(note_content, note_id, token: str) -> str:
    telegraph = Telegraph(access_token=token)
    page = await telegraph.create_page(title=f"Заметка #{note_id}", content=note_content)
    return page.url
