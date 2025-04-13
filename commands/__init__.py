from collections.abc import Callable

from app_context import AppContext

from .birthdays_show import birthdays_show

from .contacts_add import contacts_add
from .contacts_delete import contacts_delete
from .contacts_edit import contacts_edit
from .contacts_list import contacts_list
from .contacts_search import contacts_search
from .contacts_show import contacts_show
from .notes_add import notes_add
from .notes_delete import notes_delete
from .notes_edit import notes_edit
from .notes_list import notes_list
from .notes_search import notes_search
from .notes_show import notes_show

COMMANDS: dict[str, Callable[[AppContext], None]] = {
    'add contact': contacts_add,
    'delete contact': contacts_delete,
    'edit contact': contacts_edit,
    'list contacts': contacts_list,
    'search contacts': contacts_search,
    'show contact': contacts_show,

    'add note': notes_add,
    'edit note': notes_edit,
    'delete note': notes_delete,
    'list notes': notes_list,
    'search notes': notes_search,
    'show notes': notes_show,

    'show birthdays': birthdays_show,
}
