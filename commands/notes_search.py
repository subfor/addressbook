from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

from app_context import AppContext

def notes_search(context: AppContext):
    tag_completer = WordCompleter(
        context.state.notes.get_autocomplete_words(), ignore_case=True
    )
    session = PromptSession(completer=tag_completer)

    search_term = session.prompt("🔍Enter the tag to search for: ").strip()
    notes = context.state.notes.search_notes_by_tags(search_term)

    if notes:
        context.interface.draw_notes(notes)
    else:
        context.interface.draw_info('No matching notes found by tag')