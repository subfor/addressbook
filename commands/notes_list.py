from app_context import AppContext

def notes_list(context: AppContext):
    notes = context.state.notes.get_all_notes()
    if notes:
        context.interface.draw_notes(notes)
    else:
        context.interface.draw_info('No notes found')
