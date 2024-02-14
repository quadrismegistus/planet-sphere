import 'leaflet/dist/leaflet.css';
import { Redirect, Route } from 'react-router-dom';
import {
  IonApp,
  setupIonicReact,
} from '@ionic/react';
import React, {useEffect} from 'react';
import { ModalProvider } from './components/ModalProvider'
import { ReverseGeocoderProvider } from './components/ReverseGeocoder'
import { GeolocationProvider } from './components/GeolocationProvider';
import TabBar from './components/TabBar'
import { AuthProvider } from './components/Authentication';

// css
import './App.css';
import '@ionic/react/css/core.css';
import '@ionic/react/css/normalize.css';
import '@ionic/react/css/structure.css';
import '@ionic/react/css/typography.css';
import '@ionic/react/css/padding.css';
import '@ionic/react/css/float-elements.css';
import '@ionic/react/css/text-alignment.css';
import '@ionic/react/css/text-transformation.css';
import '@ionic/react/css/flex-utils.css';
import '@ionic/react/css/display.css';
import './theme/variables.css';

setupIonicReact();

const App: React.FC = () => {

  useEffect(() => {
    console.log('booting App')
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
      <AuthProvider>
        <GeolocationProvider>
          <ReverseGeocoderProvider>
            <ModalProvider>
              <TabBar />
            </ModalProvider>
          </ReverseGeocoderProvider>
        </GeolocationProvider>
      </AuthProvider>
    </IonApp>
  );
}
export default App;
