"""The dashboard page."""
from ..imports import *


class LoginModalState(rx.State):
    is_open: bool = False

    def toggle_is_open(self):
        self.is_open = not self.is_open

class FormStateUsername(rx.State):
    username: str = ''

    @rx.var
    def is_error(self) -> bool:
        return self.username and len(self.username)<MIN_USERNAME_LEN


def login_modal() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """    

    content_do_login = rx.modal_body(
        rx.form(
            rx.vstack(
                rx.hstack(
                    rx.form_label('username', html_for='username'),
                    rx.form_control(
                        rx.input(
                            default_value=UserState.username,
                            name='username',
                            on_blur=FormStateUsername.set_username,
                        ),
                        rx.cond(
                            FormStateUsername.is_error,
                            rx.form_error_message(
                                f'Name should be {MIN_USERNAME_LEN} or more characters'
                            )
                        ),
                        is_invalid=FormStateUsername.is_error,
                        is_required=True
                    ),
                ),
                rx.hstack(
                    rx.form_label('password', html_for='password'),
                    rx.input(
                        default_value='',
                        name='password',
                        type_='password'
                    )
                ),
                rx.button("submit", type_="submit"),
            ),
            on_mount=UserState.init,
            on_submit=UserState.handle_login
        )
    )

    content_logged_in = rx.modal_body(
        rx.vstack(
            rx.text(f'You are logged in as {UserState.username}.'),
            rx.button('Logout', on_click=UserState.handle_logout)
        )
    )

    return rx.box(
        rx.modal(
            rx.modal_overlay(
                rx.modal_content(
                    rx.modal_header("login/register"),
                    rx.cond(UserState.logged_in, content_logged_in, content_do_login),
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


class LocationModalState(rx.State):
    is_open: bool = False
    def toggle_is_open(self):
        self.is_open = not self.is_open


def location_modal() -> rx.Component:
    return rx.box(
        rx.modal(
            rx.modal_overlay(
                rx.modal_content(
                    rx.modal_header("location"),
                    rx.modal_body(
                        rx.text(f'You are currently located at {MapState.placename}.'),
                        rx.code_block(
                            MapState.place_json
                        )
                    ),
                ),
            ),
            is_open=LocationModalState.is_open,
            close_on_esc=True,
            close_on_overlay_click=True,
            return_focus_on_close=True,
            auto_focus=True,
            block_scroll_on_mount=False,
            on_close=LocationModalState.toggle_is_open
        ),
    )

