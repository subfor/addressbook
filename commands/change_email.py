from prompt_toolkit import PromptSession

from addressbook import AddressBook
from ui import get_name, draw_record, get_old_email, get_new_email

def change_email(book: AddressBook, session: PromptSession):
    name = get_name(session)
    old_email = get_old_email(session)
    new_email = get_new_email(session)
    record = book.find(name)
    if record and record.edit_email(old_email, new_email):
        print("\n✅ Email updated.")
        draw_record(record.get_info())
    else:
        print("[!] Contact or email not found.")
