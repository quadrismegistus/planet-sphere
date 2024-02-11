import { Redirect, Route } from 'react-router-dom';
import {
  IonApp,
  IonHeader,
  IonPage,
  IonIcon,
  IonImg,
  IonLabel,
  IonRouterOutlet,
  IonTabBar,
  IonTabButton,
  IonTabs,
  setupIonicReact,
  IonModal,
  IonList,
  IonItem
} from '@ionic/react';
import { IonReactRouter } from '@ionic/react-router';
import { settingsOutline, personOutline, mapOutline, journalOutline, newspaperOutline } from 'ionicons/icons';
import React, {useEffect,useState} from 'react';
import MapTab from '../pages/MapTab';
import UserTab from '../pages/UserTab';
import PostTab from '../pages/PostTab';
import SettingsTab from '../pages/SettingsTab';
import { useModal } from './ModalProvider'


const TabBar: React.FC = () => {
  const { showPostModal, showLoginModal } = useModal();

  return (
    <IonReactRouter>
        <IonTabs>
          <IonRouterOutlet>
            <Route path="/" component={MapTab} exact />
          </IonRouterOutlet>

          <IonTabBar slot="top">
            
            <IonTabButton tab="logo" href="/">
              <h1 className='logo'>flatearth</h1>
            </IonTabButton>
            
            <IonTabButton tab="map" href="/">
              <IonIcon aria-hidden="true" icon={mapOutline} />
            </IonTabButton>

            <IonTabButton tab="post" onClick={showPostModal}>
              <IonIcon aria-hidden="true" icon={newspaperOutline} />
            </IonTabButton>

            <IonTabButton tab="acct" onClick={showLoginModal}>
              <IonIcon aria-hidden="true" icon={personOutline} />
            </IonTabButton>

            <IonTabButton tab="settings">
              <IonIcon aria-hidden="true" icon={settingsOutline} />
            </IonTabButton>
            
          </IonTabBar>
        </IonTabs>
      </IonReactRouter>
  );
};

export default TabBar;
