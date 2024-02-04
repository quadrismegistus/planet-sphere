import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonButton } from '@ionic/react';
import ExploreContainer from '../components/ExploreContainer';
import { GeolocationDisplay } from '../components/GeolocationDisplay';
import { GeolocationProvider } from '../components/GeolocationProvider';
import './MapTab.css';


const MapTab: React.FC = () => {
  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Map</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonHeader collapse="condense">
          <IonToolbar>
            <IonTitle size="large">Mapping</IonTitle>
          </IonToolbar>
        </IonHeader>
        <ExploreContainer name="Tab 1 page" />
        <GeolocationProvider>
          <GeolocationDisplay />
        </GeolocationProvider>
        {/* <IonButton onClick={ () => printCurrentPosition() }>
          Ok?
        </IonButton> */}
      </IonContent>
    </IonPage>
  );
};

export default MapTab;