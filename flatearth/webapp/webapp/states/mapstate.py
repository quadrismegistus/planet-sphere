from ..imports import *
from flatearth.utils.mapping import *
from .colorstate import ColorState

projections = ["airy", "aitoff", "albers", "albers usa", "august", "azimuthal equal area", "azimuthal equidistant", "baker", "bertin1953", "boggs", "bonne", "bottomley", "bromley", "collignon", "conic conformal", "conic equal area", "conic equidistant", "craig", "craster", "cylindrical equal area", "cylindrical stereographic", "eckert1", "eckert2", "eckert3", "eckert4", "eckert5", "eckert6", "eisenlohr", "equal earth", "equirectangular", "fahey", "foucaut", "foucaut sinusoidal", "ginzburg4", "ginzburg5", "ginzburg6", "ginzburg8", "ginzburg9", "gnomonic", "gringorten", "gringorten quincuncial", "guyou", "hammer", "hill", "homolosine", "hufnagel", "hyperelliptical", "kavrayskiy7", "lagrange", "larrivee", "laskowski", "loximuthal", "mercator", "miller", "mollweide", "mt flat polar parabolic", "mt flat polar quartic", "mt flat polar sinusoidal", "natural earth", "natural earth1", "natural earth2", "nell hammer", "nicolosi", "orthographic", "patterson", "peirce quincuncial", "polyconic", "rectangular polyconic", "robinson", "satellite", "sinu mollweide", "sinusoidal", "stereographic", "times", "transverse mercator", "van der grinten", "van der grinten2", "van der grinten3", "van der grinten4", "wagner4", "wagner6", "wiechel", "winkel tripel", "winkel3"]
PROJECTION = 'nicolosi'


def init_map() -> go.Figure:
    scatter = go.Scattergeo()
    fig = go.Figure(scatter)
    fig.update_geos(
        visible=True,
        showframe=False,
        # resolution=50,
        showcountries=True,
        showcoastlines=True,
        showland=True,
        showocean=True,
        showrivers=False,
        showlakes=False,
        projection_type=PROJECTION,
        **styles.map_colors_light
    )
    relayout_fig(fig)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def init_layout(fig=None):
    fig = init_map() if fig is None else fig
    return fig.to_dict().get('layout', {})






class MapState(ColorState):
    fig: go.Figure = init_map()
    layout: dict = init_layout()
    geoloc: dict[str, float] = {'lat': 0.0, 'lon': 0.0}
    geolocated: bool = False
    seen: set = set()
    read: set = set()
    projection: str = ''

    def set_projection(self, proj):
        self.fig = self.fig.update_geos(projection_type=proj.lower())
        self.layout = init_layout(self.fig)


    def toggle_dark_mode(self):
        self.darkmode = not self.darkmode 
        self.fig = self.fig.update_geos(**self.map_colors)
        self.layout = init_layout(self.fig)
        self.store_opt('darkmode',self.darkmode)
        # return rx.call_script(
        #     f'document.body.style.backgroundColor="{self.bgcolor}"; ' 
        # )

        
        

    

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

        # colors = [post.place.geo.country_color for post in posts]
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

    def set_place(self):
        place = Place.locate(ip=self.ip) 
        self.place_data = place.data
        self.place_json = place.json
        self.place_name = place.name

    def set_coords(self, geoloc):
        if geoloc and geoloc != self.geoloc:
            self.geoloc = geoloc
            self.geolocated = True
            self.add_point(trace_name='My location',**geoloc)

    def check_geolocation(self):
        return rx.call_script(
            "window.geoloc",
            callback=MapState.set_coords,
        )

    @rx.background
    async def watch_geolocation(self):
        naptime=3
        i=0
        while True:
            async with self:
                yield self.check_geolocation()
                if self.geolocated:
                    break
            await asyncio.sleep(naptime)

    def geolocate(self):
        lat,lon = geo_ip(self.router.session.client_ip,hostname_required=True)
        self.add_point(lat,lon)
        self.geoloc = {'lat':lat, 'lon':lon}
        return rx.call_script(scripts.geoloc_js)







