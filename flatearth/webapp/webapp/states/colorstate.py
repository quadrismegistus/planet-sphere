from ..imports import *
from ..styles import *

DARK_MODE_DEFAULT = False

class ColorState(rx.State):
    darkmode: bool = DARK_MODE_DEFAULT

    @rx.var
    def map_colors(self) -> dict:
        return map_colors_dark if self.darkmode else map_colors_light
    
    @rx.var
    def bgcolor(self) -> str:
        return bgcolor_dark if self.darkmode else bgcolor_light
    
    @rx.var
    def classname(self) -> str:
        return 'color_inverted' if self.darkmode else 'color_normal'
    
    @rx.var
    def filter(self) -> str:
        return 'color_inverted' if self.darkmode else 'color_normal'
    
    @rx.var
    def text_color(self):
        return 'white' if self.darkmode else 'black'
    
    @rx.var
    def invert_filter(self):
        return 'invert(100%)' if self.darkmode else 'invert(0%)'

    def toggle_dark_mode(self):
        self.darkmode = not self.darkmode
        
        