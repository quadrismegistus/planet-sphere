"""Sidebar component for the app."""

from ..imports import *
from .iconlinks import *
from .account import *

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
        font_size='1.25rem',
        padding_right='1rem',
        letter_spacing='.1em',
        padding_y=0,
        # color=ColorState.text_color
    )
    
    
    user_btn = icon_link(
        'account-avatar-head',
        on_click=LoginModalState.toggle_is_open
    )
    darkmode_btn = icon_link(
        'darkmode',
        on_click=MapState.toggle_dark_mode,
        icon_kwargs=dict(
            margin_left='.2rem'
        )
    )
    post_btn = icon_link(
        'post'
    )
    location_btn = icon_link(
        'location',
        on_click=LocationModalState.toggle_is_open
    )

    return rx.vstack(
        rx.hstack(
            sitename,
            # map_btn,
            user_btn,
            location_btn,
            post_btn,
            darkmode_btn,
            # rx.spacer(),
        ),
        login_modal(),
        location_modal(),
        width="100%",
        padding_y=".5rem",
        z_index=100,
        height='3rem',
        # border_bottom='1px solid #cdcdcd',
        filter=ColorState.invert_filter,
        backdrop_filter='blur(5px)',
        background_color='rgb(255,255,255)',
        # on_mount=ColorState.watch_sys_darkmode
    )
