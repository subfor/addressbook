from app_context import AppContext
from ui import get_name

def contacts_show(context: AppContext):
    name = get_name()
    record = context.state.book.find(name)
    if record:
        context.interface.draw_record(record)
    else:
        context.interface.draw_info("Contact not found")
