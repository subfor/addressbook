from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Основные команды, которые будут подхватываться автодополнением
COMMANDS = [
    "add contact",
    "add email",
    "add birthday",
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
    "edit note",
    "delete note",
    "search notes",
]

# Улучшенный Completer, чтобы не предлагать команды, когда начинаем вводить аргументы
class CommandCompleter(WordCompleter):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip().lower()
        if " " in text:
            return
        yield from super().get_completions(document, complete_event)

# Стиль для prompt_toolkit — контрастный
style = Style.from_dict(
    {
        "prompt": "bold #00ffff",  # яркий голубой (бирюзовый)
        "": "#ffffff",  # основной текст белый
        "completion-menu.completion": "bg:#1f1f1f #aaaaaa",
        "completion-menu.completion.current": "bg:#00ffff #ffffff",
        "scrollbar.background": "bg:#3a3a3a",
        "scrollbar.button": "bg:#5f5f5f",
        "bottom-toolbar": "italic #888888",
    }
)

# Объект для автодополнения
autocomplete = CommandCompleter(COMMANDS, ignore_case=True)

# Console из rich для вывода цветного текста и таблиц
console = Console()

# Нижняя панелька подсказок
def bottom_toolbar() -> list:
    return [
        ("class:bottom-toolbar", " 🧠 Tab — autocomplete | Ctrl+C or exit/quit — exit")
    ]

def draw_header() -> None:
    """
    Отрисовывает верхнюю панель с краткими подсказками команд.
    """
    table = Table.grid(expand=True)
    table.add_column(justify="left", ratio=1)
    table.add_column(justify="left", ratio=1)
    table.add_column(justify="left", ratio=1)

    # Подсказки команд (двухсловных)
    table.add_row(
        "[bold bright_cyan]add contact[/bold bright_cyan] [white]NAME PHONE[/white]",
        "[bold bright_cyan]add birthday[/bold bright_cyan] [white]NAME DATE[/white]",
        "[bold bright_cyan]add note[/bold bright_cyan] [white]TITLE CONTENT [TAGS][/white]",
    )
    table.add_row(
        "[bold bright_cyan]change phone[/bold bright_cyan] [white]NAME OLD NEW[/white]",
        "[bold bright_cyan]show phone[/bold bright_cyan] [white]NAME[/white]",
        "[bold bright_cyan]show birthday[/bold bright_cyan] [white]NAME[/white]",
    )
    table.add_row(
        "[bold bright_cyan]add email[/bold bright_cyan] [white]NAME EMAIL[/white]",
        "[bold bright_cyan]change email[/bold bright_cyan] [white]NAME OLD_EMAIL NEW_EMAIL[/white]",
        "[bold bright_cyan]set address[/bold bright_cyan] [white]NAME ADDRESS[/white]",
    )
    table.add_row(
        "[bold bright_cyan]all contacts[/bold bright_cyan]",
        "[bold bright_cyan]show birthdays[/bold bright_cyan]",
        "[bold bright_cyan]exit / quit[/bold bright_cyan]",
    )

    panel = Panel(
        table,
        title="[bold bright_magenta]📒 Address Book[/bold bright_magenta]",
        subtitle="[bright_magenta]Manage contacts, phones, birthdays, notes[/bright_magenta]",
        border_style="bright_magenta",
        padding=(1, 2),
    )

    console.print(panel)


def draw_contacts(contacts: list) -> None:
    """
    Отрисовывает таблицу со всеми найденными контактами.
    """
    table = Table(title="Found contacts", border_style="bright_magenta")

    table.add_column("Contact name", justify="left", style="bright_yellow", no_wrap=True)
    table.add_column("Phones", style="bright_cyan")
    table.add_column("Birthday", justify="left", style="bright_green")
    table.add_column("Email", justify="left", style="bright_white")
    table.add_column("Address", justify="left", style="bright_blue")
    table.add_column("Notes", justify="left", style="bright_magenta")

    for contact in contacts:
        name_str = str(contact.name.value)
        phones_str = (
            "; ".join(p.value for p in contact.phones) if contact.phones else "-"
        )
        birthday_str = (
            contact.birthday.value.strftime("%d.%m.%Y")
            if contact.birthday
            else "-"
        )
        emails_str = (
            ", ".join(e.value for e in contact.emails)
            if contact.emails
            else "-"
        )
        address_str = str(contact.address.value) if contact.address else "-"
        notes_str = (
            "; ".join(note.title for note in contact.notes)
            if contact.notes
            else "No notes"
        )

        table.add_row(
            name_str, phones_str, birthday_str, emails_str, address_str, notes_str
        )

    console.print(table)


def draw_record(record: list) -> None:
    """
    Отрисовывает панель (Panel) с подробной информацией по одному контакту.
    record: [name, phones, birthday, emails, address, notes]
    """
    name, phones, b_day, emails, address, notes = record

    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold bright_cyan", justify="left")
    table.add_column(style="white", overflow="fold")

    table.add_row("📱 Phones:", phones)
    table.add_row("🎂 Birthday:", b_day)
    table.add_row("📧 Emails:", emails)
    table.add_row("🏠 Address:", address)
    table.add_row("📝 Notes:", notes)

    panel = Panel(
        table,
        title=f"[bold bright_magenta]{name}[/bold bright_magenta]",
        border_style="bright_magenta",
        padding=(1, 2),
        expand=False,
    )
    console.print(panel)