from .imports import *
from flatearth.utils import geodecode
from flatearth.models import *


class State(rx.State):
    """Define empty state to allow access to rx.State.router."""

    place_data: dict = {}
    place_json: str = ''

    @rx.var
    def ip(self) -> str:
        return self.router.session.client_ip
    
    def set_place(self):
        place = Place.loc(ip=self.ip)
        self.place_data = place.data
        self.place_json = place.json
    
    