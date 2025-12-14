/**
 * TypeScript Type Definitions for Physical AI Textbook Chat API
 *
 * Generated from: chat-api-openapi.yaml
 * Version: 1.0.0
 * Date: 2025-12-14
 *
 * Use these types in the frontend Chatbot UI to ensure type safety
 * when communicating with the backend chat endpoint.
 */

// ============================================================================
// Request Types
// ============================================================================

/**
 * Student question request payload
 *
 * Validation constraints:
 * - question: 3-10,000 characters
 * - cannot be only whitespace
 */
export interface StudentQuestion {
  /** The student's learning question about Physical AI or Humanoid Robotics */
  question: string;
}

/**
 * Validation helper for StudentQuestion
 * Returns validation error message or null if valid
 */
export function validateStudentQuestion(
  question: string
): string | null {
  const trimmed = question.trim();

  if (trimmed.length === 0) {
    return "Question cannot be empty";
  }

  if (trimmed.length < 3) {
    return "Question must be at least 3 characters long";
  }

  if (trimmed.length > 10000) {
    return "Question must not exceed 10,000 characters";
  }

  return null; // Valid
}

// ============================================================================
// Response Types
// ============================================================================

/**
 * Successful response from the AI tutor
 *
 * Contains:
 * - Educational response aligned with Global Constitution
 * - Agent name for debugging/transparency
 * - Timestamp for analytics
 */
export interface TutorResponse {
  /** Educational response content */
  response: string;

  /** Name of the agent that generated this response */
  agent_name: string;

  /** When the response was generated (ISO 8601 UTC) */
  timestamp: string;
}

/**
 * Error response from the API
 *
 * All error responses use this structure for consistent handling
 */
export interface ValidationError {
  /** Category of error for client-side handling */
  error_type: ErrorType;

  /** User-friendly error message */
  message: string;

  /** Field that failed validation (null for non-validation errors) */
  field: string | null;

  /** When the error occurred (ISO 8601 UTC) */
  timestamp: string;
}

/**
 * Error type enum for handling different error scenarios
 */
export enum ErrorType {
  /** Input validation failed (HTTP 422) */
  VALIDATION = "validation",

  /** AI service unavailable (HTTP 500) */
  SERVICE = "service",

  /** Request took > 30 seconds (HTTP 504) */
  TIMEOUT = "timeout",

  /** Too many requests (HTTP 429) */
  RATE_LIMIT = "rate_limit",
}

/**
 * Health check response
 */
export interface HealthResponse {
  /** Service health status */
  status: "healthy";

  /** Whether the AI agent is initialized and ready */
  agent_ready: boolean;

  /** When the health check was performed */
  timestamp: string;
}

// ============================================================================
// API Client Types
// ============================================================================

/**
 * API response wrapper (discriminated union for type safety)
 */
export type ChatApiResponse =
  | { success: true; data: TutorResponse }
  | { success: false; error: ValidationError; statusCode: number };

/**
 * Chat API client configuration
 */
export interface ChatApiConfig {
  /** Base URL of the chat API (e.g., "http://localhost:8000") */
  baseUrl: string;

  /** Request timeout in milliseconds (default: 35000 = 35 seconds) */
  timeout?: number;

  /** Custom headers to include in all requests */
  headers?: Record<string, string>;
}

// ============================================================================
// Example API Client Implementation
// ============================================================================

/**
 * Example chat API client for frontend integration
 *
 * Usage:
 * ```typescript
 * const client = new ChatApiClient({ baseUrl: "http://localhost:8000" });
 * const response = await client.sendQuestion("What is Physical AI?");
 *
 * if (response.success) {
 *   console.log(response.data.response);
 * } else {
 *   console.error(response.error.message);
 * }
 * ```
 */
export class ChatApiClient {
  private config: Required<ChatApiConfig>;

  constructor(config: ChatApiConfig) {
    this.config = {
      baseUrl: config.baseUrl,
      timeout: config.timeout ?? 35000,
      headers: config.headers ?? {},
    };
  }

  /**
   * Send a question to the AI tutor
   *
   * @param question - Student's learning question
   * @returns Promise resolving to success/error response
   *
   * @throws Never throws - all errors are returned in the response object
   */
  async sendQuestion(question: string): Promise<ChatApiResponse> {
    // Client-side validation
    const validationError = validateStudentQuestion(question);
    if (validationError) {
      return {
        success: false,
        statusCode: 422,
        error: {
          error_type: ErrorType.VALIDATION,
          message: validationError,
          field: "question",
          timestamp: new Date().toISOString(),
        },
      };
    }

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), this.config.timeout);

      const response = await fetch(`${this.config.baseUrl}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...this.config.headers,
        },
        body: JSON.stringify({ question } satisfies StudentQuestion),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      // Success response
      if (response.ok) {
        const data: TutorResponse = await response.json();
        return { success: true, data };
      }

      // Error response
      const error: ValidationError = await response.json();
      return { success: false, statusCode: response.status, error };
    } catch (err) {
      // Network or timeout error
      const isTimeout = err instanceof Error && err.name === "AbortError";

      return {
        success: false,
        statusCode: isTimeout ? 504 : 500,
        error: {
          error_type: isTimeout ? ErrorType.TIMEOUT : ErrorType.SERVICE,
          message: isTimeout
            ? "Request timed out. Please try again."
            : "Network error. Please check your connection.",
          field: null,
          timestamp: new Date().toISOString(),
        },
      };
    }
  }

  /**
   * Check API health status
   *
   * @returns Promise resolving to health status or null if unhealthy
   */
  async checkHealth(): Promise<HealthResponse | null> {
    try {
      const response = await fetch(`${this.config.baseUrl}/health`, {
        method: "GET",
        headers: this.config.headers,
      });

      if (response.ok) {
        return await response.json();
      }

      return null;
    } catch {
      return null;
    }
  }
}

// ============================================================================
// React Hook Example (Optional)
// ============================================================================

/**
 * Example React hook for chat integration
 *
 * Usage in a React component:
 * ```typescript
 * function ChatInterface() {
 *   const { sendMessage, loading, error, response } = useChatApi();
 *
 *   const handleSubmit = async (question: string) => {
 *     await sendMessage(question);
 *   };
 *
 *   return (
 *     <div>
 *       {loading && <p>Loading...</p>}
 *       {error && <p>Error: {error.message}</p>}
 *       {response && <p>{response.response}</p>}
 *     </div>
 *   );
 * }
 * ```
 */
export interface UseChatApiReturn {
  /** Send a message to the AI tutor */
  sendMessage: (question: string) => Promise<void>;

  /** Loading state */
  loading: boolean;

  /** Last error (null if no error) */
  error: ValidationError | null;

  /** Last successful response (null if no response yet) */
  response: TutorResponse | null;

  /** Reset error and response state */
  reset: () => void;
}

// Note: Actual implementation would use React hooks (useState, useCallback)
// This is just the interface definition for reference
