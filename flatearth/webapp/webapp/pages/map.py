"""The home page of the app."""
from ..imports import *


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
        on_click=HoverState.toggle_freeze_display,
    )
    rxfig._add_style({
        # 'width': WindowState.screen_width_px,
        # 'height': WindowState.proportional_height_px,
        'width':'100%',
        'height':'100%',
        'margin': 0,
        'padding': 0,
    })

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

    projs = rx.box(
        rx.select(
            [x.title() for x in projections],
            placeholder="Select a projection",
            on_change=MapState.set_projection,
            default_value=PROJECTION.title()
        ),
        width='10rem',
        margin_left='auto',
        position='absolute',
        right=0,
        top=0
    )



    return rx.box(
        rx.script(scripts.geoloc_js),
        rx.script(scripts.hover_js),
        # btn,
        rxfig,
        # projs,
        txtbox,
        height='100dvh',
        # height='fit-content',
        width='100dvw',
        position='absolute',
        top=0,
        left=0,
        margin_top='3rem',
        align_items='top',
        on_click=HoverState.toggle_freeze_display,
        on_mount=[
            # MapState.geolocate, 
            MapState.watch_geolocation, 
            MapState.start_posts,
            HoverState.watch_hover
        ],
        # border='1px dotted blue'
    )
