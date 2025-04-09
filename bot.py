from functools import wraps

from prompt_toolkit import PromptSession

from addressbook import (AddressBook, DateFormatError, EmailFormatError,
                         PhoneFormatError, Record)
from ui import (autocomplete, bottom_toolbar, draw_contacts, draw_header,
                draw_record, style)


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, IndexError):
            match func.__name__:
                case "parse_input":
                    print("Command can not be blank")
                case "add_contact":
                    print("Usage: add contact NAME PHONE_NUMBER")
                case "add_email":
                    print("Usage: add email NAME EMAIL")
                case "change_phone":
                    print("Usage: change NAME OLD_NUMBER NEW_NUMBER")
                case "change_email":
                    print("Usage: change email NAME OLD_EMAIL NEW_EMAIL")
                case "show_phone":
                    print("Usage: phone NAME")
                case "add_birthday":
                    print("Usage: add birthday NAME DATE(DD.MM.YYYY)")
                case "show_birthday":
                    print("Usage: show birthday NAME")
                case "set_address":
                    print("Usage: set address NAME ADDRESS")
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


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    existing_record = book.find(name)

    if existing_record:
        if existing_record.add_phone(phone):
            print("Phone number added to existing contact.")
            draw_record(existing_record.get_info())
        else:
            return "Phone number already exists."
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        print("New contact added.")
        draw_record(record.get_info())


@input_error
def change_phone(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        print("Contact does not exist.")
    else:
        if record.edit_phone(old_phone, new_phone):
            print("Contact updated.")
            draw_record(record.get_info())
        else:
            print("Old phone number not found")


@input_error
def change_email(args, book: AddressBook):
    name, old_email, new_email = args
    record = book.find(name)
    if record is None:
        print("Contact does not exist.")
    else:
        if record.edit_email(old_email, new_email):
            print("Contact updated.")
            draw_record(record.get_info())
        else:
            print("Old email number not found")


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        draw_record(record.get_info())
    else:
        print("Contact not found")


@input_error
def add_email(args, book: AddressBook):
    name, email = args
    existing_record = book.find(name)

    if existing_record:
        if existing_record.add_email(email):
            print("Email added to existing contact.")
            draw_record(existing_record.get_info())
        else:
            return "Email already exists."
    else:
        record = Record(name)
        record.add_email(email)
        book.add_record(record)
        print("New contact added.")
        draw_record(record.get_info())


def show_all(book: AddressBook):
    if not book:
        return "Contacts not found."
    return draw_contacts(contacts=book.get_all_records())


@input_error
def add_birthday(args, book: AddressBook):
    name, b_date = args
    record = book.find(name)
    if record:
        record.add_birthday(b_date)
        draw_record(record.get_info())
    else:
        print("Contact not found")


@input_error
def set_address(args, book: AddressBook):
    name, *address_parts = args
    address = " ".join(address_parts)
    record = book.find(name)
    if record:
        record.set_address(address)
        draw_record(record.get_info())
    else:
        print("Contact not found")


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return str(record.birthday)
        else:
            return "Birthday not set"
    return "Contact not found"


@input_error
def show_birthdays_next_week(book: AddressBook):
    birthdays = book.get_upcoming_birthday()
    if birthdays:
        text = ""
        for person in birthdays:
            text += (
                f"Name: {person['name']}, "
                f"Congratulation date: {person['congratulation_date']}\n"
            )
        return text.strip()
    return "Birthdays not found"


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
                add_contact(args, book)
            case "add email":
                add_email(args, book)
            case "all contacts":
                show_all(book)
            case "add birthday":
                add_birthday(args, book)
            case "set address":
                set_address(args, book)
            case "show birthday":
                if message := show_birthday(args, book):
                    print(message)
            case "show birthdays":
                if message := show_birthdays_next_week(book):
                    print(message)
            case "change phone":
                change_phone(args, book)
            case "change email":
                change_email(args, book)
            case "show phone":
                show_phone(args, book)
            case _:
                print("Invalid command.")
    book.save()
    print("📁 Address book saved. Bye!")


if __name__ == "__main__":
    main()
