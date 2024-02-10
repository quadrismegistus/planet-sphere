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
  id: number
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
  id: number;
  lat: number;
  lon: number;
  content: string
}


export function MapDisplay() {
  const markerRef = useRef<mapboxgl.Marker | null>(null);
  const mapRef = useRef<MapRef|null>(null);
  const [markers, setMarkers] = useState<MarkerDatum[]>([]);
  const { coords, loading } = useGeolocation();
  const [clickedMarkerId, setClickedMarkerId] = useState<number>();
  // State to manage the active popup and its content
  const [activePopup, setActivePopup] = useState<PopupState>({lat:0, lon:0, content:''});
  const [showPopup, setShowPopup] = useState(false);
  const [posts, setPosts] = useState<PostObject[]>([]);
  const [currentPostIndex, setCurrentPostIndex] = useState<number>(0);
  const [currentPostId, setCurrentPostId] = useState<number>(0);
  const [readPostIds, setReadPostIds] = useState<Set<number>>(new Set());


  // Handler for arrow key press to navigate between places
  const handleKeyPress = (event: KeyboardEvent) => {
    if (event.key === 'ArrowLeft') {
      // Go to the previous place
      // setCurrentPostIndex((prevIndex) => (prevIndex > 0 ? prevIndex - 1 : posts.length - 1));
      advancePostIndex();
    } else if (event.key === 'ArrowRight') {
      // Go to the next place
      advancePostIndex();
      // setCurrentPostIndex((prevIndex) => (prevIndex + 1) % posts.length);
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
      setCurrentPostId(post.id);
    }
  }, [posts,currentPostIndex]);

  // Handler for map click event
  const handleMapClick = (event: MapLayerMouseEvent) => {
    // Perform flyTo using the map instance
    flyTo({lat:event.lngLat.lat, lon:event.lngLat.lng})
  };

  const advancePostIndex = () => {
    setCurrentPostIndex((prevIndex) => {
      let nextIndex = prevIndex;
      do {
        // Move to the next index or loop back to the start if at the end of the array
        nextIndex = nextIndex < posts.length - 1 ? nextIndex + 1 : 0;
        // Check if the next index is not in readPostIds
      } while (readPostIds.has(posts[nextIndex].id) && nextIndex !== prevIndex);
      
      // Return the next index if it's not read, or return the current index if all posts are read
      return nextIndex;
    });
  }

  const setActiveMarker = (id:number) => {
    const post = posts[id];
    setClickedMarkerId(post.id);
    setActivePopup({content: post.content, lat:post.lat, lon:post.lon});
    setShowPopup(true);
  }

  const handleMarkerClick = (marker: MarkerDatum, event:MapLayerMouseEvent) => {
    event.originalEvent?.stopPropagation();
    // console.log('marker',marker);
    // setClickedMarkerId(marker.id);
    setActivePopup({content: marker.content, lat:marker.lat, lon:marker.lon});
    flyTo({lat:marker.lat, lon:marker.lon});
    // setShowPopup(true);
    // console.log('done')
    console.log(marker);
    // setActiveMarker(currentPostIndex);
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
      console.log('fetching posts')
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

      // setPosts(sortedData); // Set the places in state
      setPosts((prevPlaces) => {
        // Merge prevPlaces and sortedData
        const mergedArray = [...prevPlaces, ...sortedData];
        
        // Filter out duplicates based on post.id, preserving the first occurrence of each id
        const uniquePosts = mergedArray.filter((post, index, self) => 
          index === self.findIndex((findPost) => (
            findPost.id === post.id
          ))
        );
      
        return uniquePosts;
      });
    } catch (error) {
      console.error('Error fetching places', error);
    }
  };

  // Fetch places on component mount
  useEffect(() => {
    fetchPosts();
  }, []);

  // Handle keydown event
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'ArrowDown') {
        // setShowPopup(false);
        // setPosts((prevPlaces) => prevPlaces.filter((_, index) => index !== currentPostIndex));
        // Optionally, move to the next place or reset to the first if at the end
        const post = posts[currentPostIndex];
        setReadPostIds(new Set(readPostIds).add(post.id));
        setCurrentPostIndex((prevIndex) => prevIndex < posts.length - 1 ? prevIndex + 1 : 0);
        setActiveMarker(currentPostIndex);
        console.log(readPostIds, currentPostIndex);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [posts, currentPostIndex]);

  // Check for remaining unread posts and fetch more if needed
  useEffect(() => {
    const unreadCount = posts.filter(post => !readPostIds.has(post.id)).length;
    console.log(posts.length, unreadCount,'lengths')
    const threshold = 5; // For example, fetch more when only 5 unread markers are left
    if (unreadCount <= threshold) {
      // fetchPosts();
    }
  }, [posts, readPostIds]);


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
          onClick={handleMapClick} // Attach the click event handler
      >
          <NavigationControl position="top-right" />
          {/* <Marker longitude={coords.lon} latitude={coords.lat} anchor="bottom" popup={popup} ref={markerRef} scale={.5} /> */}
          
          {posts.map((marker,index) => 
            !readPostIds.has(marker.id) && (
            <Marker
              key={'marker-' + marker.id.toString() +'-'+index.toString()} // Use unique id for key, not index
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
