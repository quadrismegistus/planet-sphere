import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar } from '@ionic/react';
import ExploreContainer from '../components/ExploreContainer';
import './PostTab.css';

const PostTab: React.FC = () => {
  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Post</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonHeader collapse="condense">
          <IonToolbar>
            <IonTitle size="large">Post</IonTitle>
          </IonToolbar>
        </IonHeader>
        <ExploreContainer name="Post page" />
      </IonContent>
    </IonPage>
  );
};

export default PostTab;
