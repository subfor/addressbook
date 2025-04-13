from app_context import AppContext

def notes_edit(context: AppContext):
    """
    Edit an existing note
    """

    title = input("Enter the title of the note you want to edit: ")

    note = context.state.notes.find_note_by_title(title)

    if not note:
        context.interface.draw_failure('Note not found')

    new_title = input(f"Enter new title (current: {note.title}): ")
    new_content = input(f"Enter new content (current: {note.content}): ")
    new_tags = [
        tag.strip()
        for tag in input(
            f"Enter new tags (current: {', '.join(note.tags)}): "
        ).split(",")
        if tag.strip()
    ]
    context.state.notes.edit_note(note, new_title, new_content, new_tags)
    context.interface.draw_note(note)
