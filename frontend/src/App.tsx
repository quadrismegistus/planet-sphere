import 'leaflet/dist/leaflet.css';
import { Redirect, Route } from 'react-router-dom';
import {
  IonApp,
  IonHeader,
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
import { settingsOutline, personOutline, mapOutline, moonOutline } from 'ionicons/icons';
import React, {useEffect} from 'react';
import MapTab from './pages/MapTab';
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
            <Route exact path="/map">
              <MapTab />
            </Route>
            {/* <Route exact path="/tab2">
              <HomeContainer />
            </Route> */}
            {/* <Route path="/tab3">
              <Tab3 />
            </Route> */}
            <Route exact path="/">
              <Redirect to="/map" />
            </Route>
          </IonRouterOutlet>
          <IonTabBar slot="top">
            <IonTabButton tab="tab1" href="/map">
              <h1 className='logo'>flatearth</h1>
            </IonTabButton>
            <IonTabButton tab="tab1" href="/map">
              <IonIcon aria-hidden="true" icon={mapOutline} />
              {/* <IonLabel>Tab 1</IonLabel> */}
            </IonTabButton>
            <IonTabButton tab="tab2" href="/me">
              <IonIcon aria-hidden="true" icon={personOutline} />
              {/* <IonLabel>Tab 2</IonLabel> */}
            </IonTabButton>
            <IonTabButton tab="tab3" href="/settings">
              <IonIcon aria-hidden="true" icon={settingsOutline} />
              {/* <IonLabel>Tab 3</IonLabel> */}
            </IonTabButton>
          </IonTabBar>
        </IonTabs>
      </IonReactRouter>
    </IonApp>
  );
}
export default App;
