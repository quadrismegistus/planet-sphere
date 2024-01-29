"""Sidebar component for the app."""

from ..imports import *


def header_item(text: str, icon: str, url: str) -> rx.Component:
    """Sidebar item.

    Args:
        text: The text of the item.
        icon: The icon of the item.
        url: The URL of the item.

    Returns:
        rx.Component: The sidebar item component.
    """
    # Whether the item is active.
    active = (rx.State.router.page.path == f"/{text.lower()}") | (
        (rx.State.router.page.path == "/") & text == "Home")

    return rx.link(
        rx.hstack(
            # rx.image(
            #     src=icon,
            #     height="2.5em",
            #     padding="0.5em",
            # ),
            rx.text(text, width='100%', text_align='center'),
            bg=rx.cond(
                active,
                styles.accent_color,
                "transparent",
            ),
            color=rx.cond(
                active,
                styles.accent_text_color,
                styles.text_color,
            ),
            border_radius=styles.border_radius,
            box_shadow=styles.box_shadow,
            # width="100%",
            # padding_x="1em",
            height='5rem'),
        href=url,
        width="100%",
    )


def header() -> rx.Component:
    """Sidebar header.

    Returns:
        The sidebar header component.
    """
    # Get all the decorated pages and add them to the sidebar.
    from reflex.page import get_decorated_pages

    items = [
        header_item(
            text=page.get("title", page["route"].strip("/").capitalize()),
            icon=page.get("image", "/github.svg"),
            url=page["route"],
        ) for page in get_decorated_pages()
    ]

    return rx.box(
        rx.hstack(
            rx.box(rx.heading('reverse earth', size='lg'),
                   width='100em',
                   text_align='center'),
            *items,
            rx.spacer(),
        ),
        width="100%",
        border_bottom=styles.border,
        # padding="1em"
    )
