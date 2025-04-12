from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from addressbook import (DateFormatError, EmailFormatError, NameFormatError,
                         PhoneFormatError, Record, RangeFormatError)

# Validete input


def validated_prompt(label: str, validator=None, completer=None, optional=False):
    def wrapper(session: PromptSession | None = None,
                label: str = label,
                validator=validator,
                completer=completer):
        if session is None:
            session = PromptSession(completer=completer)

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

    return wrapper


# Input functions

get_birthday_range = validated_prompt("Enter range to look for birthdays", validator=Record.validate_name)
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

autocomplete = CommandCompleter(COMMANDS, ignore_case=True)

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

# Header


def draw_header() -> None:
    table = Table.grid(expand=True)
    table.add_column(justify="left", ratio=1)
    table.add_column(justify="left", ratio=1)
    table.add_column(justify="left", ratio=1)

    for i in range(0, len(COMMANDS) // 3 + (1 if len(COMMANDS) % 3 != 0 else 0)):
        table.add_row(
            f"[bold cyan]{COMMANDS[i * 3]}[/bold cyan]",
            "" if i * 3 + 2 > len(COMMANDS) else f"[bold cyan]{COMMANDS[i * 3 + 1]}[/bold cyan]",
            "" if i * 3 + 3 > len(COMMANDS) else f"[bold cyan]{COMMANDS[i * 3 + 2]}[/bold cyan]",
        )

    panel = Panel(
        table,
        title="[bold magenta]📒 Address Book[/bold magenta]",
        subtitle="[magenta]Interactive assistant.[/magenta]",
        border_style="bright_magenta",
        padding=(1, 2),
    )

    console.print(panel)

# Formatted output


def draw_contacts(contacts: list) -> None:
    table = Table(title="Found contacts")
    table.add_column("Contact name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Phones", style="magenta")
    table.add_column("Birthday", justify="left", style="green")
    table.add_column("Email", justify="left", style="green")
    table.add_column("Address", justify="left", style="green")
    for contact in contacts:
        table.add_row(*contact)
    console.print(table)

def draw_record(record: list) -> None:
    name, phones, b_day, emails, address = record
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan", justify="left")
    table.add_column(style="white", overflow="fold")

    table.add_row(" Phones:", phones)
    table.add_row("🎂 Birthday:", b_day)
    table.add_row("📧 Emails:", emails)
    table.add_row("🏠 Address:", address)

    panel = Panel(
        table,
        title=f"[bold magenta]{name}[/bold magenta]",
        border_style="bright_magenta",
        padding=(1, 2),
        expand=False,
    )
    console.print(panel)

def draw_single_note(note) -> None:
    table = Table.grid(padding=(0, 2))
    table.add_column(justify="left", style="bold cyan")
    table.add_column(justify="left", style="white")

    table.add_row("📝 Title:", note.title)
    table.add_row("🗒 Content:", note.content)
    table.add_row("🏷 Tags:", ", ".join(note.tags) if note.tags else "—")
    table.add_row("📅 Created:", note.created_at.strftime("%Y-%m-%d %H:%M"))
    table.add_row("🕓 Updated:", note.updated_at.strftime("%Y-%m-%d %H:%M"))

    panel = Panel(
        table,
        title=f"[bold magenta]{note.title}[/bold magenta]",
        border_style="bright_magenta",
        padding=(1, 2),
        expand=False,
    )

    console.print(panel)


def draw_notes(notes: list) -> None:
    table = Table(title="📂 All Notes")

    table.add_column("📝 Title", style="bold cyan", no_wrap=True)
    table.add_column("🗒 Content", style="white")
    table.add_column("🏷 Tags", style="magenta")
    table.add_column("📅 Created", style="green")
    table.add_column("🕓 Updated", style="green")

    for note in notes:
        tags = ", ".join(note.tags) if note.tags else "—"
        table.add_row(
            note.title,
            note.content,
            tags,
            note.created_at.strftime("%Y-%m-%d %H:%M"),
            note.updated_at.strftime("%Y-%m-%d %H:%M"),
        )

    console.print(table)
