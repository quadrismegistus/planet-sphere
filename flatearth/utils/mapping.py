from ..imports import *
import plotly.graph_objects as go
px.set_mapbox_access_token(MAPBOX_ACCESS_TOKEN)

map_colors_dark = dict(
    countrycolor='rgba(255,255,255,0.15)',
    landcolor='#324D36',
    coastlinecolor='rgba(0,0,0,0.5)',
    oceancolor="#121A3D",
    bgcolor='rgba(0,0,0,0)',
    rivercolor='#305e88'
)

map_colors_light = dict(
    countrycolor='rgba(255,255,255,0.15)',
    landcolor='darkseagreen',
    coastlinecolor='rgba(0,0,0,0.5)',
    oceancolor="lightskyblue",
    bgcolor='rgba(0,0,0,0)',
    rivercolor='#4788dc'
)

projections = ["airy", "aitoff", "albers", "albers usa", "august", "azimuthal equal area", "azimuthal equidistant", "baker", "bertin1953", "boggs", "bonne", "bottomley", "bromley", "collignon", "conic conformal", "conic equal area", "conic equidistant", "craig", "craster", "cylindrical equal area", "cylindrical stereographic", "eckert1", "eckert2", "eckert3", "eckert4", "eckert5", "eckert6", "eisenlohr", "equal earth", "equirectangular", "fahey", "foucaut", "foucaut sinusoidal", "ginzburg4", "ginzburg5", "ginzburg6", "ginzburg8", "ginzburg9", "gnomonic", "gringorten", "gringorten quincuncial", "guyou", "hammer", "hill", "homolosine", "hufnagel", "hyperelliptical", "kavrayskiy7", "lagrange", "larrivee", "laskowski", "loximuthal", "mercator", "miller", "mollweide", "mt flat polar parabolic", "mt flat polar quartic", "mt flat polar sinusoidal", "natural earth", "natural earth1", "natural earth2", "nell hammer", "nicolosi", "orthographic", "patterson", "peirce quincuncial", "polyconic", "rectangular polyconic", "robinson", "satellite", "sinu mollweide", "sinusoidal", "stereographic", "times", "transverse mercator", "van der grinten", "van der grinten2", "van der grinten3", "van der grinten4", "wagner4", "wagner6", "wiechel", "winkel tripel", "winkel3"]
PROJECTION = 'nicolosi'


def init_map() -> go.Figure:
    scatter = go.Scattergeo()
    fig = go.Figure(scatter)
    fig.update_geos(
        visible=True,
        showframe=False,
        # resolution=50,
        showcountries=False,
        showcoastlines=True,
        showland=True,
        showocean=True,
        showrivers=True,
        showlakes=False,
        projection_type=PROJECTION,
        **map_colors_light
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


def relayout_fig(fig:go.Figure, width=1000, height=800) -> go.Figure:
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        autosize=True,
        showlegend=False,
        xaxis=dict(visible=False, showgrid=False, showline=False), 
        yaxis=dict(visible=False, showgrid=False, showline=False),
    )
    fig.layout._config = {'responsive':True, 'scrollZoom':True, 'displayModeBar':False}
    return fig


def plot_map2() -> go.Figure:
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/Nuclear%20Waste%20Sites%20on%20American%20Campuses.csv')
    site_lat = df.lat
    site_lon = df.lon
    locations_name = df.text

    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
            lat=site_lat,
            lon=site_lon,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=17,
                color='rgb(255, 0, 0)',
                opacity=0.7
            ),
            text=locations_name,
            hoverinfo='text'
        ))

    fig.add_trace(go.Scattermapbox(
            lat=site_lat,
            lon=site_lon,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=8,
                color='rgb(242, 177, 172)',
                opacity=0.7
            ),
            hoverinfo='none'
        ))

    fig.update_layout(
        title='Nuclear Waste Sites on Campus',
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=MAPBOX_ACCESS_TOKEN,
            bearing=0,
            center=dict(
                lat=38,
                lon=-94
            ),
            pitch=0,
            zoom=3,
            style='light'
        ),
    )

    return fig


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


