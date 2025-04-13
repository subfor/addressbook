from typing import Optional, Callable, cast

from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import Validator
from rich.console import Console

from addressbook import (DateFormatError, EmailFormatError, NameFormatError,
                         PhoneFormatError, Record, RangeFormatError)

# Validete input

# def validated_prompt(label: str, validator=None, completer=None, optional=False):
def validated_prompt(
        label: str,
        validator: Optional[Callable[[str], None]] = None,
        completer: Optional[WordCompleter] = None,
        optional: bool = False,
) -> Callable[..., str]:
    def wrapper(
            *,
            session: PromptSession | None = None,
            label: str = label,
            validator=validator,
            live_validator=None,
            completer=completer,
    ):
        if session is None:
            session = PromptSession(
                completer=completer,
                validator=(
                    None
                    if not live_validator
                    else Validator.from_callable(live_validator)
                ),
            )

        while True:
            try:
                value = session.prompt(f"🔹 {label}: ", completer=completer).strip()
                if not value and optional:
                    return ""
                if validator:
                    validator(value)
                return value
            except KeyboardInterrupt:
                raise
            except RangeFormatError as e:
                print(f"[!] {e.message}")
            except NameFormatError:
                print("[!] Name cannot be blank")
            except PhoneFormatError:
                print("[!] Wrong phone format.")
            except EmailFormatError:
                print("[!] Wrong email format.")
            except DateFormatError:
                print("[!] Invalid date format. Use DD.MM.YYYY.")
            except EOFError:
                print("[!] Aborted")
                return None
            except Exception:
                print("[!] Invalid input. Try again.")

    return cast(Callable[..., str], wrapper)

# Input functions

get_birthday_range = validated_prompt(
    "Enter range to look for birthdays", validator=Record.validate_name
)
get_name = validated_prompt("Enter name", validator=Record.validate_name)
get_phone = validated_prompt("Enter phone", validator=Record.validate_phone)
get_email = validated_prompt(
    "Enter email (optional)", validator=Record.validate_email, optional=True
)
get_birthday = validated_prompt(
    "Enter birthday (DD.MM.YYYY, optional)",
    validator=Record.validate_birthday,
    optional=True,
)
get_address = validated_prompt("Enter address (optional)", optional=True)

get_old_phone = validated_prompt("Enter old phone", validator=Record.validate_phone)
get_new_phone = validated_prompt("Enter new phone", validator=Record.validate_phone)
get_old_email = validated_prompt("Enter old email", validator=Record.validate_email)
get_new_email = validated_prompt("Enter new email", validator=Record.validate_email)

get_term = validated_prompt("Enter search term")

def get_confirm(question: str) -> bool | None:
    answer = prompt(
        f"🔹 {question} (yes/no)? ",
        completer=WordCompleter(["yes", "no"]),
        validator=Validator.from_callable(lambda v: v == "yes" or v == "no"),
    )

    return answer == "yes"

# Autocomplete

COMMANDS = [
    "add contact",
    "add email",
    "add birthday",
    "add note",
    "delete contact",
    "hello",
    "all contacts",
    "exit",
    "quit",
    "set address",
    "show birthday",
    "show birthdays",
    "change phone",
    "change email",
    "show phone",
    "edit note",
    "remove note",
    "search notes",
    "show notes",
]

class CommandCompleter(WordCompleter):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip().lower()
        if " " in text:
            return
        yield from super().get_completions(document, complete_event)

style = Style.from_dict(
    {
        "prompt": "bold #00ffcc",
        "": "#ffffff",
        "completion-menu.completion": "bg:#1f1f1f #aaaaaa",
        "completion-menu.completion.current": "bg:#00afff #ffffff",
        "scrollbar.background": "bg:#3a3a3a",
        "scrollbar.button": "bg:#5f5f5f",
        "bottom-toolbar": "italic #888888",
    }
)

console = Console()

def bottom_toolbar() -> list:
    return [
        ("class:bottom-toolbar", " 🧠 Tab — autocomplete | Ctrl+C or exit/quit — exit")
    ]

# Formatted output
