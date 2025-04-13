from prompt_toolkit.completion import WordCompleter

from .prompt_helper import prompt_helper

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
    """
    Prompts user to input a text command and returns the response
    """
    return commands_session.prompt()
