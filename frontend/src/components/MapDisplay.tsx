import { arrowBackOutline, arrowForwardOutline, checkmarkOutline, repeatOutline, heartOutline } from 'ionicons/icons';
import { IonIcon } from '@ionic/react';
import React, { useState,useEffect,useRef } from 'react';
import Map, { Marker, MapRef, MapLayerMouseEvent } from 'react-map-gl';
import { useGeolocation } from "./GeolocationProvider";
import { useModal } from './ModalProvider'
import { IonButton } from '@ionic/react';
import { PostObject, Place } from '../types/types'
import { PostPopup, PostMarker } from './Post';
import { useReverseGeocoder } from './ReverseGeocoder';
import { useTimeline } from './TimelineProvider';
import { SHOW_POPUPS, ZOOMIN_ZOOM, ZOOMOUT_ZOOM, MAPBOX_ACCESS_TOKEN, PROJECTION } from '../vars';
import { flyToOnMap, MyLocationMarker } from '../utils/maputils';
import 'mapbox-gl/dist/mapbox-gl.css';
import { MapToolbar } from './MapToolbar';
import { countSubstring } from '../utils/utils'
import { activePostState, postsQueueState, postsLoadedState, postsQueueIndexState } from '../entities/timelineEnts';


export const MapDisplay: React.FC = () => {
  const mapRef = useRef<MapRef|null>(null);
  const { coords, loading } = useGeolocation();
  const { activatePost, getNextPost, getPrevPost, markPostRead } = useTimeline();
  const [ mapLoaded, setMapLoaded] = useState(false);
  const { postIsOpen } = useModal();
  const { currentPlaceInfo } = useReverseGeocoder();
  
  const activePost = activePostState.use();
  const postsQueue = postsQueueState.use();
  const postsQueueIndex = postsQueueIndexState.use();
  const postsLoaded = postsLoadedState.use();

  // hook to listen to keys
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if ((event.key === 'ArrowDown') && activePost) { unzoomActivePost(); event.stopPropagation(); }
      if ((event.key === 'ArrowRight')) { console.log('right'); event.stopPropagation(); advancePost();  }
      if ((event.key === 'ArrowLeft')) { regressPost(); event.stopPropagation(); }
      if ((event.key === 'ArrowUp') && activePost) { zoomActivePost(); event.stopPropagation(); }
      if ((event.key === ' ')) { freezeMap(); event.stopPropagation(); }
      if ((event.key === 'Enter') && activePost) { markPostRead(activePost); event.stopPropagation(); }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);


  // fly to current place if post open
  useEffect(() => { 
    if(postIsOpen && currentPlaceInfo) {
      flyToPlace(currentPlaceInfo)
    }
  }, [postIsOpen,currentPlaceInfo]);

  // fly to current post
  useEffect(() => { 
    if(activePost) {
      console.log('activePost changed, flying there now:',activePost);
      flyToPost(activePost)
    }
  }, [activePost]);

  // Handler for advancing posts (marking as read)
  const advancePost = () => { 
    const next = getNextPost(); 
    console.log('advancing post',next); 
};
  const regressPost = () => { 
    const prev = getPrevPost(); 
    console.log('regressing post',prev); 
};
  const markActivePostRead = () => { 
    if(activePost) { markPostRead(activePost) } 
  }

  const zoomActivePost = () => { 
    if(activePost && mapRef.current) flyToPost(activePost, mapRef.current.getZoom()+1, 1); 
  }
  const unzoomActivePost = () => { 
    if(activePost && mapRef.current) flyToPost(activePost, mapRef.current.getZoom()-1, 1); 
  }
  const freezeMap = () => { 
    if(mapRef.current) mapRef.current.getMap().stop(); 
  }; 

  const clickPost = (post: PostObject, event:MapLayerMouseEvent) => {
    console.log('clickPost',post,event);
    event.originalEvent.stopPropagation();
    activatePost(post);
  };

  const flyToPost = (post:PostObject|undefined, zoom:number|undefined = undefined, speed:number=0) => {
    if(mapRef.current && post && post.place) {
      console.log('flying to post:',post);
      flyToPlace(post.place);
    }
  };

  const flyToPlace = (place:Place|undefined, zoom:number|undefined = undefined, speed:number=1) => {
    if(place && mapRef.current) {
      console.log('flying to place:',place);
      flyToOnMap(
        mapRef.current, 
        {lat:place.lat, lon:place.lon},
        zoom !== undefined ? zoom : countSubstring(place.long_name,', ')*2,
        speed
      );
    }
  }

  


  return (
      <div className='mapContainer'>
      <Map
          ref={mapRef}
          key='bigmap'
          initialViewState={{
              latitude: 0,
              longitude: 0,
              zoom: ZOOMOUT_ZOOM,
          }}
          maxZoom={ZOOMIN_ZOOM}
          minZoom={ZOOMOUT_ZOOM}
          mapStyle="mapbox://styles/ryanheuser/clsfj542r03ey01pbexmje2us"
          mapboxAccessToken={MAPBOX_ACCESS_TOKEN}
          scrollZoom={true}
          onLoad={() => setMapLoaded(true)}
          projection={{name:PROJECTION}}
      >
          <MyLocationMarker coords = {coords} />
          {postsQueue.map((post,index) => 
            <PostMarker key={post.id.toString()} post={post} activePost={activePost} clickPost={clickPost} />
          )}
      {SHOW_POPUPS && activePost && (<PostPopup key={'post-popup-'.concat(activePost.id.toString())} post={activePost} />)}
      </Map>

      <MapToolbar regressPost={regressPost} advancePost={advancePost} markActivePostRead={markActivePostRead} />
    </div>
  );
}