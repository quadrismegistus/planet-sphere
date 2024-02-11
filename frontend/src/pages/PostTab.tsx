import { authenticate } from '../components/Authentication';
import { GeolocationProvider, useGeolocation } from '../components/GeolocationProvider';
import { MAPBOX_ACCESS_TOKEN } from '../components/MapDisplay';
import Map, { Marker, NavigationControl, MapRef, MapEvent, MapLayerMouseEvent, Popup, MapMouseEvent, MarkerEvent } from 'react-map-gl';
import React, { useState, useEffect, useRef } from 'react';
import {
    IonContent,
    IonPage,
    useIonViewWillEnter,
  } from '@ionic/react';
import { useHistory, useLocation } from 'react-router-dom';
import './PostTab.css';
import { MiniMapDisplay } from '../components/MiniMap';


const PostTab: React.FC = () => {
    const history = useHistory();
    const [username, setUsername] = useState('');
    const mapRef = useRef<MapRef|null>(null);
    const { coords, loading } = useGeolocation();

    useIonViewWillEnter(() => {
        checkAuth();
    });

    const checkAuth = () => {
        console.log('Checking auth status');
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          // Redirect to the login page if no access token is found
          console.log('No access token found, redirecting to /acct');
          history.push('/acct');
        } else {
          const storedUsername = localStorage.getItem('username');
          if (storedUsername) {
            setUsername(storedUsername);
          }
        }
      };

    if(!username) { return <IonPage></IonPage>; }
  
    return (
        // <IonPage>
        // <IonContent className="ion-padding">
        // <MiniMapDisplay />
        // </IonContent>
        // </IonPage>
        <div>hello</div>
    );
}

export default PostTab;
