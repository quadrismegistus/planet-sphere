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
import { postsQueueState, activePostState } from '../entities/timelineEnts';
import { useTextareaWithLimit } from '../utils/utils';

const PostModal: React.FC = () => {
    const { postIsOpen, hidePostModal, showLoginModal } = useModal();
    const { user } = useAuth();
    const { chosenGeonamesId } = useReverseGeocoder();
    const { value, charsRemaining, handleChange } = useTextareaWithLimit(360);
    const [errormsg, SetErrormsg] = useState('');
    
    useEffect(() => {
        if(!user && postIsOpen) {
            console.log('redirecting to login')
            showLoginModal();
        }
    }, [postIsOpen,user]);

    const handleSubmit = async (event:React.FormEvent) => {
      if(!user) return

      try {
        const message = {
            access_token:user.accessToken,
            post_txt: value,
            geonames_id:chosenGeonamesId,
          };
          console.log('message',message);
          const response = await axios.post(REACT_APP_API_URL+'/users/post', message);
          const newPostInfo = response.data;
          postsQueueState.set(oldPosts => [newPostInfo, ...oldPosts]);
          activePostState.set(newPostInfo);
          hidePostModal();
      } catch (error:any) {
        SetErrormsg(error.toString())
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
      <div className='error'>{errormsg}</div>
      </IonContent>
      </IonModal>
  );
}

export default PostModal;
