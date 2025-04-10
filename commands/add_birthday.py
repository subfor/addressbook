from prompt_toolkit import PromptSession

from addressbook import AddressBook
from ui import get_name, get_birthday, draw_record

def add_birthday(book: AddressBook, session: PromptSession):
    name = get_name(session)
    birthday = get_birthday(session)
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        print("\n✅ Birthday added.")
        draw_record(record.get_info())
    else:
        print("Contact not found")
