from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator

from .prompt_helper import prompt_helper

def prompt_select(message: str, options: list[str]):
    session = prompt_helper(message=message,
                            completer=WordCompleter(options),
                            complete_while_typing=True,
                            validator=Validator.from_callable(lambda i: i in options),
                            validate_while_typing=True)

    return session.prompt()
