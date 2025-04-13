from addressbook import AddressBook
from notes import NotesManager

class AppState:
    """
    Combines all parts of bots state and handles their persistence
    """
    def __init__(self, *, notes: NotesManager, book: AddressBook):
        self.book = book
        self.notes = notes

    @staticmethod
    def load(*, notes_file: str = None, book_file: str = None) -> "AppState":
        notes = NotesManager.load(notes_file) if notes_file else NotesManager.load()
        book = AddressBook.load(book_file) if book_file else AddressBook.load()

        return AppState(notes=notes, book=book)

    def save(self):
        self.book.save()
        self.notes.save()
