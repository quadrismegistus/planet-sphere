from ..imports import *
from ..styles import *
from flatearth.utils.mapping import map_colors_dark, map_colors_light


class ColorState(rx.State):
    app_darkmode: bool = DARK_MODE_DEFAULT
    sys_darkmode: bool = DARK_MODE_DEFAULT
    darkmode: bool = DARK_MODE_DEFAULT
    opts_json: str = rx.LocalStorage('{}')
    src_darkmode: Literal['app','system'] = 'app' # or 'system' or 'app'

    def init(self):
        if self.opts_json:
            opts = from_json(str(self.opts_json))
            self.app_darkmode = opts.get('app_darkmode',self.app_darkmode)
            self.src_darkmode = opts.get('app_darkmode',self.src_darkmode)
        
            
    @rx.var
    def darkmode(self):
        return (
            self.sys_darkmode 
            if self.src_darkmode=='system' 
            else self.app_darkmode
        )

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
        self.app_darkmode = not self.darkmode
        self.src_darkmode = 'app'
        self.store_opt('app_darkmode',self.app_darkmode)
        self.store_opt('src_darkmode',self.src_darkmode)


    def check_sys_darkmode(self):
        return rx.call_script(
            "window.systemColorScheme",
            callback=ColorState.set_sys_darkmode,
        )
    
    def set_sys_darkmode(self, darkmode_str):
        darkmode = darkmode_str == 'dark'
        if self.sys_darkmode != darkmode:
            self.sys_darkmode=darkmode
            self.src_darkmode='system'
            self.store_opt('src_darkmode',self.src_darkmode)



    @rx.background
    async def watch_sys_darkmode(self):
        while True:
            async with self:
                yield self.check_sys_darkmode()
            await asyncio.sleep(.5)