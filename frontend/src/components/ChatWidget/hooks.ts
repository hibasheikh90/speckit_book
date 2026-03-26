import { useState, useEffect, useRef } from 'react';
import { ChatService } from './chat-service';

// React hook to use the chat service
export const useChatService = () => {
  const [isConnected, setIsConnected] = useState(false);
  const chatService = useRef(new ChatService()).current;

  useEffect(() => {
    chatService.loadRateLimitState();
    chatService.connect();
    setIsConnected(true);

    return () => {
      chatService.disconnect();
      chatService.saveRateLimitState();
    };
  }, []);

  return {
    sendMessage: chatService.sendMessage.bind(chatService),
    sendStreamingMessage: chatService.sendStreamingMessage.bind(chatService),
    connect: () => {
      chatService.connect();
      setIsConnected(true);
    },
    disconnect: () => {
      chatService.disconnect();
      setIsConnected(false);
    },
    isConnected
  };
};