import { useEffect, useState, ReactNode, createContext, useContext } from 'react';
import pako from 'pako';
import geodist from 'geodist';
import { useGeolocation } from './GeolocationProvider';

interface City {
  lat: number;
  lon: number;
  city: string;
  // other properties as needed
}

export interface ReverseGeocoderLocationType {
    city: string;
    country: string;
    lat: number
    lon: number
    geonames_id: number
    distance: number
}

export interface ReverseGeocoderContextType {
    cityInfo: any
}

export const defaultReverseGeocoderLocationType: ReverseGeocoderLocationType = {
    city: "",
    country: "",
    lat: 0,
    lon: 0,
    geonames_id: 0,
    distance: 0
};

export const defaultReverseGeocoderContextType: ReverseGeocoderContextType = {
    cityInfo:defaultReverseGeocoderLocationType
}
    
export const ReverseGeocoderContext = createContext<ReverseGeocoderContextType>(defaultReverseGeocoderContextType);


export const ReverseGeocoderProvider: React.FC<{children:ReactNode}> = ({ children }) => {
    const [cities, setCities] = useState<ReverseGeocoderLocationType[]>([]);
    const [loadingCity, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<Error | null>(null);
    const [cityInfo, setCityInfo] = useState<ReverseGeocoderLocationType>(defaultReverseGeocoderLocationType)
    const { coords, loading } = useGeolocation();
    const url = '/cities.json.gz'

    
    useEffect(() => {
        fetch(url)
        .then((response) => {
            if (!response.ok) {
            throw new Error(`Network response was not ok for ${url}`);
            }
            return response.json();
        })
        .then((jsonData) => {
            setCities(jsonData);
        })
        .catch((err) => {
            setError(err);
        })
        .finally(() => {
            setLoading(false);
        });
    }, []);

    useEffect(() => {
        const cityInfo = findClosestLocation();
        console.log('found cityInfo,',cityInfo);
        setCityInfo(cityInfo);
    },[coords]);


    const findClosestLocation = () => {
        console.log('cities',coords);
        if(coords && coords.lat && coords.lon && cities.length) {
            let closestLocation = cities[0];
            let shortestDistance = Infinity;
        
            cities.forEach((city) => {
            const distance = geodist(
                { lat: coords.lat, lon: coords.lon },
                { lat: city.lat, lon: city.lon },
                { exact: true, unit: 'kilometers' }
            );
        
            if (distance < shortestDistance) {
                shortestDistance = distance;
                closestLocation = city;
            }
            });
        
            closestLocation['distance'] = shortestDistance;
            return closestLocation;
        } else {
            return defaultReverseGeocoderLocationType;
        }
    }
      
    
    if (error) console.log(error);
  
    return (
        <ReverseGeocoderContext.Provider value={{ cityInfo }}>
            {children}
        </ReverseGeocoderContext.Provider>
    );
  };

export const useReverseGeocoder = () => useContext(ReverseGeocoderContext);
