from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import yes_no_dialog, input_dialog
from prompt_toolkit.validation import Validator

from notes import Note, NotesManager

from addressbook import Record, AddressBook, Email, Phone, Birthday

from ui import (draw_contacts, draw_record, draw_single_note, get_address,
                get_birthday, get_email, get_name, get_new_email, get_birthday_range,
                get_new_phone, get_old_email, get_old_phone, get_phone, get_term)



def add_contact(book: AddressBook):
    name = get_name()

    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
        print(f"Creating contact for {name}")
    else:
        print(f"Contact for {name} already exists")
        return

    phone = get_phone()
    email = get_email()
    birthday = get_birthday()
    address = get_address()

    if phone:
        record.add_phone(phone)
    if email:
        record.add_email(email)
    if birthday:
        record.set_birthday(birthday)
    if address:
        record.set_address(address)

    print("\n✅ Contact saved.")
    draw_record(record.get_info())


def edit_contact(book: AddressBook):
    name_completer = WordCompleter([name for name in book.keys()])

    name = get_name(completer=name_completer)

    record = book.find(name)
    if not record:
        print(f"Contact for {name} not found")
        return
    else:
        print(f"Found contact for {name}")

    words = ['phones', 'emails', 'address', 'birthday']

    focus = prompt('What do you want to edit? ',
                           completer=WordCompleter(words),
                           validator=Validator.from_callable(lambda i: i in words),
                           validate_while_typing=True)

    match focus:
        case 'phones':
            for phone in [phone for phone in record.phones]:
                dialog = yes_no_dialog(title=f"Keep phone?",
                                       text=f"Should keep {phone.value}?")

                data = dialog.run()

                if not data:
                    record.phones = [p for p in record.phones if phone.value != p.value]

            dialog = input_dialog(title=f"Add phone?",
                                  text="Input new phone:",
                                  validator=Validator.from_callable(Phone.validate_phone))

            data = dialog.run()

            if data:
                record.add_phone(data)
        case 'emails':
            for email in [email for email in record.emails]:
                dialog = yes_no_dialog(title=f"Keep email?",
                                       text=f"Should keep {email.value}?")

                data = dialog.run()

                if not data:
                    record.emails = [e for e in record.emails if email.value != e.value]

            dialog = input_dialog(title=f"Add email?",
                                text="Input new email:",
                                validator=Validator.from_callable(Email.is_email_valid))

            data = dialog.run()

            if data:
                record.add_email(data)
        case 'address':
            dialog = input_dialog(title=f"Update address",
                                  text=f"What is the address (leave blank to unset)?",
                                  default=record.address.value if record.address else '')
            data = dialog.run()

            if data is None:
                return

            record.set_address(data)
        case 'birthday':
            validator = lambda value: True if value == '' else Birthday.validate_date(value)

            dialog = input_dialog(title=f"Update birthday",
                                  text=f"When is the birthday (DD.MM.YYYY or leave blank to unset)?",
                                  default=record.birthday.stringify_date() if record.birthday else '',
                                  validator=Validator.from_callable(validator))
            data = dialog.run()

            if data is None:
                return

            record.set_birthday(data)

    print("✅Contact saved.")
    draw_record(record.get_info())

def delete_contact(book: AddressBook):
    name_completer = WordCompleter([name for name in book.keys()])

    name = get_name(completer=name_completer)

    record = book.find(name)
    if not record:
        print(f"Contact for {name} not found")
        return
    else:
        print(f"Found contact for {name}")

    draw_record(record.get_info())

    should_delete = prompt(message="Are you sure you want to delete this contact (yes/no)?",
                    completer=WordCompleter(['yes', 'no']),
                    validator=Validator.from_callable(lambda v: v == 'yes' or v == 'no'))

    if should_delete != 'yes':
        return

    book.delete(name)

    print("✅Contact deleted.")

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
        record.set_birthday(birthday)
        print("\n✅ Birthday added.")
        draw_record(record.get_info())
    else:
        print("Contact not found")

def search_contacts(book: AddressBook):
    term = get_term()

    if term is None:
        return

    records = [record for record in book.values() if record.check(term)]

    print(f"Found {len(records)} contacts")

    if len(records) == 0:
        return

    draw_contacts(contacts=[record.get_info() for record in records])

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
    range_int = int(get_birthday_range())

    birthdays = book.get_upcoming_birthday(limit=range_int)

    if birthdays:
        text = ""
        for person in birthdays:
            text += (
                f"Name: {person['name']}, "
                f"Birthday: {person['birthday']}, "
                f"Congratulation date: {person['congratulation_date']}"
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

