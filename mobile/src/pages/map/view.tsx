
import React from 'react';
import GoogleMapReact from 'google-map-react';
import {
  IonPage, IonContent, IonHeader, IonToolbar, IonButtons, IonMenuButton, IonTitle, IonText, IonButton, IonItem, IonLabel, IonSpinner
} from '@ionic/react';
import './styles.css';
const AnyReactComponent = () => (
  <div style={{
    color: 'white', background: 'red', padding: '10px', display: 'inline-flex', textAlign: 'center', alignItems: 'center', justifyContent: 'center', borderRadius: '100%', transform: 'translate(-80%, -100%)'
  }}>
    <div className="pointer">
    </div>
  </div>
);
const HomeView = (props: any) => {
  const { center, getGeoLocation, loading } = props
  return (
    <>
      <IonPage id='main'>
        <IonHeader>
          <IonToolbar color='dark'>
            <IonButtons slot='start'>
              <IonMenuButton ></IonMenuButton>
            </IonButtons>
            <IonTitle slot="start">Map Geolocation</IonTitle>
          </IonToolbar>
        </IonHeader>
        <IonContent>
          {loading && <div className="full-content">
            <IonSpinner name="lines" />
          </div>}
          {!loading && <div className="GeoMap">
            <GoogleMapReact
              bootstrapURLKeys={{ key: 'AIzaSyCgfF7O8nBILgyGcSDlmuhBbHy9vArxTyY' }}
              defaultCenter={center}
              defaultZoom={16}
            >
              <AnyReactComponent />
            </GoogleMapReact>
          </div>}
          <IonItem className='geoAbs'>
            <IonLabel>
              <IonText>lat={center.lat}</IonText>
              <IonText> lng={center.lon}</IonText>
            </IonLabel>
          </IonItem>
          <IonButton onClick={getGeoLocation} className='geoFooter'>Get Current Location</IonButton>
        </IonContent>
      </IonPage>
    </>
  )
}
export default HomeView