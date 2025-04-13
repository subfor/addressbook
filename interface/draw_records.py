from rich.console import Console
from rich.table import Table

from addressbook import Record


def draw_records(console: Console, records: list[Record], title:str):
    table = Table(title=title)
    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Phones", style="magenta")
    table.add_column("Birthday", justify="left", style="green")
    table.add_column("Email", justify="left", style="green")
    table.add_column("Address", justify="left", style="green")
    for contact in records:
        table.add_row(*contact.get_info())
    console.print(table)