import React, { useContext } from 'react';
import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar } from '@ionic/react';
import ExploreContainer from '../components/ExploreContainer';
import './HomeTab.css';
import { LocationContext } from '../contexts/LocationContext';

const HomeTab: React.FC = () => {
  const { location } = useContext(LocationContext);


  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Home</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonHeader collapse="condense">
          <IonToolbar>
            <IonTitle size="large">Home</IonTitle>
          </IonToolbar>
        </IonHeader>
        <ExploreContainer name="Home page" />
        {location && (
          <div>
            <p>City: {location.city}</p>
            <p>Country: {location.country}</p>
            <p>Coords (city): {location.latitude}, {location.longitude}</p>
          </div>
        )}
      </IonContent>
    </IonPage>
  );
};

export default HomeTab;
