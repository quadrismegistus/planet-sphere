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
        rx.link('flatearth',href='/'), 
        font_family='Courier', 
        font_weight='normal',
        font_size='1.75rem',
        padding_right='1rem',
        letter_spacing='.1em',
        padding_y=0,
        # color=ColorState.text_color
    )
    
    darkmode_btn = icon_link('darkmode',on_click=MapState.toggle_dark_mode)
    user_btn = icon_link('account-avatar-head',href='/account')
    # map_btn = icon_link('map-location-pin', href='/')

    return rx.vstack(
        rx.hstack(
            sitename,
            # map_btn,
            user_btn,
            darkmode_btn,
            # rx.spacer(),
        ),
        width="100%",
        padding_y=".5rem",
        z_index=100,
        height='3rem',
        # border_bottom='1px solid #cdcdcd',
        filter=ColorState.invert_filter,
        backdrop_filter='blur(5px)',
        background_color='rgb(250,250,250)'

    )
