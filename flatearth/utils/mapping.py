from ..imports import *
import plotly.graph_objects as go
px.set_mapbox_access_token(MAPBOX_ACCESS_TOKEN)


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