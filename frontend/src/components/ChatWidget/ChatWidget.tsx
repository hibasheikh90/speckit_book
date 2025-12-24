import React, { useState, useEffect } from 'react';
import './chat-widget.css';
import { ChatWindow } from './ChatWindow';
import { ChatWidgetState } from './models';
import { useChat } from '../../contexts/ChatContext';

interface ChatWidgetProps {}

export const ChatWidget: React.FC<ChatWidgetProps> = () => {
  const { isChatVisible, closeChat } = useChat();
  const [widgetState, setWidgetState] = useState<ChatWidgetState>(() => {
    const state = new ChatWidgetState();
    // Override default to have the chat window closed initially
    state.isExpanded = false;
    // Set visibility based on global state
    state.isVisible = isChatVisible;
    return state;
  });
  const [showChatWindow, setShowChatWindow] = useState<boolean>(false);

  // Load widget state from localStorage on initial render
  useEffect(() => {
    const savedState = localStorage.getItem('chatWidgetState');
    if (savedState) {
      try {
        const parsedState = JSON.parse(savedState);
        setWidgetState(prevState => {
          const newState = new ChatWidgetState();
          newState.isExpanded = parsedState.isExpanded || false;
          // Only make it visible if the global state says it should be
          newState.isVisible = isChatVisible && (parsedState.isVisible !== false);
          newState.position = parsedState.position || { x: 20, y: 20 };
          newState.unreadCount = parsedState.unreadCount || 0;
          newState.lastMessagePreview = parsedState.lastMessagePreview || '';
          return newState;
        });

        // If the widget was expanded when last closed and is now visible, show the chat window
        if (parsedState.isExpanded && isChatVisible) {
          setShowChatWindow(true);
        }
      } catch (e) {
        console.warn('Failed to parse saved chat widget state, using defaults');
      }
    } else {
      // If no saved state, initialize with chat closed but button visible if global state allows
      setWidgetState(prevState => {
        const newState = new ChatWidgetState();
        newState.isExpanded = false;
        newState.isVisible = isChatVisible;
        newState.position = { x: 20, y: 20 };
        newState.unreadCount = 0;
        newState.lastMessagePreview = '';
        return newState;
      });
    }
  }, [isChatVisible]); // Add isChatVisible as dependency

  // Save widget state to localStorage whenever it changes
  useEffect(() => {
    const stateToSave = {
      isExpanded: widgetState.isExpanded,
      isVisible: widgetState.isVisible,
      position: widgetState.position,
      unreadCount: widgetState.unreadCount,
      lastMessagePreview: widgetState.lastMessagePreview
    };
    localStorage.setItem('chatWidgetState', JSON.stringify(stateToSave));
  }, [widgetState]);

  const toggleChat = () => {
    setWidgetState(prevState => {
      const newState = new ChatWidgetState();
      // Copy all properties from previous state
      Object.assign(newState, prevState);
      // Then apply the toggle
      newState.toggleExpanded();
      return newState;
    });

    if (!showChatWindow) {
      setShowChatWindow(true);
    }
  };

  const closeChatInternal = () => {
    setWidgetState(prevState => {
      const newState = new ChatWidgetState();
      // Copy all properties from previous state
      Object.assign(newState, prevState);
      // Then apply the toggle
      newState.toggleExpanded();
      return newState;
    });
    setShowChatWindow(false);
    closeChat(); // Close the global chat state too
  };

  // Only render if widget is visible based on global state
  if (!isChatVisible) {
    return null;
  }

  return (
    <div className="chat-widget-container">
      {showChatWindow ? (
        <ChatWindow
          onClose={closeChatInternal}
          onUnreadMessage={(message: string) => {
            setWidgetState(prevState => {
              const newState = new ChatWidgetState();
              // Copy all properties from previous state
              Object.assign(newState, prevState);
              // Apply the new message changes
              newState.addUnreadMessage();
              newState.setLastMessagePreview(message);
              return newState;
            });
          }}
        />
      ) : (
        <button
          className="chat-widget-button"
          onClick={toggleChat}
          aria-label="Open chat"
          data-unread={widgetState.unreadCount.toString()}
        >
          💬
        </button>
      )}
    </div>
  );
};

// Wrapper component that handles the global chat visibility state
export const ChatWidgetWithProvider: React.FC = () => {
  const { isChatVisible, openChat, closeChat } = useChat();

  // Render the toggle button when chat is not visible
  if (!isChatVisible) {
    return (
      <button
        className="chat-widget-button"
        onClick={openChat}
        aria-label="Open chat"
      >
        💬
      </button>
    );
  }

  // Otherwise, render the actual ChatWidget
  return <ChatWidget />;
};