from ..imports import *
from ..styles import *
from flatearth.utils.mapping import map_colors_dark, map_colors_light

DARK_MODE_DEFAULT = False

class ColorState(rx.State):
    darkmode: bool = DARK_MODE_DEFAULT
    opts_json: str = rx.LocalStorage('{}')

    def init(self):
        if self.opts_json:
            opts = from_json(str(self.opts_json))
            darkmode = opts.get('darkmode',self.darkmode)
            if darkmode != self.darkmode: 
                return self.toggle_dark_mode()
            
    

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

    def store_opt(self, key, val):
        opts = from_json(str(self.opts_json))
        opts[key] = val
        self.opts_json = to_json(opts)

    def toggle_dark_mode(self):
        self.darkmode = not self.darkmode
        self.store_opt('darkmode',self.darkmode)


    def check_sys_darkmode(self):
        return rx.call_script(
            "systemColorScheme",
            callback=ColorState.set_sys_darkmode,
        )
    
    def set_sys_darkmode(self, darkmode_str):
        darkmode = darkmode_str == 'dark'
        if darkmode != self.darkmode:
            self.toggle_dark_mode()

    @rx.background
    async def watch_sys_darkmode(self):
        while True:
            async with self:
                yield self.check_sys_darkmode()
            await asyncio.sleep(.5)