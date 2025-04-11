from typing import List, Optional
from datetime import datetime

class Note:
    def __init__(self, title: str, content: str, tags: Optional[List[str]] = None):
        self.title = title
        self.content = content
        self.tags = tags if tags else []
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def update_content(self, content: str):
        self.content = content
        self.updated_at = datetime.now()

    def add_tag(self, tag: str):
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()

    def remove_tag(self, tag: str):
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()

class NotesManager:
    def __init__(self):
        self.notes = []

    def add_note(self, title: str, content: str, tags: Optional[List[str]] = None):
        note = Note(title, content, tags)
        self.notes.append(note)
        print("\n✅ Note added.")
        
    def get_all_notes(self): 
        return self.notes

    def search_notes_by_title(self, term): 
        return [note for note in self.notes if term.lower() in note.title.lower()]

    def search_notes_by_tags(self, term): 
        return [note for note in self.notes if any(term.lower() in tag.lower() for tag in note.tags)]

    def show_all_notes(self):
        return self.get_all_notes()

    def remove_note(self, note: Note):
        if note in self.notes:
            self.notes.remove(note)
            print(f"\n✅ Note '{note.title}' removed.")
        else:
            print("[!] Note not found.")

    def find_note_by_title(self, title: str):
        """Find a note by its title."""
        for note in self.notes:
            if note.title.lower() == title.lower(): 
                return note
        return None 
    
    def edit_note(self, note: Note, new_title: str, new_content: str, new_tags: List[str]):
        note.title = new_title
        note.content = new_content
        note.tags = new_tags
        note.updated_at = datetime.now()
        print(f"\n✅ Note '{note.title}' updated.")

    def display_notes(self, notes: List[Note]):
        from ui import draw_notes  
        draw_notes(notes)