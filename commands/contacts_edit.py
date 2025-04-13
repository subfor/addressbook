from prompt_toolkit.completion import WordCompleter

from addressbook import Birthday, Email
from app_context import AppContext
from ui import get_name, get_phone, get_address, get_birthday, get_email

edit_sections = ['phones', 'emails', 'address', 'birthday']

def contacts_edit(context: AppContext):
    name_completer = WordCompleter([name for name in context.state.book.keys()])

    name = get_name(completer=name_completer)

    record = context.state.book.find(name)
    if record is None:
        context.interface.draw_failure(f"Contact for {name} not found")
        return

    context.interface.draw_success(f"Found contact for {name}")
    context.interface.draw_record(record)

    focus = context.interface.prompt_select('What do you want to edit',
                                            edit_sections)

    match focus:
        case 'phones':
            phone_input = get_phone(label='Enter a new or existing phone number',
                                    completer=WordCompleter([phone.value for phone in record.phones]))

            exists = len([phone for phone in record.phones if phone.value == phone_input]) > 0

            if exists:
                print(f"Contact already has this phone")

                should_delete = context.interface.prompt_confirm("Do you want to delete this phone from this contact")

                if should_delete:
                    record.remove_phone(phone_input)

                    print("✅Phone deleted from contact.")
            else:
                print(f"Contact does not have this phone")

                should_add = context.interface.prompt_confirm("Do you want to add this phone to this contact")

                if should_add:
                    record.add_phone(phone_input)

                    print("✅Phone added to contact.")
        case 'emails':
            email_input = get_email(label='Enter a new or existing email',
                                    completer=WordCompleter([email.value for email in record.emails]),
                                    live_validator=Email.is_email_valid)

            exists = len([email for email in record.emails if email.value == email_input]) > 0

            if exists:
                print(f"Contact already has this email")

                should_delete = context.interface.prompt_confirm("Do you want to delete this email from this contact")

                if should_delete:
                    record.remove_email(email_input)

                    print("✅Email deleted from contact.")
            else:
                print(f"Contact does not have this phone")

                should_delete = context.interface.prompt_confirm("Do you want to add this email to this contact")

                if should_delete:
                    record.add_email(email_input)

                    print("✅Email added to contact.")
        case 'address':
            address = get_address(label='Enter new address (leave blank to unset)')

            record.set_address(address)
        case 'birthday':
            validator = lambda value: True if value == '' else Birthday.validate_date(value)

            birthday = get_birthday(label="Enter new birthday (leave blank to unset)",
                                    live_validator=validator)

            record.set_birthday(birthday)

    context.interface.draw_success("Contact updated")
    context.interface.draw_record(record)
