import { authenticate } from '../components/Authentication';
import React, { useState } from 'react';
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

  const history = useHistory();

  const login = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await authenticate(username, password);
      history.push('/acct');
    } catch (error) {
      alert('Authentication failed!');
      console.log(error);
    }
  };

  const logout = async () => {
    localStorage.setItem('accessToken','');
    localStorage.setItem('username','');
    history.push('/acct');
  };

  const accessToken = localStorage.getItem('accessToken');
  const userToken = localStorage.getItem('username');


    return (
        <IonPage>
        <IonContent className="ion-padding">
        {!accessToken ? (

            <form onSubmit={login}>
            <IonItem>
                {/* <IonLabel position="floating">Username</IonLabel> */}
                <IonInput value={username} onIonChange={e => setUsername(e.detail.value!)} required type="text" label="Username"></IonInput>
            </IonItem>
            <IonItem>
                <IonInput value={password} onIonChange={e => setPassword(e.detail.value!)} required type="password" label="Password"></IonInput>
            </IonItem>
            <IonButton expand="block" type="submit" className="ion-margin-top">
                Login / register
            </IonButton>
        </form>
        ) : (
                     // Logged in, show different content or redirect
          <div>
          <p>You are logged in, {userToken}!</p>

          <IonButton onClick={logout} type="submit">log out</IonButton>
          {/* You can add more user-specific content here or redirect the user */}
        </div>
        )}
        </IonContent>
        </IonPage>
    );
}

export default UserTab;
