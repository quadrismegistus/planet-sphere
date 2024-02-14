import { useEffect, useState, ReactNode, createContext, useContext, Dispatch, SetStateAction } from 'react';
import pako from 'pako';
import geodist from 'geodist';
import { useGeolocation } from './GeolocationProvider';
import { REACT_APP_API_URL } from '../vars';
import axios from 'axios';

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


export const defaultReverseGeocoderLocationType: ReverseGeocoderLocationType = {
    city: "",
    country: "",
    lat: 0,
    lon: 0,
    geonames_id: 0,
    distance: 0
};

    

export interface PlaceInfoType {
    adminCode1: string
    adminCodes1: {string:string}
    adminName1: string
    contained_by: PlaceInfoType[]
    countryCode: string
    countryId: string
    countryName: string
    fcl: string
    fclName: string
    fcode: string
    fcodeName: string
    geonames_id: number
    id: number
    lat: number
    lon: number
    name: string
    population: number
}

interface ReverseGeocoderContextType {
    placeInfo: PlaceInfoType | null; // Adjust according to your initial state
    chosenGeonamesId: number | null; // Or string depending on your ID type
    setChosenGeonamesId: (id: number | null) => void; // Function to update the chosenGeonamesId
    chosenPlaceInfo: PlaceInfoType | null;
    currentPlaceInfo: PlaceInfoType | null;
}

const ReverseGeocoderContext = createContext<ReverseGeocoderContextType | null>(null);




// Explicitly define the return type of the hook
const usePersistedState = (
    key: string,
    defaultValue: number | null
  ): [number | null, Dispatch<SetStateAction<number | null>>] => {
    const [state, setState] = useState<number | null>(() => {
      const storedValue = localStorage.getItem(key);
      console.log('found',storedValue,'in localStorage');
      if (storedValue !== null) {
        // Attempt to parse the stored value as an integer
        const parsedValue = parseInt(JSON.parse(storedValue), 10);
        // Return the parsed integer if it's a valid number; otherwise, fall back to defaultValue
        return !isNaN(parsedValue) ? parsedValue : defaultValue;
      }
      return defaultValue;
    });
  
    useEffect(() => {
        console.log('converting to string')
      // Convert state to string for localStorage, but ensure we're dealing with null correctly
      const valueToStore = state === null ? null : JSON.stringify(state);
      if(valueToStore) localStorage.setItem(key, valueToStore);
    }, [key, state]);
  
    return [state, setState];
  };




export const ReverseGeocoderProvider: React.FC<{children:ReactNode}> = ({ children }) => {
    const [cities, setCities] = useState<ReverseGeocoderLocationType[]>([]);
    const [placeInfo, setPlaceInfo ] = useState<PlaceInfoType|null>(null);
    const [loadingCity, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<Error | null>(null);
    const [cityInfo, setCityInfo] = useState<ReverseGeocoderLocationType>(defaultReverseGeocoderLocationType)
    const { coords, loading } = useGeolocation();
    const url = '/cities.json.gz'
    const [chosenGeonamesId, setChosenGeonamesId] = usePersistedState('chosenGeonamesId', null);
    const [chosenPlaceInfo, setChosenPlaceInfo] = useState<PlaceInfoType|null>(null);
    const [currentPlaceInfo, setCurrentPlaceInfo] = useState<PlaceInfoType|null>(null);

    console.log('chosen place id =',chosenGeonamesId)
    
    useEffect(() => {
        console.log('fetching',url);
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
        console.log('finished fetching',url);
    }, []);

    const getChosenPlaceInfo = (geonamesId:number): PlaceInfoType|undefined => {
        if(placeInfo && geonamesId) {
            const places = [placeInfo].concat(placeInfo.contained_by);
            const chosenPlaceInfo = places.find(place => place.geonames_id === geonamesId);
            return chosenPlaceInfo;
        } else {
            return undefined;
        }
    };


    useEffect(() => {
        console.log('chosenGeonamesId place changed to',chosenGeonamesId,placeInfo)

        if(placeInfo && chosenGeonamesId) {
            const chosenInfo = getChosenPlaceInfo(chosenGeonamesId);
            console.log('setting chosen place to',chosenInfo)
            if(chosenInfo) {
                setChosenPlaceInfo(chosenInfo);
                setCurrentPlaceInfo(chosenInfo);
            }
        }
    }, [chosenGeonamesId,placeInfo]);

    useEffect(() => {
        const cityInfo = findClosestLocation();
        console.log('found cityInfo,',cityInfo);
        setCityInfo(cityInfo);
    },[coords]);

    useEffect(() => {
        const fetchAndSetPlaceInfo = async () => {
            if(cityInfo && cityInfo.geonames_id) {
                const result = await fetchPlaceInfo(cityInfo.geonames_id);
                if(result!=null) {
                    setPlaceInfo(result);
                }
            }        
        };

        fetchAndSetPlaceInfo();
    }, [cityInfo]);

    const fetchPlaceInfo = async (geonames_id:number): Promise<PlaceInfoType|null> => {
        try {
            const response = await axios.get(REACT_APP_API_URL+'/places/query', { params: { geonames_id } });
            console.log('response!!',response.data);
            return response.data;
        } catch (error) {
            console.error('Failed to fetch location info:', error);
            return null;
        }
    };
    

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
        <ReverseGeocoderContext.Provider value={{placeInfo, chosenGeonamesId, setChosenGeonamesId, chosenPlaceInfo, currentPlaceInfo}}>
            {children}
        </ReverseGeocoderContext.Provider>
    );
  };

  export const useReverseGeocoder = (): ReverseGeocoderContextType => {
    const context = useContext(ReverseGeocoderContext);
    if (context === null) {
        throw new Error('useReverseGeocoder must be used within a ReverseGeocoderProvider');
    }
    return context;
};