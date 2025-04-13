from prompt_toolkit.completion import NestedCompleter, WordCompleter

from .prompt_helper import prompt_helper, style

# commands_completer = NestedCompleter.from_nested_dict({
#     'add contact': None,
#     'add note': None,
#     'add': {
#         'contact',
#         'note',
#     },
#     'delete contact': None,
#     'delete note': None,
#     'delete': {
#         'contact',
#         'note',
#     },
#     'edit contact': None,
#     'edit note': None,
#     'edit': {
#         'contact',
#         'note',
#     },
#     'exit': None,
#     'hello': None,
#     'list contacts': None,
#     'list notes': None,
#     'list': {
#         'contacts',
#         'notes',
#     },
#     'show birthdays': None,
#     'show contact': None,
#     'show note': None,
#     'show': {
#         'birthdays'
#         'contact',
#         'note',
#     },
#     'search contacts': None,
#     'search notes': None,
#     'search': {
#         'contacts',
#         'notes',
#     },
#     'quit': None,
# })

class CommandCompleter(WordCompleter):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip().lower()
        if " " in text:
            return
        yield from super().get_completions(document, complete_event)

commands_completer = CommandCompleter([name for name in {
    'add contact',
    'delete contact',
    'edit contact',
    'list contacts',
    'search contacts',
    'show contact',

    'add note',
    'edit note',
    'delete note',
    'list notes',
    'search notes',
    'show notes',

    'show birthdays',
}])

bottom_toolbar_default = [("class:bottom-toolbar",
                           " 🧠 Tab — autocomplete | Ctrl+C or exit/quit — exit")]

commands_session = prompt_helper(message=[("class:prompt", ">>> ")],
                                 completer=commands_completer,
                                 complete_while_typing=True,
                                 bottom_toolbar=bottom_toolbar_default)

def prompt_command():
    return commands_session.prompt()
