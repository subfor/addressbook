from app_context import AppContext

from ui import get_term

def contacts_search(context: AppContext):
    """
    Searches through contacts for matches on name, phones, emails, birthday and address
    """
    term = get_term()

    if term is None:
        return

    records = [record for record in context.state.book.values() if record.check(term)]

    context.interface.draw_info(f"Found {len(records)} contacts")

    if len(records) == 0:
        return

    context.interface.draw_records(records)
