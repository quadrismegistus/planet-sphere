import React, { useState, useEffect } from 'react';
import { IonContent, IonHeader, IonTitle, IonToolbar, IonModal, IonButton, IonInput, IonItem, IonLabel } from '@ionic/react';
import { useAuth } from './Authentication'; // Adjust the import path as needed
import { useModal } from './ModalProvider';

// const LoginModal: React.FC<{ isOpen: boolean; onClose: () => void; }> = ({ isOpen, onClose }) => {
const LoginModal: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const { login, user, logout } = useAuth();
  const { loginIsOpen, hideLoginModal, showLoginModal } = useModal();{}

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(username, password);
      hideLoginModal();
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "An unknown error occurred";
      setErrorMessage(errorMessage);
    }
  };

  // Reset error message whenever username or password changes
  useEffect(() => {
    console.log('resetting LoginModal error message')
    setErrorMessage("");
  }, [username, password]);

  return (
    <IonModal isOpen={loginIsOpen} onDidDismiss={hideLoginModal} className='side-modal'>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Login</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent className="ion-padding">
        {!user ? (
        <form onSubmit={handleLogin}>
          <IonItem>
            <IonInput value={username} onIonChange={e => setUsername(e.detail.value!)} required type="text" label="username"></IonInput>
          </IonItem>
          <IonItem>
            <IonInput value={password} onIonChange={e => setPassword(e.detail.value!)} required type="password" label="password"></IonInput>
          </IonItem>
          {errorMessage && <div className="error">{errorMessage}</div>}
          <IonButton expand="block" type="submit" className="ion-margin-top">
            Login / Register  
          </IonButton>
        </form>
        ) : (
            <div>
              <div>Congrats</div>
            <IonButton expand="block" type="submit" className="ion-margin-top" onClick={logout}>
            log out
          </IonButton>
          </div>
        )}
      </IonContent>
    </IonModal>
  );
};

export default LoginModal;
