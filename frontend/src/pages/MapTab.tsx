import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonButton, IonModal, IonIcon, IonFooter } from '@ionic/react';
import ExploreContainer from '../components/ExploreContainer';
import { GeolocationDisplay } from '../components/GeolocationDisplay';
import { MapDisplay } from '../components/MapDisplay';
import PostModal from '../components/PostModal';
import LoginModal from '../components/LoginModal';
import { GeolocationProvider } from '../components/GeolocationProvider';
import './MapTab.css';
import { arrowBackOutline, arrowForwardOutline } from 'ionicons/icons';



const MapTab: React.FC = () => {

  return (
    <IonPage>
      <IonContent fullscreen>
          <MapDisplay />
          <PostModal />
          <LoginModal />

      </IonContent>
    </IonPage>
  );
};

export default MapTab;