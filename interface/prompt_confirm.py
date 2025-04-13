from .prompt_select import prompt_select

def prompt_confirm(message: str):
    return prompt_select(message, ['yes', 'no'])
