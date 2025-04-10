from prompt_toolkit import PromptSession

from addressbook import AddressBook
from ui import get_name, get_address, draw_record

def set_address(book: AddressBook, session: PromptSession):
    name = get_name(session)
    address = get_address(session)
    record = book.find(name)
    if record:
        record.set_address(address)
        print("\n✅ Address set.")
        draw_record(record.get_info())
    else:
        print("Contact not found")
