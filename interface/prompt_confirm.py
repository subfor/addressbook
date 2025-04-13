from .prompt_select import prompt_select

def prompt_confirm(message: str):
    """
    Prompts user to confirm an action by enter 'yes' or 'no' and returns the response
    """
    result = prompt_select(message, ['yes', 'no'])

    return result == 'yes'
