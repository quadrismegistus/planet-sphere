import { TextareaCustomEvent } from '@ionic/react';
import React, {useState} from 'react';

export function countSubstring(str:string, substring:string) {
  const regex = new RegExp(substring, 'g');
  const matches = str.match(regex);
  return matches ? matches.length : 0;
}

// Custom hook for handling textarea with character limit
export function useTextareaWithLimit(limit = 360) {
  const [value, setValue] = useState('');

  // Calculate the number of characters remaining
  const charsRemaining = limit - value.length;

  // Update the state value when the user types in the textarea
  const handleChange = (event: TextareaCustomEvent) => {
    if(event.target.value!=undefined) setValue(event.target.value);
  };

  return { value, charsRemaining, handleChange };
}