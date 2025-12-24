# Chatbot Frontend UI and API Integration

## Feature Description
Finalize the chatbot frontend UI and integrate it with the existing backend `/chat` endpoint. Focus on UI polish and API integration. Do not modify backend code.

## User Scenarios & Testing

### Primary User Flow
1. User visits the website and sees the floating chat widget
2. User clicks the chat widget to open the chat interface
3. User types a question about Physical AI and Humanoid Robotics
4. User submits the message and sees it appear in the chat
5. User receives a response from the AI tutor
6. Conversation continues with multiple exchanges

### Secondary User Flows
1. User minimizes the chat widget and continues browsing
2. User reopens the chat widget to continue conversation
3. User sees rate limit messages when sending too many requests
4. User receives error messages for invalid inputs

### Testing Scenarios
- Send valid messages of various lengths (3-10,000 characters)
- Test rate limiting (send 4 messages within 30 seconds)
- Test error handling for invalid messages (too short, too long)
- Verify message history persists across page refreshes
- Test UI responsiveness on different screen sizes
- Verify the chat widget appears correctly on all pages

## Functional Requirements

### UI Polish Requirements
1. **Visual Design**: Enhance the current chat interface with improved visual styling, animations, and user feedback elements
2. **Responsive Design**: Ensure the chat interface works seamlessly on mobile, tablet, and desktop devices
3. **User Experience**: Improve the typing indicators, message transitions, and overall interaction flow
4. **Accessibility**: Add proper ARIA labels, keyboard navigation, and screen reader support
5. **Performance**: Optimize rendering of message history and smooth scrolling

### API Integration Requirements
1. **Backend Connection**: Integrate with the existing `/chat` endpoint using proper request/response handling
2. **Authentication Handling**: Update API calls to work with the authentication-removed endpoint (no Authorization header needed)
3. **Error Handling**: Implement proper error handling for various HTTP status codes (422, 429, 500, 504)
4. **Rate Limiting**: Implement client-side rate limiting (3 requests per 30 seconds) to complement backend rate limiting
5. **Message Validation**: Validate message length (3-10,000 characters) before sending to backend
6. **State Persistence**: Maintain chat history and widget state using localStorage

### Data Models
1. **ChatMessage**: Store message content, sender (user/ai), timestamp, and status
2. **ChatSession**: Manage conversation context and rate limiting state
3. **ChatWidgetState**: Track widget visibility, position, and expansion state

## Success Criteria

### User Experience Metrics
- Users can successfully send and receive messages without authentication barriers
- 95% of users complete at least one full conversation (question + response) on first try
- Average response time from user input to AI response is under 3 seconds
- Zero authentication-related errors during chat interactions

### Technical Metrics
- UI renders smoothly with no jank or performance issues
- API integration handles all error cases gracefully
- Rate limiting prevents excessive backend requests
- Message validation prevents invalid inputs from reaching backend
- All UI elements are accessible and keyboard navigable

### Quality Metrics
- All UI elements follow modern design principles with consistent styling
- Mobile responsiveness works across all common screen sizes
- No console errors during normal usage
- All user flows complete without technical barriers

## Key Entities

### Frontend Components
- **ChatWidget**: Floating button that opens/closes the chat interface
- **ChatWindow**: Main chat interface with message history and input area
- **ChatService**: Service layer handling API communication and state management
- **MessageDisplay**: Component for rendering individual messages with sender context
- **InputArea**: Message input field with send button and validation feedback

### Backend API Contract
- **Endpoint**: POST `/chat`
- **Request Format**: `{ "message": "string (3-10,000 chars)" }`
- **Response Format**: `{ "response": "string", "agent_name": "string" }`
- **Error Responses**:
  - 422: Validation error (invalid message format)
  - 429: Rate limit exceeded
  - 500: Internal server error
  - 504: Request timeout

## Assumptions
- Backend `/chat` endpoint is accessible without authentication (as per recent changes)
- Backend endpoint accepts JSON requests and returns JSON responses
- Backend handles rate limiting at the server level
- Network connectivity is available during chat interactions
- Users have JavaScript enabled in their browsers
- Users are accessing the site through a modern web browser

## Scope
### In Scope
- UI polish and visual improvements to existing chat components
- API integration with the `/chat` endpoint
- Authentication removal from API calls (since auth was removed from backend)
- Rate limiting implementation
- Message validation
- State persistence
- Responsive design improvements
- Accessibility enhancements

### Out of Scope
- Backend code modifications
- Database schema changes
- Authentication system modifications
- New backend endpoint creation
- Server-side performance optimizations
- AI model training or improvements

## Dependencies
- Existing backend `/chat` endpoint is operational
- FastAPI backend is running and accessible
- Environment variable `REACT_APP_BACKEND_URL` is properly configured
- Network connectivity to backend service