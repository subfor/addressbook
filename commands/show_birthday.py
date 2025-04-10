from prompt_toolkit import PromptSession

from addressbook import AddressBook
from ui import get_name

def show_birthday(book: AddressBook, session: PromptSession):
    name = get_name(session)
    record = book.find(name)
    if record:
        if record.birthday:
            print(record.birthday)
        else:
            print("Birthday not set")
    else:
        print("Contact not found")
