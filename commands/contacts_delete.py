from prompt_toolkit.completion import WordCompleter

from app_context import AppContext
from ui import get_name

def contacts_delete(context: AppContext):
    """
    Deletes an existing contact
    """
    name_completer = WordCompleter([name for name in context.state.book.keys()])

    name = get_name(completer=name_completer)

    record = context.state.book.find(name)
    if not record:
        print(f"Contact for {name} not found")
        return

    context.interface.draw_info(f"Found contact for {name}")
    context.interface.draw_record(record)

    should_delete = context.interface.prompt_confirm("Are you sure you want to delete this contact")

    if not should_delete:
        return

    context.state.book.delete(name)

    context.interface.draw_success("Contact deleted")
