import React, { createContext, useState, useEffect, ReactNode } from 'react';
import { Geolocation } from '@capacitor/geolocation';
import { featuresContaining, feature } from '@rapideditor/country-coder';
import { nearestCity, nearestCities } from 'cityjs';

// Define the type for your context state
interface LocationState {
  latitude: number,
  longitude: number,
  name: string;
  country: string;
}

class LocationStateList {
  locations: LocationState[] = [];
}


// Define the type for your context value
interface LocationContextValue {
  locations: LocationStateList | null;
}

// Creating the context with a default value
export const LocationContext = createContext<LocationContextValue>({
  locations: null
});

interface LocationProviderProps {
  children: ReactNode; // Explicitly type 'children' as ReactNode
}

interface Point {
  lat: number;
  lon: number;
}



class PolygonUtils {
  public getPolygonCentroid(vertices: number[][]): Point {
    const centroid: Point = { lat: 0, lon: 0 };
    const vertexCount: number = vertices.length;

    let area: number = 0;
    let x0: number = 0; // Current vertex X
    let y0: number = 0; // Current vertex Y
    let x1: number = 0; // Next vertex X
    let y1: number = 0; // Next vertex Y
    let a: number = 0;  // Partial signed area
    let i: number = 0; // Counter

    for (; i < vertexCount - 1; ++i) {
      x0 = vertices[i][0];
      y0 = vertices[i][1];
      x1 = vertices[i + 1][0];
      y1 = vertices[i + 1][1];

      a = x0 * y1 - x1 * y0;

      area += a;

      centroid.lon += (x0 + x1) * a;
      centroid.lat += (y0 + y1) * a;
    }

    // Do last vertex separately to avoid performing an expensive
    // modulus operation in each iteration.
    x0 = vertices[i][0];
    y0 = vertices[i][1];
    x1 = vertices[0][0];
    y1 = vertices[0][1];

    a = x0 * y1 - x1 * y0;

    area += a;
    centroid.lon += (x0 + x1) * a;
    centroid.lat += (y0 + y1) * a;
    area *= 0.5;

    centroid.lon /= (6 * area);
    centroid.lat /= (6 * area);

    return centroid;
  }
}



export const LocationProvider: React.FC<LocationProviderProps> = ({ children }) => {

  // const [location, setLocation] = useState<LocationState | null>(null);
  const [locations, setLocations] = useState<LocationStateList | null>(null);

  useEffect(() => {
    const setCurrentLocations = async () => {
      try {
        const coordinates = await Geolocation.getCurrentPosition();
        const { latitude, longitude } = coordinates.coords;
        const point = {latitude:latitude, longitude:longitude}
        const city = nearestCity(point);
        const locationList = new LocationStateList();
        locationList.locations.push({
          'name':city.name,
          'country':city.countryCode,
          'latitude':city.latitude,
          'longitude':city.longitude,
        })
        // other options
        const places = featuresContaining([longitude,latitude]);
        const utils = new PolygonUtils();
        for (const place of places) {
          const geo = place.geometry;
          if (geo) {
            const coords = geo.coordinates[0][0];
            console.log(coords);
            const props = place.properties;
            const centroid = utils.getPolygonCentroid(coords)
            console.log(centroid);
            var country = props.country;
            if (!country) { country = ''; }
            locationList.locations.push({
              'name':props.nameEn,
              'country':country,
              'latitude':centroid.lat,
              'longitude':centroid.lon,
            })
          }
        }
        setLocations(locationList);
      } catch (error) {
        console.error('Error getting location', error);
      }
    };

    setCurrentLocations();
  }, []);

  return (
    <LocationContext.Provider value={{ locations }}>
      {children}
    </LocationContext.Provider>
  );
};