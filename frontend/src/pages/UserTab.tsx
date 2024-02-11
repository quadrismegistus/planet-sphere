import { useAuth } from '../components/Authentication'; // Adjust the import path as needed
import { authenticate } from '../components/Authentication';
import React, { useEffect, useState } from 'react';
import {
    IonContent,
    IonHeader,
    IonTitle,
    IonToolbar,
    IonPage,
    useIonViewDidEnter,
    useIonViewDidLeave,
    useIonViewWillEnter,
    useIonViewWillLeave,
    IonLabel,
    IonItem,
    IonInput,
    IonButton
  } from '@ionic/react';
import { useHistory } from 'react-router-dom';






const UserTab: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const { login, logout, user } = useAuth();


  const history = useHistory();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(username, password);
      // Redirect is handled within the login function
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "An unknown error occurred";
      setErrorMessage(errorMessage);
    }
  };

  const handleLogout = async () => {
    logout();
  };

  // const accessToken = localStorage.getItem('accessToken');
  // const userToken = localStorage.getItem('username');

  useEffect(() => {
    setErrorMessage("");
  }, [username, password]);


    return (
        <IonPage>
        <IonContent className="ion-padding">
        {!user ? (

            <form onSubmit={handleLogin}>
            <IonItem>
                {/* <IonLabel position="floating">Username</IonLabel> */}
                <IonInput value={username} onIonChange={e => setUsername(e.detail.value!)} required type="text" label="Username"></IonInput>
            </IonItem>
            <IonItem>
                <IonInput value={password} onIonChange={e => setPassword(e.detail.value!)} required type="password" label="Password"></IonInput>
            </IonItem>
            {errorMessage && <div className='error'>{errorMessage}</div>}
            <IonButton expand="block" type="submit" className="ion-margin-top">
                Login / register
            </IonButton>
        </form>
        ) : (
                     // Logged in, show different content or redirect
          <div>
          <p>You are logged in, {user.username}!</p>

          <IonButton onClick={logout} type="submit">log out</IonButton>
          {/* You can add more user-specific content here or redirect the user */}
        </div>
        )}
        </IonContent>
        </IonPage>
    );
}

export default UserTab;
