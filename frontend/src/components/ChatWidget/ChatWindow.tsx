import React, { useState, useEffect } from 'react';
import { ChatContainer, MessageList, Message, MessageInput, ConversationHeader } from '@chatscope/chat-ui-kit-react';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import { ChatSession, ChatMessage, MessageSender } from './models';

interface ChatWindowProps {
  onClose: () => void;
  onUnreadMessage: (message: string) => void;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({ onClose, onUnreadMessage }) => {
  const [session, setSession] = useState<ChatSession>(() => {
    // Initialize session from localStorage if available
    const savedSession = localStorage.getItem('chatSession');
    if (savedSession) {
      try {
        const parsed = JSON.parse(savedSession);
        const session = new ChatSession(parsed.sessionId);
        session.messages = parsed.messages.map((msg: any) => new ChatMessage(
          msg.id, msg.content, msg.sender as MessageSender, msg.timestamp, msg.status, msg.typingIndicator
        ));
        session.connectionStatus = parsed.connectionStatus || 'disconnected';
        session.lastActivity = parsed.lastActivity;
        session.rateLimitInfo = parsed.rateLimitInfo || {
          requestsMade: 0,
          windowStart: new Date().toISOString(),
          remainingRequests: 3
        };
        return session;
      } catch (e) {
        console.warn('Failed to parse saved chat session, creating new one');
        return new ChatSession();
      }
    }
    return new ChatSession();
  });

  const [isTyping, setIsTyping] = useState<boolean>(false);

  // Save session to localStorage whenever it changes
  useEffect(() => {
    const sessionData = {
      sessionId: session.sessionId,
      messages: session.messages,
      connectionStatus: session.connectionStatus,
      lastActivity: session.lastActivity,
      rateLimitInfo: session.rateLimitInfo
    };
    localStorage.setItem('chatSession', JSON.stringify(sessionData));
  }, [session]);

  const handleSend = async (message: string) => {
    // Trim the message and validate length
    const trimmedMessage = message.trim();

    // Validate message length (3-10,000 characters as per spec)
    if (trimmedMessage.length < 3) {
      // Don't send messages shorter than 3 characters
      return;
    }

    if (trimmedMessage.length > 10000) {
      // Don't send messages longer than 10,000 characters
      // Add error message to UI
      const errorId = `error-${Date.now()}`;
      const errorMessage = new ChatMessage(
        errorId,
        'Message is too long. Please keep your message under 10,000 characters.',
        'system',
        new Date().toISOString(),
        'error'
      );

      setSession(prev => {
        const newSession = new ChatSession(prev.sessionId);
        newSession.messages = [...prev.messages, errorMessage];
        newSession.connectionStatus = prev.connectionStatus;
        newSession.lastActivity = new Date().toISOString();
        newSession.rateLimitInfo = { ...prev.rateLimitInfo };
        return newSession;
      });
      return;
    }

    // Check rate limit
    if (!session.incrementRateLimit()) {
      // Rate limit exceeded - add error message to UI
      const errorId = `error-${Date.now()}`;
      const errorMessage = new ChatMessage(
        errorId,
        'Rate limit exceeded. Please wait before sending another message.',
        'system',
        new Date().toISOString(),
        'error'
      );

      setSession(prev => {
        const newSession = new ChatSession(prev.sessionId);
        newSession.messages = [...prev.messages, errorMessage];
        newSession.connectionStatus = prev.connectionStatus;
        newSession.lastActivity = new Date().toISOString();
        newSession.rateLimitInfo = { ...prev.rateLimitInfo };
        return newSession;
      });

      return;
    }

    // Add user message to UI immediately
    const userMessageId = `msg-${Date.now()}`;
    const userMessage = new ChatMessage(
      userMessageId,
      trimmedMessage,
      'student',
      new Date().toISOString(),
      'sent'
    );

    setSession(prev => {
      const newSession = new ChatSession(prev.sessionId);
      newSession.messages = [...prev.messages, userMessage];
      newSession.connectionStatus = prev.connectionStatus;
      newSession.lastActivity = new Date().toISOString();
      newSession.rateLimitInfo = { ...prev.rateLimitInfo };
      return newSession;
    });

    // In a real implementation, we would send this to the backend
    // For now, we'll simulate a response after a delay
    setIsTyping(true);

    // Simulate API call delay
    setTimeout(() => {
      const responseId = `resp-${Date.now()}`;
      const responseMessage = new ChatMessage(
        responseId,
        `I received your message: "${trimmedMessage}". This is a simulated response. In the full implementation, this would come from the AI tutor backend.`,
        'tutor',
        new Date().toISOString(),
        'received'
      );

      setSession(prev => {
        const newSession = new ChatSession(prev.sessionId);
        newSession.messages = [...prev.messages, responseMessage];
        newSession.connectionStatus = prev.connectionStatus;
        newSession.lastActivity = new Date().toISOString();
        newSession.rateLimitInfo = { ...prev.rateLimitInfo };
        return newSession;
      });

      setIsTyping(false);

      // Notify parent component of new message for unread count
      if (onUnreadMessage && !document.hasFocus()) {
        onUnreadMessage(responseMessage.content);
      }
    }, 1000 + Math.random() * 1000); // Random delay between 1-2 seconds
  };

  return (
    <div className="chat-window" role="dialog" aria-modal="true" aria-label="Chat window">
      <ConversationHeader>
        <ConversationHeader.Back onClick={onClose} aria-label="Close chat" />
        <ConversationHeader.Content userName="AI Tutor" />
      </ConversationHeader>

      <ChatContainer>
        <MessageList>
          {session.messages.map((msg) => (
            <Message
              key={msg.id}
              model={{
                message: msg.content,
                sender: msg.sender,
                direction: msg.sender === 'student' ? 'outgoing' : 'incoming',
                position: 'normal'
              }}
              avatarPosition={msg.sender === 'student' ? 'tr' : 'tl'}
            />
          ))}
          {isTyping && (
            <Message
              model={{
                message: "AI Tutor is typing...",
                sender: 'tutor',
                direction: 'incoming',
                position: 'normal'
              }}
              avatarPosition="tl"
            />
          )}
        </MessageList>

        <MessageInput
          placeholder="Type your question about Physical AI..."
          onSend={handleSend}
          attachButton={false}
        />
      </ChatContainer>
    </div>
  );
};