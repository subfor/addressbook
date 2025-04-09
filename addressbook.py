import pickle
import re
from collections import UserDict
from datetime import datetime, timedelta
from typing import Optional, List
from email_validator import EmailNotValidError, validate_email

# Ваши классы для работы с контактами

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
        # Исправили кавычки внутри f-строки
        return f"Birthday: {self.value.strftime('%d.%m.%Y')}"


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


class Note:
    def __init__(self, title: str, content: str, tags: Optional[List[str]] = None):
        self.title = title
        self.content = content
        self.tags = tags if tags else []  # Если теги не переданы, инициализируем пустым списком
        self.created_at = datetime.now()  # Дата создания
        self.updated_at = self.created_at  # Дата последнего обновления

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


class Notebook:
    def __init__(self):
        self.notes = []

    def add_note(self, note: Note):
        self.notes.append(note)

    def delete_note(self, title: str) -> bool:
        for i, note in enumerate(self.notes):
            if note.title == title:
                self.notes.pop(i)
                return True
        return False

    def search_by_tag(self, tag: str) -> List[Note]:
        return [note for note in self.notes if tag in note.tags]

    def display_all_notes(self):
        if not self.notes:
            print("No notes available.")
        else:
            for note in self.notes:
                print(note.display())
                print("-" * 20)

    def find_by_title(self, title: str) -> Optional[Note]:
        for note in self.notes:
            if note.title == title:
                return note
        return None


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.emails = []
        self.address = None
        self.notes = []  # Поле для заметок

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

    def add_note(self, note: Note) -> None:
        """Добавляет заметку к контакту."""
        self.notes.append(note)

    def get_info(self) -> list:
        phones = "; ".join(p.value for p in self.phones) if self.phones else "-"
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "-"
        emails = ", ".join(e.value for e in self.emails) if self.emails else "-"
        address = self.address.value if self.address else "-"
        notes = "; ".join(note.title for note in self.notes) if self.notes else "-"
        return [self.name.value, phones, birthday, emails, address, notes]

    def __get_phone_index(self, phone_number: str) -> Optional[int]:
        for index, phone in enumerate(self.phones):
            if phone.value == phone_number:
                return index
        return None

    def __get_email_index(self, email_str: str) -> Optional[int]:
        for index, email in enumerate(self.emails):
            if email.value == email_str:
                return index
        return None

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "not set"
        emails = ", ".join(e.value for e in self.emails) if self.emails else "not set"
        address = self.address.value if self.address else "not set"
        notes = "; ".join(note.title for note in self.notes) if self.notes else "No notes"
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones}, "
            f"Birthday: {birthday}, "
            f"Emails: {emails}, "
            f"Address: {address}, "
            f"Notes: {notes}"
        )


class AddressBook(UserDict):

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
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

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday_data_obj = record.birthday.value
            birthday_this_year = birthday_data_obj.replace(year=today_date.year)

            if birthday_this_year < today_date:
                birthday_this_year = birthday_this_year.replace(year=today_date.year + 1)

            days_until_birthday = (birthday_this_year - today_date).days

            if 0 <= days_until_birthday < 7:
                congrats_date = birthday_this_year + timedelta(
                    days=self.__check_weekend(birthday_this_year)
                )
                congrat_list.append({
                    "name": record.name.value,
                    "congratulation_date": congrats_date.strftime("%d.%m.%Y"),
                })

        return congrat_list

    def get_all_records(self) -> list:
        # Возвращаем список объектов Record с полными данными
        return list(self.data.values())

    def __check_weekend(self, date: datetime.date) -> int:
        # Python 3.10+ — match-case
        # При необходимости заменить на if-elif-else для более старых версий
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
    