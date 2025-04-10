from functools import wraps

from prompt_toolkit import PromptSession

from addressbook import (AddressBook, DateFormatError, EmailFormatError,
                         PhoneFormatError)
from ui import (autocomplete, bottom_toolbar, draw_header, style)

from commands import find_command

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
    session = PromptSession(
        completer=autocomplete, complete_while_typing=True, style=style
    )
    print("Welcome to Personal Helper")
    try:
        while True:
            user_input = session.prompt(
                [("class:prompt", ">>> ")], bottom_toolbar=bottom_toolbar
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
                case _:
                    command_fn = find_command(command)

                    if command_fn is None:
                        print("Invalid command.")
                        continue

                    command_fn(book, session)
    except KeyboardInterrupt:
        print("\n[✋] Interrupted by user (Ctrl+C)")
    book.save()
    print("\n📁 Address book saved. Bye!")


if __name__ == "__main__":
    main()
