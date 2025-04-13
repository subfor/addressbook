from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from notes import Note

def draw_note(console: Console, note: Note) -> None:
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
