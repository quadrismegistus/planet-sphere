import { useGeolocation } from "./GeolocationProvider";

// const ShowLocation: React.FC = () => {
export function GeolocationDisplay() {
    const { coords, loading } = useGeolocation();
    if (loading) return <div>Loading geolocation...</div>;
  
    return (
      <div>
        Current Location: Latitude {coords.lat}, Longitude {coords.lon}
      </div>
    );
}
