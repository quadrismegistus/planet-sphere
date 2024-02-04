from ..imports import *
from .userstate import UserState

class ModalStates(UserState):
    login_is_open: bool = False
    location_is_open: bool = False
    posting_is_open: bool = False

    def open_location_modal(self):
        self.location_is_open = True
    def close_location_modal(self):
        self.location_is_open = False

    def open_login_modal(self):
        self.login_is_open = True
    def close_login_modal(self):
        self.login_is_open = False

    def open_posting_modal(self):
        self.posting_is_open = True
    def close_posting_modal(self):
        self.posting_is_open = False
