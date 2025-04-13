from rich.panel import Panel
from rich.table import Table

from addressbook import Record

def draw_record(console, record: Record):
    """
    Displays a single contact in a card view in console
    """
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan", justify="left")
    table.add_column(style="white", overflow="fold")

    table.add_row("📞 Phones:", "; ".join([phone.value for phone in record.phones]))
    table.add_row("🎂 Birthday:", record.birthday.value.strftime("%d.%m.%Y") if record.birthday is not None else "-")
    table.add_row("📧 Emails:", ", ".join(e.value for e in record.emails) if record.emails else "-")
    table.add_row("🏠 Address:", record.address.value if record.address else "-")

    panel = Panel(
        table,
        title=f"[bold magenta]{record.name.value}[/bold magenta]",
        border_style="bright_magenta",
        padding=(1, 2),
        expand=False,
    )
    console.print(panel)
