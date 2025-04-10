from prompt_toolkit import PromptSession

from addressbook import AddressBook, Record
from ui import get_name, get_email, draw_record

def add_email(book: AddressBook, session: PromptSession):
    name = get_name(session)
    email = get_email(session)
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    if email:
        record.add_email(email)
        print("\n✅ Email added.")
        draw_record(record.get_info())
