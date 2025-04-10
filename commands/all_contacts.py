from addressbook import AddressBook, Record
from ui import draw_contacts


def all_contacts(book: AddressBook):
    if not book:
        return "Contacts not found."
    return draw_contacts(contacts=book.get_all_records())
