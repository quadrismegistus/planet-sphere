from ..imports import *

box_width=400
box_height=400
box_offset=5
box_offset_h = box_offset

class HoverState(rx.State):
    hover_json: str = ''
    hover_dict: dict = {}
    mouseX: int = 0
    mouseY: int = 0
    screen_width: int = 800
    screen_height: int = 600
    box_display:str='none'

    def set_hover_json(self, data):
        hover_json,mouseX,mouseY,screen_width,screen_height = data
        self.mouseX=mouseX
        self.mouseY=mouseY
        self.screen_width=screen_width
        self.screen_height=screen_height
        self.box_display = 'block' if hover_json else 'none'
        self.hover_json = hover_json
        if hover_json:
            self.hover_dict = from_json64(hover_json)

    @rx.var
    def hover_post_html(self):
        return f'''
<h3>{self.hover_dict['user']['name']}</h3>
<p>{self.hover_dict['text']['txt']}</p>
<p>{self.hover_dict['place']['name']}</p>
        ''' if self.hover_dict else ''
    
    @rx.var
    def box_left(self):
        maxW = self.screen_width - box_width - box_offset
        thisW = self.mouseX + box_offset
        return thisW if thisW<maxW else maxW
    
    @rx.var
    def box_top(self):
        maxH = self.screen_height - box_offset_h
        thisH = self.mouseY + box_offset_h
        return thisH if thisH<maxH else maxH


    def check_hover(self):
        return rx.call_script(
            "[window.hover_json, window.mouseX, window.mouseY, window.innerWidth, window.innerHeight]",
            callback=HoverState.set_hover_json,
        )
    
    # @rx.var
    # def margin_left(self, box_width=400):
    #     over = self.mouseX + box_width - self.screen_width
    #     return -over if over else 0
    
    # @rx.var
    # def margin_top(self, box_height=400):
    #     over = self.mouseY + box_height - self.screen_height
    #     return -over if over else 0



    
    
    @rx.background
    async def watch_hover(self):
        while True:
            async with self:
                yield self.check_hover()
            await asyncio.sleep(.1)