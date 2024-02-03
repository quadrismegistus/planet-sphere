from ..imports import *
from .userstate import UserState

class ModalStates(UserState):
    login_is_open: bool = False
    location_is_open: bool = False
    posting_is_open: bool = False

    def toggle_login_is_open(self):
        self.login_is_open = not self.login_is_open

    def toggle_location_is_open(self):
        self.location_is_open = not self.location_is_open
    
    def toggle_posting_is_open(self):
        self.posting_is_open = not self.posting_is_open

