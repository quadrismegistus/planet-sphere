import { arrowBackOutline, arrowForwardOutline, checkmarkOutline } from 'ionicons/icons';
import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonModal, IonIcon, IonFooter, IonLabel, IonTabButton,IonTabBar } from '@ionic/react';
import axios from 'axios';
import 'mapbox-gl/dist/mapbox-gl.css';
import React, { useState,useEffect } from 'react';
import Map, { Marker, NavigationControl, MapRef, MapEvent, MapLayerMouseEvent, Popup, MapMouseEvent, MarkerEvent } from 'react-map-gl';
import { useGeolocation } from "./GeolocationProvider";
import {useRef, useMemo, useCallback} from 'react';
import { useModal } from './ModalProvider'
import mapboxgl from 'mapbox-gl';
import { IonButton } from '@ionic/react';

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
  size: number;
  content: string
}


export function MapDisplay() {
  const mapRef = useRef<MapRef|null>(null);
  const { coords, loading } = useGeolocation();
  const [readPostIds, setReadPostIds] = useState<Set<number>>(new Set());
  const [postsQueue, setPostsQueue] = useState<PostObject[]>([]);
  const [activePost, setActivePost] = useState<PostObject | null>(null);
  const [popupInfo, setPopupInfo] = useState<PopupState|null>(null);
  const [postsLoaded, setPostsLoaded] = useState(false);
  const [mapLoaded, setMapLoaded] = useState(false);
  const { postIsOpen } = useModal();


  // Function to fetch posts
  const fetchPosts = async () => {
    try {
      const queryData = {
        type: "latest",
        seen: Array.from(readPostIds)
      };
      console.log(queryData);
      const response = await axios.post<PostObject[]>(process.env.API_URL+'/posts/query', queryData);
      console.log(response);
      const uniqueNewPosts = response.data.filter(post => !postsQueue.some(existingPost => existingPost.id === post.id));
      console.log('new',uniqueNewPosts);
      setPostsQueue(prevPosts => [...prevPosts, ...uniqueNewPosts]);
      setPostsLoaded(true); // Indicate posts have been loaded
    } catch (error) {
      console.error('Error fetching posts', error);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  // Call advancePost once both the map and posts have loaded
  useEffect(() => {
    if (postsLoaded && mapLoaded) {
      advancePost();
    }
  }, [postsLoaded, mapLoaded]);

  // Handler for advancing posts (marking as read)
  const advancePost = () => {
    console.log('advancing',postsQueue);
    if (postsQueue.length) {
      const newActivePost = postsQueue.shift();
      if (newActivePost) { 
        activatePost(newActivePost); 
        setPostsQueue(postsQueue => [...postsQueue, newActivePost]);
      }
    } else {
      setActivePost(null);
      setPopupInfo(null);
    }
  };

  // Handler for moving posts backwards (marking the last as unread and moving it to the front)
  const regressPost = () => {
    console.log('regressing', postsQueue);
    if (postsQueue.length) {
      const newActivePost = postsQueue.pop(); // Remove the last element
      if (newActivePost) {
        activatePost(newActivePost);
        // Add the post back to the start of the queue
        setPostsQueue(postsQueue => [newActivePost, ...postsQueue]);
      }
    } else {
      setActivePost(null);
      setPopupInfo(null);
    }
  };

  // useEffect(() => {
  //   flyTo(coords, 17, .2);
  // }, [postIsOpen]);

  const markPostRead = (post: PostObject) => {
    console.log('marking post read',post);
    
    console.log(readPostIds);
    console.log(postsQueue);
    setPopupInfo(null);
    
      // Update readPostIds with the new post ID
    setReadPostIds(prev => {
      const updatedReadPostIds = new Set(prev);
      updatedReadPostIds.add(post.id);
      console.log(updatedReadPostIds);

      // Immediately use the updatedReadPostIds for filtering
      setPostsQueue(postsQueue => postsQueue.filter(p => !updatedReadPostIds.has(p.id)));
      advancePost();
      
      // Proceed with updating the state
      return updatedReadPostIds;
    });
  };

  const markActivePostRead = () => {
    console.log("hello");
    if(activePost) markPostRead(activePost);
  }

  const clickPost = (post: PostObject, event:MapLayerMouseEvent) => {
    console.log('clickPost',post,event);
    event.originalEvent.stopPropagation();
    activatePost(post);
    // Optionally move the post to the front or back of the queue
    // markPostAsSeen(post); // or similar logic as needed
  };

  const activatePost = (post:PostObject) => {
    setActivePost(post);
    setPopupInfo({ lat:post.lat, lon:post.lon, content:post.content });
    // markPostAsSeen(post);
    flyTo({lat:post.lat, lon:post.lon})
  };



  const flyTo = (newCoords: Coordinates, zoom:number=0, speed:number=.5) => {
    if(mapRef.current){
      const map = mapRef.current.getMap(); // Get the map instance
      // map.setCenter([newCoords.lon, newCoords.lat]);
      map.flyTo({
          center: [newCoords.lon, newCoords.lat],
          // essential: true // this animation is considered essential with respect to prefers-reduced-motion
          speed: speed,
          zoom: zoom ? zoom : map.getZoom()
      });
    }
  };


  // Add event listener for keydown to advance posts
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if ((event.key === 'ArrowDown') && activePost) {
        markPostRead(activePost);
        event.stopPropagation();
      } else if ((event.key === 'ArrowRight')) {
        advancePost();
        event.stopPropagation();
      }


    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [activePost, postsQueue]);

  // Effect to fetch more posts when needed
  useEffect(() => {
    const unreadCount = postsQueue.length;
    if (unreadCount <= 10) { // Threshold
      fetchPosts();
    }
  }, [postsQueue]);

  // if (loading) return <div>Loading geolocation...</div>;

  

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
          onLoad={() => setMapLoaded(true)} // Set mapLoaded to true when the map finishes loading
          // onClick={handleMapClick} // Attach the click event handler
      >
          {/* <NavigationControl position="top-right" /> */}
          {/* <Marker longitude={coords.lon} latitude={coords.lat} anchor="bottom" popup={popup} ref={markerRef} scale={.5} /> */}
          <Marker key="myloc" longitude={coords.lon} latitude={coords.lat}>
          <img
            src="blur.png"
            alt="My location"
            width="20em"
          />
          </Marker>
          {postsQueue.map((post,index) => !readPostIds.has(post.id) && (
            <Marker
              // key={post.id.toString()+'-'+index.toString()} // Use unique id for key, not index
              key={post.id.toString()+'-'+index.toString()} // Use unique id for key, not index
              longitude={post.lon}
              latitude={post.lat}
              scale={post.size}
              onClick={(event) => clickPost(post,event)} // Add click handler to marker
            />
          ))}
      {popupInfo && (
        <Popup
          latitude={popupInfo.lat}
          longitude={popupInfo.lon}
          closeButton={false}
          closeOnClick={true}
          anchor="top"
          onClose={() => setPopupInfo(null)} // Reset clicked marker id on close
      >
        <div dangerouslySetInnerHTML={{ __html: popupInfo.content }} />
        </Popup>
            )}
      </Map>

      <div className='toolbar'>
      {/* <IonToolbar className="toolbar"> */}
            <IonButton className='prevbtn' fill="clear" onClick={regressPost}>
              <IonIcon aria-hidden="true" icon={arrowBackOutline} />
              <IonLabel>Prev</IonLabel>
            </IonButton>
            <IonButton className='readbtn' fill="clear" onClick={markActivePostRead}>
              <IonIcon aria-hidden="true" icon={checkmarkOutline} />
              <IonLabel>Read</IonLabel>
            </IonButton>
            <IonButton className='nextbtn' fill="clear" onClick={advancePost}>
              <IonLabel>Next</IonLabel>

              <IonIcon aria-hidden="true" icon={arrowForwardOutline} />
            </IonButton>
            </div>
          {/* </IonToolbar> */}
      

      </div>
  );
}

export { MAPBOX_ACCESS_TOKEN };