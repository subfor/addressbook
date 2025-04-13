from functools import wraps

from addressbook import (DateFormatError, EmailFormatError,
                         PhoneFormatError)
from app_context import AppContext
from commands import COMMANDS

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
    print("Welcome to Personal Helper")

    context = AppContext.create()

    context.interface.draw_header([command for command in COMMANDS.keys()]+['hello', 'quit / exit'])

    while True:
        try:
            user_input = context.interface.prompt_command()

            command = user_input.strip()

            match command:
                case "exit" | "quit":
                    break
                case "hello":
                    print("How can I help you?")
                case _:
                    command_fn = COMMANDS.get(command)

                    if command_fn is None:
                        print("❌Invalid command")
                    else:
                        command_fn(context)
        except EOFError:
            print("❗Aborted (Ctrl+D)")
        except KeyboardInterrupt:
            print("✋Interrupted by user (Ctrl+C)")
            break

    context.state.save()
    print("📁Address book saved. Bye!")


if __name__ == "__main__":
    main()
