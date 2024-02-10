import axios from 'axios';
import 'mapbox-gl/dist/mapbox-gl.css';
import React, { useState,useEffect } from 'react';
import Map, { Marker, NavigationControl, MapRef, MapEvent, MapLayerMouseEvent, Popup, MapMouseEvent, MarkerEvent } from 'react-map-gl';
import { useGeolocation } from "./GeolocationProvider";
import {useRef, useMemo, useCallback} from 'react';
import mapboxgl from 'mapbox-gl';

const MAPBOX_ACCESS_TOKEN_b64 = 'cGsuZXlKMUlqb2ljbmxoYm1obGRYTmxjaUlzSW1FaU9pSmpiRzFuYmpGM2NtNHdZV2Q1TTNKelpXOXVibXB3YzJwbEluMC5PQ0ZBVlppa0JHREZTOVRlQ0F6aDB3';
const MAPBOX_ACCESS_TOKEN = atob(MAPBOX_ACCESS_TOKEN_b64);

interface MarkerDatum {
  id: string
  lat: number
  lon: number
  content: string
}

interface PopupState {
  content: string
  lat: number
  lon: number
}

interface Coordinates {
  lat: number;
  lon: number;
};

interface PostObject {
  id: string;
  lat: number;
  lon: number;
  content: string
}


export function MapDisplay() {
  const markerRef = useRef<mapboxgl.Marker | null>(null);
  const mapRef = useRef<MapRef|null>(null);
  const [markers, setMarkers] = useState<MarkerDatum[]>([]);
  const { coords, loading } = useGeolocation();
  const [clickedMarkerId, setClickedMarkerId] = useState<string>();
  // State to manage the active popup and its content
  const [activePopup, setActivePopup] = useState<PopupState>({lat:0, lon:0, content:''});
  const [showPopup, setShowPopup] = useState(false);
  const [posts, setPosts] = useState<PostObject[]>([]);
  const [currentPostIndex, setCurrentPostIndex] = useState<number>(0);


  // Handler for arrow key press to navigate between places
  const handleKeyPress = (event: KeyboardEvent) => {
    if (event.key === 'ArrowLeft') {
      // Go to the previous place
      setCurrentPostIndex((prevIndex) => (prevIndex > 0 ? prevIndex - 1 : posts.length - 1));
    } else if (event.key === 'ArrowRight') {
      // Go to the next place
      setCurrentPostIndex((prevIndex) => (prevIndex + 1) % posts.length);
    }
  };

  // Add event listener on component mount and cleanup on unmount
  useEffect(() => {
    window.addEventListener('keydown', handleKeyPress);

    return () => {
      window.removeEventListener('keydown', handleKeyPress);
    };
  }, [posts.length]); // Rerun when places.length changes

  // Effect to fly to a new place when currentPlaceIndex changes
  useEffect(() => {
    const post = posts[currentPostIndex];
    if (post && mapRef.current) {
      flyTo({lat:post.lat, lon:post.lon})
      setActiveMarker(currentPostIndex);
      // mapRef.current.flyTo({
      //   center: [place.lon, place.lat],
      //   zoom: 10,
      //   speed: 1,
      //   curve: 1,
      //   essential: true,
      //   // transitionInterpolator: new FlyToInterpolator(),
      // });
    }
  }, [currentPostIndex, posts]);


  // Assuming flyTo is a function that pans the map to new coordinates
  // useEffect(() => {
  //   mapRef.current?.flyTo({
  //     center: [coords.lon, coords.lat],
  //     zoom: 3,
  //   });
  // }, [coords]); // Depend on coords to re-run when coords change


  // Handler for map click event
  const handleMapClick = (event: MapLayerMouseEvent) => {
    // Perform flyTo using the map instance
    mapRef.current?.flyTo({
      center: event.lngLat,
      zoom: 3,
      speed: 1, // Adjust the flying speed
    });
  };

  const handleMarkerClick1 = (marker: MarkerDatum, event:MapLayerMouseEvent) => {
    // Prevent the map click event from firing when a marker is clicked
    event.originalEvent?.stopPropagation();
    setClickedMarkerId(marker.id);
  };

  const setActiveMarker = (id:number) => {
    const marker = posts[id];
    setClickedMarkerId(marker.id);
    setActivePopup({content: marker.content, lat:marker.lat, lon:marker.lon});
    setShowPopup(true);
  }

  const handleMarkerClick = (marker: MarkerDatum, event:MapLayerMouseEvent) => {
    event.originalEvent?.stopPropagation();
    setClickedMarkerId(marker.id);
    setActivePopup({content: marker.content, lat:marker.lat, lon:marker.lon});
    setShowPopup(true);
    console.log('done')
    
    // try {
    //   // Fetch data from the server
    //   const response = await fetch(`http://localhost:8000/place/${marker.lat}/${marker.lon}`);
    //   const result = await response.json();
    //   console.log('result',result);
      
    //   // Update the active popup content and position
    //   setClickedMarkerId(marker.id);
    //   setActivePopup({content: result.name, lat:result.lat, lon:result.lon});
    //   console.log('popup',activePopup);
    //   setShowPopup(true); // Show the popup
    // } catch (error) {
    //   console.error('Error fetching place data', error);
    // }
  };

  const flyTo = (newCoords: Coordinates) => {
    if(mapRef.current){
      const map = mapRef.current.getMap(); // Get the map instance
      map.flyTo({
          center: [newCoords.lon, newCoords.lat],
          // essential: true // this animation is considered essential with respect to prefers-reduced-motion
          speed:1
      });
    }
  };

  // Function to fetch places from the server
  const fetchPosts = async () => {
    try {
      const response = await axios.get<PostObject[]>('http://localhost:8000/posts/latest');
      
      // Example of sorting the response data
      const sortedData = response.data.sort((a, b) => {
        // First, compare by latitude
        if (a.lat < b.lat) return -1;
        if (a.lat > b.lat) return 1;

        // If the latitudes are equal, then sort by longitude
        if (a.lon < b.lon) return -1;
        if (a.lon > b.lon) return 1;

        // If both latitude and longitude are equal, return 0 (no sorting)
        return 0;
      });

      setPosts(sortedData); // Set the places in state
    } catch (error) {
      console.error('Error fetching places', error);
    }
  };

  // Fetch places on component mount
  useEffect(() => {
    fetchPosts();
  }, []);


  if (loading) return <div>Loading geolocation...</div>;

  

  return (
      <div className='mapContainer'>
      <Map
          ref={mapRef}
          initialViewState={{
              latitude: coords.lat,
              longitude: coords.lon,
              zoom: 2
          }}
          // mapStyle="mapbox://styles/mapbox/streets-v11"
          mapStyle="mapbox://styles/ryanheuser/clsfj542r03ey01pbexmje2us"
          mapboxAccessToken={MAPBOX_ACCESS_TOKEN}
          scrollZoom={true}
          // onClick={handleMapClick} // Attach the click event handler
      >
          <NavigationControl position="top-right" />
          {/* <Marker longitude={coords.lon} latitude={coords.lat} anchor="bottom" popup={popup} ref={markerRef} scale={.5} /> */}
          
          {posts.map((marker, index) => (
            <Marker
              key={marker.id} // Use unique id for key, not index
              longitude={marker.lon}
              latitude={marker.lat}
              onClick={(event) => handleMarkerClick(marker, event)} // Add click handler to marker
            >
            {(clickedMarkerId==marker.id) && showPopup && (

                <Popup
                latitude={activePopup.lat}
                longitude={activePopup.lon}
                closeButton={true}
                closeOnClick={true}
                anchor="top"
                onClose={() => setClickedMarkerId("")} // Reset clicked marker id on close
              >
                {/* {marker.content} */}
                <div dangerouslySetInnerHTML={{ __html: activePopup.content }} />
                {/* {activePopup.content} */}
                </Popup>
            )}

            </Marker>
          ))}
      </Map>
      </div>
  );
}



// import {
//   useIonViewDidEnter,
// } from '@ionic/react';
// import { Marker, Popup, MapContainer, TileLayer, useMap } from 'react-leaflet'
// import { useGeolocation } from "./GeolocationProvider";

// // const ShowLocation: React.FC = () => {
// export function MapDisplay() {
//     useIonViewDidEnter(() => {
//       window.dispatchEvent(new Event('resize'));
//     });
    
//     const { coords, loading } = useGeolocation();
//     if (loading) return <div>Loading geolocation...</div>;
  
//     return (
//       <MapContainer
//         center={{ lat: coords.lat, lng: coords.lon }}
//         zoom={2}
//         id="map"
//         scrollWheelZoom={false}>
//         <TileLayer
//           attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
//           url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
//         />
//       </MapContainer>
//     );
// }
