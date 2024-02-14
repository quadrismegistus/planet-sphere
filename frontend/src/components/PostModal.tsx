import { IonContent, IonHeader, IonModal, IonTitle, IonToolbar, IonButton, IonInput, IonItem, IonLabel, IonTextarea, TextareaCustomEvent, IonIcon } from '@ionic/react';
import { useModal } from './ModalProvider';
import { useAuth } from './Authentication';
import React, { useState, useEffect } from 'react';
import { useReverseGeocoder } from './ReverseGeocoder';
import LocationSelect from './LocationSelect';
import './PostModal.css';
import { closeOutline } from 'ionicons/icons';
import { REACT_APP_API_URL } from '../vars';
import axios from 'axios';

// Custom hook for handling textarea with character limit
function useTextareaWithLimit(limit = 360) {
  const [value, setValue] = useState('');

  // Calculate the number of characters remaining
  const charsRemaining = limit - value.length;

  // Update the state value when the user types in the textarea
  const handleChange = (event: TextareaCustomEvent) => {
    if(event.target.value!=undefined) setValue(event.target.value);
  };

  return { value, charsRemaining, handleChange };
}

const PostModal: React.FC = () => {
    const { postIsOpen, hidePostModal, showPostModal, showLoginModal } = useModal();
    const { user } = useAuth();
    const { chosenGeonamesId } = useReverseGeocoder();
    const { value, charsRemaining, handleChange } = useTextareaWithLimit(360);


    useEffect(() => {
        if(!user && postIsOpen) {
            console.log('redirecting to login')
            showLoginModal();
        }
    }, [postIsOpen,user]);

    const handleSubmit = async (event:React.FormEvent) => {
      if(!user) return

      try {
          const response = await axios.post(REACT_APP_API_URL+'/login', {
            username: user.username,
            access_token:user.accessToken,
            geonames_id:chosenGeonamesId
          });
          console.log('posted:',response.data);
      } catch (error) {
        // Handle any errors, such as showing login failure messages
        throw error;
      }
    };

    return (
      <IonModal isOpen={postIsOpen} onDidDismiss={hidePostModal} className="side-modal">
      <IonHeader>
      <IonToolbar>
         
        <IonIcon aria-hidden="true" icon={closeOutline} onClick={hidePostModal} />

        <IonTitle>
          Post {user && (<span> as {user.username}</span>)}
        </IonTitle>
        
        </IonToolbar>
      </IonHeader>
      <IonContent className="ion-padding">
      <IonTextarea
        autofocus={false}
        label="post:"
        rows={10}
        // style={{borderBottom:'none', height:'300px'}}
        maxlength={360}
        value={value}
        helperText={"Characters remaining: ".concat(charsRemaining.toString()).concat('/360')}
        onIonInput={handleChange}
      />
      <LocationSelect label="from:" />
      <IonButton type='submit' fill='clear' style={{float:'right'}} onClick={handleSubmit}>Post</IonButton>        
      </IonContent>
      </IonModal>
  );
}

export default PostModal;
