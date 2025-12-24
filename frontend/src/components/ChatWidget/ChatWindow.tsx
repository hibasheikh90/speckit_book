import React, { useState, useEffect, useRef } from 'react';
import './chat-widget.css';
import { ChatSession, ChatMessage, MessageSender } from './models';
import { ChatService } from './chat-service';

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
        session.connectionStatus = parsed.connectionStatus || 'connected';
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
  const [currentMessage, setCurrentMessage] = useState<string>('');
  const [validationError, setValidationError] = useState<string>('');
  const [rateLimitCountdown, setRateLimitCountdown] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatService = useRef(new ChatService());

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [session.messages, isTyping]);

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

  // Handle rate limit countdown
  useEffect(() => {
    if (rateLimitCountdown === null || rateLimitCountdown <= 0) {
      return;
    }

    const timer = setInterval(() => {
      setRateLimitCountdown(prev => {
        if (prev === null || prev <= 1) {
          return null;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [rateLimitCountdown]);

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const message = e.target.value;
    setCurrentMessage(message);

    // Clear validation error when user starts typing
    if (validationError) {
      setValidationError('');
    }

    // Validate message length in real-time
    if (message.length > 10000) {
      setValidationError('Message exceeds 10,000 character limit');
    }
  };

  const handleSend = async () => {
    // Trim the message and validate length
    const trimmedMessage = currentMessage.trim();

    // Validate message length (3-10,000 characters as per spec)
    if (trimmedMessage.length < 3) {
      setValidationError('Message must be at least 3 characters');
      return;
    }

    if (trimmedMessage.length > 10000) {
      setValidationError('Message must be less than 10,000 characters');
      return;
    }

    // Check rate limit
    if (!session.incrementRateLimit()) {
      const timeRemaining = session.getTimeUntilRateLimitReset();
      setRateLimitCountdown(Math.ceil(timeRemaining / 1000));
      setValidationError(`Rate limit exceeded. Try again in ${Math.ceil(timeRemaining / 1000)}s`);
      return;
    }

    // Clear input and errors
    setCurrentMessage('');
    setValidationError('');
    setIsLoading(true);

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
      newSession.connectionStatus = 'connected';
      newSession.lastActivity = new Date().toISOString();
      newSession.rateLimitInfo = { ...prev.rateLimitInfo };
      return newSession;
    });

    // Show typing indicator
    setIsTyping(true);

    try {
      // Send message to backend
      await chatService.current.sendMessage(trimmedMessage, (response: string) => {
        const responseId = `resp-${Date.now()}`;
        const responseMessage = new ChatMessage(
          responseId,
          response,
          'tutor',
          new Date().toISOString(),
          'received'
        );

        setSession(prev => {
          const newSession = new ChatSession(prev.sessionId);
          newSession.messages = [...prev.messages, responseMessage];
          newSession.connectionStatus = 'connected';
          newSession.lastActivity = new Date().toISOString();
          newSession.rateLimitInfo = { ...prev.rateLimitInfo };
          return newSession;
        });

        // Notify parent component of new message for unread count
        if (onUnreadMessage && !document.hasFocus()) {
          onUnreadMessage(responseMessage.content);
        }
      });
    } catch (error) {
      // Handle errors gracefully
      const errorId = `error-${Date.now()}`;
      let errorMsg = 'Unable to send message. Please try again.';

      if (error instanceof Error) {
        if (error.message.includes('Rate limit')) {
          errorMsg = error.message;
        } else if (error.message.includes('timeout')) {
          errorMsg = 'Request timed out. Please try again.';
        } else if (error.message.includes('Network') || error.message.includes('fetch')) {
          errorMsg = 'Unable to connect. Please check your connection.';
        } else if (error.message.includes('500')) {
          errorMsg = 'Service temporarily unavailable. Please try again.';
        }
      }

      const errorMessage = new ChatMessage(
        errorId,
        errorMsg,
        'system',
        new Date().toISOString(),
        'error'
      );

      setSession(prev => {
        const newSession = new ChatSession(prev.sessionId);
        newSession.messages = [...prev.messages, errorMessage];
        newSession.connectionStatus = 'error';
        newSession.lastActivity = new Date().toISOString();
        newSession.rateLimitInfo = { ...prev.rateLimitInfo };
        return newSession;
      });
    } finally {
      setIsTyping(false);
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-window" role="dialog" aria-modal="true" aria-label="Chat window">
      {/* Header */}
      <div className="chat-header">
        <h3 className="chat-header-title">AI Tutor</h3>
        <div className="chat-header-controls">
          <button
            className="chat-header-button"
            onClick={onClose}
            aria-label="Close chat"
            title="Close chat"
          >
            ✕
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="chat-messages">
        {session.messages.length === 0 && (
          <div className="welcome-message">
            <div className="welcome-icon">👋</div>
            <h4 className="welcome-title">Welcome!</h4>
            <p className="welcome-text">
              I'm your AI tutor for Physical AI and Humanoid Robotics.
            </p>
            <p className="welcome-subtitle">Ask me anything about:</p>
            <ul className="welcome-topics">
              <li>Physical AI concepts</li>
              <li>Robotics fundamentals</li>
              <li>Course materials</li>
            </ul>
          </div>
        )}

        {session.messages.map((msg) => (
          <div
            key={msg.id}
            className={`message ${
              msg.sender === 'student' ? 'message-sent' :
              msg.sender === 'system' ? 'message-error' :
              'message-received'
            }`}
          >
            {msg.content}
          </div>
        ))}

        {isTyping && (
          <div className="message message-typing">
            AI Tutor is typing...
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="chat-input-container">
        {validationError && (
          <div className="validation-error" role="alert">
            ⚠️ {validationError}
          </div>
        )}

        {rateLimitCountdown && rateLimitCountdown > 0 && (
          <div className="rate-limit-notice" role="status">
            Rate limit exceeded. Try again in {rateLimitCountdown}s
          </div>
        )}

        <div className="chat-input-wrapper">
          <textarea
            className="chat-input"
            placeholder="Type your question about Physical AI..."
            value={currentMessage}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            disabled={isLoading || rateLimitCountdown !== null}
            rows={1}
            aria-label="Message input"
          />
          <div className="chat-input-footer">
            <span className={`char-counter ${currentMessage.length > 9500 ? 'warning' : ''}`}>
              {currentMessage.length} / 10000
            </span>
            <button
              className="send-button"
              onClick={handleSend}
              disabled={
                isLoading ||
                rateLimitCountdown !== null ||
                currentMessage.trim().length < 3 ||
                currentMessage.length > 10000
              }
              aria-label="Send message"
              title="Send message"
            >
              {isLoading ? '⏳' : '➤'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
