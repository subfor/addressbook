from addressbook import AddressBook

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
