export interface Coordinates {
  lat: number;
  lon: number;
};

export interface PopupState {
  content: string
  lat: number
  lon: number
}

export interface PostObject1 {
  id: number;
  lat: number;
  lon: number;
  size: number;
  content: string;
  zoom: number
}

export interface PostObject {
  id: number;
  timestamp: number;
  user: User;
  text: Text;
  place: Place;
  likes: User[];
}

interface User {
  id: number;
  name: string;
}

interface Text {
  id: number;
  txt: string;
  lang: string;
  translations: Translation[];
}

export interface Place {
  id: number;
  lat: number;
  lon: number;
  name: string;
  long_name: string;
  geonames_id: number;
  contained_by: Place[];
}

// Define Translation interface if you have a specific structure for translations
interface Translation {
  id: number;
  txt: string;
  lang: string;
}




export interface ReverseGeocoderPlace {
  city: string;
  country: string;
  lat: number
  lon: number
  geonames_id: number
  distance: number
}

export interface ReverseGeocoderContextType {
  placeInfo: Place | null; // Adjust according to your initial state
  chosenGeonamesId: number | null; // Or string depending on your ID type
  setChosenGeonamesId: (id: number | null) => void; // Function to update the chosenGeonamesId
  chosenPlaceInfo: Place | null;
  currentPlaceInfo: Place | null;
}

