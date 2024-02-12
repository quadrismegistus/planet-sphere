import { getDistance } from 'geolib';
import { arrowBackOutline, arrowForwardOutline, checkmarkOutline, glassesOutline, locateOutline, locationOutline, heartOutline, repeatOutline, searchOutline, locate, globeOutline } from 'ionicons/icons';
import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonModal, IonIcon, IonFooter, IonLabel, IonTabButton,IonTabBar } from '@ionic/react';
import axios from 'axios';
import 'mapbox-gl/dist/mapbox-gl.css';
import React, { useState,useEffect } from 'react';
import Map, { Marker, NavigationControl, MapRef, MapEvent, MapLayerMouseEvent, Popup, MapMouseEvent, MarkerEvent, Projection } from 'react-map-gl';
import { useGeolocation } from "./GeolocationProvider";
import {useRef, useMemo, useCallback} from 'react';
import { useModal } from './ModalProvider'
import mapboxgl from 'mapbox-gl';
import { IonButton } from '@ionic/react';
import { REACT_APP_API_URL } from '../vars'

const MAPBOX_ACCESS_TOKEN_b64 = 'cGsuZXlKMUlqb2ljbmxoYm1obGRYTmxjaUlzSW1FaU9pSmpiRzFuYmpGM2NtNHdZV2Q1TTNKelpXOXVibXB3YzJwbEluMC5PQ0ZBVlppa0JHREZTOVRlQ0F6aDB3';
const MAPBOX_ACCESS_TOKEN = atob(MAPBOX_ACCESS_TOKEN_b64);

const PROJECTION = 'lambertConformalConic';
const ZOOMOUT_ZOOM = 1;
const ZOOMIN_ZOOM = 16;



const createTimeoutManager = () => {
  let timerId: number | null = null;

  return {
    setTimeout: (callback: () => void, delay: number) => {
      if (timerId !== null) {
        clearTimeout(timerId);
      }
      timerId = window.setTimeout(callback, delay);
    },
    clearTimeout: () => {
      if (timerId !== null) {
        clearTimeout(timerId);
        timerId = null;
      }
    }
  };
};

// Usage
const timeoutManager = createTimeoutManager();



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
  const [isZoomingIn, setIsZoomingIn] = useState<boolean|null>(null)


  // Function to fetch posts
  const fetchPosts = async () => {
    try {
      const queryData = {
        type: "latest",
        seen: Array.from(readPostIds)
      };
      console.log(queryData);
      const response = await axios.post<PostObject[]>(REACT_APP_API_URL+'/posts/query', queryData);
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
      setTimeout(() => { advancePost(); }, 1000);
    }
  }, [postsLoaded, mapLoaded]);

  // Handler for advancing posts (marking as read)
  const advancePost = () => {
    console.log('advancing',postsQueue);
    if (postsQueue.length) {
      const newActivePost = postsQueue.shift();
      if (newActivePost) { 
        activatePost(newActivePost, true); 
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
        activatePost(newActivePost, true);
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

  const zoomActivePost = () => {
    if(activePost && mapRef && mapRef.current) {
      setIsZoomingIn(false);
      flyTo({lat: activePost.lat, lon:activePost.lon}, mapRef.current.getZoom()+2, 1);
    }
  }
  const unzoomActivePost = () => {
    if(activePost && mapRef && mapRef.current) {
      setIsZoomingIn(false);
      flyTo({lat: activePost.lat, lon:activePost.lon}, mapRef.current.getZoom()-2, 1);
    }
  }

  const unzoomActivePosition = () => {
    if(mapRef && mapRef.current) {
      setIsZoomingIn(true);
      flyTo(null, mapRef.current.getZoom()-1, 1);
    }
  }

  const zoomActivePosition = () => {
    if(mapRef && mapRef.current) {
      setIsZoomingIn(true);
      flyTo(null, mapRef.current.getZoom()+1, 1);
    }
  }

  const freezeMap = () => {
    if(mapRef.current){
      const map = mapRef.current.getMap(); // Get the map instance
      map.stop();
    }
  }; 

  const clickPost = (post: PostObject, event:MapLayerMouseEvent) => {
    console.log('clickPost',post,event);
    event.originalEvent.stopPropagation();
    activatePost(post);
    // Optionally move the post to the front or back of the queue
    // markPostAsSeen(post); // or similar logic as needed
  };

  const activatePost = (post:PostObject, zoomout=false) => {
    setActivePost(post);
    setPopupInfo({ lat:post.lat, lon:post.lon, content:post.content });
    // markPostAsSeen(post);
    if (zoomout) flyToZoomOut({lat:post.lat, lon:post.lon})
    else flyTo({lat:post.lat, lon:post.lon})
  };

  const flyTo = (newCoords: Coordinates|null=null, zoom:number|null=null, speed:number=0) => {
    if(mapRef.current){
      const map = mapRef.current.getMap(); // Get the map instance
      const latlng=map.getCenter()
      if(newCoords==null) newCoords={lat:latlng.lat, lon:latlng.lng}
      
      const calculateFlyToSpeed = (startCoords: Coordinates, endCoords: Coordinates): number => {
        // Calculate distance in meters
        const distance = getDistance(startCoords, endCoords);
        const maxDistanceOnEarth = 40030000; // Adjust this to control how distance affects speed
        const maxDistance = maxDistanceOnEarth / 10; // Adjust this to control how distance affects speed
        const distanceNow = distance>maxDistance ? maxDistance : distance
      
        // Define speed modulation parameters
        const maxSpeed = 2; // Maximum speed for close destinations
        const minSpeed = 0.01; // Minimum speed for distant destinations
  
        const maxZoom = 6;
        const zoomnow = map.getZoom() < maxZoom-1 ? map.getZoom()+1 : maxZoom
        
      
        // Calculate speed based on distance
        let speed = minSpeed + ((distanceNow / maxDistance) * (zoomnow/maxZoom) * (maxSpeed - minSpeed));
        
        // Ensure speed stays within defined bounds
        if (speed < minSpeed) speed = minSpeed;
        if (speed > maxSpeed) speed = maxSpeed;
      
        return speed;
      };
    
    
    
    
      const currentCoords = map.getCenter(); // Get current map center
      speed = speed ? speed : calculateFlyToSpeed({lat: currentCoords.lng, lon:currentCoords.lng}, newCoords);
      map.flyTo({
          center: [newCoords.lon, newCoords.lat],
          speed: speed,
          zoom: ((zoom!=null) ? zoom : map.getZoom())
          // curve: 1
      });
      // map.once('moveend', () => { setIsZoomingIn(null); })
    }
  };

  // const flyToZoomOut = (newCoords: Coordinates, zoom:number=0, speed:number=1) => {
  //   if(mapRef.current){
  //     timeoutManager.clearTimeout();
  //     setIsZoomingIn(false);
  //     const zoomNow = mapRef.current.getZoom()
  //     const minZoom = 3;
  //     flyTo(newCoords, zoomNow < minZoom ? minZoom : zoomNow);
  //     // mapRef.current.getMap().panTo(newCoords, {duration:1000});
  //   }
  // };
  // const flyToZoomOut = (newCoords: Coordinates, zoom:number=0, speed:number=1) => {
  //   if(mapRef.current){
  //     const map = mapRef.current.getMap()
  //     timeoutManager.clearTimeout();
  //     setIsZoomingIn(false);
  //     flyTo(null, ZOOMOUT_ZOOM, 2);
  //     timeoutManager.setTimeout(() => {
  //       flyTo(newCoords, ZOOMIN_ZOOM, .05);
  //     }, 2000);
  //   }
  // };
  const flyToZoomOut = (newCoords: Coordinates, zoom:number=0, speed:number=.5) => {
    if(mapRef.current){
      setIsZoomingIn(false);
      const zoomNow = mapRef.current.getZoom()
      const minZoom = 3;
      flyTo(newCoords, zoom ? zoom : (zoomNow>minZoom ? zoomNow : minZoom), speed);
    }
  };


  // const flyToZoomOut = (newCoords: Coordinates, zoom:number=0, speed:number=1) => {
  //   if(mapRef.current){
  //     timeoutManager.clearTimeout();
  //     const map = mapRef.current.getMap(); // Get the map instance
  //     const currentCoords = map.getCenter(); // Get current map center
  //     const zoomNow = map.getZoom()

  //     // Calculate midpoint coordinates
  //     const midCoords = {
  //       lon: (currentCoords.lng + newCoords.lon) / 2,
  //       lat: (currentCoords.lat + newCoords.lat) / 2,
  //     };
      
  //     setIsZoomingIn(false);

  //     zoom = zoom>=ZOOMOUT_ZOOM ? zoom : 4;
      
  //     const halfzoom = ((zoom - ZOOMOUT_ZOOM) / 2) + ZOOMOUT_ZOOM

  //     map.flyTo({
  //     //     // center: [midCoords.lon, midCoords.lat],
  //         center: [newCoords.lon, newCoords.lat],
  //     //     // center: [0,0],
  //     //     // essential: true // this animation is considered essential with respect to prefers-reduced-motion
  //     //     // speed: 1,
  //         speed: zoomNow/6,
  //         zoom: zoom,
  //     //     // zoom: map.getZoom()
  //         curve: 1,
  //     });
  //     // map.once('moveend', () => {
  //     //   timeoutManager.setTimeout(() => {
  //     //     map.flyTo({
  //     //       center: [newCoords.lon, newCoords.lat],
  //     //       // essential: true // this animation is considered essential with respect to prefers-reduced-motion
  //     //       speed: 2,
  //     //       zoom: zoom
  //     //     });
  //     //     map.once('moveend', () => { 
  //     //       setIsZoomingIn(true);
  //     //     });
  //     //   }, 500);
  //     // });
  //   }
  // };


  // Add event listener for keydown to advance posts
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      console.log(event.key);
      if ((event.key === 'ArrowDown') && activePost) {
        // markPostRead(activePost);
        unzoomActivePost();
        // unzoomActivePosition();
        event.stopPropagation();
      } else if ((event.key === 'ArrowRight')) {
        advancePost();
        event.stopPropagation();
      } else if ((event.key === 'ArrowLeft')) {
        regressPost();
        event.stopPropagation();
      } else if ((event.key === 'ArrowUp') && activePost) {
        zoomActivePost();
        // zoomActivePosition();
        event.stopPropagation();
      } else if ((event.key === ' ')) {
        freezeMap();
        event.stopPropagation();
      } else if ((event.key === 'Enter') && activePost) {
        markPostRead(activePost);
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
              latitude: 0, //coords.lat,
              longitude: 0, //coords.lon,
              zoom: ZOOMOUT_ZOOM,
          }}
          maxZoom={17}
          minZoom={0}
        //   viewState={{
        //     latitude: 0, //coords.lat,
        //     longitude: 0, //coords.lon,
        //     zoom: 2,
        //     width: 1000,
        //     height: 1000,
        //     bearing: 0,
        //     pitch: 0,
        //     padding: {top: 0,
        //       bottom: 0,
        //       left: 0,
        //       right: 0}
        // }}
          // mapStyle="mapbox://styles/mapbox/streets-v11"
          mapStyle="mapbox://styles/ryanheuser/clsfj542r03ey01pbexmje2us"
          // mapStyle="mapbox://styles/ryanheuser/clshu3oty018v01qrfqq00tpd"
          mapboxAccessToken={MAPBOX_ACCESS_TOKEN}
          scrollZoom={true}
          onLoad={() => setMapLoaded(true)} // Set mapLoaded to true when the map finishes loading
          // onClick={handleMapClick} // Attach the click event handler
          projection={{name:PROJECTION}} // or any other supported projection type
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
              // scale={post.size}
              onClick={(event) => clickPost(post,event)} // Add click handler to marker
            >
              {getMarkerSVG(post.size, (activePost && activePost.id==post.id) ? "red" : "blue")}
            </Marker>
          ))}
      {popupInfo && activePost && (
        <Popup
          latitude={popupInfo.lat}
          longitude={popupInfo.lon}
          closeButton={false}
          closeOnClick={true}
          offset={activePost.size * 40} // Adjust this value as needed to position the popup above the marker
          anchor="bottom" // This makes the popup's bottom edge aligned with the marker position      
          onClose={() => setPopupInfo(null)} // Reset clicked marker id on close
      >
        <div dangerouslySetInnerHTML={{ __html: popupInfo.content }} />
        </Popup>

        // <Marker latitude={activePost.lat} longitude={activePost.lon}>
        //   {getMarkerSVG(activePost.size, '#ff0')}
        // </Marker>

            )}
      </Map>



      <div className='toolbar'>
        {/* <div className='toolbtnbar'> */}
      {/* <IonToolbar className="toolbar"> */}
            <IonButton className='prevbtn' fill="clear" onClick={regressPost}>
              <IonIcon aria-hidden="true" icon={arrowBackOutline} />
              {/* <IonLabel>Prev</IonLabel> */}
            </IonButton>


            {/* <IonButton className='readbtn' fill="clear" onClick={isZoomingIn ? unzoomActivePost : zoomActivePost}>
              <IonIcon aria-hidden="true" icon={isZoomingIn ? globeOutline : locateOutline} />
            </IonButton> */}
            
            <IonButton className='readbtn' fill="clear" onClick={markActivePostRead}>
              <IonIcon aria-hidden="true" icon={repeatOutline} />
              {/* <IonLabel>Read</IonLabel> */}
            </IonButton>
            
            <IonButton className='readbtn' fill="clear" onClick={markActivePostRead}>
              <IonIcon aria-hidden="true" icon={heartOutline} />
              {/* <IonLabel>Read</IonLabel> */}
            </IonButton>

            <IonButton className='readbtn' fill="clear" onClick={markActivePostRead}>
              <IonIcon aria-hidden="true" icon={checkmarkOutline} />
              {/* <IonLabel>Read</IonLabel> */}
            </IonButton>



            
            <IonButton className='nextbtn' fill="clear" onClick={advancePost}>
              {/* <IonLabel>Next</IonLabel> */}
              <IonIcon aria-hidden="true" icon={arrowForwardOutline} />
            </IonButton>
            </div>
          {/* </IonToolbar> */}
      
          {popupInfo && (<div className="postbar" dangerouslySetInnerHTML={{ __html: popupInfo.content }} />)}
      
          {/* </div> */}
      </div>
  );
}


const getMarkerSVG = (size:number, color:string = "#ffe") => {
  return (
    // <svg height={size*50} width={size*35} viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    //   <g fill="none" stroke="#000" stroke-width="1">
    //       <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
    //       <circle cx="12" cy="9" r="1" fill="#000" />
    //   </g>
    //   <path d="M12 22s-7-7.75-7-13 3.13-7 7-7 7 3.13 7 7-7 13-7 13z" fill={color} />
    // </svg>
  <svg height={size*50} width={size*50} viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none"><path fill={color} stroke="#000" fill-rule="evenodd" d="M11.291 21.706 12 21l-.709.706zM12 21l.708.706a1 1 0 0 1-1.417 0l-.006-.007-.017-.017-.062-.063a47.708 47.708 0 0 1-1.04-1.106 49.562 49.562 0 0 1-2.456-2.908c-.892-1.15-1.804-2.45-2.497-3.734C4.535 12.612 4 11.248 4 10c0-4.539 3.592-8 8-8 4.408 0 8 3.461 8 8 0 1.248-.535 2.612-1.213 3.87-.693 1.286-1.604 2.585-2.497 3.735a49.583 49.583 0 0 1-3.496 4.014l-.062.063-.017.017-.006.006L12 21zm0-8a3 3 0 1 0 0-6 3 3 0 0 0 0 6z" clip-rule="evenodd"/></svg>
  )
}

export { MAPBOX_ACCESS_TOKEN };