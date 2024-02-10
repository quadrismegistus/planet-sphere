import 'mapbox-gl/dist/mapbox-gl.css';
import React, { useState,useEffect } from 'react';
import Map, { Marker, NavigationControl, MapRef, MapEvent, MapLayerMouseEvent, Popup, MapMouseEvent, MarkerEvent } from 'react-map-gl';
import { useGeolocation } from "./GeolocationProvider";
import {useRef, useMemo, useCallback} from 'react';
import mapboxgl from 'mapbox-gl';

const MAPBOX_ACCESS_TOKEN_b64 = 'cGsuZXlKMUlqb2ljbmxoYm1obGRYTmxjaUlzSW1FaU9pSmpiRzFuYmpGM2NtNHdZV2Q1TTNKelpXOXVibXB3YzJwbEluMC5PQ0ZBVlppa0JHREZTOVRlQ0F6aDB3';
const MAPBOX_ACCESS_TOKEN = atob(MAPBOX_ACCESS_TOKEN_b64);

interface MarkerDatum {
  id: string
  lat: number
  lon: number
  content: string
}

interface Coordinates {
  lat: number;
  lon: number;
};

export function MapDisplay() {
  const markerRef = useRef<mapboxgl.Marker | null>(null);
  const mapRef = useRef<MapRef|null>(null);
  const [markers, setMarkers] = useState<MarkerDatum[]>([]);
  const { coords, loading } = useGeolocation();
  const [clickedMarkerId, setClickedMarkerId] = useState<string>();


  // Assuming flyTo is a function that pans the map to new coordinates
  useEffect(() => {
    mapRef.current?.flyTo({
      center: [coords.lon, coords.lat],
      zoom: 3,
    });
  }, [coords]); // Depend on coords to re-run when coords change


  const popup = useMemo(() => {
    return new mapboxgl.Popup().setText('Hello world!');
  }, [])

  const togglePopup = useCallback(() => {
    markerRef.current?.togglePopup();
  }, []);

  // Function to generate random markers
  const generateRandomMarkers = (count: number) => {
    const newMarkers: MarkerDatum[] = Array.from({ length: count }, (_, index) => ({
      id: `marker-${index}`,  
      // Assuming the map is global, adjust the range as needed
      lat: Math.random() * 180 - 90, // Latitude range -90 to 90
      lon: Math.random() * 360 - 180, // Longitude range -180 to 180
      content: "Hello <b>world</b>."
    }));
    setMarkers(newMarkers);
  };

  // Effect to generate markers on component mount
  useEffect(() => {
    generateRandomMarkers(10); // Generate 10 random markers
  }, []);

  // // Function to add a marker
  // const addMarker = (longitude, latitude) => {
  //   const newMarker = { longitude, latitude };
  //   setMarkers([...markers, newMarker]);
  // };x

  // Handler for map click event
  const handleMapClick = (event: MapLayerMouseEvent) => {
    // Perform flyTo using the map instance
    mapRef.current?.flyTo({
      center: event.lngLat,
      zoom: 3,
      speed: 1, // Adjust the flying speed
    });
  };

  const handleMarkerClick = (marker: MarkerDatum, event:MapLayerMouseEvent) => {
    // Prevent the map click event from firing when a marker is clicked
    event.originalEvent?.stopPropagation();
    setClickedMarkerId(marker.id);
  };

  const flyTo = (newCoords: Coordinates) => {
    if(mapRef.current){
      const map = mapRef.current.getMap(); // Get the map instance
      map.flyTo({
          center: [newCoords.lon, newCoords.lat],
          essential: true // this animation is considered essential with respect to prefers-reduced-motion
      });
    }
  };



  if (loading) return <div>Loading geolocation...</div>;

  

  return (
      <Map
          ref={mapRef}
          initialViewState={{
              latitude: coords.lat,
              longitude: coords.lon,
              zoom: 2
          }}
          style={{width: '100%', height: '100%'}}
          // mapStyle="mapbox://styles/mapbox/streets-v11"
          mapStyle="mapbox://styles/ryanheuser/clsfj542r03ey01pbexmje2us"
          mapboxAccessToken={MAPBOX_ACCESS_TOKEN}
          scrollZoom={true}
          // onClick={handleMapClick} // Attach the click event handler
      >
          <NavigationControl position="top-right" />
          {/* <Marker longitude={coords.lon} latitude={coords.lat} anchor="bottom" popup={popup} ref={markerRef} scale={.5} /> */}
          
          {markers.map((marker, index) => (
            <Marker
              key={marker.id} // Use unique id for key, not index
              longitude={marker.lon}
              latitude={marker.lat}
              onClick={(event) => handleMarkerClick(marker, event)} // Add click handler to marker
            >
            {clickedMarkerId === marker.id && (

                <Popup
                latitude={marker.lat}
                longitude={marker.lon}
                closeButton={true}
                closeOnClick={true}
                anchor="top"
                onClose={() => setClickedMarkerId("")} // Reset clicked marker id on close
              >
                {/* {marker.content} */}
                <div dangerouslySetInnerHTML={{ __html: marker.content }} />
                </Popup>
            )}

            </Marker>
          ))}
      </Map>
  );
}



// import {
//   useIonViewDidEnter,
// } from '@ionic/react';
// import { Marker, Popup, MapContainer, TileLayer, useMap } from 'react-leaflet'
// import { useGeolocation } from "./GeolocationProvider";

// // const ShowLocation: React.FC = () => {
// export function MapDisplay() {
//     useIonViewDidEnter(() => {
//       window.dispatchEvent(new Event('resize'));
//     });
    
//     const { coords, loading } = useGeolocation();
//     if (loading) return <div>Loading geolocation...</div>;
  
//     return (
//       <MapContainer
//         center={{ lat: coords.lat, lng: coords.lon }}
//         zoom={2}
//         id="map"
//         scrollWheelZoom={false}>
//         <TileLayer
//           attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
//           url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
//         />
//       </MapContainer>
//     );
// }
