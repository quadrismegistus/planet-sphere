import { useEffect, useState, Dispatch, SetStateAction } from 'react';


// Explicitly define the return type of the hook
export const usePersistedState = (
    key: string,
    defaultValue: number | null
  ): [number | null, Dispatch<SetStateAction<number | null>>] => {
    const [state, setState] = useState<number | null>(() => {
      const storedValue = localStorage.getItem(key);
      console.log('found',storedValue,'in localStorage');
      if (storedValue !== null) {
        // Attempt to parse the stored value as an integer
        const parsedValue = parseInt(JSON.parse(storedValue), 10);
        // Return the parsed integer if it's a valid number; otherwise, fall back to defaultValue
        return !isNaN(parsedValue) ? parsedValue : defaultValue;
      }
      return defaultValue;
    });
  
    useEffect(() => {
        console.log('converting to string')
      // Convert state to string for localStorage, but ensure we're dealing with null correctly
      const valueToStore = state === null ? null : JSON.stringify(state);
      if(valueToStore) localStorage.setItem(key, valueToStore);
    }, [key, state]);
  
    return [state, setState];
  };


