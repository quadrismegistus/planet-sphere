from ..imports import *


def merge_dicts(*ld):
    od = {}
    for d in ld:
        for k in d:
            if not k in od or d[k]:
                od[k] = d[k]
    return od


def first(l, default=None):
    for x in l:
        return x
    return default



def wrap_text(text, width=WRAP_WIDTH, linebreak='\n'):
    """
    Wraps a long string into lines with a maximum of 'width' characters per line.
    Allows using either '\n' or '<br>' as linebreak.

    Args:
    text (str): The long string to wrap.
    width (int): The maximum number of characters per line.
    linebreak (str, optional): The line break character. Defaults to '\n'.

    Returns:
    str: The wrapped text.
    """
    import textwrap
    wrapper = textwrap.TextWrapper(
        width=width, 
        break_long_words=False, 
        replace_whitespace=False
    )
    wrapped_lines = wrapper.wrap(text)
    return linebreak.join(wrapped_lines)

def wrap_html(text, width=WRAP_WIDTH):
    return wrap_text(text, width=width, linebreak='<br>')

def trunc(x,n=100):
    n-=3
    return x[:n]+'...' if len(x)>n else x


def translate_range(value, original_range, new_range):
    (x, y) = original_range
    (x2, y2) = new_range

    # Translate the value
    translated_value = (value - x) / (y - x) * (y2 - x2) + x2

    return translated_value