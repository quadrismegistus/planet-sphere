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

def to_json(x, as_str=True):
    o=orjson.dumps(
        x, 
        option=orjson.OPT_SERIALIZE_NUMPY|orjson.OPT_SERIALIZE_UUID
    )
    return o.decode('utf-8') if as_str else o

def from_json(x):
    return orjson.loads(str(x) if type(x)!=bytes else x)

def to_json64(x):
    x_json_b = to_json(x,as_str=False)
    x_json_b64 = b64encode(x_json_b)
    x_json_b64_str = x_json_b64.decode('utf-8')
    return x_json_b64_str

def from_json64(x_json_b64_str):
    x_json_b64 = x_json_b64_str.encode('utf-8')
    x_json_b = b64decode(x_json_b64)
    x = orjson.loads(x_json_b)
    return x


# Function to interpolate between two colors
def interpolate_color(start_color, end_color, fraction):
    # Ensure the fraction is between 0 and 1
    fraction = max(0, min(1, fraction))
    
    # Interpolate between the RGB values of the start and end colors
    new_color = colour.Color(
        rgb=[
            start_color.rgb[0] + (end_color.rgb[0] - start_color.rgb[0]) * fraction,
            start_color.rgb[1] + (end_color.rgb[1] - start_color.rgb[1]) * fraction,
            start_color.rgb[2] + (end_color.rgb[2] - start_color.rgb[2]) * fraction,
        ]
    )
    return new_color
