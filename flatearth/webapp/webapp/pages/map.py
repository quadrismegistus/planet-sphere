"""The home page of the app."""
from ..imports import *
from flatearth.utils.mapping import *

def plot_map(width=1000, height=1000) -> go.Figure:
    df = px.data.gapminder().query("year == 2007")
    # fig = px.scatter_geo(df, 
    #     locations="iso_alpha",
    #     # color="continent", # which column to use to set the color of markers
    #     hover_name="country", # column added to hover information
    #     size="pop", # size of markers
    #     projection="miller",
    # )
    fig = go.Figure(
        go.Scattergeo()
    )
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
        projection_type='baker'
    )
    relayout_fig(fig)
    return fig


@template(route="/", title="Map", image="/map-location-pin.svg")
def map_page() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """

    fig = plot_map()
    layout = fig.to_dict().get('layout',{})
    rxfig = rx.plotly(data=fig, layout=layout, use_resize_handler=True)
    rxfig._add_style({'width':'100%','height':'100%', 'margin':0,'padding':0,'border':'none'})
    return rx.box(
        rxfig, 
        height='99dvh', 
        width='99dvw', 
        position='absolute',
        top=0,
        left=0,
        align_items='top',
        padding_top='5rem'
        # z_index=-1
    )