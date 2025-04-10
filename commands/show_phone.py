from prompt_toolkit import PromptSession

from addressbook import AddressBook
from ui import get_name, draw_record

def show_phone(book: AddressBook, session: PromptSession):
    name = get_name(session)
    record = book.find(name)
    if record:
        draw_record(record.get_info())
    else:
        print("Contact not found")
