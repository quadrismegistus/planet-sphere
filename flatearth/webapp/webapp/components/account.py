"""The dashboard page."""
from ..imports import *



class FormStateUsername(rx.State):
    username: str = ''

    @rx.var
    def is_error(self) -> bool:
        return self.username and len(self.username)<MIN_USERNAME_LEN


def login_modal_body() -> rx.Component:
    return rx.modal_body(
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

def loggedin_modal_body() -> rx.Component:
    return rx.modal_body(
        rx.vstack(
            rx.text(f'You are logged in as {UserState.username}.'),
            rx.button('Logout', on_click=UserState.handle_logout)
        )
    )

def login_modal() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """    

    

    

    return rx.box(
        rx.modal(
            rx.modal_overlay(
                rx.modal_content(
                    rx.modal_header("login/register"),
                    rx.cond(UserState.logged_in, loggedin_modal_body(), login_modal_body()),
                    rx.modal_footer(
                        rx.button('Close', on_click=ModalStates.toggle_login_is_open)
                    )
                ),
            ),
            is_open=ModalStates.login_is_open,
            close_on_esc=True,
            close_on_overlay_click=True,
            return_focus_on_close=True,
            auto_focus=True,
            block_scroll_on_mount=False,
            on_close=ModalStates.toggle_login_is_open
        ),
    )







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
                    rx.modal_footer(
                        rx.button('Close', on_click=ModalStates.toggle_location_is_open)
                    )
                ),
            ),
            is_open=ModalStates.location_is_open,
            # close_on_esc=True,
            # close_on_overlay_click=True,
            # return_focus_on_close=True,
            # auto_focus=True,
            # block_scroll_on_mount=False,
            on_close=ModalStates.toggle_location_is_open
        ),
    )







def post_modal() -> rx.Component:
    return rx.box(
        rx.modal(
            rx.modal_overlay(
                rx.modal_content(
                    rx.modal_header(
                        rx.cond(
                            UserState.logged_in,
                            "post",
                            "login/register",
                        )
                    ),
                    rx.cond(
                        UserState.logged_in, 
                        post_modal_body(), 
                        login_modal_body()
                    ),
                )
            ),
            is_open=ModalStates.posting_is_open,
            close_on_esc=True,
            close_on_overlay_click=True,
            return_focus_on_close=True,
            auto_focus=True,
            block_scroll_on_mount=False,
            on_close=ModalStates.toggle_posting_is_open
        ),
    )

def post_modal_body() -> rx.Component:
    return rx.form(
            rx.vstack(
                rx.text_area(name='post'),
                rx.button("submit", type_="submit"),
            ),
        on_submit=UserState.handle_post
    )