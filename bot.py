from functools import wraps
from datetime import datetime
from typing import Optional, List

from prompt_toolkit import PromptSession

# ------------------------------------------------------------------------
# 1. Функция parse_input
# ------------------------------------------------------------------------
def parse_input(user_input: str) -> list:
    """
    Пример простейшего парсера.
    Возвращает список [command, arg1, arg2, ...] или пустой список, если нет команды.
    Логика: первые два слова — команда, остальное — аргументы.
    """
    user_input = user_input.strip()
    if not user_input:
        return []
    parts = user_input.split()
    if len(parts) < 2:
        return parts

    command = " ".join(parts[:2]).lower()  # Например: "add contact"
    args = parts[2:]
    return [command] + args


# ------------------------------------------------------------------------
# 2. Импортируем нужные вещи из addressbook.py и ui.py
# ------------------------------------------------------------------------
from addressbook import (
    AddressBook,
    DateFormatError,
    EmailFormatError,
    PhoneFormatError,
    Record
)
from ui import (
    autocomplete,
    bottom_toolbar,
    draw_contacts,
    draw_header,
    draw_record,
    style
)

# ------------------------------------------------------------------------
# 3. Класс Note (хранится внутри Record.notes)
# ------------------------------------------------------------------------
class Note:
    def __init__(self, title: str, content: str, tags: Optional[List[str]] = None):
        self.title = title
        self.content = content
        self.tags = tags if tags else []
        self.created_at = datetime.now()     # Дата создания
        self.updated_at = self.created_at    # Дата последнего обновления

    def add_tag(self, tag: str):
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()

    def remove_tag(self, tag: str):
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()

    def update_content(self, content: str):
        self.content = content
        self.updated_at = datetime.now()

    def display(self) -> str:
        """
        Метод для отображения заметки.
        """
        return (
            f"Title: {self.title}\n"
            f"Content: {self.content}\n"
            f"Tags: {', '.join(self.tags) if self.tags else 'No tags'}\n"
            f"Created At: {self.created_at.strftime('%d.%m.%Y %H:%M:%S')}\n"
            f"Updated At: {self.updated_at.strftime('%d.%m.%Y %H:%M:%S')}\n"
        )


# ------------------------------------------------------------------------
# 4. Декоратор для обработки ошибок
# ------------------------------------------------------------------------
def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, IndexError):
            match func.__name__:
                case "parse_input":
                    print("Command cannot be blank.")
                case "add_contact":
                    print("Usage: add contact NAME PHONE_NUMBER")
                case "add_email":
                    print("Usage: add email NAME EMAIL")
                case "change_phone":
                    print("Usage: change phone NAME OLD_NUMBER NEW_NUMBER")
                case "change_email":
                    print("Usage: change email NAME OLD_EMAIL NEW_EMAIL")
                case "show_phone":
                    print("Usage: show phone NAME")
                case "add_birthday":
                    print("Usage: add birthday NAME DATE(DD.MM.YYYY)")
                case "show_birthday":
                    print("Usage: show birthday NAME")
                case "set_address":
                    print("Usage: set address NAME ADDRESS")
                case "add_note":
                    print("Usage: add note NAME TITLE CONTENT [TAGS...]")
                case "show_notes":
                    print("Usage: show notes NAME")
                case "search_notes":
                    print("Usage: search notes TAG")
                case "delete_note":
                    print("Usage: delete note NAME NOTE_TITLE")
                case "edit_note":
                    print("Usage: edit note NAME NOTE_TITLE")
                case _:
                    print(f"Error in {func.__name__}")
        except PhoneFormatError:
            print("Wrong phone format.")
        except EmailFormatError:
            print("Wrong email format.")
        except DateFormatError:
            print("Invalid date format. Use DD.MM.YYYY")

    return inner


# ------------------------------------------------------------------------
# 5. Основные функции для работы с контактами
# ------------------------------------------------------------------------
@input_error
def add_contact(args, book: AddressBook):
    """
    add contact NAME PHONE
    """
    name, phone = args
    existing_record = book.find(name)

    if existing_record:
        if existing_record.add_phone(phone):
            print("Phone number added to existing contact.")
            draw_record(existing_record.get_info())
        else:
            print("Phone number already exists.")
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        print("New contact added.")
        draw_record(record.get_info())


@input_error
def change_phone(args, book: AddressBook):
    """
    change phone NAME OLD_NUMBER NEW_NUMBER
    """
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        print("Contact does not exist.")
    else:
        if record.edit_phone(old_phone, new_phone):
            print("Contact updated.")
            draw_record(record.get_info())
        else:
            print("Old phone number not found.")


@input_error
def change_email(args, book: AddressBook):
    """
    change email NAME OLD_EMAIL NEW_EMAIL
    """
    name, old_email, new_email = args
    record = book.find(name)
    if record is None:
        print("Contact does not exist.")
    else:
        if record.edit_email(old_email, new_email):
            print("Contact updated.")
            draw_record(record.get_info())
        else:
            print("Old email address not found.")


@input_error
def show_phone(args, book: AddressBook):
    """
    show phone NAME
    """
    name = args[0]
    record = book.find(name)
    if record:
        draw_record(record.get_info())
    else:
        print("Contact not found.")


@input_error
def add_email(args, book: AddressBook):
    """
    add email NAME EMAIL
    """
    name, email = args
    existing_record = book.find(name)

    if existing_record:
        if existing_record.add_email(email):
            print("Email added to existing contact.")
            draw_record(existing_record.get_info())
        else:
            print("Email already exists.")
    else:
        record = Record(name)
        record.add_email(email)
        book.add_record(record)
        print("New contact added.")
        draw_record(record.get_info())


def show_all(book: AddressBook):
    """
    all contacts
    """
    if not book:
        return "Contacts not found."
    return draw_contacts(contacts=book.get_all_records())


@input_error
def add_birthday(args, book: AddressBook):
    """
    add birthday NAME DD.MM.YYYY
    """
    name, b_date = args
    record = book.find(name)
    if record:
        record.add_birthday(b_date)
        draw_record(record.get_info())
    else:
        print("Contact not found.")


@input_error
def set_address(args, book: AddressBook):
    """
    set address NAME ADDRESS...
    """
    name, *address_parts = args
    address = " ".join(address_parts)
    record = book.find(name)
    if record:
        record.set_address(address)
        draw_record(record.get_info())
    else:
        print("Contact not found.")


@input_error
def show_birthday(args, book: AddressBook):
    """
    show birthday NAME
    """
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return str(record.birthday)
        else:
            return "Birthday not set."
    return "Contact not found."


@input_error
def show_birthdays_next_week(book: AddressBook):
    """
    show birthdays
    """
    birthdays = book.get_upcoming_birthday()
    if birthdays:
        text = ""
        for person in birthdays:
            text += (
                f"Name: {person['name']}, "
                f"Congratulation date: {person['congratulation_date']}\n"
            )
        return text.strip()
    return "Birthdays not found."


# ------------------------------------------------------------------------
# 6. Функции для работы со ЗАМЕТКАМИ непосредственно в контакте
# ------------------------------------------------------------------------
@input_error
def add_note(args, book: AddressBook):
    """
    add note CONTACT_NAME TITLE CONTENT [TAGS...]
    Пример: add note Nastya Meeting DiscussProject urgent important
    """
    name = args[0]
    title = args[1]
    content = args[2]
    tags = args[3:]

    record = book.find(name)
    if not record:
        print(f"Contact '{name}' not found.")
        return

    note = Note(title, content, tags)
    record.add_note(note)
    print(f"Note '{title}' added to contact '{name}'.")


@input_error
def show_notes(args, book: AddressBook):
    """
    show notes NAME
    Выводит все заметки, которые привязаны к указанному контакту.
    """
    name = args[0]
    record = book.find(name)
    if not record:
        print(f"Contact '{name}' not found.")
        return

    if not record.notes:
        print(f"No notes for contact '{name}'.")
        return

    for note in record.notes:
        print(note.display())
        print("-" * 20)


@input_error
def search_notes_by_tag(args, book: AddressBook):
    """
    search notes TAG
    Ищет указанный тег во ВСЕХ контактах и выводит результаты.
    """
    tag = args[0]
    found_any = False

    # Перебираем все контакты, смотрим их notes
    for record in book.get_all_records():
        matched_notes = []
        for note in record.notes:
            if tag in note.tags:
                matched_notes.append(note)
        if matched_notes:
            print(f"\nContact: {record.name.value}")
            for note in matched_notes:
                print(note.display())
                print("-" * 20)
            found_any = True

    if not found_any:
        print(f"No notes found with tag: {tag}")


@input_error
def delete_note_by_title(args, book: AddressBook):
    """
    delete note NAME NOTE_TITLE
    Удаляет заметку (по title) из конкретного контакта.
    """
    name = args[0]
    title = args[1]

    record = book.find(name)
    if not record:
        print(f"Contact '{name}' not found.")
        return

    # Ищем заметку в record.notes
    for i, note in enumerate(record.notes):
        if note.title == title:
            record.notes.pop(i)
            print(f"Note '{title}' deleted from contact '{name}'.")
            return
    print(f"Note '{title}' not found in contact '{name}'.")


@input_error
def edit_note_by_title(args, book: AddressBook):
    """
    edit note NAME NOTE_TITLE
    Потом попросит ввести новый контент и теги.
    """
    name = args[0]
    title = args[1]

    record = book.find(name)
    if not record:
        print(f"Contact '{name}' not found.")
        return

    # Ищем заметку
    for note in record.notes:
        if note.title == title:
            new_content = input("Enter new content: ").strip()
            new_tags_input = input("Enter new tags (comma separated): ").strip()

            if new_content:
                note.update_content(new_content)
            if new_tags_input:
                note.tags = [tag.strip() for tag in new_tags_input.split(",")]
                note.updated_at = datetime.now()

            print(f"Note '{title}' updated for contact '{name}'.")
            return

    print(f"Note '{title}' not found in contact '{name}'.")


# ------------------------------------------------------------------------
# 7. Точка входа (main)
# ------------------------------------------------------------------------
def main():
    # Отрисовка заголовка/баннера
    draw_header()

    # Загрузка адресной книги (или создание, если не найдена)
    book = AddressBook.load()

    # Создаём PromptSession от prompt_toolkit
    session = PromptSession(
        completer=autocomplete,
        complete_while_typing=True,
        style=style
    )

    print("Welcome to AddressBook & Notebook!")

    while True:
        try:
            user_input = session.prompt(
                [("class:prompt", ">>> ")],
                bottom_toolbar=bottom_toolbar
            )
        except KeyboardInterrupt:
            print("\nCtrl+C pressed. Exiting.")
            break

        # Парсим ввод пользователя (двухсловная команда + аргументы)
        if not (parsed_user_input := parse_input(user_input)):
            continue

        command, *args = parsed_user_input

        match command:
            case "exit" | "quit":
                break

            case "hello":
                print("How can I help you?")

            # --- Контакты
            case "add contact":
                add_contact(args, book)

            case "add email":
                add_email(args, book)

            case "all contacts":
                show_all(book)

            case "add birthday":
                add_birthday(args, book)

            case "set address":
                set_address(args, book)

            case "show birthday":
                if message := show_birthday(args, book):
                    print(message)

            case "show birthdays":
                if message := show_birthdays_next_week(book):
                    print(message)

            case "change phone":
                change_phone(args, book)

            case "change email":
                change_email(args, book)

            case "show phone":
                show_phone(args, book)

            # --- Заметки (теперь внутри контактов)
            case "add note":
                add_note(args, book)

            case "show notes":
                show_notes(args, book)

            case "search notes":
                search_notes_by_tag(args, book)

            case "delete note":
                delete_note_by_title(args, book)

            case "edit note":
                edit_note_by_title(args, book)

            case _:
                print("Invalid command.")

    # Сохраняем адресную книгу перед выходом
    book.save()
    print("📁 Address book saved. Bye!")


if __name__ == "__main__":
    main()
    