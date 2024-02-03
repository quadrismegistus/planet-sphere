from ..imports import *
from .colorstate import ColorState

class LocationState(ColorState):
    geoloc: dict[str, float] = {}
    geolocated: bool = False
    place_data: dict = {}


    @rx.var
    def placename(self) -> str:
        return self.place_data.get('name','Unknown Location')

    @rx.var
    def place_json(self) -> str:
        return json.dumps(self.place_data,indent=4)

    def check_geolocation(self):
        from .mapstate import MapState
        return rx.call_script(
            "window.geoloc",
            callback=MapState.set_coords,
        )

    @rx.background
    async def watch_geolocation(self):
        naptime=.5
        while True:
            async with self:
                yield self.check_geolocation()
            await asyncio.sleep(naptime)

    def geolocate(self):
        return rx.call_script(scripts.geoloc_js)

    def set_place(self,lat=0,lon=0):
        place = Place.locate(lat=lat,lon=lon)
        self.place_data = place.data
    
    @rx.var
    def placename(self) -> str:
        return self.place_data.get('name','Unknown Location')

    @rx.var
    def place_json(self) -> str:
        return json.dumps({k:v for k,v in self.place_data.items() if v},indent=4)

    
