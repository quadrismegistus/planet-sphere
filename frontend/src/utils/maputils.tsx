import { Coordinates } from "../types/types";
import { getDistance } from 'geolib';
import { ReactNode } from "react";
import { MapRef, Marker } from 'react-map-gl';

export const calculateFlyToSpeed = (startCoords: Coordinates, endCoords: Coordinates, zoomNow: number): number => {
    // Calculate distance in meters
    const distance = getDistance(startCoords, endCoords);
    const maxDistanceOnEarth = 40030000; // Adjust this to control how distance affects speed
    const maxDistance = maxDistanceOnEarth / 10; // Adjust this to control how distance affects speed
    const distanceNow = distance>maxDistance ? maxDistance : distance
  
    // Define speed modulation parameters
    const maxSpeed = 2; // Maximum speed for close destinations
    const minSpeed = 0.01; // Minimum speed for distant destinations

    const maxZoom = 6;
    
  
    // Calculate speed based on distance
    let speed = minSpeed + ((distanceNow / maxDistance) * (zoomNow/maxZoom) * (maxSpeed - minSpeed));
    
    // Ensure speed stays within defined bounds
    if (speed < minSpeed) speed = minSpeed;
    if (speed > maxSpeed) speed = maxSpeed;
  
    return speed;
  };


export const flyToOnMap = ( map:MapRef, newCoords: Coordinates|null = null, zoom:number|null, speed:number = 0) => {
    const latlng=map.getCenter()
    const currentCoords = {lat:latlng.lat, lon:latlng.lng};
    const zoomNow = map.getZoom();
    if(newCoords==null) newCoords=currentCoords;
    if(!speed) {
        speed = calculateFlyToSpeed(
            currentCoords, 
            newCoords,
            zoomNow
        );
    }
    map.flyTo({
        center: [newCoords.lon, newCoords.lat],
        speed: speed,
        zoom: ((zoom!=null) ? zoom : zoomNow)
    });
  };




export function getMarkerSVG(size:number, color:string = "#ffe") {
    return <svg height={size*50} width={size*50} viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none"><path fill={color} stroke="#000" fillRule="evenodd" d="M11.291 21.706 12 21l-.709.706zM12 21l.708.706a1 1 0 0 1-1.417 0l-.006-.007-.017-.017-.062-.063a47.708 47.708 0 0 1-1.04-1.106 49.562 49.562 0 0 1-2.456-2.908c-.892-1.15-1.804-2.45-2.497-3.734C4.535 12.612 4 11.248 4 10c0-4.539 3.592-8 8-8 4.408 0 8 3.461 8 8 0 1.248-.535 2.612-1.213 3.87-.693 1.286-1.604 2.585-2.497 3.735a49.583 49.583 0 0 1-3.496 4.014l-.062.063-.017.017-.006.006L12 21zm0-8a3 3 0 1 0 0-6 3 3 0 0 0 0 6z" clipRule="evenodd"/></svg>;
}
 
interface MyLocationMarkerProps {
    coords:Coordinates|null;
}


export const MyLocationMarker: React.FC<MyLocationMarkerProps> = ({coords = null}) => {
    if(!coords) return null;

    return (
        <Marker 
            key="myloc" 
            longitude={coords.lon} 
            latitude={coords.lat}
        >
            <img src="blur.png" alt="My location" width="20em" />
        </Marker>
    );
}