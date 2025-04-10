from functools import wraps

from prompt_toolkit import PromptSession

from addressbook import (AddressBook, DateFormatError, EmailFormatError,
                         PhoneFormatError, Record)
from ui import (autocomplete, bottom_toolbar, draw_contacts, draw_header,
                draw_record, get_address, get_birthday, get_email, get_name,
                get_new_email, get_new_phone, get_old_email, get_old_phone,
                get_phone, style)


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, IndexError):
            match func.__name__:
                case "parse_input":
                    print("Command can not be blank")
                case _:
                    print(f"error in {func.__name__}")
        except PhoneFormatError:
            print("Wrong phone format.")
        except EmailFormatError:
            print("Wrong email format.")
        except DateFormatError:
            print("Invalid date format. Use DD.MM.YYYY")

    return inner


@input_error
def parse_input(user_input):
    parts = user_input.strip().lower().split()
    if not parts:
        return None
    if len(parts) >= 2:
        command = f"{parts[0]} {parts[1]}"
        args = parts[2:]
    else:
        command = parts[0]
        args = []
    return command, *args


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


def show_phone(book: AddressBook, session: PromptSession):
    name = get_name(session)
    record = book.find(name)
    if record:
        draw_record(record.get_info())
    else:
        print("Contact not found")


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


def show_all(book: AddressBook):
    if not book:
        return "Contacts not found."
    return draw_contacts(contacts=book.get_all_records())


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


def show_birthdays_next_week(book: AddressBook):
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


def main():
    draw_header()
    book = AddressBook.load()
    session = PromptSession(
        completer=autocomplete, complete_while_typing=True, style=style
    )
    print("Welcome to AddressBook!")
    while True:
        try:
            user_input = session.prompt(
                [("class:prompt", ">>> ")], bottom_toolbar=bottom_toolbar
            )
        except KeyboardInterrupt:
            print("Ctrl+c")
            break
        if not (parsed_user_input := parse_input(user_input)):
            continue
        command, *args = parsed_user_input

        match command:
            case "exit" | "quit":
                break
            case "hello":
                print("How can I help you?")
            case "add contact":
                add_contact(book, session)
            case "add email":
                add_email(book, session)
            case "all contacts":
                show_all(book)
            case "add birthday":
                add_birthday(book, session)
            case "set address":
                set_address(book, session)
            case "show birthday":
                show_birthday(book, session)
            case "show birthdays":
                show_birthdays_next_week(book)
            case "change phone":
                change_phone(book, session)
            case "change email":
                change_email(book, session)
            case "show phone":
                show_phone(book, session)
            case _:
                print("Invalid command.")
    book.save()
    print("\n📁 Address book saved. Bye!")


if __name__ == "__main__":
    main()
