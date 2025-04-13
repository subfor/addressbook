from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, DummyCompleter
from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import Validator, DummyValidator

style = Style.from_dict(
    {
        "prompt": "bold #00ffcc",
        "": "#ffffff",
        "completion-menu.completion": "bg:#1f1f1f #aaaaaa",
        "completion-menu.completion.current": "bg:#00afff #ffffff",
        "scrollbar.background": "bg:#3a3a3a",
        "scrollbar.button": "bg:#5f5f5f",
        "bottom-toolbar": "italic #888888",
    }
)

def prompt_helper(message: AnyFormattedText = None,
                  *,
                  complete_while_typing: bool = True,
                  validate_while_typing: bool = True,
                  enable_history_search: bool = False,
                  search_ignore_case: bool = True,
                  validator: Validator | None = None,
                  completer: Completer | None = None,
                  bottom_toolbar: AnyFormattedText = None):
    return PromptSession(message=message,
                         style=style,
                         complete_while_typing=complete_while_typing,
                         validate_while_typing=validate_while_typing,
                         enable_history_search=enable_history_search,
                         search_ignore_case=search_ignore_case,
                         validator=validator,
                         completer=completer,
                         bottom_toolbar=bottom_toolbar)
