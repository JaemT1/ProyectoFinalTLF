import re

def validar_regex(regex):
    """Valida si la expresión regular es correcta."""
    try:
        re.compile(regex)
        return True
    except re.error:
        return False