from ..imports import *
from .utils import interpolate_color, translate_range, to_json
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


def init_map(darkmode=False) -> go.Figure:
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
        **(map_colors_light if not darkmode else map_colors_dark)
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


def traces_removed(
        fig:go.Figure, 
        bad_trace_names:Optional[set]=None, 
        good_trace_names:Optional[set]=None,
        bad_trace_startswith:Optional[str]=None,
        bad_trace_endswith:Optional[str]=None,
        ):
    
    if bad_trace_names: 
        bad_trace_names={str(x) for x in bad_trace_names}
    if good_trace_names: 
        good_trace_names={str(x) for x in good_trace_names}
    if bad_trace_startswith != None: 
        bad_trace_startswith=str(bad_trace_startswith)
    if bad_trace_endswith != None: 
        bad_trace_endswith=str(bad_trace_endswith)
    return go.Figure(
        data=[
            trace 
            for trace in fig.data
            if trace.name
            and (not bad_trace_names or trace.name not in bad_trace_names)
            and (not good_trace_names or trace.name in good_trace_names)
            and (not bad_trace_startswith or not trace.name.startswith(bad_trace_startswith))
            and (not bad_trace_endswith or not trace.name.endswith(bad_trace_endswith))
        ],
        layout=fig.layout
    )

def jiggle(lat_or_lon):
    num = random.random() / 10
    num = -num if random.random()>.5 else num
    return lat_or_lon + num


def post_map_df(posts=None, from_color='purple', to_color='pink', min_size=5, max_size=20, jiggle_positions=False):
    from flatearth.models import Post
    if not posts: posts = Post.latest()

    posts_ld=[]
    def add_post(post):
        posts_ld.append(dict(
            id=post['id'],
            user_id=post['user']['id'],
            lat=post['place']['lat'],
            lon=post['place']['lon'],
            timestamp=post['timestamp'],
            num_likes=len(post['likes']),
            data=to_json(post),
            reply_to=post.get('reply_to',{}).get('id',0),
            repost_of=post.get('repost_of',{}).get('id',0)
        ))

    def related_posts(postd, keys=['reply_to','repost_of']):
        relposts={}
        for key in keys:
            if postd.get(key): 
                relposts[postd[key]['id']]=postd[key]
                relposts={**relposts, **related_posts(postd[key])}
        return relposts

    for post in posts:
        post = dict(post.data) if isinstance(post,Post) else post
        add_post(post)
        others = related_posts(post).values()
        for postx in others:
            add_post(postx)
    
    def norm(s:pd.Series):
        return (s-s.min()) / (s.max() - s.min()) if (s.max() - s.min()) else np.nan

    df = pd.DataFrame(posts_ld).drop_duplicates('id')
    if len(df):
        color1,color2=Color(from_color),Color(to_color)
        # df['color'] = norm(df['timestamp']).apply(
        #     lambda t: interpolate_color(color1,color2,t).hex
        # )
        df['color']=df['user_id'].apply(get_color)

        s=df['num_likes']
        df['size'] = s.apply(
            lambda n: translate_range(
                n, 
                (s.min(), s.max()),
                (min_size,max_size)
            )
        )
    
    if jiggle_positions:
        df['lat']=df['lat'].apply(jiggle)
        df['lon']=df['lon'].apply(jiggle)

    return df

def get_color(name):
    color = RGB_color_picker(name)
    color.set_saturation(1)
    return color.hex