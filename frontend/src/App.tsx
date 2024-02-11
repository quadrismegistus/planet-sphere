import 'leaflet/dist/leaflet.css';
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
  setupIonicReact
} from '@ionic/react';
import { IonReactRouter } from '@ionic/react-router';
import { settingsOutline, personOutline, mapOutline, journalOutline, newspaperOutline } from 'ionicons/icons';
import React, {useEffect} from 'react';
import MapTab from './pages/MapTab';
import UserTab from './pages/UserTab';
import PostTab from './pages/PostTab';
import SettingsTab from './pages/SettingsTab';
// import HomeContainer from './components/geoloc/container';
// import Tab3 from './pages/Tab3';
import './App.css';

/* Core CSS required for Ionic components to work properly */
import '@ionic/react/css/core.css';

/* Basic CSS for apps built with Ionic */
import '@ionic/react/css/normalize.css';
import '@ionic/react/css/structure.css';
import '@ionic/react/css/typography.css';

/* Optional CSS utils that can be commented out */
import '@ionic/react/css/padding.css';
import '@ionic/react/css/float-elements.css';
import '@ionic/react/css/text-alignment.css';
import '@ionic/react/css/text-transformation.css';
import '@ionic/react/css/flex-utils.css';
import '@ionic/react/css/display.css';

/* Theme variables */
import './theme/variables.css';

setupIonicReact();

const App: React.FC = () => {
  useEffect(() => {
    // Function to toggle dark mode
    const toggleDarkMode = (matches: boolean) => {
      document.body.classList.toggle('dark', matches);
    };

    // Create MediaQueryList object
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

    // Initial check
    toggleDarkMode(prefersDark.matches);

    // Listen for changes
    prefersDark.addEventListener('change', (e) => toggleDarkMode(e.matches));

    // Clean up
    return () => {
      prefersDark.removeEventListener('change', (e) => toggleDarkMode(e.matches));
    };
  }, []);

  const toggleDarkMode = () => {
    document.body.classList.toggle('dark');
  };


  return (
    <IonApp>
      <IonReactRouter>
        <IonTabs>
          <IonRouterOutlet>
            <Route path="/map" component={MapTab} exact />
            <Route path="/acct" component={UserTab} exact />
            <Route path="/post" component={PostTab} exact />
            <Route path="/settings" component={SettingsTab} exact />
            <Route exact path="/" render={() => <Redirect to="/map" />} />
          </IonRouterOutlet>

          <IonTabBar slot="top">
            
            <IonTabButton tab="logo" href="/">
              <h1 className='logo'>flatearth</h1>
            </IonTabButton>
            
            <IonTabButton tab="map" href="/map">
              <IonIcon aria-hidden="true" icon={mapOutline} />
            </IonTabButton>
            
            <IonTabButton tab="acct" href="/acct">
              <IonIcon aria-hidden="true" icon={personOutline} />
            </IonTabButton>
            
            <IonTabButton tab="post" href="/post">
              <IonIcon aria-hidden="true" icon={newspaperOutline} />
            </IonTabButton>

            <IonTabButton tab="settings" href="/settings">
              <IonIcon aria-hidden="true" icon={settingsOutline} />
            </IonTabButton>
            
          </IonTabBar>
        </IonTabs>
      </IonReactRouter>
    </IonApp>
  );
}
export default App;
