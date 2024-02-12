import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';
import { accessToken } from 'mapbox-gl';
import { REACT_APP_API_URL } from '../vars'


// Function to authenticate user by sending credentials to the backend
export const authenticate = async (username:string, password:string) => {
    try {
        const response = await axios.post(REACT_APP_API_URL+'/login', {
        username,
        password,
        });
      if ("access_token" in response.data) {
        // Assuming the backend responds with a token on successful authentication
        const accessToken = response.data["access_token"];
        // Store the token in localStorage or handle it as needed
        localStorage.setItem('username', username);
        localStorage.setItem('accessToken', accessToken);
        return accessToken;
      } else {
        throw new Error(response.data['msg']);
      }
    } catch (error) {
      // Handle any errors, such as showing login failure messages
      throw error;
    }
  };



interface User {
  username: string;
  accessToken: string
}

interface AuthContextType {
  user: User | null;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const defaultContextValue: AuthContextType = {
  user: null,
  setUser: () => {},
  login: async () => {},
  logout: () => {},
};

const AuthenticationContext = createContext<AuthContextType>(defaultContextValue);

export const useAuth = () => useContext(AuthenticationContext);


export const AuthProvider: React.FC<{children: ReactNode}> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const history = useHistory();

  const login = async (username: string, password: string) => {
    try {
      // Here you should replace this with your actual authentication logic
      const accessToken = await authenticate(username, password);
      localStorage.setItem('accessToken', accessToken); // Simulate setting an access token
      localStorage.setItem('username', username);
      setUser({ username:username, accessToken:accessToken });
      // history.push('/map'); // Assuming successful login redirects to the map
    } catch (error) {
      // Handle error - perhaps by using an error boundary, logging, or custom error handling logic
      console.error(error);
      throw error; // Re-throw to let calling component handle it
    }
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('username');
    setUser(null);
    // history.push('/acct'); // Redirect to login page on logout
  };

  // Check for existing authentication on component mount
  const checkAuth = () => {
    console.log('Checking auth status');
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      const storedUsername = localStorage.getItem('username');
      if (storedUsername) {
        // If there's a username stored, set the user state
        setUser({ username: storedUsername, accessToken: accessToken });
        // Optionally, redirect the user to a certain page upon automatic login
        // history.push('/dashboard'); // Example redirect
      }
    } else {
      // If no accessToken is found, consider redirecting the user to a login page
      // history.push('/login'); // Example redirect
      // For this specific case, you might not redirect automatically
      // since the check is at the app's root level.
    }
  };

  useEffect(() => {
    checkAuth();
  }, [history]);


  return (
    <AuthenticationContext.Provider value={{ user, setUser, login, logout }}>
      {children}
    </AuthenticationContext.Provider>
  );
};
