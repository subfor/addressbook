from rich.console import Console
from rich.panel import Panel
from rich.table import Table

def draw_header(console: Console, commands: list[str]) -> None:
    table = Table.grid(expand=True)
    table.add_column(justify="left", ratio=1)
    table.add_column(justify="left", ratio=1)
    table.add_column(justify="left", ratio=1)

    for i in range(0, len(commands) // 3 + (1 if len(commands) % 3 != 0 else 0)):
        table.add_row(
            f"[bold cyan]{commands[i * 3]}[/bold cyan]",
            "" if i * 3 + 2 > len(commands) else f"[bold cyan]{commands[i * 3 + 1]}[/bold cyan]",
            "" if i * 3 + 3 > len(commands) else f"[bold cyan]{commands[i * 3 + 2]}[/bold cyan]",
        )

    panel = Panel(
        table,
        title="[bold magenta]📒 Address Book[/bold magenta]",
        subtitle="[magenta]Interactive assistant.[/magenta]",
        border_style="bright_magenta",
        padding=(1, 2),
    )

    console.print(panel)
