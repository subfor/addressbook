from prompt_toolkit import PromptSession

from addressbook import AddressBook

from ui import get_name, get_old_phone, get_new_phone, draw_record

def change_phone(book: AddressBook, session: PromptSession):
    name = get_name(session)
    old_phone = get_old_phone(session)
    new_phone = get_new_phone(session)
    record = book.find(name)
    if record and record.edit_phone(old_phone, new_phone):
        print("\n✅ Phone updated.")
        draw_record(record.get_info())
    else:
        print("[!] Contact or phone not found.")
