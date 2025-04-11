from ui import draw_notes
from typing import List, Optional
from datetime import datetime
import pickle

class Note:
    def __init__(self, title: str, content: str, tags: Optional[List[str]] = None):
        self.title = title
        self.content = content
        self.tags = tags if tags else []
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def update_content(self, new_content: str):
        self.content = new_content
        self.updated_at = datetime.now()

    def add_tag(self, tag: str):
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()

    def remove_tag(self, tag: str):
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()

def __str__(self) -> str:
    if not self.notes:
        return "[!] No notes found."

    
    sorted_notes = sorted(
        self.notes,
        key=lambda n: (len(n.tags), n.created_at)
    )

    return "\n\n".join(str(note) for note in sorted_notes)

class NotesManager:
    def __init__(self):
        self.notes = []

    def add_note(self, title: str, content: str, tags: Optional[List[str]] = None):
        if self.find_note_by_title(title):
            print("[!] Note with this title already exists.")
            return
        note = Note(title, content, tags)
        self.notes.append(note)
        print("\n✅ Note added.")

    def get_all_notes(self) -> List[Note]:
        return self.notes

    def search_notes_by_title(self, term: str) -> List[Note]:
        return [note for note in self.notes if term.lower() in note.title.lower()]

    def search_notes_by_tags(self, term: str) -> List[Note]:
        return [note for note in self.notes if any(term.lower() in tag.lower() for tag in note.tags)]

    def find_note_by_title(self, title: str) -> Optional[Note]:
        for note in self.notes:
            if note.title.lower() == title.lower():
                return note
        return None

    def find_and_remove_note(self, title: str):
        note = self.find_note_by_title(title)
        if note:
            self.notes.remove(note)
            print(f"\n✅ Note '{note.title}' removed.")
        else:
            print("[!] Note not found.")

    def remove_note(self, note: Note):
        if note in self.notes:
            self.notes.remove(note)
            print(f"\n✅ Note '{note.title}' removed.")
        else:
            print("[!] Note not found.")

    def edit_note(self, note: Note, new_title: str, new_content: str, new_tags: List[str]):
        note.title = new_title
        note.content = new_content
        note.tags = new_tags
        note.updated_at = datetime.now()
        print(f"\n✅ Note '{note.title}' updated.")

    def display_notes(self, notes: List[Note]):

     sorted_notes = sorted(notes, key=lambda n: (len(n.tags), n.created_at))
     draw_notes(sorted_notes)

    def get_autocomplete_words(self) -> List[str]:
        titles = [note.title for note in self.notes]
        tags = [tag for note in self.notes for tag in note.tags]
        return titles + tags

    def save(self, filename="notes.pkl") -> None:
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename: str = "notes.pkl") -> "NotesManager":
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            print("⚠️ Notes Book not found, created new.")
            return NotesManager()

    def __str__(self) -> str:
        return "\n".join(
            f"{note.title} | {note.content} | {', '.join(note.tags)} | Created: {note.created_at.strftime('%Y-%m-%d %H:%M')} | Updated: {note.updated_at.strftime('%Y-%m-%d %H:%M')}"
            for note in self.notes
        )
