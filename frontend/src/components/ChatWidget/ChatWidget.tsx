import React, { useState, useEffect } from 'react';
import './chat-widget.css';
import { ChatWindow } from './ChatWindow';
import { ChatWidgetState } from './models';
import { useChat } from '../../contexts/ChatContext';

interface ChatWidgetProps {}

export const ChatWidget: React.FC<ChatWidgetProps> = () => {
  const { closeChat } = useChat();
  const [widgetState, setWidgetState] = useState<ChatWidgetState>(() => {
    const state = new ChatWidgetState();
    // Override default to have the chat window closed initially
    state.isExpanded = false;
    // Widget button is always visible
    state.isVisible = true;
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
          // Widget button is always visible
          newState.isVisible = true;
          newState.position = parsedState.position || { x: 20, y: 20 };
          newState.unreadCount = parsedState.unreadCount || 0;
          newState.lastMessagePreview = parsedState.lastMessagePreview || '';
          return newState;
        });

        // If the widget was expanded when last closed, show the chat window
        if (parsedState.isExpanded) {
          setShowChatWindow(true);
        }
      } catch (e) {
        console.warn('Failed to parse saved chat widget state, using defaults');
      }
    } else {
      // If no saved state, initialize with chat closed but button visible
      setWidgetState(prevState => {
        const newState = new ChatWidgetState();
        newState.isExpanded = false;
        newState.isVisible = true;
        newState.position = { x: 20, y: 20 };
        newState.unreadCount = 0;
        newState.lastMessagePreview = '';
        return newState;
      });
    }
  }, []); // Run once on mount

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
  // Simply render ChatWidget - it handles all visibility logic internally
  return <ChatWidget />;
};