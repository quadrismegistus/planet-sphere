"""The other page."""
from webapp.templates import template

import reflex as rx


@template(route="/other", title="Other")
def other() -> rx.Component:
    """The other page.

    Returns:
        The UI for the other page.
    """
    return rx.vstack(
        rx.heading("Other", font_size="3em"),
        rx.text("Welcome to Reflex!"),
        rx.text(
            "You can edit this page in ",
            rx.code("{your_app}/pages/other.py"),
        ),
    )
