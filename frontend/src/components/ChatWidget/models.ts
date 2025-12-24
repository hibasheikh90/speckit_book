// Type definitions
export type MessageSender = 'student' | 'tutor' | 'system';
export type MessageStatus = 'sent' | 'received' | 'pending' | 'error';
export type ConnectionStatus = 'connected' | 'connecting' | 'disconnected' | 'error';

export interface RateLimitInfo {
  requestsMade: number;
  windowStart: string;
  remainingRequests: number;
}

export interface Position {
  x: number;
  y: number;
}

// ChatMessage entity model
export class ChatMessage {
  id: string;
  content: string;
  sender: MessageSender;
  timestamp: string;
  status: MessageStatus;
  typingIndicator: boolean;

  constructor(
    id: string,
    content: string,
    sender: MessageSender,
    timestamp: string = new Date().toISOString(),
    status: MessageStatus = 'sent',
    typingIndicator: boolean = false
  ) {
    this.id = id;
    this.content = content;
    this.sender = sender; // 'student' or 'tutor'
    this.timestamp = timestamp;
    this.status = status; // 'sent', 'received', 'pending', 'error'
    this.typingIndicator = typingIndicator;

    // Validate content length (3-10000 characters as per spec)
    if (content.length < 3 || content.length > 10000) {
      throw new Error('Message content must be between 3 and 10,000 characters');
    }

    // Validate sender
    if (!['student', 'tutor', 'system'].includes(sender)) {
      throw new Error('Sender must be "student", "tutor", or "system"');
    }

    // Validate status
    if (!['sent', 'received', 'pending', 'error'].includes(status)) {
      throw new Error('Status must be "sent", "received", "pending", or "error"');
    }
  }
}

// ChatSession entity model
export class ChatSession {
  sessionId: string;
  messages: ChatMessage[];
  connectionStatus: ConnectionStatus;
  lastActivity: string;
  rateLimitInfo: RateLimitInfo;

  constructor(sessionId: string = `session_${Date.now()}`) {
    this.sessionId = sessionId;
    this.messages = [];
    this.connectionStatus = 'disconnected'; // 'connected', 'connecting', 'disconnected', 'error'
    this.lastActivity = new Date().toISOString();
    this.rateLimitInfo = {
      requestsMade: 0,
      windowStart: new Date().toISOString(),
      remainingRequests: 3
    };

    // Validate session ID
    if (!sessionId || typeof sessionId !== 'string') {
      throw new Error('Session ID must be a valid string');
    }
  }

  addMessage(message: ChatMessage): void {
    if (this.messages.length >= 100) {
      // Remove oldest messages if limit exceeded (to prevent memory issues)
      this.messages = this.messages.slice(1);
    }
    this.messages.push(message);
    this.lastActivity = new Date().toISOString();
  }

  updateConnectionStatus(status: ConnectionStatus): void {
    if (!['connected', 'connecting', 'disconnected', 'error'].includes(status)) {
      throw new Error('Connection status must be "connected", "connecting", "disconnected", or "error"');
    }
    this.connectionStatus = status;
    this.lastActivity = new Date().toISOString();
  }

  incrementRateLimit(): boolean {
    const now = new Date();
    const windowStart = new Date(this.rateLimitInfo.windowStart);

    // Reset window if it's been more than 30 seconds
    if (now.getTime() - windowStart.getTime() > 30000) {
      this.rateLimitInfo.requestsMade = 0;
      this.rateLimitInfo.remainingRequests = 3;
      this.rateLimitInfo.windowStart = now.toISOString();
    }

    if (this.rateLimitInfo.remainingRequests > 0) {
      this.rateLimitInfo.requestsMade += 1;
      this.rateLimitInfo.remainingRequests -= 1;
      return true;
    }
    return false; // Rate limit exceeded
  }

  getTimeUntilRateLimitReset(): number {
    const now = new Date();
    const windowStart = new Date(this.rateLimitInfo.windowStart);
    const elapsed = now.getTime() - windowStart.getTime();
    return Math.max(0, 30000 - elapsed); // 30 seconds window
  }
}

// ChatWidgetState entity model
export class ChatWidgetState {
  isExpanded: boolean;
  isVisible: boolean;
  position: Position;
  unreadCount: number;
  lastMessagePreview: string;

  constructor() {
    this.isExpanded = false;
    this.isVisible = true; // Button is visible by default
    this.position = { x: 20, y: 20 }; // Default position from bottom-right
    this.unreadCount = 0;
    this.lastMessagePreview = '';
  }

  toggleExpanded(): void {
    this.isExpanded = !this.isExpanded;
    if (!this.isExpanded) {
      this.unreadCount = 0; // Clear unread count when opening
    }
  }

  toggleVisibility(): void {
    this.isVisible = !this.isVisible;
  }

  addUnreadMessage(): void {
    this.unreadCount += 1;
  }

  setLastMessagePreview(message: string): void {
    this.lastMessagePreview = message.length > 50 ? message.substring(0, 50) + '...' : message;
  }
}