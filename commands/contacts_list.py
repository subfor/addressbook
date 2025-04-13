from app_context import AppContext

def contacts_list(context: AppContext):
    """
    Lists all the contacts in the address book
    """

    records = context.state.book.list_records()

    if len(records) == 0:
        context.interface.draw_info('Contacts not found')
    else:
        context.interface.draw_records(records, 'All contacts')
