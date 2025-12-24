# Implementation Plan: Chatbot Homepage Integration and UI Redesign

**Branch**: `001-chatbot-homepage-redesign` | **Date**: 2025-12-24 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-chatbot-homepage-redesign/spec.md`

## Summary

Integrate the existing chatbot component onto the homepage, connect it to the backend `/chat` API endpoint, redesign the UI with a modern clean layout, and eliminate all frontend runtime errors. All changes are frontend-only; the backend API remains unchanged.

**Primary Requirement**: Enable users to access the AI tutor chatbot directly from the homepage with a modern, error-free interface.

**Technical Approach**:
1. Fix existing runtime error in ChatWidget.tsx (`closeChat` undefined reference)
2. Import and render ChatWidgetWithProvider component in homepage (index.tsx)
3. Update CSS for modern chat UI design (gradients, smooth animations, responsive breakpoints)
4. Verify zero runtime errors through TypeScript validation and browser console testing
5. Use existing @chatscope/chat-ui-kit-react components with custom styling
6. Maintain existing backend API contract (no backend changes)

## Technical Context

**Language/Version**: TypeScript 5.6.2 / JavaScript ES6+
**Primary Dependencies**:
- React 19.0.0 (concurrent features, latest stable)
- Docusaurus 3.9.2 (static site generator, homepage framework)
- @chatscope/chat-ui-kit-react 2.1.1 (chat UI components)
- @chatscope/chat-ui-kit-styles 1.4.0 (chat UI styling)

**Storage**:
- localStorage (chat session persistence, widget state)
- Session storage not required (no cross-tab communication)

**Testing**:
- TypeScript compiler (`npm run typecheck`)
- Manual testing with browser DevTools Console
- Docusaurus build verification (`npm run build`)

**Target Platform**:
- Modern browsers (Chrome/Edge/Firefox/Safari last 2 versions)
- Desktop (1024px+), Tablet (768px-1023px), Mobile (320px-767px)
- No IE11 support (React 19 requirement)

**Project Type**: Web application (Docusaurus frontend + FastAPI backend)

**Performance Goals**:
- Chat opens in < 2 seconds (SC-001)
- Message round-trip < 5 seconds excluding backend (SC-002)
- Zero runtime errors (SC-003)
- 95%+ successful API requests (SC-004)

**Constraints**:
- No backend modifications allowed (user requirement)
- Must return full updated frontend files
- Zero runtime errors mandatory (FR-012)
- Must work within Docusaurus architecture
- Rate limiting: 3 requests per 30 seconds (client-side)

**Scale/Scope**:
- Single-page integration (homepage only)
- ~10 modified/created files
- ~500-1000 lines of code (including CSS)
- Expected 4-6 hours implementation time

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Educational-First Design ✅ PASS

**Requirement**: Features must serve learning goals and be accessible to learners with varying backgrounds.

**Compliance**:
- ✅ Chatbot provides direct access to AI tutor from homepage
- ✅ User-friendly error messages (no technical jargon exposed)
- ✅ Input validation prevents confusion (3-10,000 char limit)
- ✅ Modern UI improves learning experience (clear visual hierarchy)
- ✅ Responsive design works on all devices (accessibility for all learners)

**Justification**: This feature directly enhances the primary learning interface by making the AI tutor immediately accessible and user-friendly.

### II. AI-Native Content Creation ✅ PASS

**Requirement**: All development must leverage AI tooling following spec-driven development.

**Compliance**:
- ✅ Specification created (`spec.md`) defining all requirements
- ✅ Planning artifacts generated (`plan.md`, `research.md`, `data-model.md`)
- ✅ Contracts documented (`api-contract.md`, `component-contract.md`)
- ✅ PHR will be created to capture this planning session
- ✅ ADR candidates identified (see Section below)

**Justification**: This entire planning process follows SDD principles with comprehensive documentation.

### III. RAG-First Information Architecture ✅ PASS

**Requirement**: Integrated RAG chatbot is the primary interface for dynamic learning.

**Compliance**:
- ✅ Homepage integration makes RAG chatbot primary user touchpoint
- ✅ Existing backend `/chat` endpoint connects to RAG system
- ✅ Chatbot already supports citation and context (backend feature)
- ✅ This feature increases visibility and accessibility of RAG system

**Justification**: Moving chatbot to homepage elevates RAG to primary learning interface as required by constitution.

### IV. Personalization & Accessibility ⚠️ PARTIAL (Non-blocking)

**Requirement**: Logged-in users must be able to customize content and translate to Urdu.

**Compliance**:
- ⚠️ Chatbot accessible without login (no authentication required per spec)
- ✅ Keyboard navigation supported (Tab, Enter, Escape)
- ✅ ARIA labels for screen readers
- ✅ High contrast support in CSS
- ✅ Responsive design for all devices
- ⚠️ Urdu translation not in scope for this feature (chatbot responses only)
- ⚠️ Personalization not in scope (chatbot provides general responses)

**Justification**: Basic accessibility met (WCAG 2.1 AA). Personalization and Urdu support are future features beyond current scope. This is acceptable as chatbot still provides educational value to all users.

### V. Security & Privacy by Design ✅ PASS

**Requirement**: Secure credential handling, no PII in logs, environment variables for secrets.

**Compliance**:
- ✅ No authentication required (no credentials handled)
- ✅ Backend URL from environment variable (`REACT_APP_BACKEND_URL`)
- ✅ No PII collected or stored (messages stored in localStorage only)
- ✅ Input validation prevents XSS (message content sanitized)
- ✅ Rate limiting prevents abuse (3 requests per 30 seconds)
- ✅ Error messages don't expose backend details

**Justification**: No security vulnerabilities introduced. All sensitive data (if any) handled by backend.

### VI. Performance & Scalability Standards ✅ PASS

**Requirement**: Frontend <2s page load, Backend <200ms p95 for RAG queries.

**Compliance**:
- ✅ Static Docusaurus site ensures fast page load
- ✅ Chat opens in <2 seconds (local React state, no network)
- ✅ Backend performance not affected (no backend changes)
- ✅ Frontend rate limiting prevents backend overload
- ✅ React.memo and useCallback for rendering optimization
- ✅ localStorage persistence lightweight

**Justification**: Performance targets met or exceeded. No performance regressions introduced.

### VII. Open Source & Reproducibility ✅ PASS

**Requirement**: Public repo, clear setup, versioned dependencies, no secrets in version control.

**Compliance**:
- ✅ All code changes in feature branch `001-chatbot-homepage-redesign`
- ✅ Dependencies already versioned in `package.json`
- ✅ `.env.example` approach for configuration
- ✅ Quickstart guide (`quickstart.md`) provides setup instructions
- ✅ No secrets hardcoded (backend URL configurable)

**Justification**: Feature follows existing repository patterns and maintains reproducibility.

### Constitutional Compliance Summary

**Overall Status**: ✅ **PASS** (6 full passes, 1 partial)

**Non-Blocking Issues**:
- Personalization (IV): Not in scope for chatbot feature (future enhancement)
- Urdu translation (IV): Backend feature, not frontend integration

**Recommendation**: Proceed with implementation. All core principles satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/001-chatbot-homepage-redesign/
├── spec.md                  # Feature specification (✅ Created by /sp.specify)
├── plan.md                  # This file (✅ Created by /sp.plan)
├── research.md              # Phase 0 output (✅ Created by /sp.plan)
├── data-model.md            # Phase 1 output (✅ Created by /sp.plan)
├── quickstart.md            # Phase 1 output (✅ Created by /sp.plan)
├── contracts/               # Phase 1 output (✅ Created by /sp.plan)
│   ├── api-contract.md      # Backend API contract documentation
│   └── component-contract.md # React component contracts
├── checklists/              # Quality validation checklists
│   └── requirements.md      # Spec quality checklist (✅ All passed)
└── tasks.md                 # Phase 2 output (⏳ Created by /sp.tasks - NOT YET CREATED)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── components/
│   │   ├── ChatWidget/               # Chat components (MODIFY)
│   │   │   ├── ChatWidget.tsx        # ✏️ Fix closeChat() error
│   │   │   ├── ChatWindow.tsx        # ✅ Keep existing
│   │   │   ├── chat-widget.css       # ✏️ Redesign UI styles
│   │   │   ├── chat-service.ts       # ✅ Keep existing
│   │   │   ├── models.ts             # ✅ Keep existing
│   │   │   └── hooks.ts              # ✅ Keep existing
│   │   └── HomepageFeatures/         # ✅ Keep existing
│   ├── contexts/
│   │   └── ChatContext.tsx           # ✅ Verify provider exists
│   ├── pages/
│   │   └── index.tsx                 # ✏️ Add ChatWidget import
│   └── theme/
│       └── Layout/                   # ✅ Keep existing
├── .env                              # ✏️ Add REACT_APP_BACKEND_URL
├── .env.example                      # ➕ Create (optional)
├── package.json                      # ✅ No changes needed
└── tsconfig.json                     # ✅ No changes needed

backend/                              # ✅ NO CHANGES (per user requirement)
└── src/
    └── backend/
        └── main.py                   # ✅ Keep existing /chat endpoint
```

**Structure Decision**: Web application structure (frontend + backend). Frontend changes only. All modifications are in existing `frontend/` directory. Backend remains completely unchanged per user constraint.

**Key Files to Modify** (5 total):
1. `frontend/src/components/ChatWidget/ChatWidget.tsx` - Fix runtime error
2. `frontend/src/components/ChatWidget/chat-widget.css` - Redesign UI
3. `frontend/src/pages/index.tsx` - Add ChatWidget to homepage
4. `frontend/.env` - Add backend URL configuration
5. `frontend/.env.example` - Document environment variables

**Files to Verify** (no changes needed, verify only):
- `frontend/src/contexts/ChatContext.tsx` - Ensure ChatProvider exists
- `frontend/src/components/ChatWidget/ChatWindow.tsx` - Verify no errors
- `frontend/src/components/ChatWidget/chat-service.ts` - Verify API integration
- `frontend/package.json` - Verify dependencies installed

## Complexity Tracking

No constitutional violations requiring justification. All changes align with existing architecture and principles.

## Phase 0: Research Summary

**Completed**: ✅ See [research.md](./research.md)

**Key Decisions Made**:
1. **Frontend Stack**: Docusaurus 3.9.2 + React 19 + TypeScript 5.6.2 (existing)
2. **Chat UI Library**: @chatscope/chat-ui-kit-react 2.1.1 (already installed)
3. **Backend Integration**: Existing `/chat` POST endpoint (no changes)
4. **Homepage Integration**: Import ChatWidget into `index.tsx`
5. **State Management**: React Context API (existing ChatContext)
6. **Styling**: Custom CSS + @chatscope components (modern gradients, animations)
7. **Error Resolution**: Fix `closeChat` reference in ChatWidget.tsx
8. **Performance**: React.memo, useMemo, useCallback for optimization
9. **Accessibility**: WCAG 2.1 AA basics (ARIA, keyboard nav, contrast)
10. **Responsiveness**: Mobile-first, breakpoints at 768px and 1024px
11. **Testing**: Manual + TypeScript + DevTools Console
12. **Browser Support**: Modern evergreen (last 2 versions)

**Unknowns Resolved**: All technical unknowns from spec have been researched and documented.

## Phase 1: Design & Contracts Summary

**Completed**: ✅ See [data-model.md](./data-model.md) and [contracts/](./contracts/)

### Data Model

**Core Entities** (5 total):
1. **ChatMessage**: Single message with id, content, sender, timestamp, status
2. **ChatSession**: Conversation state with messages, rate limit, connection status
3. **ChatWidgetState**: UI state (expanded, visible, position, unread count)
4. **ChatRequest**: API request with message text
5. **ChatResponse**: API response with response text, agent name, timestamp

**Validation Rules**:
- Message length: 3-10,000 characters (trim before validation)
- Rate limit: 3 requests per 30-second window
- Timestamp format: ISO 8601 (e.g., "2025-12-24T10:30:00.000Z")

**State Management**:
- React Context: `ChatContext` provides global visibility state
- Component State: `ChatWidget` and `ChatWindow` manage local UI state
- Persistence: localStorage for session and widget state (cleared on page reload)

### API Contract

**Endpoint**: `POST {BACKEND_URL}/chat`

**Request**:
```json
{
  "message": "string (3-10,000 chars)"
}
```

**Success Response** (200):
```json
{
  "response": "string",
  "agent_name": "string",
  "timestamp": "string (ISO 8601)"
}
```

**Error Responses**:
- 422: Validation error → "Please check your message and try again"
- 429: Rate limit → "Too many requests. Please wait 30 seconds"
- 500: Server error → "AI tutor temporarily unavailable"
- 504: Timeout → "Request timed out. Please try again"
- Network: Connection error → "Unable to connect. Check your connection"

**Rate Limiting**:
- Frontend: 3 requests per 30 seconds (proactive)
- Backend: 3 requests per minute (per IP)

**Timeout**: 30 seconds (frontend configurable)

### Component Contract

**Component Hierarchy**:
```
Homepage → ChatProvider → ChatWidget → [ChatToggleButton | ChatWindow]
ChatWindow → ChatHeader + ChatMessageList + ChatInput
ChatMessageList → ChatMessage[]
```

**Key Components** (9 total):
1. **ChatProvider**: Global visibility context
2. **ChatWidget**: Main container (toggle + window)
3. **ChatToggleButton**: FAB button to open chat
4. **ChatWindow**: Full chat interface
5. **ChatHeader**: Title bar with close button
6. **ChatMessageList**: Scrollable message container
7. **ChatMessage**: Individual message bubble
8. **ChatInput**: Text input with send button
9. **ChatService**: API communication class

**Props & Events**: See [contracts/component-contract.md](./contracts/component-contract.md)

## Architecture Decision Records (ADR Candidates)

**Significant Decisions Requiring Documentation**:

### ADR-001: Use Existing @chatscope UI Library vs Build Custom

**Decision**: Use @chatscope/chat-ui-kit-react for UI components

**Rationale**:
- Already installed and working
- Provides accessibility (ARIA, keyboard nav) out of the box
- Saves development time (4-6 hours vs 12-16 hours custom)
- Battle-tested in production applications
- Customizable via CSS (meets modern design requirement)

**Alternatives Considered**:
- Build from scratch: More control, but much longer timeline
- Material-UI Chat: Not installed, adds dependency
- HeadlessUI + custom: More work, same result

**Consequences**:
- Dependency on external library (acceptable trade-off)
- Library updates may require changes
- Custom styling may conflict with library updates

**Recommendation**: Document with `/sp.adr use-chatscope-ui-library`

### ADR-002: Frontend Rate Limiting vs Backend Only

**Decision**: Implement rate limiting on both frontend (3/30s) and backend (3/min)

**Rationale**:
- Frontend proactive limiting improves UX (immediate error, no network wait)
- Backend limiting prevents abuse and protects AI service quota
- Dual approach ensures users never hit backend limit unintentionally
- Frontend state management already in place

**Alternatives Considered**:
- Backend only: Poorer UX, network requests wasted
- Frontend only: Vulnerable to manipulation
- No rate limiting: Backend overload, quota exhaustion

**Consequences**:
- Frontend and backend must stay in sync (30s vs 60s window acceptable)
- More complex state management (rate limit tracking)
- Better user experience and system protection

**Recommendation**: Document with `/sp.adr frontend-rate-limiting`

### ADR-003: localStorage vs SessionStorage for Persistence

**Decision**: Use localStorage for chat session and widget state

**Rationale**:
- Requirement FR-014: Preserve history during current session
- "Current session" interpreted as browser tab session (until page reload)
- localStorage persists across tab reload (better UX if user accidentally refreshes)
- sessionStorage would lose data on refresh (poor UX)
- Data cleared on page navigation (acceptable per spec: "not persistent across sessions")

**Alternatives Considered**:
- sessionStorage: More secure, but loses data on refresh
- No persistence: Poor UX, loses conversation on refresh
- Backend persistence: Out of scope, requires backend changes

**Consequences**:
- Data persists across refresh (may confuse users expecting fresh start)
- Privacy consideration: Messages stored locally (acceptable for educational content)
- Clear on logout or cache clear (standard behavior)

**Recommendation**: Document with `/sp.adr localstorage-persistence`

**Note**: User can run `/sp.adr` after `/sp.tasks` to generate ADR files for these decisions.

## Implementation Roadmap

### Phase 2: Tasks (Next Step)

Run `/sp.tasks` to generate:
- `specs/001-chatbot-homepage-redesign/tasks.md`
- Testable task breakdown following TDD (red-green-refactor)
- Each task with acceptance criteria and test cases

**Expected Tasks** (estimated):
1. Fix ChatWidget.tsx closeChat error (15 min)
2. Add ChatWidget to homepage (15 min)
3. Redesign chat-widget.css (2 hours)
4. Configure environment variables (15 min)
5. Test all requirements (1-2 hours)
6. Fix any discovered bugs (30 min - 1 hour)
7. Build production and verify (30 min)

**Total Estimated Time**: 4-6 hours

### Phase 3: Implementation

After `/sp.tasks` generates task list:
1. Follow tasks in order (TDD: red → green → refactor)
2. Run `npm run typecheck` after each task
3. Test in browser after each task
4. Verify no console errors
5. Update PHRs for significant changes

### Phase 4: Review & Deploy

1. Final testing checklist (see quickstart.md)
2. Create pull request
3. Code review
4. Merge to main branch
5. Deploy to production (GitHub Pages or Vercel)

## Success Criteria Verification

**From Spec** (8 criteria):

| ID | Criteria | How to Verify | Target |
|----|----------|---------------|--------|
| SC-001 | Open chatbot in <2 seconds | Measure click to render time | <2s |
| SC-002 | Message round-trip <5 seconds | Measure send to response display | <5s |
| SC-003 | Zero runtime errors | Browser console monitoring | 0 errors |
| SC-004 | 95%+ successful API requests | Network tab success rate | >95% |
| SC-005 | Responsive 320px-1920px | Test all breakpoints | All sizes work |
| SC-006 | 80%+ user satisfaction | User feedback (post-launch) | >80% |
| SC-007 | 100% input validation | Test edge cases | 100% |
| SC-008 | User-friendly error messages | Review all error paths | All friendly |

**Verification Plan**: See [quickstart.md](./quickstart.md) Testing section

## Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Browser compatibility issues | Low | Medium | Test in Chrome, Firefox, Safari |
| Backend API changes | Low | High | API contract documented, backend frozen |
| TypeScript errors | Medium | Low | Run typecheck frequently |
| CSS conflicts with Docusaurus | Low | Medium | Scope CSS with class prefixes |
| Performance regression | Low | Medium | Benchmark before/after |
| Accessibility gaps | Medium | Medium | Follow WCAG 2.1 AA checklist |

## Next Steps

1. ✅ **Complete**: Spec, Plan, Research, Data Model, Contracts, Quickstart
2. ⏳ **Next**: Run `/sp.tasks` to generate implementation tasks
3. ⏳ **Then**: Implement tasks following TDD approach
4. ⏳ **Finally**: Test, review, deploy

## Appendix: File Manifest

**Created by /sp.plan** (✅ Complete):
- ✅ `specs/001-chatbot-homepage-redesign/plan.md` (this file)
- ✅ `specs/001-chatbot-homepage-redesign/research.md`
- ✅ `specs/001-chatbot-homepage-redesign/data-model.md`
- ✅ `specs/001-chatbot-homepage-redesign/quickstart.md`
- ✅ `specs/001-chatbot-homepage-redesign/contracts/api-contract.md`
- ✅ `specs/001-chatbot-homepage-redesign/contracts/component-contract.md`

**To be Created by /sp.tasks**:
- ⏳ `specs/001-chatbot-homepage-redesign/tasks.md`

**To be Modified during Implementation**:
- ⏳ `frontend/src/components/ChatWidget/ChatWidget.tsx`
- ⏳ `frontend/src/components/ChatWidget/chat-widget.css`
- ⏳ `frontend/src/pages/index.tsx`
- ⏳ `frontend/.env`
- ⏳ `frontend/.env.example`

---

**Plan Version**: 1.0
**Last Updated**: 2025-12-24
**Status**: ✅ Ready for /sp.tasks
