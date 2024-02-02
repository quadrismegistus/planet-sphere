"""The dashboard page."""
from ..imports import *


class LoginModalState(rx.State):
    is_open: bool = False

    def toggle_is_open(self):
        self.is_open = not self.is_open


def login_modal() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """    

    content_do_login = rx.modal_body(
        rx.form(
            rx.hstack(
                rx.form_label('User', html_for='username'),
                rx.input(
                    default_value=UserState.username,
                    name='username',
                )
            ),
            rx.hstack(
                rx.form_label('Password', html_for='password'),
                rx.input(
                    default_value='',
                    name='password',
                    type_='password'
                )
            ),
            rx.button("Login", type_="submit"),
            on_mount=UserState.init,
            on_submit=UserState.handle_login
        )
    )

    content_logged_in = rx.modal_body(
        f'You are logged in as {UserState.username}.'
    )

    return rx.box(
        rx.modal(
            rx.modal_overlay(
                rx.modal_content(
                    rx.modal_header("User"),
                    rx.cond(UserState.username, content_logged_in, content_do_login),
                    rx.modal_footer(
                        # rx.button(
                        #     "Close", 
                        #     on_click=LoginModalState.toggle_is_open
                        # )
                    ),
                )
            ),
            is_open=LoginModalState.is_open,
            close_on_esc=True,
            close_on_overlay_click=True,
            return_focus_on_close=True,
            auto_focus=True,
            block_scroll_on_mount=False,
            on_close=LoginModalState.toggle_is_open
        ),
    )

