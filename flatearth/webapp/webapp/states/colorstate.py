from ..imports import *
from ..styles import *

DARK_MODE_DEFAULT = False

class ColorState(rx.State):
    darkmode: bool = False
    map_colors: dict = map_colors_dark if DARK_MODE_DEFAULT else map_colors_dark
    bgcolor: dict = bgcolor_dark if DARK_MODE_DEFAULT else bgcolor_light

    def toggle_dark_mode(self):
        dm = self.darkmode = not self.darkmode
        self.map_colors=map_colors_dark if dm else map_colors_light
        self.bgcolor = bgcolor_dark if dm else bgcolor_light
        return rx.call_script(
            f'document.body.style.backgroundColor="{self.bgcolor}"; ' 
            f'console.log("{self.bgcolor}"); '
        )
        