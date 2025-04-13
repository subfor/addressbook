from app_context import AppContext
from ui import get_name, get_phone, get_email, get_birthday, get_address

def contacts_add(context: AppContext):
    name = get_name()

    record = context.state.book.find(name)
    if record:
        context.interface.draw_info(f"Contact for {name} already exists")
        return
    else:
        context.interface.draw_info(f"Creating contact for {name}")

    phone = get_phone()
    email = get_email()
    birthday = get_birthday()
    address = get_address()

    record = context.state.book.add(name)

    if phone:
        record.add_phone(phone)
    if email:
        record.add_email(email)
    if birthday:
        record.set_birthday(birthday)
    if address:
        record.set_address(address)

    context.interface.draw_success("Contact saved")
    context.interface.draw_record(record)
