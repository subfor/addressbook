from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import yes_no_dialog, input_dialog
from prompt_toolkit.validation import Validator

from addressbook import Record, AddressBook, Email, Phone, Birthday
from ui import get_phone, get_email, get_name, get_birthday, get_address, get_old_phone, get_new_phone, get_new_email, \
    get_old_email, draw_record, draw_contacts, get_term


def add_contact(book: AddressBook):
    name = get_name()

    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
        print(f"Creating contact for {name}")
    else:
        print(f"Contact for {name} already exists")
        return

    phone = get_phone()
    email = get_email()
    birthday = get_birthday()
    address = get_address()

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


def edit_contact(book: AddressBook):
    name = get_name()

    record = book.find(name)
    if not record:
        print(f"Contact for {name} not found")
        return
    else:
        print(f"Found contact for {name}")

    words = ['phones', 'emails', 'address', 'birthday']

    focus = prompt('What do you want to edit? ',
                           completer=WordCompleter(words),
                           validator=Validator.from_callable(lambda i: i in words),
                           validate_while_typing=True)

    match focus:
        case 'phones':
            for phone in [phone for phone in record.phones]:
                dialog = yes_no_dialog(title=f"Keep phone?",
                                       text=f"Should keep {phone.value}?")

                data = dialog.run()

                if not data:
                    record.phones = [p for p in record.phones if phone.value != p.value]

            dialog = input_dialog(title=f"Add phone?",
                                  text="Input new phone:",
                                  validator=Validator.from_callable(Phone.validate_phone))

            data = dialog.run()

            if data:
                record.add_phone(data)
        case 'emails':
            for email in [email for email in record.emails]:
                dialog = yes_no_dialog(title=f"Keep email?",
                                       text=f"Should keep {email.value}?")

                data = dialog.run()

                if not data:
                    record.emails = [e for e in record.emails if email.value != e.value]

            dialog = input_dialog(title=f"Add email?",
                                text="Input new email:",
                                validator=Validator.from_callable(Email.is_email_valid))

            data = dialog.run()

            if data:
                record.add_email(data)
        case 'address':
            dialog = input_dialog(title=f"Add address",
                                  text=f"Should update address?",
                                  default=record.address.value)
            data = dialog.run()

            if data is None:
                return

            record.set_address(data)
        case 'birthday':
            dialog = input_dialog(title=f"Add birthday",
                                  text=f"Should update birthday?",
                                  default=record.birthday.stringify_date(),
                                  validator=Validator.from_callable(Birthday.validate_date))
            data = dialog.run()

            if data is None:
                return

            record.add_birthday(data)

    print("✅Contact saved.")
    draw_record(record.get_info())


def change_phone(book: AddressBook):
    name = get_name()
    old_phone = get_old_phone()
    new_phone = get_new_phone()
    record = book.find(name)
    if record and record.edit_phone(old_phone, new_phone):
        print("\n✅ Phone updated.")
        draw_record(record.get_info())
    else:
        print("[!] Contact or phone not found.")


def change_email(book: AddressBook):
    name = get_name()
    old_email = get_old_email()
    new_email = get_new_email()
    record = book.find(name)
    if record and record.edit_email(old_email, new_email):
        print("\n✅ Email updated.")
        draw_record(record.get_info())
    else:
        print("[!] Contact or email not found.")


def show_phone(book: AddressBook):
    name = get_name()
    record = book.find(name)
    if record:
        draw_record(record.get_info())
    else:
        print("Contact not found")


def add_email(book: AddressBook):
    name = get_name()
    email = get_email()
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    if email:
        record.add_email(email)
        print("\n✅ Email added.")
        draw_record(record.get_info())


def show_all(book: AddressBook):
    if not book:
        return "Contacts not found."
    return draw_contacts(contacts=book.get_all_records())


def add_birthday(book: AddressBook):
    name = get_name()
    birthday = get_birthday()
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        print("\n✅ Birthday added.")
        draw_record(record.get_info())
    else:
        print("Contact not found")

def search_contacts(book: AddressBook):
    term = get_term()

    if term is None:
        return

    records = [record for record in book.values() if record.check(term)]

    print(f"Found {len(records)} contacts")

    if len(records) == 0:
        return

    draw_contacts(contacts=[record.get_info() for record in records])

def set_address(book: AddressBook):
    name = get_name()
    address = get_address()
    record = book.find(name)
    if record:
        record.set_address(address)
        print("\n✅ Address set.")
        draw_record(record.get_info())
    else:
        print("Contact not found")


def show_birthday(book: AddressBook):
    name = get_name()
    record = book.find(name)
    if record:
        if record.birthday:
            print(record.birthday)
        else:
            print("Birthday not set")
    else:
        print("Contact not found")


def show_birthdays(book: AddressBook):
    birthdays = book.get_upcoming_birthday()
    if birthdays:
        text = ""
        for person in birthdays:
            text += (
                f"Name: {person['name']}, "
                f"Congratulation date: {person['congratulation_date']}\n"
            )
        print(text.strip())
    else:
        print("Birthdays not found")
