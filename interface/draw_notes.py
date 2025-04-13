from rich.console import Console
from rich.table import Table

from notes import Note

def draw_notes(console: Console, notes: list[Note]) -> None:
    """
    Displays a list of notes in a table view using rows in console
    """
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
