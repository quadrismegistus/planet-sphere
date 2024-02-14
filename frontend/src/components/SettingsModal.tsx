import { IonContent, IonHeader, IonTitle, IonToolbar, IonButton, IonInput, IonItem, IonLabel } from '@ionic/react';
import { useModal } from './ModalProvider';
import React, { useState, useEffect, ReactNode } from 'react';
import {
    IonModal,
  } from '@ionic/react';
import { useReverseGeocoder } from './ReverseGeocoder';
import LocationSelect from './LocationSelect'

const SettingsModal: React.FC = () => {
    const { settingsIsOpen, hideSettingsModal, showSettingsModal } = useModal();
    
    return (
        <IonModal isOpen={settingsIsOpen} onDidDismiss={hideSettingsModal} className="side-modal">
            <IonHeader>
                <IonToolbar>
                    <IonTitle>Settings</IonTitle>
                </IonToolbar>
            </IonHeader>
          <IonContent className="ion-padding">
            <LocationSelect />
          </IonContent>
        </IonModal>
    );
}

export default SettingsModal;
