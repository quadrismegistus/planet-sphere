import { useModal } from './ModalProvider';
import React from 'react';
import { useReverseGeocoder } from './ReverseGeocoder';
import { useGeolocation } from './GeolocationProvider';

const LocationSelect: React.FC = () => {
    const { settingsIsOpen, hideSettingsModal, showSettingsModal } = useModal();
    const { placeInfo, chosenGeonamesId, setChosenGeonamesId } = useReverseGeocoder();
    const { coords, loading } = useGeolocation();

    const handleSelectionChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
      setChosenGeonamesId(parseInt(event.target.value));
      console.log('chosen geonames id =',chosenGeonamesId);
    };

    const getPlaceInfoContent = () => {
      if(placeInfo == null) return <div>Loading</div>;
      const places = [placeInfo].concat(placeInfo.contained_by);
      return (
        <select name="geonames_id" onChange={handleSelectionChange}>
        {places.map((place) => (
          <option key={place.geonames_id} value={place.geonames_id}>
            {place.name}
          </option>
        ))}
        </select>
      )
    }

    return getPlaceInfoContent();
}

export default LocationSelect;
