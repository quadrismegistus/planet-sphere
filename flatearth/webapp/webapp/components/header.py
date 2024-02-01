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
        (rx.State.router.page.path == "/") & text == "Map")

    return rx.link(
        rx.hstack(
            rx.image(
                src=icon,
                height="3rem",
                padding=".5rem",
                alt=text
            ),
            # rx.text(text, width='fit-content', padding_right='1em', font_family='cursive'),
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
            # box_shadow=styles.box_shadow,
            # width="100%",
            # padding_x="1em",
            # height='5rem'
            ),
        href=url,
        # width="100%",
    )


def header() -> rx.Component:
    """Sidebar header.

    Returns:
        The sidebar header component.
    """
    # Get all the decorated pages and add them to the sidebar.
    from reflex.page import get_decorated_pages

    page_index = ['Map','Feed']

    items = [
        header_item(
            text=page.get("title", page["route"].strip("/").capitalize()),
            icon=page.get("image", "/github.svg"),
            url=page["route"],
        ) for page in sorted(
            get_decorated_pages(), 
            key=lambda page: page_index.index(page.get('title')) if page.get('title') in set(page_index) else len(page_index)
        )
    ]

    return rx.box(
        rx.hstack(
            rx.heading(
                'flat earth', 
                font_family='cursive', 
                font_size='2rem',
                padding_x='1rem',
                color='#555555',
            ),
            rx.spacer(),

            # rx.heading(
            #     State.place_name, 
            #     font_family='cursive', 
            #     font_size='1rem',
            #     padding_x='1rem',
            #     on_mount=State.set_place
            # ),

            *items,
        ),
        width="100%",
        # border_bottom=styles.border,
        # height='5rem',
        padding_y=".5rem",
        z_index=100
    )
