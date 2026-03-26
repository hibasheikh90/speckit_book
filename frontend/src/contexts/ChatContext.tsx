import React, { createContext, useContext, useState, ReactNode } from 'react';

interface ChatContextType {
  isChatVisible: boolean;
  openChat: () => void;
  closeChat: () => void;
  toggleChat: () => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isChatVisible, setIsChatVisible] = useState(false);

  const openChat = () => setIsChatVisible(true);
  const closeChat = () => setIsChatVisible(false);
  const toggleChat = () => setIsChatVisible(prev => !prev);

  return (
    <ChatContext.Provider value={{ isChatVisible, openChat, closeChat, toggleChat }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = (): ChatContextType => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};