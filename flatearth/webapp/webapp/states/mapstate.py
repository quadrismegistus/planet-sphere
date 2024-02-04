from ..imports import *
from flatearth.models import Post
from flatearth.utils.mapping import *
from .colorstate import ColorState
from .feedstate import FeedState


class MapState(FeedState):
    fig: go.Figure = init_map()
    layout: dict = init_layout()
    projection: str = PROJECTION
    map_darkmode: bool = DARK_MODE_DEFAULT
    max_on_map: int = 5
    posts_on_map: dict = {}

    def clear_traces(self):
        self.fig = go.Figure(data=[], layout=self.layout)

    @property
    def trace_d(self):
        return {
            int(trace.name):trace 
            for trace in self.fig.data 
            if trace.name and trace.name.isdigit()
        }

    
    def set_projection(self, proj):
        self.fig = self.fig.update_geos(projection_type=proj.lower())
        self.layout = init_layout(self.fig)

    def toggle_dark_mode_map(self):
        self.map_darkmode = not self.map_darkmode
        self.fig = self.fig.update_geos(
            **self.map_colors
        )
        self.layout = init_layout(self.fig)
    
    @rx.background
    async def watch_map_darkmode(self):
        while True:
            async with self:
                if self.darkmode != self.map_darkmode:
                    self.toggle_dark_mode_map()
            await asyncio.sleep(.5)
        
    @rx.var
    def orig_post_ids(self) -> set:
        return {
            int(trace.name)
            for trace in self.fig.data
            if trace.name and trace.name.isdigit()
            and not self.pending.get(trace.name,{}).get('repost_of') and not self.pending.get(trace.name,{}).get('reply_to')
        }
    @rx.var
    def post_ids(self) -> set:
        return {
            int(trace.name)
            for trace in self.fig.data
            if trace.name and trace.name.isdigit()
        }
    
    @rx.var
    def num_orig_posts(self): return len(self.orig_post_ids)
    @rx.var
    def num_posts(self): return len(self.post_ids)
    
    def add_posts(self):
        num_needed = self.max_on_map - self.num_orig_posts
        if num_needed<1: return
        posts_on_map = [
            self.posts_on_map[str(id)]
            for id in self.post_ids
        ]
        pending_not_on_map = [
            d
            for d in self.pending.values()
            if d['id'] not in self.post_ids|self.seen
        ][:num_needed]

        logger.debug(f'pending not on map {len(pending_not_on_map)}')
        
        df = post_map_df(
            posts_on_map + pending_not_on_map,
            max_size=50,
            jiggle_positions=True
        )
        fig = self.fig

        def add_row_point(row):
            self.posts_on_map[str(row.id)]=from_json(row.data)
            return fig.add_scattergeo(
                lat=[row.lat],
                lon=[row.lon],
                customdata=[row.html],
                hovertemplate="%{customdata}",
                name=row.id,
                marker_size=[row.size],
                # hovertemplate=" ",
                marker_color=[row.color],
                marker_symbol='circle-dot',
                marker_opacity=.666,
                marker_line_width=0,
                showlegend=False,
            )

        def add_row_line(row1,row2,type='reply'):
            return fig.add_scattergeo(
                lat=[row1.lat, row2.lat],
                lon=[row1.lon, row2.lon],
                customdata=[row1.html],
                hovertemplate="%{customdata}",
                name=f'{row.id}_{row2.id}',
                hoverinfo='skip',
                mode = 'lines',
                line = dict(
                    width = 2,
                    # color = '#e59cff' if type=='reply' else '#e9ec9f'
                    color=row1.color,
                ),
                opacity = .8,
                showlegend=False,
            )

        trace_d = self.trace_d
        rows={row.id:row for i,row in df.iterrows()}

        for row in rows.values():
            if row.reply_to:
                row2=rows[row.reply_to]
                fig=add_row_line(row,row2,'reply')
                print(row.id,'reply',row2.id)
            if row.repost_of:
                row2=rows[row.repost_of]
                fig=add_row_line(row,row2,'repost')
                print(row.id,'repost',row2.id)

        for row in rows.values():
            if row.id not in trace_d:
                fig=add_row_point(row)
            else:
                trace=trace_d[row.id]
                trace.marker.size=[row.size]
                trace.marker.color=[row.color]

        self.fig = fig

    @rx.background
    async def watch_posts(self):
        while True:
            async with self:
                num_map = self.num_posts
                num_orig = self.num_orig_posts
                if num_orig < self.max_on_map:
                    logger.debug(['watch_posts',num_map,num_orig,len(self.pending)])
                    logger.debug(f'not enough ids on map. have {num_orig} original posts, {num_map} total posts, but would like {self.max_on_map-num_orig} to reach {self.max_on_map} maximum')
                    
                    self.add_posts()
            await asyncio.sleep(1)

    def set_blue_dot(self, lat=0, lon=0):
        if lat is None or lon is None: return
        fig = traces_removed(self.fig, {LOC_TRACE_NAME})
        fig.add_scattergeo(
            lat=[lat],
            lon=[lon],
            name=LOC_TRACE_NAME,
            marker_size=10,
            hovertext=None,
            hoverinfo=None,
            hovertemplate="%{customdata}",
            customdata=[' '],
            marker_color='#5383EC',  # blue
            marker_symbol='circle-dot',
            showlegend=False,
        )
        self.fig = fig

    def set_coords(self, geoloc):
        if geoloc and geoloc != self.geoloc:
            self.geoloc = geoloc
            self.geolocated = True
            self.set_blue_dot(**geoloc)
            self.set_place(**geoloc)

    def remove_point(self, id=0):
        self.fig = traces_removed(
            self.fig, 
            bad_trace_names={id}, 
            bad_trace_startswith=f'{id}_',
            bad_trace_endswith=f'_{id}',
        )
        # del self.posts_on_map[str(id)]



