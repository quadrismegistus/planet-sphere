from ..imports import *
from flatearth.models import Post
from flatearth.utils.mapping import *
from .colorstate import ColorState
from .locstate import LocationState

LOC_TRACE_NAME='My location'

class MapState(LocationState):
    fig: go.Figure = init_map()
    layout: dict = init_layout()
    seen: set = set()
    read: set = set()
    projection: str = PROJECTION
    map_darkmode: bool = DARK_MODE_DEFAULT

    def clear_traces(self):
        self.fig = go.Figure(data=[], layout=self.layout)

    def set_projection(self, proj):
        self.fig = self.fig.update_geos(projection_type=proj.lower())
        self.layout = init_layout(self.fig)

    def toggle_dark_mode_map(self):
        self.map_darkmode = not self.map_darkmode
        self.fig = self.fig.update_geos(
            **self.map_colors
        )
        self.layout = init_layout(self.fig)
    
    @rx.background
    async def watch_map_darkmode(self):
        while True:
            async with self:
                if self.darkmode != self.map_darkmode:
                    self.toggle_dark_mode_map()
            await asyncio.sleep(.5)
        
    def add_point(self, lat=None, lon=None, trace_name=''):
        if lat is None or lon is None: return
        fig = traces_removed(self.fig, {trace_name})
        fig.add_scattergeo(
            lat=[lat],
            lon=[lon],
            customdata=["You are here"],
            name=trace_name,
            marker_size=10,
            hovertext=None,
            hoverinfo=None,
            hovertemplate="%{customdata}",
            marker_color='#5383EC',  # blue
            marker_symbol='circle-dot',
            showlegend=False,
        )
        self.fig = fig

    def add_posts(self, posts=None, trace_name='latest'):
        df = post_map_df(posts)
        fig = traces_removed(self.fig, good_trace_names={LOC_TRACE_NAME})
        
        for i,row in df.iterrows():
            fig.add_scattergeo(
                lat=[row.lat],
                lon=[row.lon],
                customdata=[row.data],
                name=row.id,
                marker_size=[row.size],
                hovertemplate="%{customdata}",
                marker_color=[row.color],
                marker_symbol='square-open',
                marker_opacity=1,
                marker_line_width=2,
                showlegend=False,
            )
            
            
        self.fig = fig

    def start_posts(self):
        self.add_posts()            

    def set_blue_dot(self, lat=0, lon=0):
        self.add_point(trace_name=LOC_TRACE_NAME,lat=lat,lon=lon)
        i=0

    

    # def check_geolocation(self):
    #     return rx.call_script(
    #         "window.geoloc",
    #         callback=MapState.set_coords,
    #     )

    # @rx.background
    # async def watch_geolocation(self):
    #     naptime=3
    #     i=0
    #     while True:
    #         async with self:
    #             yield self.check_geolocation()
    #             if self.geolocated:
    #                 break
    #         await asyncio.sleep(naptime)

    # def geolocate(self):
    #     # lat,lon = geo_ip(self.router.session.client_ip,hostname_required=True)
    #     # print([lat,lon])
    #     self.set_coords({'lat':0,'lon':0})
    #     # self.geolocated = False  # not true geoloc
    #     return rx.call_script(scripts.geoloc_js)

    def set_coords(self, geoloc):
        if geoloc and geoloc != self.geoloc:
            self.geoloc = geoloc
            self.geolocated = True
            self.set_blue_dot(**geoloc)
            self.set_place(**geoloc)





