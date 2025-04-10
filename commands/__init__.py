from typing import Callable, Union

from prompt_toolkit import PromptSession

from addressbook import AddressBook

from .add_birthday import add_birthday
from .add_contact import add_contact
from .add_email import add_email
from .all_contacts import all_contacts
from .change_email import change_email
from .change_phone import change_phone
from .set_address import set_address
from .show_birthday import show_birthday
from .show_birthdays import show_birthdays
from .show_phone import show_phone

commands_mapping: dict[str, Callable[[AddressBook, PromptSession], None]] = {
    'add contact': add_contact,
    'change phone': change_phone,
    'add email': add_email,
    'all contacts': all_contacts,
    'add birthday': add_birthday,
    'change email': change_email,
    'show phone': show_phone,
    'set address': set_address,
    'show birthday': show_birthday,
    'show birthdays': show_birthdays,
}

def find_command(input_str: str) -> Union[Callable[[AddressBook, PromptSession], None], None]:
    return commands_mapping[input_str]
