from functools import wraps

from prompt_toolkit import PromptSession, prompt

from addressbook import (AddressBook, DateFormatError, EmailFormatError,
                         PhoneFormatError)
from commands import (add_birthday, add_contact, add_email, add_note_function,
                      change_email, change_phone, edit_note_function,
                      remove_note_function, search_notes_function, set_address,
                      show_all, show_all_notes_function, show_birthday,
                      show_birthdays, show_phone, search_contacts, edit_contact, delete_contact)
from notes import NotesManager
from ui import autocomplete, bottom_toolbar, draw_header, style


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


def main():
    draw_header()
    book = AddressBook.load()
    notes_manager = NotesManager.load()
    session = PromptSession(
        completer=autocomplete, complete_while_typing=True, style=style
    )
    print("Welcome to Personal Helper")
    try:
        while True:
            user_input = session.prompt(
                [("class:prompt", ">>> ")], bottom_toolbar=bottom_toolbar,
                completer=autocomplete, complete_while_typing=True, style=style,
                validator=None,
            )

            parsed_user_input = parse_input(user_input)

            if not parsed_user_input:
                continue

            command, *args = parsed_user_input

            match command:
                case "exit" | "quit":
                    break
                case "hello":
                    print("How can I help you?")
                case "add contact":
                    add_contact(book)
                case "add email":
                    add_email(book)
                case "all contacts":
                    show_all(book)
                case "add birthday":
                    add_birthday(book)
                case "delete contact":
                    delete_contact(book)
                case "edit contact":
                    edit_contact(book)
                case "set address":
                    set_address(book)
                case "show birthday":
                    show_birthday(book)
                case "show birthdays":
                    show_birthdays(book)
                case "change phone":
                    change_phone(book)
                case "change email":
                    change_email(book)
                case "show phone":
                    show_phone(book)
                case "search contacts":
                    search_contacts(book)
                case "add note":
                    add_note_function(notes_manager)
                case "edit note":
                    edit_note_function(notes_manager)
                case "remove note":
                    remove_note_function(notes_manager)
                case "search notes":
                    search_notes_function(notes_manager)
                case "show notes":
                    show_all_notes_function(notes_manager)

                case _:
                    print("Invalid command.")
    except KeyboardInterrupt:
        print("\n[✋] Interrupted by user (Ctrl+C)")
    notes_manager.save()
    book.save()
    print("\n📁 Address book saved. Bye!")


if __name__ == "__main__":
    main()
