import { useEffect, useState, ReactNode, createContext, useContext, Dispatch, SetStateAction } from 'react';
import pako from 'pako';
import geodist from 'geodist';
import { useGeolocation } from './GeolocationProvider';
import { REACT_APP_API_URL } from '../vars';
import axios from 'axios';
import { Place, ReverseGeocoderContextType, ReverseGeocoderPlace } from '../types/types';
import { usePersistedState } from '../utils/persistence';



const ReverseGeocoderContext = createContext<ReverseGeocoderContextType | null>(null);

export const ReverseGeocoderProvider: React.FC<{children:ReactNode}> = ({ children }) => {
    const url = '/cities.json.gz'
    const [cities, setCities] = useState<ReverseGeocoderPlace[]>([]);
    const [placeInfo, setPlaceInfo ] = useState<Place|null>(null);
    const [loadingCity, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<Error | null>(null);
    const [cityInfo, setCityInfo] = useState<ReverseGeocoderPlace|null>(null);
    const { coords, loading } = useGeolocation();
    const [chosenGeonamesId, setChosenGeonamesId] = usePersistedState('chosenGeonamesId', null);
    const [chosenPlaceInfo, setChosenPlaceInfo] = useState<Place|null>(null);
    const [currentPlaceInfo, setCurrentPlaceInfo] = useState<Place|null>(null);

    // Hook for loading data
    // -> cities
    useEffect(() => {
        console.log('fetching', url);
    
        // IIFE to handle the async operation
        (async () => {
            try {
                const response = await axios.get<ReverseGeocoderPlace[]>(url);
                if (response.data) setCities(response.data);
            } catch (error:any) {
                console.error("Error fetching city data:", error);
                setError(error.toString());
            }
        })(); // Immediately invoke the async function
    }, []);

    // Hook for finding closest city
    // coords -> cityInfo
    useEffect(() => {
        if(cities && coords && coords.lat && coords.lon && cities.length) {
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
            
            const cityInfo = closestLocation;
            console.log('found cityInfo,',cityInfo);
            setCityInfo(cityInfo);
        }
    },[coords]);
    
    // Hook for getting place info on city
    // cityInfo -> placeInfo
    useEffect(() => {
        (async () => {
            if(cityInfo && cityInfo.geonames_id) {
                const response = await axios.get<Place>(REACT_APP_API_URL+'/places/query', { 
                    params: { geonames_id: cityInfo.geonames_id } 
                });
                const place = response.data;
                if(place) {
                    setPlaceInfo(place);
                    setCurrentPlaceInfo(place);
                }
            }        
        })();
    }, [cityInfo]);

    // Hook for updating chosen place place
    // placeInfo,chosenGeonamesId -> chosenPlaceInfo
    useEffect(() => {
        console.log('chosenGeonamesId place changed to',chosenGeonamesId,placeInfo)

        if(placeInfo && chosenGeonamesId) {
            const places = [placeInfo].concat(placeInfo.contained_by);
            const chosenInfo = places.find(place => place.geonames_id === chosenGeonamesId);
            if(chosenInfo) {
                console.log('setting chosen place to',chosenInfo)
                setChosenPlaceInfo(chosenInfo);
                setCurrentPlaceInfo(chosenInfo);
            }
        }
    }, [chosenGeonamesId,placeInfo]);


    return (
        <ReverseGeocoderContext.Provider value={{placeInfo, chosenGeonamesId, setChosenGeonamesId, chosenPlaceInfo, currentPlaceInfo}}>
            {children}
        </ReverseGeocoderContext.Provider>
    );
  };

  
  export const useReverseGeocoder = (): ReverseGeocoderContextType => {
    const context = useContext(ReverseGeocoderContext);
    if (context === null)
        throw new Error('useReverseGeocoder must be used within a ReverseGeocoderProvider');
    return context;
};