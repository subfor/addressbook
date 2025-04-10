from functools import wraps
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from addressbook import (DateFormatError, EmailFormatError, NameFormatError,
                         PhoneFormatError, Record, Comment)

# Validating input
def validated_prompt(label: str, validator=None, optional=False):
    def wrapper(session: PromptSession):
        while True:
            try:
                value = session.prompt(f"🔹 {label}: ").strip()
                if not value and optional:
                    return ""
                if validator:
                    validator(value)
                return value
            except KeyboardInterrupt:
                raise
            except (NameFormatError, PhoneFormatError, EmailFormatError, DateFormatError) as e:
                print(f"[!] {e}")
            except Exception as e:
                print(f"[!] Invalid input: {e}")
    return wrapper

# Input functions
get_name = validated_prompt("Enter name", validator=Record.validate_name)
get_phone = validated_prompt("Enter phone", validator=Record.validate_phone)
get_email = validated_prompt("Enter email (optional)", validator=Record.validate_email, optional=True)
get_birthday = validated_prompt("Enter birthday (DD.MM.YYYY, optional)", validator=Record.validate_birthday, optional=True)
get_address = validated_prompt("Enter address (optional)", optional=True)

# Additional input functions for comments
get_comment = validated_prompt("Enter comment for contact", optional=True)

def get_new_email(session: PromptSession):
    return session.prompt("🔹 Enter new email: ").strip()

def get_new_phone(session: PromptSession):
    return session.prompt("🔹 Enter new phone: ").strip()

# Autocomplete
COMMANDS = [
    "add contact",
    "add email",
    "add birthday",
    "add comment",
    "add note",
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
    "show notes",
]

class CommandCompleter(WordCompleter):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip().lower()
        if not any(text in command for command in COMMANDS):
            return
        yield from super().get_completions(document, complete_event)

autocomplete = CommandCompleter(COMMANDS, ignore_case=True)

style = Style.from_dict({
    "prompt": "bold #00ffcc",
    "": "#ffffff",
    "completion-menu.completion": "bg:#1f1f1f #aaaaaa",
    "completion-menu.completion.current": "bg:#00afff #ffffff",
    "scrollbar.background": "bg:#3a3a3a",
    "scrollbar.button": "bg:#5f5f5f",
    "bottom-toolbar": "italic #888888",
    "address": "bold #00ff00",  # Пример корректного цвета для address
    "comment": "italic #20b2aa",  # стиль для комментариев
})

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

    table.add_row("[bold cyan]add contact[/bold cyan]", "[bold cyan]add birthday[/bold cyan]", "[bold cyan]add note[/bold cyan]")
    table.add_row("[bold cyan]change phone[/bold cyan]", "[bold cyan]show phone[/bold cyan]", "[bold cyan]show birthday[/bold cyan]")
    table.add_row("[bold cyan]add email[/bold cyan]", "[bold cyan]change email[/bold cyan]", "[bold cyan]set address[/bold cyan]")
    table.add_row("[bold cyan]all contacts[/bold cyan]", "[bold cyan]birthdays[/bold cyan]", "[bold cyan]exit / quit[/bold cyan]")

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
    table.add_column("Address", justify="left", style="address")  # Применение стиля для адреса
    table.add_column("Comment", justify="left", style="comment")  # Применение стиля для комментария

    for contact in contacts:
        if not isinstance(contact, (list, tuple)) or len(contact) != 6:
            print(f"Invalid contact format: {contact}")
            continue
        table.add_row(*contact)
    console.print(table)

def draw_record(record: list) -> None:
    if not isinstance(record, list) or len(record) != 6:
        print(f"Invalid record format: {record}")
        return

    name, phones, b_day, emails, address, comment = record
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan", justify="left")
    table.add_column(style="white", overflow="fold")

    table.add_row("📱 Phones:", phones)
    table.add_row("🎂 Birthday:", b_day)
    table.add_row("📧 Emails:", emails)
    table.add_row("🏠 Address:", address, style="address")  # Применение стиля для адреса
    table.add_row("💬 Comment:", comment, style="comment")  # Применение стиля для комментария

    panel = Panel(
        table,
        title=f"[bold magenta]{name}[/bold magenta]",
        border_style="bright_magenta",
        padding=(1, 2),
        expand=False,
    )
    console.print(panel)