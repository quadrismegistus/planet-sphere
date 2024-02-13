import React, { createContext, useContext, useState, ReactNode } from 'react';

interface ModalContextType {
  postIsOpen: boolean;
  loginIsOpen: boolean;
  locationIsOpen: boolean;
  setPostIsOpen: (isOpen: boolean) => void;
  hidePostModal: () => void;
  showPostModal: () => void;
  setLoginIsOpen: (isOpen: boolean) => void;
  hideLoginModal: () => void;
  showLoginModal: () => void;
  setLocationIsOpen: (isOpen: boolean) => void;
  hideLocationModal: () => void;
  showLocationModal: () => void;
}

const defaultModalContextValue: ModalContextType = {
  postIsOpen: false,
  loginIsOpen: false,
  locationIsOpen: false,
  setPostIsOpen: () => {},
  hidePostModal: () => {},
  showPostModal: () => {},
  setLoginIsOpen: () => {},
  hideLoginModal: () => {},
  showLoginModal: () => {},
  setLocationIsOpen: () => {},
  hideLocationModal: () => {},
  showLocationModal: () => {},
};

const ModalContext = createContext<ModalContextType>(defaultModalContextValue);

export const useModal = () => useContext(ModalContext);

// Define an interface for the props expected by ModalProvider
interface ModalProviderProps {
  children: ReactNode; // This type is appropriate for component children
}

export const ModalProvider: React.FC<ModalProviderProps> = ({ children }) => {
  const [postIsOpen, setPostIsOpen] = useState(false);
  const [loginIsOpen, setLoginIsOpen] = useState(false);
  const [locationIsOpen, setLocationIsOpen] = useState(false);

  const hidePostModal = () => { console.log('hiding login'); setPostIsOpen(false); }
  const showPostModal = () => { console.log('showing post'); setPostIsOpen(true); setLoginIsOpen(false); }
  const hideLoginModal = () => { console.log('hiding login'); setLoginIsOpen(false); }
  const showLoginModal = () => { console.log('showing login'); setLoginIsOpen(true); setPostIsOpen(false); }

  const hideLocationModal = () => { console.log('hiding login'); setLocationIsOpen(false); }
  const showLocationModal = () => { console.log('showing login'); setLocationIsOpen(true); setPostIsOpen(false); }


  return (
    <ModalContext.Provider value={{ postIsOpen, setPostIsOpen, hidePostModal, showPostModal, loginIsOpen, hideLoginModal, showLoginModal, setLoginIsOpen, locationIsOpen, setLocationIsOpen, hideLocationModal, showLocationModal }}>
      {children}
    </ModalContext.Provider>
  );
};
