import { Component, createContext, useContext, ReactNode } from 'react';
import { Geolocation } from '@capacitor/geolocation';

// Create a context
// Define the shape of your context data
interface GeolocationContextType {
    coords: {
      lat: number;
      lon: number;
    };
    loading: boolean;
  }
  
// Provide a default value matching the context type
const defaultGeolocationContext: GeolocationContextType = {
    coords: {
        lat: 0,
        lon: 0,
    },
    loading: true, // Assuming true as default; adjust as needed
};

// Create the context with the default value
const GeolocationContext = createContext<GeolocationContextType>(defaultGeolocationContext);


// Extend props type to include children
interface GeolocationProviderProps {
    children: ReactNode;
  }
  
export class GeolocationProvider extends Component<GeolocationProviderProps> {
    state: GeolocationContextType = {
        coords: {
            lat: 0,
            lon: 0,
        },
        loading: true,
    };

    watchId?: string;

    componentDidMount() {
        Geolocation.watchPosition({}, (position, err) => {
        if (!err && position) {
            console.log(position);
            this.setState({
            coords: {
                lat: position.coords.latitude,
                lon: position.coords.longitude,
            },
            loading: false,
            });
        } else {
            // Handle the error case
            console.error(err); // For demonstration; in a real application, handle errors appropriately
            this.setState({ loading: false });
        }
        });
    }

    componentWillUnmount() {
        if (this.watchId) {
        Geolocation.clearWatch({ id: this.watchId });
        }
    }

    render() {
        const { children } = this.props;
        return (
        <GeolocationContext.Provider value={this.state}>
            {children}
        </GeolocationContext.Provider>
        );
    }
}

// Hook to use geolocation context
export const useGeolocation = () => useContext(GeolocationContext);

