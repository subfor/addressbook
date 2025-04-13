import pickle
import re
from collections import UserDict
from datetime import datetime, timedelta
from typing import Optional

from email_validator import EmailNotValidError, validate_email

class RangeFormatError(Exception):
    def __init__(self, message):
        self.message = message

class NameFormatError(Exception):
    pass


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
        if name:
            super().__init__(name.strip().capitalize())
        else:
            raise NameFormatError("[!]Name cannot be blank")


class Phone(Field):
    def __init__(self, phone: str):
        if self.validate_phone(phone):
            super().__init__(phone)
        else:
            raise PhoneFormatError(f"[!]Wrong phone format {phone}")

    @staticmethod
    def validate_phone(value: str) -> bool:
        pattern = re.compile(r"^\d{10}$")
        return bool(pattern.match(value))


class Birthday(Field):
    def __init__(self, value):
        if self.validate_date(value):
            b_date = datetime.strptime(value.strip(), "%d.%m.%Y").date()
            super().__init__(b_date)
        else:
            raise DateFormatError("Invalid date format. Use DD.MM.YYYY")

    @staticmethod
    def validate_date(value):
        pattern = re.compile(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.\d{4}$")
        return bool(pattern.match(value.strip()))

    def stringify_date(self):
        return self.value.strftime('%d.%m.%Y')

    def __str__(self):
        return f"Birthday: {self.value.strftime('%d.%m.%Y')}"


class Email(Field):
    def __init__(self, value):
        try:
            email_info = validate_email(value, check_deliverability=False)
            super().__init__(email_info.normalized)
        except EmailNotValidError as e:
            raise EmailFormatError(f"Invalid email format: {e.args[0]}") from e

    @staticmethod
    def is_email_valid(value: str):
        try:
            validate_email(value, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False

    def __str__(self):
        return f"Email: {self.value}"


class Address(Field):
    def __init__(self, value: str):
        super().__init__(value.strip())


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Optional[Birthday] = None
        self.emails: list[Email] = []
        self.address: Optional[Address] = None

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

    def set_birthday(self, b_date: str | None) -> None:
        if b_date is None or b_date == '':
            self.birthday = None
        else:
            self.birthday = Birthday(b_date)

    def set_address(self, address: str | None) -> None:
        self.address = None if address is None or address == "" else Address(address)

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
            f"Emails: {emails if self.emails else 'not set'}, "
            f"Address: {self.address if self.address else 'not set'}"
        )

    @staticmethod
    def validate_range(range_str: str):
        try:
            rang_int = int(range_str)
        except ValueError as e:
            raise RangeFormatError('Range must be a positive integer between 7 and 365') from e
        if rang_int < 7 or rang_int > 365:
            raise RangeFormatError('Range must be a positive integer between 7 and 365')

    @staticmethod
    def validate_name(name: str):
        Name(name)

    @staticmethod
    def validate_phone(phone: str):
        Phone(phone)

    @staticmethod
    def validate_email(email: str):
        Email(email)

    @staticmethod
    def validate_birthday(b_day: str):
        Birthday(b_day)

    def check(self, term: str):
        term = term.strip().lower()

        if term in self.name.value.lower():
            return True
        if len([phone.value for phone in self.phones if term in phone.value]) > 0:
            return True
        if self.birthday and term in self.birthday.value.strftime("%d.%m.%Y"):
            return True
        if len([email.value for email in self.emails if term in email.value.lower()]) > 0:
            return True
        if self.address and term in self.address.value.lower():
            return True
        return False

class AddressBook(UserDict[str, Record]):
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

    def get_upcoming_birthday(self, limit=7) -> list:
        today_date = datetime.today().date()
        congrat_list = []

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

            if 0 <= days_until_birthday < limit:
                congrats_date = birthday_this_year + timedelta(
                    days=self.__check_weekend(birthday_this_year)
                )

                congrat_list.append(
                    {
                        "name": record.name.value,
                        "birthday": record.birthday.value,
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