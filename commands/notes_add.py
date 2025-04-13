from app_context import AppContext


def notes_add(context: AppContext):
    """
    Add a new note
    """
    title = input("Enter note title: ")

    note = context.state.notes.find_note_by_title(title)

    if note is not None:
        context.interface.draw_failure('Note with this title already exists')
        return

    content = input("Enter note content: ")
    tags = [
        tag.strip()
        for tag in input("Enter tags (comma separated): ").split(",")
        if tag.strip()
    ]

    note = context.state.notes.add_note(title, content, tags)

    context.interface.draw_success('Note added')

    context.interface.draw_note(note)
