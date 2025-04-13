from rich.console import Console

from addressbook import Record
from notes import Note

from .draw_header import draw_header
from .draw_note import draw_note
from .draw_notes import draw_notes
from .draw_record import draw_record
from .draw_records import draw_records
from .prompt_command import prompt_command
from .prompt_select import prompt_select


class AppInterface:
    def __init__(self):
        self.console = Console()
        pass

    def draw_header(self, commands: list[str]):
        draw_header(self.console, commands)

    def draw_note(self, note: Note) -> None:
        draw_note(self.console, note)

    def draw_notes(self, notes: list[Note]) -> None:
        draw_notes(self.console, notes)

    def draw_record(self, record: Record) -> None:
        draw_record(self.console, record)

    def draw_records(self, records: list[Record], title="Found contacts") -> None:
        draw_records(self.console, records, title)

    def draw_info(self, message: str):
        print(f"ℹ️{message}")

    def draw_failure(self, message: str):
        print(f"⛔️{message}")

    def draw_warning(self, message: str):
        print(f"⚠️{message}")

    def draw_success(self, message: str):
        print(f"✅{message}")

    def prompt_command(self):
        return prompt_command()

    def prompt_select(self, message: str, options: list[str]):
        return prompt_select(message, options)
