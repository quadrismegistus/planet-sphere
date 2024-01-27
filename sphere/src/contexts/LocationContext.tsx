import React, { createContext, useState, useEffect, ReactNode } from 'react';
import { Geolocation } from '@capacitor/geolocation';
import { featuresContaining, feature } from '@rapideditor/country-coder';
import { nearestCity, nearestCities } from 'cityjs';

// Define the type for your context state
interface LocationState {
  latitude: number,
  longitude: number,
  city: string;
  country: string;
}

// Define the type for your context value
interface LocationContextValue {
  location: LocationState | null;
}

// Creating the context with a default value
export const LocationContext = createContext<LocationContextValue>({
  location: null
});

interface LocationProviderProps {
  children: ReactNode; // Explicitly type 'children' as ReactNode
}

export const LocationProvider: React.FC<LocationProviderProps> = ({ children }) => {

  const [location, setLocation] = useState<LocationState | null>(null);

  useEffect(() => {
    const setCurrentLocation = async () => {
      try {
        const coordinates = await Geolocation.getCurrentPosition();
        const { latitude, longitude } = coordinates.coords;
        const point = {latitude:latitude, longitude:longitude}
        const city = nearestCity(point);
        console.log(city);

        const places = featuresContaining([longitude,latitude]);
        

        setLocation({
          latitude: city.latitude,
          longitude: city.longitude,
          city: city.name,
          country: city.countryCode
        });
      } catch (error) {
        console.error('Error getting location', error);
      }
    };

    setCurrentLocation();
  }, []);

  return (
    <LocationContext.Provider value={{ location }}>
      {children}
    </LocationContext.Provider>
  );
};