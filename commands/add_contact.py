from prompt_toolkit import PromptSession

from addressbook import AddressBook, Record
from ui import get_name, get_phone, get_email, get_birthday, get_address, draw_record

def add_contact(book: AddressBook, session: PromptSession):
    name = get_name(session)
    phone = get_phone(session)
    email = get_email(session)
    birthday = get_birthday(session)
    address = get_address(session)

    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)

    if phone:
        record.add_phone(phone)
    if email:
        record.add_email(email)
    if birthday:
        record.add_birthday(birthday)
    if address:
        record.set_address(address)

    print("\n✅ Contact saved.")
    draw_record(record.get_info())
