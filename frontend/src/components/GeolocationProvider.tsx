import React, { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import { Geolocation } from '@capacitor/geolocation';
import axios from 'axios';
import { REACT_APP_API_URL } from '../vars'

// Define the shape of your context data
interface GeolocationContextType {
  coords: {
    lat: number;
    lon: number;
  };
  loading: boolean;
  locationInfo: any; // Adjust according to the data structure you expect
}

const defaultGeolocationContext: GeolocationContextType = {
  coords: { lat: 0, lon: 0 },
  loading: true,
  locationInfo: null,
};

const GeolocationContext = createContext<GeolocationContextType>(defaultGeolocationContext);

interface GeolocationProviderProps {
  children: ReactNode;
}

export const GeolocationProvider: React.FC<GeolocationProviderProps> = ({ children }) => {
  const [coords, setCoords] = useState({ lat: 0, lon: 0 });
  const [loading, setLoading] = useState(true);
  const [locationInfo, setLocationInfo] = useState<any>(null);

  useEffect(() => {
    console.log('booting GeolocationProvider')
    // Declare an async function inside the useEffect
    const startWatchingPosition = async () => {
      const watchId = await Geolocation.watchPosition({}, (position, err) => {
        if (!err && position) {

          setCoords({
            lat: position.coords.latitude,
            lon: position.coords.longitude,
          });
          setLoading(false);

          // Fetch additional location info asynchronously
          // fetchLocationInfo(position.coords.latitude, position.coords.longitude);
        } else {
          console.error(err);
          setLoading(false);
        }
      });

      // Cleanup function
      return () => {
        Geolocation.clearWatch({ id: watchId });
      };
    };

    // Call the async function
    startWatchingPosition();
  }, []);

  
  return (
    <GeolocationContext.Provider value={{ coords, loading, locationInfo }}>
      {children}
    </GeolocationContext.Provider>
  );
};

// Hook to use geolocation context
export const useGeolocation = () => useContext(GeolocationContext);

