from app_context import AppContext
from ui import get_confirm


def notes_delete(context: AppContext):
    title = input("Enter the title of the note you want to remove: ")

    note = context.state.notes.find_note_by_title(title)

    if not note:
        context.interface.draw_failure("Note not found")
        return

    context.interface.draw_note(note)

    should_delete = get_confirm("Are you sure you want to delete this contact")

    if should_delete:
        return

    context.interface.draw_success('Note removed')