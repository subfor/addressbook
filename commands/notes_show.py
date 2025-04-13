from app_context import AppContext

def notes_show(context: AppContext):
    title = input("Enter note title: ")

    note = context.state.notes.find_note_by_title(title)

    if note is None:
        context.interface.draw_failure('Note with this title does not exist')
        return

    context.interface.draw_note(note)
