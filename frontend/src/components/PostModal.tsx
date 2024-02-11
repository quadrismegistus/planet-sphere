import { IonContent, IonHeader, IonTitle, IonToolbar, IonButton, IonInput, IonItem, IonLabel } from '@ionic/react';
import { useModal } from './ModalProvider';
import { useAuth } from './Authentication';
import { GeolocationProvider, useGeolocation } from './GeolocationProvider';
import { MAPBOX_ACCESS_TOKEN } from './MapDisplay';
import Map, { Marker, NavigationControl, MapRef, MapEvent, MapLayerMouseEvent, Popup, MapMouseEvent, MarkerEvent } from 'react-map-gl';
import React, { useState, useEffect, useRef } from 'react';
import {
    IonModal,
    IonPage,
    useIonViewWillEnter,
  } from '@ionic/react';
import { useHistory, useLocation } from 'react-router-dom';
import './PostModal.css';
import { MiniMapDisplay } from './MiniMap';
import LoginModal from './LoginModal';


const PostModal: React.FC = () => {
    const { postIsOpen, hidePostModal, showPostModal, showLoginModal } = useModal();
    const { user } = useAuth();
    const { coords, loading, locationInfo } = useGeolocation();

    useEffect(() => {
        if(!user && postIsOpen) {
            showLoginModal();
        }
    }, [postIsOpen,user]);

    return (
        <IonModal isOpen={postIsOpen} onDidDismiss={hidePostModal}className="side-modal">
        <IonHeader>
        <IonToolbar>
          <IonTitle>Post {user && locationInfo && (<span>from {locationInfo["city"]}</span>)}</IonTitle>
        </IonToolbar>
      </IonHeader>
        {user && locationInfo && (
          <IonContent className="ion-padding">
            {locationInfo["name"]}
          </IonContent>
        )}
        </IonModal>
    );
}

export default PostModal;
