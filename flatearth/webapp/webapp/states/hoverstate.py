from ..imports import *
from .mapstate import MapState
from flatearth.utils.mapping import traces_removed

box_width=400
box_height=400
box_offset=5
box_offset_h = box_offset

class HoverState(MapState):
    hover_id: str = ''
    mouseX: int = 0
    mouseY: int = 0
    screen_width: int = 800
    screen_height: int = 600
    box_display:str='none'
    marked_read: bool = False
    hover_html: str = ''

    def set_hover_json(self, data):
        hover_id0,mouseX,mouseY,screen_width,screen_height,hover_key = data
        hover_id=hover_id0.strip().split('_')[0]
        if hover_id.isdigit():
            if hover_id!=self.hover_id:
                logger.debug(f'focusing new post: {hover_id} [{hover_id0}]')
                self.hover_id=hover_id
                self.box_display = 'block'
                self.mouseX=mouseX
                self.mouseY=mouseY
                self.screen_width=screen_width
                self.screen_height=screen_height
                self.marked_read=False
                
                with logmap('making html'):
                    hover_dict=self.posts_on_map.get(hover_id,{})
                    if not hover_dict: 
                        logger.error(f'no data for post {self.hover_id}')
                    else:
                        self.hover_html=f'''
                            <h3>{hover_dict['user']['name']}</h3>
                            <p>{hover_dict['text']['txt']}</p>
                            <p>{hover_dict['place']['name']}</p>
                        '''


        
        if (
            not self.marked_read 
            and self.hover_id
            and hover_key=='d'
            ):
            post_id=int(self.hover_id)
            self.hover_id=''
            self.hover_key=''
            self.hover_dict={}
            self.marked_read=True
            self.box_display='none'

            self.mark_read(post_id)
            self.remove_point(post_id)
            
            

    def clear_hover(self):
        self.marked_read=False
        self.box_display='none'
        self.hover_id=''
        self.hover_key=''
        self.hover_dict={}


    def toggle_freeze_display(self):
        if self.box_display=='block':
            self.freeze_display = not self.freeze_display
        else:
            self.freeze_display = False

    def alert(self):
        return rx.window_alert('What???')
    
    @rx.var
    def box_left(self):
        maxW = self.screen_width - box_offset
        thisW = self.mouseX + box_offset
        return thisW if thisW<maxW else maxW
    
    @rx.var
    def box_top(self):
        maxH = self.screen_height - box_offset_h
        thisH = self.mouseY + box_offset_h
        return thisH if thisH<maxH else maxH


    def check_hover(self):
        return rx.call_script(
            "[window.hover_json, window.mouseX, window.mouseY, window.innerWidth, window.innerHeight, window.hover_key]",
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
                with logmap('checking hover'):
                    yield self.check_hover()
            await asyncio.sleep(.1)