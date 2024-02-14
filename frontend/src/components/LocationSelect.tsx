import React from 'react';
import { IonSelect, IonSelectOption, SelectCustomEvent, IonLabel, IonItem } from '@ionic/react';
import { useReverseGeocoder } from './ReverseGeocoder';

interface LocationSelectProps {
    label: string
}


const LocationSelect: React.FC<LocationSelectProps> = ({label = 'Select location: '}) => {
    const { placeInfo, chosenGeonamesId, setChosenGeonamesId } = useReverseGeocoder();

    const handleSelectionChange = (event: SelectCustomEvent) => {
      setChosenGeonamesId(parseInt(event.target.value));
      console.log('chosen geonames id =',chosenGeonamesId);
    };

    if (placeInfo == null) return <div>Loading...</div>;
    const places = [placeInfo].concat(placeInfo.contained_by || []);
    
    const handleIonChange = (event: SelectCustomEvent) => {
        const value = event.detail.value; // The value is already a string here
        setChosenGeonamesId(value ? parseInt(value, 10) : null);
    };
    
    // Ensure chosenGeonamesId is a string or '' if null for IonSelect value compatibility
    const selectedValue = chosenGeonamesId ? chosenGeonamesId.toString() : '';
    
    return (
        // <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        // <IonLabel>{label}</IonLabel>
        // <IonItem style={{ width: 'auto', flex: 'none', margin: 0, padding: 0 }}>
            <IonSelect name="geonames_id" onIonChange={handleIonChange} value={selectedValue} label={label}>
            {places.map((place) => (
                <IonSelectOption key={place.geonames_id} value={place.geonames_id.toString()}>
                {place.name}
                </IonSelectOption>
            ))}
            </IonSelect>
        // </IonItem>
        // </div>
    );

}

export default LocationSelect;
