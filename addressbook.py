import pickle
import re
from collections import UserDict
from datetime import datetime, timedelta
from email_validator import EmailNotValidError, validate_email
from typing import Optional, List  # Импортируем Optional и List

# Custom exceptions
class NameFormatError(Exception):
    pass

class PhoneFormatError(Exception):
    pass

class DateFormatError(Exception):
    pass

class EmailFormatError(Exception):
    pass

class AddressFormatError(Exception):
    pass

# Base class for fields (Name, Phone, Birthday, Email, Address)
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Name class for handling name formatting
class Name(Field):
    def __init__(self, name: str):
        if name:
            super().__init__(name.strip().capitalize())
        else:
            raise NameFormatError("[!] Name cannot be blank")

# Phone class with validation for 10-digit phone numbers
class Phone(Field):
    def __init__(self, phone: str):
        if self.__validate_phone(phone):
            super().__init__(phone)
        else:
            raise PhoneFormatError(f"[!] Wrong phone format: {phone}")

    def __validate_phone(self, value: str) -> bool:
        pattern = re.compile(r"^\d{10}$")
        return bool(pattern.match(value))

# Birthday class with validation for date format
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
        return f"Birthday: {self.value.strftime('%d.%m.%Y')}"

# Email class with validation
class Email(Field):
    def __init__(self, value):
        try:
            email_info = validate_email(value, check_deliverability=False)
            super().__init__(email_info.normalized)
        except EmailNotValidError as e:
            raise EmailFormatError(f"Invalid email format: {e.args[0]}") from e

    def __str__(self):
        return f"Email: {self.value}"

# Address class for storing contact address
class Address(Field):
    def __init__(self, value: str):
        if value:
            super().__init__(value.strip())  # Просто убираем лишние пробелы
        else:
            raise AddressFormatError("[!] Address cannot be blank.")

# Comment class for handling comments related to contacts
class Comment:
    def __init__(self, content: str):
        self.content = content
        self.created_at = datetime.now()

    def __str__(self):
        return f"[{self.created_at.strftime('%d.%m.%Y %H:%M:%S')}] {self.content}"

# ContactNote class for handling notes associated with contacts
class ContactNote:
    def __init__(self, title: str, content: str, tags: Optional[List[str]] = None):
        self.title = title
        self.content = content
        self.tags = tags if tags else []  # Initialize as empty list if no tags provided
        self.created_at = datetime.now()  # Creation date
        self.updated_at = self.created_at  # Last update date

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
        return (
            f"Note: {self.title} - {self.content}\n"
            f"Created At: {self.created_at.strftime('%d.%m.%Y %H:%M:%S')}\n"
            f"Updated At: {self.updated_at.strftime('%d.%m.%Y %H:%M:%S')}\n"
        )

# Record class for handling a contact's details
class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.emails = []
        self.address = None  # Добавляем атрибут для хранения адреса
        self.comments = []  # Список для хранения комментариев
        
    def set_address(self, address: str) -> None:
        self.address = Address(address)  # Создаём объект Address и присваиваем его атрибуту

    def add_note(self, note: ContactNote) -> None:
        self.comments.append(note)  # Добавляем заметку в контакт

    def add_phone(self, new_phone: str) -> bool:
        if self.__get_phone_index(new_phone) is None:
            self.phones.append(Phone(new_phone))
            return True
        return False

    def add_email(self, new_email: str) -> bool:
        if self.__get_email_index(new_email) is None:
            self.emails.append(Email(new_email))
            return True
        return False

    def add_birthday(self, b_date: str) -> None:
        self.birthday = Birthday(b_date)

    def add_comment(self, comment: Comment) -> None:
        """Add a comment to the contact."""
        self.comments.append(comment)

    def get_info(self) -> list:
        phones = "; ".join(p.value for p in self.phones) if self.phones else "-"
        birthday = (
            self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "-"
        )
        emails = ", ".join(e.value for e in self.emails) if self.emails else "-"
        address = self.address.value if self.address else "-"
        comments = "; ".join(comment.content for comment in self.comments) if self.comments else "-"
        return [self.name.value, phones, birthday, emails, address, comments]

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

    @staticmethod
    def validate_name(name: str):
        """Validate name format."""
        if not name.strip():
            raise NameFormatError("[!] Name cannot be blank.")
        return True

    @staticmethod
    def validate_phone(phone: str):
        """Validate phone number format."""
        Phone(phone)
        return True

    @staticmethod
    def validate_email(email: str):
        """Validate email format."""
        Email(email)
        return True

    @staticmethod
    def validate_birthday(b_day: str):
        """Validate birthday format."""
        Birthday(b_day)
        return True

    @staticmethod
    def validate_address(address: str):
        """Validate address format."""
        Address(address)
        return True

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = (
            self.birthday.value.strftime("%d.%m.%Y")
            if self.birthday else "not set"
        )
        emails = ", ".join(e.value for e in self.emails)
        comments = "; ".join(comment.content for comment in self.comments)
        address = self.address.value if self.address else "not set"
        return (
            f"Contact name: {self.name.value}, "
            f"Phones: {phones}, "
            f"Birthday: {birthday}, "
            f"Emails: {emails}, "
            f"Address: {address}, "
            f"Comments: {comments if self.comments else 'No comments'}"
        )

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.notebook = []  # Список для хранения заметок

    # Метод для добавления заметки
    def add_note_to_notebook(self, note: ContactNote) -> None:
        self.notebook.append(note)

    def get_all_notes(self):
        return self.notebook

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name.strip().capitalize())

    def get_upcoming_birthday(self) -> list:
        today_date = datetime.today().date()
        congrat_list = []
        for record in self.data.values():
            if record.birthday:
                birthday_data_obj = record.birthday.value
                birthday_this_year = birthday_data_obj.replace(year=today_date.year)
                if birthday_this_year < today_date:
                    birthday_this_year = birthday_this_year.replace(year=today_date.year + 1)
                days_until_birthday = (birthday_this_year - today_date).days
                if 0 <= days_until_birthday < 7:
                    congrat_list.append({
                        "name": record.name.value,
                        "congratulation_date": birthday_this_year.strftime("%d.%m.%Y"),
                    })
        return congrat_list

    def get_all_records(self) -> list:
        return [record.get_info() for record in self.data.values()]

    def save(self, filename="addressbook.pkl") -> None:
        with open(filename, "wb") as f:
            pickle.dump(self.data, f)  # Сохраняем данные книги

    @staticmethod
    def load(filename="addressbook.pkl") -> "AddressBook":
        try:
            with open(filename, "rb") as f:
                data = pickle.load(f)
                book = AddressBook()
                book.data = data  # Загружаем данные в книгу
                return book
        except (FileNotFoundError, EOFError) as e:
            print(f"⚠️ Error loading address book: {e}")
            return AddressBook()  # Возвращаем пустую книгу в случае ошибки

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def __str__(self) -> str:
        return "\n".join(str(record) for record in self.data.values())