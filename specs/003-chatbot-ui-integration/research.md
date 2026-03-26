# Research: Chatbot UI Integration for Docusaurus Book

## Decision 1: Frontend Integration Method

### Rationale:
For integrating a global chat widget into Docusaurus, there are several approaches available. After researching Docusaurus architecture and best practices, I've determined that using a custom React component with theme swizzling is the most appropriate approach for this feature.

### Research Findings:
- **Docusaurus Theme Swizzling**: Docusaurus allows "swizzling" theme components to customize them. This is the recommended approach for modifying the layout to include global components like a chat widget.
- **Root Layout Wrapper**: Another approach is to wrap the entire application with a React component using the `wrapRootComponent` lifecycle API.
- **Static-Site Injection**: This would involve injecting the widget at build time, which is less flexible.

### Decision:
**Approach: Theme Component Swizzling** - Specifically, swizzling the `Layout` component to inject the chat widget globally. This approach:
- Follows Docusaurus best practices
- Maintains compatibility with future Docusaurus updates
- Allows the widget to appear on all pages consistently
- Preserves the existing layout while adding the new functionality

### Alternatives Considered:
1. **Root Layout Wrapper**: While possible, this approach is less aligned with Docusaurus patterns
2. **Static Injection**: Too rigid and doesn't allow for dynamic behavior
3. **Component Swizzling**: More granular control but might miss some pages

## Decision 2: API Communication Protocol

### Rationale:
The specification mentions streaming responses from the backend, but we need to decide on the specific communication protocol between the frontend and backend `/chat` endpoint.

### Research Findings:
- **Standard REST/JSON**: Traditional request-response pattern where the frontend sends a POST request and waits for a complete response
- **Server-Sent Events (SSE)**: Allows the server to push streaming data to the client
- **WebSocket**: Full-duplex communication channel
- **Backend Capability**: The backend is already configured to return streaming responses (as per spec context)

### Decision:
**Approach: Server-Sent Events (SSE)** - Since the backend is already configured to return streaming chat responses, SSE is the most appropriate choice because:
- It's designed for server-to-client streaming
- It's simpler than WebSockets for this use case
- It's supported natively in browsers
- It allows real-time display of responses as they're generated (fulfilling FR-004)
- It's more efficient than polling for streaming responses

### Alternatives Considered:
1. **Standard REST/JSON**: Would require waiting for complete response, not optimal for streaming
2. **WebSocket**: More complex setup than needed for this one-way streaming requirement
3. **Polling**: Inefficient and would not provide real-time experience

## Decision 3: CORS Configuration Strategy

### Rationale:
The frontend (Docusaurus) will be served from a different origin than the backend (FastAPI), requiring proper CORS configuration.

### Research Findings:
- **FastAPI CORS Middleware**: FastAPI provides built-in `CORSMiddleware` that's easy to configure
- **Development vs Production**: Different origins will be used in development (localhost) vs production
- **Security Considerations**: Need to be specific about allowed origins to prevent security issues

### Decision:
**Approach: FastAPI CORSMiddleware with Environment Configuration** - Configure CORS in the FastAPI application using environment variables to specify allowed origins, which will:
- Support both development and production environments
- Maintain security by specifying exact origins
- Work with the existing uv environment setup

### Alternatives Considered:
1. **Wildcard CORS**: Insecure and not recommended for production
2. **Proxy configuration**: More complex but not necessary for this use case

## Decision 4: Chat UI Library Selection

### Rationale:
The specification requires installing a React-compatible chat component library. We need to select the most appropriate one for educational use.

### Research Findings:
- **@chatscope/chat-ui-kit-react**: Lightweight, well-documented, good customization options
- **react-chat-elements**: Feature-rich but larger bundle size
- **react-simple-chatbot**: More limited functionality
- **Custom implementation**: More control but more development time

### Decision:
**Approach: @chatscope/chat-ui-kit-react** - This library is:
- Lightweight and well-maintained
- Provides the necessary components for a floating chat widget
- Supports customization needed for educational styling
- Has good accessibility features
- Minimal bundle size impact (aligns with NFR-002)

### Alternatives Considered:
1. **react-chat-elements**: Larger bundle size
2. **Custom implementation**: Would require more time and testing

## Decision 5: State Management Strategy

### Rationale:
The chat widget needs to maintain state across page navigation (FR-010) and handle concurrent users.

### Research Findings:
- **React Context + useState**: Suitable for local state management within the component
- **localStorage**: For persisting chat history across page navigation
- **Redux/Recoil**: More complex but unnecessary for this use case
- **Browser Session Storage**: Alternative to localStorage for session-based persistence

### Decision:
**Approach: React Context + localStorage** - This combination will:
- Use React Context for real-time state management within the component
- Use localStorage to persist chat history across page navigation
- Maintain chat state during the user session as required
- Be lightweight and efficient (aligns with NFR-001)

### Alternatives Considered:
1. **Redux**: Overkill for this simple state management requirement
2. **Session storage**: Similar to localStorage but clears on tab close