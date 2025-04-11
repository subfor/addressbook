
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

from addressbook import AddressBook, Record
from notes import Note, NotesManager
from ui import (draw_contacts, draw_record, draw_single_note, get_address,
                get_birthday, get_email, get_name, get_new_email,
                get_new_phone, get_old_email, get_old_phone, get_phone)



def add_contact(book: AddressBook):
    name = get_name()
    phone = get_phone()
    email = get_email()
    birthday = get_birthday()
    address = get_address()

    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)

    if phone:
        record.add_phone(phone)
    if email:
        record.add_email(email)
    if birthday:
        record.add_birthday(birthday)
    if address:
        record.set_address(address)

    print("\n✅ Contact saved.")
    draw_record(record.get_info())


def change_phone(book: AddressBook):
    name = get_name()
    old_phone = get_old_phone()
    new_phone = get_new_phone()
    record = book.find(name)
    if record and record.edit_phone(old_phone, new_phone):
        print("\n✅ Phone updated.")
        draw_record(record.get_info())
    else:
        print("[!] Contact or phone not found.")


def change_email(book: AddressBook):
    name = get_name()
    old_email = get_old_email()
    new_email = get_new_email()
    record = book.find(name)
    if record and record.edit_email(old_email, new_email):
        print("\n✅ Email updated.")
        draw_record(record.get_info())
    else:
        print("[!] Contact or email not found.")


def show_phone(book: AddressBook):
    name = get_name()
    record = book.find(name)
    if record:
        draw_record(record.get_info())
    else:
        print("Contact not found")


def add_email(book: AddressBook):
    name = get_name()
    email = get_email()
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    if email:
        record.add_email(email)
        print("\n✅ Email added.")
        draw_record(record.get_info())


def show_all(book: AddressBook):
    if not book:
        return "Contacts not found."
    return draw_contacts(contacts=book.get_all_records())


def add_birthday(book: AddressBook):
    name = get_name()
    birthday = get_birthday()
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        print("\n✅ Birthday added.")
        draw_record(record.get_info())
    else:
        print("Contact not found")


def set_address(book: AddressBook):
    name = get_name()
    address = get_address()
    record = book.find(name)
    if record:
        record.set_address(address)
        print("\n✅ Address set.")
        draw_record(record.get_info())
    else:
        print("Contact not found")


def show_birthday(book: AddressBook):
    name = get_name()
    record = book.find(name)
    if record:
        if record.birthday:
            print(record.birthday)
        else:
            print("Birthday not set")
    else:
        print("Contact not found")


def show_birthdays(book: AddressBook):
    birthdays = book.get_upcoming_birthday()
    if birthdays:
        text = ""
        for person in birthdays:
            text += (
                f"Name: {person['name']}, "
                f"Congratulation date: {person['congratulation_date']}\n"
            )
        print(text.strip())
    else:
        print("Birthdays not found")


def add_note_function(notes_manager: NotesManager):
    title = input("Enter note title: ")
    content = input("Enter note content: ")
    tags = [
        tag.strip()
        for tag in input("Enter tags (comma separated): ").split(",")
        if tag.strip()
    ]
    note = Note(title, content, tags)
    notes_manager.notes.append(note)
    print("\n✅ Note added.")
    draw_single_note(note)


def edit_note_function(notes_manager: NotesManager):
    title = input("Enter the title of the note you want to edit: ")
    note = notes_manager.find_note_by_title(title)
    if note:
        new_title = input(f"Enter new title (current: {note.title}): ")
        new_content = input(f"Enter new content (current: {note.content}): ")
        new_tags = [
            tag.strip()
            for tag in input(
                f"Enter new tags (current: {', '.join(note.tags)}): "
            ).split(",")
            if tag.strip()
        ]
        notes_manager.edit_note(note, new_title, new_content, new_tags)
        draw_single_note(note)
    else:
        print("[!] Note not found.")


def remove_note_function(notes_manager: NotesManager):
    title = input("Enter the title of the note you want to remove: ")
    note = notes_manager.find_note_by_title(title)
    if note:
        notes_manager.remove_note(note)
        print("\n✅ Note removed.")
    else:
        print("[!] Note not found.")


def search_notes_function(notes_manager: NotesManager):
    tag_completer = WordCompleter(
        notes_manager.get_autocomplete_words(), ignore_case=True
    )
    session = PromptSession(completer=tag_completer)

    search_term = session.prompt("🔍 Enter the tag to search for: ").strip()
    notes = notes_manager.search_notes_by_tags(search_term)

    if notes:
        notes_manager.display_notes(notes)
    else:
        print("[!] No matching notes found by tag.")


def show_all_notes_function(notes_manager: NotesManager):
    notes = notes_manager.get_all_notes()
    if notes:
        notes_manager.display_notes(notes)
    else:
        print("[!] No notes found.")

