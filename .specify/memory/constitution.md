<!--
Sync Impact Report:
- Version change: [NEW] → 1.0.0
- Initial constitution creation for Physical AI Textbook project
- Added sections: Core Principles (7), Educational Quality Standards, Technical Architecture, Governance
- Templates requiring updates:
  ✅ constitution.md (this file)
  ⚠ plan-template.md (pending review)
  ⚠ spec-template.md (pending review)
  ⚠ tasks-template.md (pending review)
- Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Educational-First Design
Every feature, interface, and interaction must serve the learning goals of students studying
Physical AI and Humanoid Robotics. Content must be:
- Accessible to learners with varying software/hardware backgrounds
- Progressive in difficulty (foundational concepts before advanced topics)
- Supported by practical examples, simulations, and hands-on exercises
- Aligned with the course modules: ROS 2, Gazebo/Unity, NVIDIA Isaac, and VLA

**Rationale**: The textbook's primary mission is education. Technical excellence without
pedagogical clarity fails students. Features that don't enhance learning create noise.

### II. AI-Native Content Creation
All content creation and maintenance MUST leverage AI tooling (Claude Code, Spec-Kit Plus)
following spec-driven development principles:
- Specifications (`specs/<feature>/spec.md`) define requirements before implementation
- Architectural plans (`specs/<feature>/plan.md`) document design decisions
- Tasks (`specs/<feature>/tasks.md`) break work into testable increments
- Prompt History Records (PHRs) capture AI collaboration for transparency and learning
- Architecture Decision Records (ADRs) document significant technical choices

**Rationale**: This project demonstrates AI-native workflows. The process is as instructive
as the product. Students and contributors learn modern AI-assisted development practices.

### III. RAG-First Information Architecture
The integrated Retrieval-Augmented Generation (RAG) chatbot is not a bonus feature—it is
the primary interface for dynamic learning:
- All textbook content MUST be vectorized and searchable via the RAG system
- Chatbot responses MUST cite specific sections/pages with accurate references
- User-selected text MUST be queryable for contextual explanations
- Question-answer quality drives content structure (optimize for retrieval clarity)

**Rationale**: Static textbooks limit engagement. RAG enables personalized, just-in-time
learning, making complex Physical AI concepts accessible through conversation.

### IV. Personalization & Accessibility (NON-NEGOTIABLE)
Logged-in users MUST be able to:
- Complete onboarding questionnaire (software/hardware background at signup)
- Request personalized content adjustments per chapter (button at chapter start)
- Translate content to Urdu (button at chapter start)
- Persist preferences across sessions

**Rationale**: Inclusivity is mandatory. Students in Pakistan and global markets have
diverse backgrounds and language needs. One-size-fits-all content excludes learners.

### V. Security & Privacy by Design
- Authentication via Better-Auth with secure credential handling (no plaintext passwords)
- User data (backgrounds, preferences) stored in Neon Serverless Postgres with encryption
- No PII in vector embeddings; user queries anonymized in logs
- API keys and secrets MUST use environment variables (`.env`), never hardcoded
- OWASP Top 10 protections: input validation, SQL injection prevention, XSS mitigation

**Rationale**: Educational platforms collect sensitive learner data. Breaches destroy
trust and violate legal obligations (GDPR, local data protection laws).

### VI. Performance & Scalability Standards
- Frontend: Docusaurus static site generation ensures <2s initial page load
- Backend: FastAPI endpoints respond in <200ms (p95) for RAG queries
- Database: Neon Postgres configured for connection pooling (max 10 concurrent)
- Vector search: Qdrant Cloud Free Tier optimized for <500ms retrieval (p95)
- Embedding generation: Batch user queries; cache frequent embeddings (Redis if needed)

**Rationale**: Slow responses disrupt learning flow. Students on limited bandwidth
(common in target markets) abandon sluggish platforms. Scalability ensures the textbook
supports cohorts of 100+ simultaneous users.

### VII. Open Source & Reproducibility
- Public GitHub repository with clear README, setup instructions, and contribution guide
- Deployment documented for GitHub Pages and Vercel (free tiers prioritized)
- All dependencies versioned (package.json, requirements.txt) with lockfiles
- Sample .env.example provided; no secrets in version control
- Docker Compose configuration for local development (backend + Postgres + Qdrant)

**Rationale**: As an educational resource and potential Panaversity foundation, the
project must be forkable, modifiable, and teachable. Reproducibility enables community
contributions and multi-institution adoption.

## Educational Quality Standards

### Content Structure
- **Module-Chapter-Section Hierarchy**: Align with 4-module course outline (ROS 2,
  Gazebo/Unity, NVIDIA Isaac, VLA)
- **Learning Objectives**: Every chapter starts with 3-5 measurable learning outcomes
- **Hands-On Labs**: Practical exercises with URDF models, Gazebo simulations, Isaac Sim
  scenarios
- **Assessments**: Self-check quizzes, code challenges, capstone project guidance
- **Prerequisites**: Explicit prerequisite knowledge listed per chapter (Python, Linux,
  linear algebra)

### Code Examples & Artifacts
- All code snippets MUST be syntax-highlighted, tested, and runnable
- Provide GitHub repo links to complete examples (separate `examples/` directory)
- URDF/SDF robot models, ROS 2 launch files, Isaac Sim scenes versioned alongside text
- Simulation setup scripts for Gazebo/Unity to minimize student friction

### Multimodal Learning
- Diagrams (ROS 2 node graphs, robot kinematics) generated via Mermaid/Draw.io
- Videos embedded for complex topics (bipedal locomotion, VSLAM visualization)
- Interactive simulations (JavaScript-based robot visualizers where feasible)
- Audio support for accessibility (text-to-speech friendly markdown)

## Technical Architecture

### Frontend (Docusaurus)
- **Framework**: Docusaurus 3.x (React-based static site generator)
- **Styling**: Minimal custom CSS; leverage Docusaurus theming for consistency
- **Components**:
  - RAG Chatbot embed (React component with WebSocket or REST to backend)
  - Personalization button (per-chapter content adjustment trigger)
  - Translation toggle (Urdu/English switcher)
  - User profile widget (shows background, preferences)
- **Build Output**: Static HTML/CSS/JS deployed to GitHub Pages or Vercel

### Backend (FastAPI + Python)
- **Framework**: FastAPI with async/await for concurrent RAG requests
- **Endpoints**:
  - `/auth/*`: Better-Auth integration (signup, signin, session management)
  - `/chat`: RAG query endpoint (text input → vector search → LLM augmentation → response)
  - `/personalize`: Content adjustment based on user background
  - `/translate`: On-demand Urdu translation (OpenAI API or DeepL)
- **Dependencies**: OpenAI Agents/ChatKit SDKs, Langchain (optional), SQLAlchemy (ORM)
- **Deployment**: Containerized (Docker) with Uvicorn ASGI server

### Database (Neon Serverless Postgres)
- **Schema**:
  - `users`: id, email, hashed_password, background_answers (JSONB), preferences (JSONB)
  - `chat_logs`: id, user_id, query, response, timestamp (for analytics, anonymized)
  - `content_versions`: id, chapter_id, user_id, personalized_content (cached adjustments)
- **Migrations**: Alembic for schema versioning
- **Backups**: Neon automatic backups; export scripts for local dev seeding

### Vector Store (Qdrant Cloud Free Tier)
- **Collections**:
  - `textbook_chunks`: Chapter/section embeddings (OpenAI `text-embedding-3-small`)
  - Metadata: chapter_title, section_id, page_url, content_type (text/code/diagram)
- **Indexing**: HNSW algorithm (default); optimize for recall over speed
- **Query Strategy**: Hybrid search (vector similarity + keyword filtering by chapter)

### Authentication (Better-Auth)
- **Provider**: Email/password (primary); optional Google OAuth for future
- **Session Management**: JWT tokens (HttpOnly cookies); 7-day expiry
- **Onboarding Flow**: Post-signup redirect to questionnaire (background capture)
- **Middleware**: FastAPI dependency injection for protected routes

## Development Workflow

### Spec-Driven Development (SDD) Cycle
1. **Specification**: Draft `spec.md` defining feature requirements and acceptance criteria
2. **Planning**: Architect in `plan.md` with API contracts, data models, ADRs
3. **Tasking**: Break into testable tasks in `tasks.md` (TDD red-green-refactor)
4. **Implementation**: Code with Claude Code assistance; capture PHRs
5. **Review**: Validate against spec; update docs; commit with semantic versioning

### Testing Requirements
- **Unit Tests**: FastAPI route tests (pytest); React component tests (Jest)
- **Integration Tests**: End-to-end RAG flow (user query → backend → Qdrant → OpenAI → response)
- **Performance Tests**: Load testing with Locust (100 concurrent users; <200ms p95)
- **Accessibility Tests**: WCAG 2.1 AA compliance (axe-core audits)

### Commit & Branching
- **Main Branch**: Protected; requires PR approval
- **Feature Branches**: `feature/<feature-name>` (aligned with specs directory)
- **Commit Messages**: Conventional Commits (e.g., `feat: add Urdu translation button`)
- **Version Tags**: Semantic versioning (v1.0.0 for initial release)

### Documentation Standards
- **README.md**: Setup, deployment, contributing guidelines
- **API Docs**: FastAPI auto-generated OpenAPI (Swagger UI at `/docs`)
- **ADRs**: Stored in `history/adr/` for architectural decisions
- **PHRs**: Stored in `history/prompts/` for AI collaboration transparency

## Governance

### Constitutional Authority
This constitution supersedes all other project practices, guidelines, or conventions.
Any conflict between this document and other documentation MUST be resolved in favor
of the constitution. Deviations require explicit amendment (see below).

### Amendment Process
1. **Proposal**: Submit GitHub issue titled "Constitution Amendment: [brief description]"
2. **Discussion**: Minimum 3-day public comment period
3. **Approval**: Requires approval from project maintainers (Panaversity core team if applicable)
4. **Migration Plan**: Document breaking changes, provide upgrade path for contributors
5. **Versioning**: Update `CONSTITUTION_VERSION` following semantic rules (see below)

### Version Incrementing Rules
- **MAJOR (X.0.0)**: Backward-incompatible governance changes (e.g., removing a core principle)
- **MINOR (1.X.0)**: New principles added or significant expansions (e.g., new security requirements)
- **PATCH (1.0.X)**: Clarifications, typo fixes, non-semantic refinements

### Compliance Verification
- All Pull Requests MUST include a checklist verifying adherence to Core Principles
- PRs introducing complexity (new dependencies, architecture changes) MUST justify against
  Principle VII (Open Source & Reproducibility)
- Quarterly constitution audits to ensure templates (spec, plan, tasks, PHR, ADR) remain aligned

### Runtime Guidance
For day-to-day development decisions not covered explicitly in this constitution,
refer to `CLAUDE.md` (agent-specific guidance) and the current feature's `plan.md`.

**Version**: 1.0.0 | **Ratified**: 2025-12-13 | **Last Amended**: 2025-12-13
