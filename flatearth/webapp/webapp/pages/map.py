"""The home page of the app."""
from ..imports import *
from flatearth.utils.mapping import *


def init_map() -> go.Figure:
    fig = go.Figure(go.Scattergeo())
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


def init_layout():
    fig = init_map()
    return fig.to_dict().get('layout', {})


class MapState(rx.State):
    fig: go.Figure = init_map()
    layout: dict = init_layout()

    def add_point(self, lat=None, lon=None):
        if not lat or not lon: lat, lon = geo_ip()
        self.fig.add_scattergeo(
            lat=[lat * random.random()],
            lon=[lon * random.random()],
            marker_size=10,
            marker_color='rgb(65, 105, 225)',  # blue
            marker_symbol='star',
            showlegend=False)

    @rx.var
    def get_fig(self) -> go.Figure:
        return self.fig

    @rx.var
    def get_layout(self) -> go.Figure:
        return self.fig


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
        use_resize_handler=False,
    )
    rxfig._add_style({
        'width': WindowState.screen_width_px,
        'height': WindowState.proportional_height_px,
        'margin': 0,
        'padding': 0,
    })

    button = rx.button("Start", on_click=MapState.add_point())

    return rx.box(
        rxfig,
        # height='99dvh',
        height='fit-content',
        width='99dvw',
        position='absolute',
        top=0,
        left=0,
        align_items='top',
        # on_click=WindowState.get_client_values,
    )
