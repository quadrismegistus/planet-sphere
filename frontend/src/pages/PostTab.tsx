import { authenticate } from '../components/Authentication';
import React, { useState, useEffect } from 'react';
import {
    IonContent,
    IonPage,
    useIonViewWillEnter,
  } from '@ionic/react';
import { useHistory, useLocation } from 'react-router-dom';


const PostTab: React.FC = () => {
    const history = useHistory();
    const location = useLocation(); // Get the current location
    const [username, setUsername] = useState('');

    useIonViewWillEnter(() => {
        checkAuth();
    });

    // useEffect(() => {
    //   // Assuming you store the access token in localStorage
    //   console.log('running')
    //   const accessToken = localStorage.getItem('accessToken');
    //   const username = localStorage.getItem('username');
    //   if (!accessToken || !username) {
    //     // Redirect to the login page if no access token is found
    //     history.push('/acct');
    //   } else {
    //     setUsername(username);
    //   }
    // }, [location.pathname]); // Dependency array includes `history` to ensure effect uses the latest value

    const checkAuth = () => {
        console.log('Checking auth status');
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          // Redirect to the login page if no access token is found
          console.log('No access token found, redirecting to /acct');
          history.push('/acct');
        } else {
          const storedUsername = localStorage.getItem('username');
          if (storedUsername) {
            setUsername(storedUsername);
          }
        }
      };

    
  
    return (
        <IonPage>
        <IonContent className="ion-padding">
        {username && (
            <div>hello {username}</div>
        )}
        </IonContent>
        </IonPage>
    );
}

export default PostTab;
