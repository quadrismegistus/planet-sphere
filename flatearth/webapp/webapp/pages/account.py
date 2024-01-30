"""The dashboard page."""
from ..imports import *
from flatearth.models import User

@template(route="/account", title="Account", image="/account-avatar-head.svg")
def account_page() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """    
    return rx.vstack(
        rx.heading("Users", font_size="3em"),
    )
