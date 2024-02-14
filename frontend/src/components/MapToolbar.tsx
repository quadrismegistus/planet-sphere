import { IonIcon, IonButton } from '@ionic/react';
import React, {} from 'react';
import { arrowBackOutline, arrowForwardOutline, checkmarkOutline, repeatOutline, heartOutline } from 'ionicons/icons';

export interface MapToolbarProps {
    regressPost: () => void;
    markActivePostRead: () => void;
    advancePost: () => void;
  }

function dflt() { };

export const MapToolbar: React.FC<MapToolbarProps> = ({regressPost = dflt, advancePost = dflt, markActivePostRead = dflt}) => {
    return (
        <div className='toolbar'>
            <IonButton className='prevbtn' fill="clear" onClick={regressPost}>
                <IonIcon aria-hidden="true" icon={arrowBackOutline} />
            </IonButton>
            
            <IonButton className='readbtn' fill="clear" onClick={markActivePostRead}>
                <IonIcon aria-hidden="true" icon={repeatOutline} />
            </IonButton>
            
            <IonButton className='readbtn' fill="clear" onClick={markActivePostRead}>
                <IonIcon aria-hidden="true" icon={heartOutline} />
            </IonButton>

            <IonButton className='readbtn' fill="clear" onClick={markActivePostRead}>
                <IonIcon aria-hidden="true" icon={checkmarkOutline} />
            </IonButton>

            <IonButton className='nextbtn' fill="clear" onClick={advancePost}>
                <IonIcon aria-hidden="true" icon={arrowForwardOutline} />
            </IonButton>
        </div>
    );
};