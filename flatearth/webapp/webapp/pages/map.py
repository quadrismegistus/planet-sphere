"""The home page of the app."""
from ..imports import *
from flatearth.utils.mapping import *

bgcolor_dark='black'
bgcolor_light='white'


map_colors_dark = dict(
    countrycolor='rgba(255,255,255,0.15)',
    landcolor='#324D36',
    coastlinecolor='rgba(0,0,0,0.5)',
    oceancolor="#121A3D",
    bgcolor='rgba(0,0,0,0)'
)

map_colors_light = dict(
    countrycolor='rgba(255,255,255,0.15)',
    landcolor='darkseagreen',
    coastlinecolor='rgba(0,0,0,0.5)',
    oceancolor="lightskyblue",
    bgcolor='rgba(0,0,0,0)'
)



geoloc_js = """
async function geoloc() {
    window.geoloc = {'lat':0.0, 'lon':0.0};
    await navigator.geolocation.getCurrentPosition(
        (pos) => { 
            window.geoloc = {
                'lat':pos.coords.latitude,
                'lon':pos.coords.longitude
            }
        }
    );
}

geoloc();
"""

hover_js = """

document.body.style.backgroundColor='black';

window.hover_json = "";
setInterval(
    function() {
        const els = window.document.getElementsByClassName('hoverlayer');
        if(els.length) {
            const el = els[0];
            const txt = el.textContent;
            if(txt!=window.hover_json) {
                window.hover_json = txt;
            }
        }
    },
    100
);

window.mouseX = 0;
window.mouseY = 0;

function updateMouseLoc(event) {
    window.mouseX = event.clientX;
    window.mouseY = event.clientY;
}

document.addEventListener('mousemove', updateMouseLoc);

"""



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
        projection_type='baker',
        **map_colors_dark
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

def traces_removed(fig, bad_trace_names:set):
    return go.Figure(
        data=[
            trace 
            # for trace,name in zip(
            #     fig.data, 
            #     fig.__trace_names()
            # ) 
            for trace in fig.data
            if trace.name not in bad_trace_names
        ],
        layout=fig.layout
    )

def jiggle(lat_or_lon):
    num = random.random() / 10
    num = -num if random.random()>.5 else num
    return lat_or_lon + num

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

class MapState(rx.State):
    fig: go.Figure = init_map()
    layout: dict = init_layout()
    geoloc: dict[str, float] = {'lat': 0.0, 'lon': 0.0}
    geolocated: bool = False
    seen: set = set()
    read: set = set()
    darkmode: bool = True

    def toggle_dark_mode(self):
        self.darkmode = not self.darkmode
        colors = (
            map_colors_dark
            if self.darkmode
            else map_colors_light
        )
        bgcolor = bgcolor_dark if self.darkmode else bgcolor_light
        self.fig = self.fig.update_geos(**colors)
        self.layout = init_layout(self.fig)
        return rx.call_script(
            f'document.body.style.backgroundColor="{bgcolor}"; ' 
            f'console.log("{bgcolor}"); '
        )


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
        return rx.call_script(geoloc_js)


@template(route="/", title="Map", image="/map-location-pin.svg")
def map_page() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    rxfig = rx.plotly(
        data=MapState.fig,
        layout=MapState.layout,
        # width=WindowState.screen_width_px,
        # height=WindowState.proportional_height_px,
        use_resize_handler=True,
    )
    rxfig._add_style({
        # 'width': WindowState.screen_width_px,
        # 'height': WindowState.proportional_height_px,
        'width':'100%',
        'height':'100%',
        'margin': 0,
        'padding': 0,
    })

    scripts = [
        rx.script(geoloc_js),
        rx.script(hover_js)
    ]

    txtbox = rx.box(
        rx.html(HoverState.hover_post_html),
        position='absolute',
        top=HoverState.box_top,
        left=HoverState.box_left,
        max_width=f'{box_width}px',
        max_height=f'{box_height}px',
        background_color='rgba(255,255,255,0.666)',
        backdrop_filter='blur(5px)',
        # overflow_y='scroll',
        border='1px solid black',
        border_radius=styles.border_radius,
        box_shadow=styles.box_shadow,
        display=HoverState.box_display,
        padding='.5rem',
        font_size='.9rem',
    )

    btn = rx.button(
        'toggle dark mode',
        on_click=MapState.toggle_dark_mode,
        margin_top='50px'
    )

    return rx.box(
        *scripts,
        btn,
        rxfig,
        txtbox,
        height='99dvh',
        # height='fit-content',
        width='99dvw',
        position='absolute',
        top=0,
        left=0,
        align_items='top',
        # on_click=WindowState.get_client_values,
        on_mount=[
            # MapState.geolocate, 
            MapState.watch_geolocation, 
            MapState.start_posts,
            HoverState.watch_hover
        ],
        # border='1px dotted blue'
    )
