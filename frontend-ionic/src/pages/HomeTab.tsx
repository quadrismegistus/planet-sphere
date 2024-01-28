import React, { useContext } from 'react';
import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar } from '@ionic/react';
import ExploreContainer from '../components/ExploreContainer';
import './HomeTab.css';
import { LocationContext } from '../contexts/LocationContext';

const HomeTab: React.FC = () => {
  const { locations } = useContext(LocationContext);


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
        {locations && (
          <div>
            <p>City: {locations.locations[0].name}</p>
            <p>Country: {locations.locations[0].country}</p>
            <p>Coords (city): {locations.locations[0].latitude}, {locations.locations[0].longitude}</p>
          </div>
        )}
      </IonContent>
    </IonPage>
  );
};

export default HomeTab;
