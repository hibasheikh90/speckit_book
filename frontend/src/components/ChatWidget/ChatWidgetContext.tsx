import React, { createContext, useContext, useState, ReactNode } from 'react';

interface ChatWidgetContextType {
  isChatOpen: boolean;
  openChat: () => void;
  closeChat: () => void;
  toggleChat: () => void;
}

const ChatWidgetContext = createContext<ChatWidgetContextType | undefined>(undefined);

export const ChatWidgetProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const openChat = () => setIsChatOpen(true);
  const closeChat = () => setIsChatOpen(false);
  const toggleChat = () => setIsChatOpen(prev => !prev);

  return (
    <ChatWidgetContext.Provider value={{ isChatOpen, openChat, closeChat, toggleChat }}>
      {children}
      {isChatOpen && <ChatWidgetWrapper />}
    </ChatWidgetContext.Provider>
  );
};

const ChatWidgetWrapper: React.FC = () => {
  // This wrapper will render the actual ChatWidget with the correct props
  // Importing dynamically to avoid circular dependencies
  const ChatWidgetModule = require('./ChatWidget');
  const ChatWidget = ChatWidgetModule.ChatWidget;
  return <ChatWidget />;
};

export const useChatWidget = (): ChatWidgetContextType => {
  const context = useContext(ChatWidgetContext);
  if (context === undefined) {
    throw new Error('useChatWidget must be used within a ChatWidgetProvider');
  }
  return context;
};