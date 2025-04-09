from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

COMMANDS = [
    "add contact",
    "add email",
    "add birthday",
    "add note",
    "hello",
    # "close",
    "all contacts",
    "exit",
    "quit",
    "set address",
    "show birthday",
    "show birthdays",
    "change phone",
    "change email",
    "show phone",
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
autocomplete = CommandCompleter(COMMANDS, ignore_case=True)


console = Console()


def bottom_toolbar() -> list:
    return [
        ("class:bottom-toolbar", " 🧠 Tab — autocomplete | Ctrl+C or exit/quit — exit")
    ]


def draw_header() -> None:

    table = Table.grid(expand=True)
    table.add_column(justify="left", ratio=1)
    table.add_column(justify="left", ratio=1)
    table.add_column(justify="left", ratio=1)

    table.add_row(
        "[bold cyan]add contact[/bold cyan] NAME PHONE",
        "[bold cyan]add birthday[/bold cyan] NAME DATE",
        "[bold cyan]add note[/bold cyan] TITLE",
    )
    table.add_row(
        "[bold cyan]change phone[/bold cyan] NAME OLD NEW",
        "[bold cyan]show phone[/bold cyan] NAME",
        "[bold cyan]show birthday[/bold cyan] NAME",
    )
    table.add_row(
        "[bold cyan]add email[/bold cyan] NAME EMAIL",
        "[bold cyan]change email[/bold cyan] NAME OLD_EMAIL NEW_EMAIL",
        "[bold cyan]set address[/bold cyan] NAME ADDRESS",
    )
    table.add_row(
        "[bold cyan]all contacts[/bold cyan] show all contacts",
        "[bold cyan]birthdays[/bold cyan] next week",
        "[bold cyan]exit / close[/bold cyan]",
    )

    panel = Panel(
        table,
        title="[bold magenta]📒 Address Book[/bold magenta]",
        subtitle="[magenta]Manage contacts, phones, birthdays, notes[/magenta]",
        border_style="bright_magenta",
        padding=(1, 2),
    )

    console.print(panel)


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
    table.add_column(
        style="bold cyan",
        justify="left",
    )
    table.add_column(style="white", overflow="fold")

    table.add_row("📱 Phones:", phones)
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
