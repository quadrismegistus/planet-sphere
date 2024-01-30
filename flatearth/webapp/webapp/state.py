from .imports import *
from flatearth.utils import geodecode
from flatearth.models import *


class State(rx.State):
    """Define empty state to allow access to rx.State.router."""

    place_data: dict = {}
    place_json: str = ''
    place_name: str = ''

    user_name: str = ''

    @rx.var
    def ip(self) -> str:
        return self.router.session.client_ip
    
    def set_place(self):
        place = Place.loc(ip=self.ip)
        self.place_data = place.data
        self.place_json = place.json
        self.place_name = place.name
    
    

class WindowState(rx.State):
    screen_width: int = 0
    screen_height: int = 0

    def set_screen_size(self, screen_size):
        self.screen_width, self.screen_height=screen_size

    def get_client_values(self):
        return [
            rx.call_script(
                "[window.innerWidth, window.innerHeight]",
                callback=WindowState.set_screen_size,
            ),
        ]
    
    @rx.var
    def screen_width_px(self) -> str:
        return str(self.screen_width - 50)+'px'
    @rx.var
    def screen_height_px(self) -> str:
        return str(self.screen_height - 50)+'px'
    
    @rx.var
    def screen_px(self) -> str:
        return str(self.screen_height if self.screen_height>self.screen_width else self.screen_width)+'px'
    
    @rx.var
    def proportional_height_px(self) -> str:
        return str(self.screen_width * .666)+'px'
