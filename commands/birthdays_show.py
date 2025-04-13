from app_context import AppContext

from ui import get_birthday_range

def birthdays_show(context: AppContext):
    range_int = int(get_birthday_range())

    birthdays = context.state.book.get_upcoming_birthday(limit=range_int)

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
