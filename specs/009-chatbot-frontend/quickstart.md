# Quickstart Guide: Chatbot Frontend Development

## Prerequisites
- Node.js 16+ installed
- Git installed
- Access to the backend API (running on localhost:8000 by default)

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd speckit_book
   ```

2. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

3. **Install dependencies**
   ```bash
   npm install
   ```

4. **Set environment variables**
   Create a `.env` file in the frontend directory:
   ```
   REACT_APP_BACKEND_URL=http://localhost:8000
   ```

5. **Start the development server**
   ```bash
   npm start
   ```

## Development

### Running the Application
- The frontend will be available at `http://localhost:3000`
- The chat widget should appear as a floating button on all pages
- Backend API should be running at `http://localhost:8000`

### Key Components
- **ChatWidget**: Floating button component (src/components/ChatWidget/ChatWidget.tsx)
- **ChatWindow**: Main chat interface (src/components/ChatWidget/ChatWindow.tsx)
- **ChatService**: API integration (src/components/ChatWidget/chat-service.ts)

### Testing Changes
1. Make changes to the components
2. The application will auto-reload
3. Test the chat functionality by sending messages
4. Verify the API integration works without authentication

## API Integration Notes
- The `/chat` endpoint no longer requires authentication
- Requests should be sent as JSON: `{"message": "your message here"}`
- Responses will be in the format: `{"response": "AI response", "agent_name": "Educational Tutor"}`
- Handle error responses appropriately (422, 429, 500, 504)

## Common Tasks

### Adding UI Polish
- Modify CSS in `src/components/ChatWidget/chat-widget.css`
- Update component styling in the JSX files
- Test responsiveness on different screen sizes

### Updating API Integration
- Modify the `sendMessage` function in `chat-service.ts`
- Update request/response handling as needed
- Ensure rate limiting is properly implemented

### Testing
- Send various message lengths to test validation
- Test rate limiting by sending multiple rapid requests
- Verify error handling works correctly