import pickle
import re
from collections import UserDict
from datetime import datetime, timedelta
from typing import List, Optional # Class Note
from email_validator import EmailNotValidError, validate_email


class PhoneFormatError(Exception):
    pass


class DateFormatError(Exception):
    pass


class EmailFormatError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name: str):
        super().__init__(name.strip().capitalize())


class Phone(Field):
    def __init__(self, phone: str):
        if self.__validate_phone(phone):
            super().__init__(phone)
        else:
            raise PhoneFormatError(f"wrong phone format {phone}")

    def __validate_phone(self, value: str) -> bool:
        pattern = re.compile(r"^\d{10}$")
        return bool(pattern.match(value))


class Birthday(Field):
    def __init__(self, value):
        if self.__validate_date(value):
            b_date = datetime.strptime(value.strip(), "%d.%m.%Y").date()
            super().__init__(b_date)
        else:
            raise DateFormatError("Invalid date format. Use DD.MM.YYYY")

    def __validate_date(self, value):
        pattern = re.compile(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.\d{4}$")
        return bool(pattern.match(value.strip()))

    def __str__(self):
        return f"Birthday: {self.value.strftime("%d.%m.%Y")}"


class Email(Field):
    def __init__(self, value):
        try:
            email_info = validate_email(value, check_deliverability=False)

            super().__init__(email_info.normalized)
        except EmailNotValidError as e:
            raise EmailFormatError(f"Invalid email format: {e.args[0]}") from e

    def __str__(self):
        return f"Email: {self.value}"


class Address(Field):
    def __init__(self, value: str):
        super().__init__(value.strip())


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.emails = []
        self.address = None

    def add_phone(self, new_phone: str) -> bool:
        if self.__get_phone_index(new_phone) is None:
            self.phones.append(Phone(new_phone))
            return True
        return False

    def remove_phone(self, phone_number: str) -> bool:
        index = self.__get_phone_index(phone_number)
        if index is not None:
            self.phones.pop(index)
            return True
        return False

    def edit_phone(self, old_number: str, new_number: str) -> bool:
        index = self.__get_phone_index(old_number)
        if index is not None:
            self.phones[index] = Phone(new_number)
            return True
        return False

    def find_phone(self, phone_number: str) -> str:
        return phone_number if self.__get_phone_index(phone_number) else ""

    def add_email(self, new_email: str) -> bool:
        if self.__get_email_index(new_email) is None:
            self.emails.append(Email(new_email))
            return True
        return False

    def remove_email(self, email_address: str) -> bool:
        index = self.__get_email_index(email_address)
        if index is not None:
            self.emails.pop(index)
            return True
        return False

    def edit_email(self, old_email: str, new_email: str) -> bool:
        index = self.__get_email_index(old_email)
        if index is not None:
            self.emails[index] = Email(new_email)
            return True
        return False

    def find_email(self, email_address: str) -> str:
        return email_address if self.__get_email_index(email_address) else ""

    def add_birthday(self, b_date: str) -> None:
        self.birthday = Birthday(b_date)

    def set_address(self, address: str) -> None:
        self.address = Address(address)

    def get_info(self) -> list:
        phones = "; ".join(p.value for p in self.phones) if self.phones else "-"
        birthday = (
            self.birthday.value.strftime("%d.%m.%Y")
            if self.birthday is not None
            else "-"
        )
        emails = ", ".join(e.value for e in self.emails) if self.emails else "-"
        address = self.address.value if self.address else "-"
        return [self.name.value, phones, birthday, emails, address]

    def __get_phone_index(self, phone_number: str) -> int | None:
        for index, phone in enumerate(self.phones):
            if phone.value == phone_number:
                return index
        return None

    def __get_email_index(self, email_str: str) -> int | None:
        for index, email in enumerate(self.emails):
            if email.value == email_str:
                return index
        return None

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = (
            self.birthday.value.strftime("%d.%m.%Y")
            if self.birthday is not None
            else "not set"
        )
        emails = ", ".join(e.value for e in self.emails)
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones}, "
            f"Birthday: {birthday}, "
            f"Emails: {emails if self.emails else "not set"}, "
            f"Address: {self.address if self.address else "not set"}"
        )


class AddressBook(UserDict):

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name.strip().capitalize())

    def delete(self, name: str) -> bool:
        try:
            del self.data[name.strip().capitalize()]
            return True
        except KeyError:
            return False

    def get_upcoming_birthday(self) -> list:
        today_date = datetime.today().date()
        congrat_list = []
        congrats_date = None

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday_data_obj = record.birthday.value
            birthday_this_year = birthday_data_obj.replace(year=today_date.year)

            if birthday_this_year < today_date:
                birthday_this_year = birthday_this_year.replace(
                    year=today_date.year + 1
                )

            days_until_birthday = (birthday_this_year - today_date).days

            if 0 <= days_until_birthday < 7:
                congrats_date = birthday_this_year + timedelta(
                    days=self.__check_weekend(birthday_this_year)
                )

                congrat_list.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": congrats_date.strftime("%d.%m.%Y"),
                    }
                )

        return congrat_list

    def get_all_records(self) -> list:
        return [record.get_info() for record in self.data.values()]

    def __check_weekend(self, date: datetime.date) -> int:
        match date.isoweekday():
            case 6:
                return 2
            case 7:
                return 1
            case _:
                return 0

    def save(self, filename="addressbook.pkl") -> None:
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename: str = "addressbook.pkl") -> "AddressBook":
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            print("⚠️ Address Book not found, created new.")
            return AddressBook()

    def __str__(self) -> str:
        return "\n".join(str(record) for record in self.data.values())
class Note:
    def __init__(self, title: str, content: str, tags: Optional[List[str]] = None):
        self.title = title
        self.content = content
        self.tags = tags if tags else []  # Якщо теги не передані, ініціалізуємо порожнім списком.
        self.created_at = datetime.now()  # Дата створення
        self.updated_at = self.created_at  # Дата останнього оновлення

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
        Метод для відображення нотатки.
        """
        return (
            f"Title: {self.title}\n"
            f"Content: {self.content}\n"
            f"Tags: {', '.join(self.tags) if self.tags else 'No tags'}\n"
            f"Created At: {self.created_at.strftime('%d.%m.%Y %H:%M:%S')}\n"
            f"Updated At: {self.updated_at.strftime('%d.%m.%Y %H:%M:%S')}\n"
        )
from functools import wraps

from prompt_toolkit import PromptSession

from addressbook import (AddressBook, DateFormatError, EmailFormatError,
                         PhoneFormatError, Record)
from ui import (autocomplete, bottom_toolbar, draw_contacts, draw_header,
                draw_record, style)


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, IndexError):
            match func.__name__:
                case "parse_input":
                    print("Command can not be blank")
                case "add_contact":
                    print("Usage: add contact NAME PHONE_NUMBER")
                case "add_email":
                    print("Usage: add email NAME EMAIL")
                case "change_phone":
                    print("Usage: change NAME OLD_NUMBER NEW_NUMBER")
                case "change_email":
                    print("Usage: change email NAME OLD_EMAIL NEW_EMAIL")
                case "show_phone":
                    print("Usage: phone NAME")
                case "add_birthday":
                    print("Usage: add birthday NAME DATE(DD.MM.YYYY)")
                case "show_birthday":
                    print("Usage: show birthday NAME")
                case "set_address":
                    print("Usage: set address NAME ADDRESS")
                case _:
                    print(f"error in {func.__name__}")
        except PhoneFormatError:
            print("Wrong phone format.")
        except EmailFormatError:
            print("Wrong email format.")
        except DateFormatError:
            print("Invalid date format. Use DD.MM.YYYY")

    return inner


@input_error
def parse_input(user_input):
    parts = user_input.strip().lower().split()
    if not parts:
        return None
    if len(parts) >= 2:
        command = f"{parts[0]} {parts[1]}"
        args = parts[2:]
    else:
        command = parts[0]
        args = []
    return command, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    existing_record = book.find(name)

    if existing_record:
        if existing_record.add_phone(phone):
            print("Phone number added to existing contact.")
            draw_record(existing_record.get_info())
        else:
            return "Phone number already exists."
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        print("New contact added.")
        draw_record(record.get_info())


@input_error
def change_phone(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        print("Contact does not exist.")
    else:
        if record.edit_phone(old_phone, new_phone):
            print("Contact updated.")
            draw_record(record.get_info())
        else:
            print("Old phone number not found")


@input_error
def change_email(args, book: AddressBook):
    name, old_email, new_email = args
    record = book.find(name)
    if record is None:
        print("Contact does not exist.")
    else:
        if record.edit_email(old_email, new_email):
            print("Contact updated.")
            draw_record(record.get_info())
        else:
            print("Old email number not found")


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        draw_record(record.get_info())
    else:
        print("Contact not found")


@input_error
def add_email(args, book: AddressBook):
    name, email = args
    existing_record = book.find(name)

    if existing_record:
        if existing_record.add_email(email):
            print("Email added to existing contact.")
            draw_record(existing_record.get_info())
        else:
            return "Email already exists."
    else:
        record = Record(name)
        record.add_email(email)
        book.add_record(record)
        print("New contact added.")
        draw_record(record.get_info())


def show_all(book: AddressBook):
    if not book:
        return "Contacts not found."
    return draw_contacts(contacts=book.get_all_records())


@input_error
def add_birthday(args, book: AddressBook):
    name, b_date = args
    record = book.find(name)
    if record:
        record.add_birthday(b_date)
        draw_record(record.get_info())
    else:
        print("Contact not found")


@input_error
def set_address(args, book: AddressBook):
    name, *address_parts = args
    address = " ".join(address_parts)
    record = book.find(name)
    if record:
        record.set_address(address)
        draw_record(record.get_info())
    else:
        print("Contact not found")


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return str(record.birthday)
        else:
            return "Birthday not set"
    return "Contact not found"


@input_error
def show_birthdays_next_week(book: AddressBook):
    birthdays = book.get_upcoming_birthday()
    if birthdays:
        text = ""
        for person in birthdays:
            text += (
                f"Name: {person['name']}, "
                f"Congratulation date: {person['congratulation_date']}\n"
            )
        return text.strip()
    return "Birthdays not found"


def main():
    draw_header()
    book = AddressBook.load()
    session = PromptSession(
        completer=autocomplete, complete_while_typing=True, style=style
    )
    print("Welcome to AddressBook!")
    while True:
        try:
            user_input = session.prompt(
                [("class:prompt", ">>> ")], bottom_toolbar=bottom_toolbar
            )
        except KeyboardInterrupt:
            print("Ctrl+c")
            break
        if not (parsed_user_input := parse_input(user_input)):
            continue
        command, *args = parsed_user_input

        match command:
            case "exit" | "quit":
                break
            case "hello":
                print("How can I help you?")
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
            case _:
                print("Invalid command.")
    book.save()
    print("📁 Address book saved. Bye!")


if __name__ == "__main__":
    main()
