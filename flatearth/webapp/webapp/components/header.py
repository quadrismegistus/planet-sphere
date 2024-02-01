"""Sidebar component for the app."""

from ..imports import *
from .iconlinks import *

def header() -> rx.Component:
    """
    Header.

    Returns:
        The sidebar header component.
    """
    
    sitename = rx.heading(
        'flat earth', 
        font_family='Courier', 
        font_weight='normal',
        font_size='1.75rem',
        padding_x='1rem',
        letter_spacing='.1em',
        padding_y=0,
        color=ColorState.text_color
    )
    
    darkmode_btn = icon_link('darkmode',on_click=MapState.toggle_dark_mode)
    user_btn = icon_link('account-avatar-head',href='/account')
    map_btn = icon_link('map-location-pin', href='/')

    return rx.box(
        rx.hstack(
            sitename,
            rx.spacer(),
            map_btn,
            user_btn,
            darkmode_btn
        ),
        width="100%",
        padding_y=".5rem",
        z_index=100,
    )
