import axios from 'axios';
import 'mapbox-gl/dist/mapbox-gl.css';
import React, { useState,useEffect } from 'react';
import Map, { Marker, NavigationControl, MapRef, MapEvent, MapLayerMouseEvent, Popup, MapMouseEvent, MarkerEvent } from 'react-map-gl';
import { useGeolocation } from "./GeolocationProvider";
import {useRef, useMemo, useCallback} from 'react';
import { MAPBOX_ACCESS_TOKEN } from './MapDisplay';

export function MiniMapDisplay() {
  const mapRef = useRef<MapRef|null>(null);
  const { coords, loading } = useGeolocation();

  if (loading) return <div>Loading geolocation...</div>;

  

  return (
    <div className='mapContainer'>
    <Map
        // ref={mapRef}
        initialViewState={{
            latitude: coords.lat,
            longitude: coords.lon,
            zoom: 18
        }}
        // mapStyle="mapbox://styles/mapbox/streets-v11"
        mapStyle="mapbox://styles/ryanheuser/clsfj542r03ey01pbexmje2us"
        mapboxAccessToken={MAPBOX_ACCESS_TOKEN}
        scrollZoom={true}
    >
        <NavigationControl position="top-right" />
        <Marker
            key='me'
            longitude={coords.lon}
            latitude={coords.lat}
        />
    </Map>
    </div>
  );
}

export { MAPBOX_ACCESS_TOKEN };