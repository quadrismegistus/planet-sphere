from ..imports import *
from flatearth.utils.mapping import *
from .colorstate import ColorState
from .locstate import LocationState


class MapState(LocationState):
    fig: go.Figure = init_map()
    layout: dict = init_layout()
    seen: set = set()
    read: set = set()
    projection: str = PROJECTION

    def set_projection(self, proj):
        self.fig = self.fig.update_geos(projection_type=proj.lower())
        self.layout = init_layout(self.fig)

    def toggle_dark_mode(self):
        self.darkmode = not self.darkmode 
        self.fig = self.fig.update_geos(**self.map_colors)
        self.layout = init_layout(self.fig)
        self.store_opt('darkmode',self.darkmode)

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
        if not posts: 
            from flatearth.models import Post
            posts=Post.latest(limit=1000)
        lats = [jiggle(post.place.lat) for post in posts]
        lons = [jiggle(post.place.lon) for post in posts]
        sizes = [len(post.likes) for post in posts]
        
        timestamps=[post.timestamp for post in posts]
        if timestamps:
            mint,maxt=min(timestamps),max(timestamps)
            recencys=[
                translate_range(
                    post.timestamp,
                    (mint,maxt),
                    (0,1)
                )
                for post in posts
            ]

            color1,color2=colour.Color('orange'),colour.Color('blue')
            # color1.set_luminance(0.5)
            # color2.set_luminance(0.75)
            colors = [
                interpolate_color(color1,color2,recency).hex
                for recency in recencys
            ]
        else:
            colors=[]

        # colors = [post.place.geo.country_color for post in posts]
        if sizes:
            mins,maxs = min(sizes),max(sizes)
            sizes = [
                translate_range(
                    v,
                    (mins,maxs),
                    (5,20)
                ) for v in sizes
            ]
        
        customdatas = [
            post.json64
            for post in posts
        ]
        fig = traces_removed(self.fig, {trace_name})
        fig.add_scattergeo(
            lat=lats,
            lon=lons,
            customdata=customdatas,
            name='',
            marker_size=sizes,
            hovertemplate="%{customdata}",
            # marker_color='#1a9549',
            marker_color=colors,
            marker_symbol='square-open',
            marker_opacity=1,
            marker_line_width=2,
            # marker_line_color='#888888',
            showlegend=False,
        )
        self.fig = fig

    def start_posts(self):
        self.add_posts()            

    def set_blue_dot(self, lat=0, lon=0):
        self.add_point(trace_name='My location',lat=lat,lon=lon)

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





