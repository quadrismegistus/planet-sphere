import axios from 'axios';
import { accessToken } from 'mapbox-gl';

// Function to authenticate user by sending credentials to the backend
export const authenticate = async (username:string, password:string) => {
    try {
        const response = await axios.post('http://localhost:8000/login', {
        username,
        password,
        });
      if(!("access_token" in response.data)) {
        throw new Error('Failed to login!!!!');
      } else {
        // Assuming the backend responds with a token on successful authentication
        const accessToken = response.data["access_token"];
        // Store the token in localStorage or handle it as needed
        localStorage.setItem('username', username);
        localStorage.setItem('accessToken', accessToken);
        return accessToken
      }
    } catch (error) {
      // Handle any errors, such as showing login failure messages
      throw new Error('Failed to login');
    }
  };