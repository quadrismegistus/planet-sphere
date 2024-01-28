"""The home page of the app."""
from ..imports import *
from round_earth import geocode



@template(route="/", title="Home", image="/github.svg")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    # with open("README.md", encoding="utf-8") as readme:
        # content = readme.read()
    
    content = f"""
```
{State.place_json}
```
"""

    return rx.markdown(
        content, 
        component_map=styles.markdown_style,
        on_mount=State.set_place
    )
