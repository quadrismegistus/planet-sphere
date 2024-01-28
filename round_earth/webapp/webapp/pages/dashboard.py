"""The dashboard page."""
from ..imports import *
from round_earth.models import User



class UserDict(rx.Base):
    id: int
    name: str


class UserListState(rx.State):
    users: List[UserDict] = []

    def set_users(self):
        self.users = [
            UserDict(id=user.id, name=user.name) for user in User.find()
        ]

@template(route="/dashboard", title="Dashboard")
def dashboard() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """

    users = rx.responsive_grid(
        rx.foreach(
            UserListState.users,
            lambda d, i: rx.box(
                rx.text(f'{d.id}. {d.name}')
            ),
        ),
        on_mount = UserListState.set_users
    )
    
    return rx.vstack(
        rx.heading("Users", font_size="3em"),
        rx.heading(State.ip, font_size="2em"),
        users
    )
