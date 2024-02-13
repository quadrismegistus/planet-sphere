import { IonContent, IonHeader, IonTitle, IonToolbar, IonButton, IonInput, IonItem, IonLabel } from '@ionic/react';
import { useModal } from './ModalProvider';
import React, { useState, useEffect, useRef } from 'react';
import {
    IonModal,
  } from '@ionic/react';
import { useReverseGeocoder,ReverseGeocoderLocationType, defaultReverseGeocoderLocationType } from './ReverseGeocoder';
import { useGeolocation } from './GeolocationProvider';

const LocationModal: React.FC = () => {
    const { locationIsOpen, hideLocationModal, showLocationModal } = useModal();
    const { cityInfo } = useReverseGeocoder();
    const { coords, loading } = useGeolocation();

    return (
        <IonModal isOpen={locationIsOpen} onDidDismiss={hideLocationModal} className="side-modal">
            <IonHeader>
                <IonToolbar>
                    <IonTitle>Location</IonTitle>
                </IonToolbar>
            </IonHeader>
        {/* {cityInfo && cityInfo.cityInfo && cityInfo.cityInfo.city && ( */}
          <IonContent className="ion-padding">
            {cityInfo && cityInfo.city && (
              <div>The closest city to you is {cityInfo.city}, {cityInfo.country}, about {Math.round(cityInfo.distance)} km away. Geonames ID = {cityInfo.geonames_id}.</div>
            )}
          </IonContent>
        {/* )} */}
        </IonModal>
    );
}

export default LocationModal;
