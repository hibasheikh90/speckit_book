import { MessageSender } from './models';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

export interface ChatRequest {
  message: string;
  sessionId?: string;
}

export interface ChatResponse {
  response: string;
  agent_name: string;
  timestamp: string;
}

export interface StreamingResponse {
  content: string;
  sender: MessageSender;
  timestamp: string;
  isPartial?: boolean;
}

export class ChatService {
  private eventSource: EventSource | null = null;
  private rateLimit: {
    requests: number[];
    maxRequests: number;
    windowMs: number;
  };

  constructor() {
    this.rateLimit = {
      requests: [],
      maxRequests: 3,
      windowMs: 30000 // 30 seconds
    };
  }

  // Check if we're within rate limit
  private isRateLimited(): boolean {
    const now = Date.now();
    // Remove old requests outside the window
    this.rateLimit.requests = this.rateLimit.requests.filter(
      timestamp => now - timestamp < this.rateLimit.windowMs
    );

    // Check if we've exceeded the limit
    if (this.rateLimit.requests.length >= this.rateLimit.maxRequests) {
      return true;
    }

    // Add current request
    this.rateLimit.requests.push(now);
    return false;
  }

  async sendMessage(message: string, onResponse: (response: string) => void): Promise<void> {
    // Validate message length (3-10,000 characters as per spec)
    const trimmedMessage = message.trim();
    if (trimmedMessage.length < 3) {
      throw new Error('Message is too short. Please enter at least 3 characters.');
    }

    if (trimmedMessage.length > 10000) {
      throw new Error('Message is too long. Please keep your message under 10,000 characters.');
    }

    // Check rate limit
    if (this.isRateLimited()) {
      throw new Error('Rate limit exceeded. Please wait before sending another message.');
    }

    // For now, use fetch instead of SSE for simplicity
    // In a real implementation, we'd use SSE for streaming
    const response = await fetch(`${BACKEND_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ message: trimmedMessage })
    });

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }

    const data: ChatResponse = await response.json();
    onResponse(data.response);
  }

  async sendStreamingMessage(message: string, onMessage: (content: string, isPartial?: boolean) => void): Promise<void> {
    // Validate message length (3-10,000 characters as per spec)
    const trimmedMessage = message.trim();
    if (trimmedMessage.length < 3) {
      throw new Error('Message is too short. Please enter at least 3 characters.');
    }

    if (trimmedMessage.length > 10000) {
      throw new Error('Message is too long. Please keep your message under 10,000 characters.');
    }

    // Check rate limit
    if (this.isRateLimited()) {
      throw new Error('Rate limit exceeded. Please wait before sending another message.');
    }

    // Use fetch with streaming response
    const response = await fetch(`${BACKEND_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'
      },
      body: JSON.stringify({ message: trimmedMessage })
    });

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('No response body');
    }

    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        // Process each line separately
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // Keep last incomplete line in buffer

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6)); // Remove 'data: ' prefix
              if (data.content) {
                onMessage(data.content, data.isPartial);
              }
            } catch (e) {
              console.error('Error parsing SSE data:', e);
            }
          }
        }
      }
    } finally {
      reader.cancel();
    }
  }

  connect(): void {
    // For streaming implementation, we would establish SSE connection here
    console.log('Chat service connected');
  }

  disconnect(): void {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
    console.log('Chat service disconnected');
  }

  // Save rate limit state to persist across sessions if needed
  saveRateLimitState(): void {
    localStorage.setItem('chatRateLimit', JSON.stringify(this.rateLimit));
  }

  // Load rate limit state from localStorage
  loadRateLimitState(): void {
    const saved = localStorage.getItem('chatRateLimit');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        this.rateLimit = {
          requests: parsed.requests || [],
          maxRequests: parsed.maxRequests || 3,
          windowMs: parsed.windowMs || 30000
        };
        // Clean up old requests
        const now = Date.now();
        this.rateLimit.requests = this.rateLimit.requests.filter(
          timestamp => now - timestamp < this.rateLimit.windowMs
        );
      } catch (e) {
        console.warn('Failed to parse saved rate limit state, using defaults');
      }
    }
  }
}