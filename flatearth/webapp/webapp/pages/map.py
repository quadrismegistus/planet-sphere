"""The home page of the app."""
from ..imports import *
from flatearth.utils.mapping import *

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
window.hover_html = ""
setInterval(
    function() {
        const els = window.document.getElementsByClassName('hoverlayer');
        if(els.length) {
            const html = els[0].innerHTML.trim();
            if (html && (html != window.hover_html)) {
                window.hover_html = html;
                console.log(html);
            }
        }
    },
    100
)
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
        showland=False,
        showocean=False,
        showrivers=False,
        showlakes=False,
        coastlinecolor='#666666',
        countrycolor="#c7c7c7",
        rivercolor="#b4d4ff",
        oceancolor="#b4d4ff",
        projection_type='baker')
    relayout_fig(fig)
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

class MapState(rx.State):
    fig: go.Figure = init_map()
    layout: dict = init_layout()
    geoloc: dict[str, float] = {'lat': 0.0, 'lon': 0.0}
    geolocated: bool = False
    hover_html: str = ''

    def add_point(self, lat=None, lon=None):
        if lat is None or lon is None: return
        fig = traces_removed(self.fig, {''})
        fig.add_scattergeo(
            lat=[lat],
            lon=[lon],
            customdata=["You are here"],
            name='',
            marker_size=10,
            hovertext=None,
            hoverinfo=None,
            hovertemplate="%{customdata}",
            marker_color='#5383EC',  # blue
            marker_symbol='circle-dot',
            showlegend=False,
        )
        self.fig = fig
        self.layout = init_layout(self.fig)

    def add_posts(self, posts=None, trace_name='latest'):
        if not posts: 
            from flatearth.models import Post
            posts=Post.latest(limit=100)
        lats = [jiggle(post.place.lat) for post in posts]
        lons = [jiggle(post.place.lon) for post in posts]
        customdatas = [
            f'{post.user.name}:<br><br>'
            f'<b>{post.txt}</b><br><br>'
            f'{post.place.name}<br>'
            f'{post.ago}<br>'
            f'#{post.id}'
            for post in posts
        ]
        fig = traces_removed(self.fig, {trace_name})
        fig.add_scattergeo(
            lat=lats,
            lon=lons,
            customdata=customdatas,
            name=trace_name,
            marker_size=10,
            hovertemplate="%{customdata}",
            marker_color='#ecc853',
            marker_symbol='circle-dot',
            showlegend=False,
        )
        self.fig = fig
        self.layout = init_layout(self.fig)

    def start_posts(self):
        self.add_posts()

    @rx.var
    def get_fig(self) -> go.Figure:
        return self.fig

    def set_place(self):
        place = Place.loc(ip=self.ip) 
        self.place_data = place.data
        self.place_json = place.json
        self.place_name = place.name

    def set_coords(self, geoloc):
        if geoloc and geoloc != self.geoloc:
            self.geoloc = geoloc
            self.geolocated = True
            self.add_point(**geoloc)

    def check_geolocation(self):
        return rx.call_script(
            "window.geoloc",
            callback=MapState.set_coords,
        )

    @rx.background
    async def watch_geolocation(self):
        await asyncio.sleep(1) 
        naptime=10
        i=0
        while True:
            async with self:
                print(self.geoloc)
                yield self.check_geolocation()
                if self.geolocated:
                    break
            await asyncio.sleep(naptime)
            i+=1
            if i>=3: break

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
        data=MapState.get_fig,
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

    return rx.box(
        *scripts,
        rxfig,
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
            MapState.start_posts
        ],
        # border='1px dotted blue'
    )
