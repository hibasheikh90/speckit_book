# Research Document: OpenAI Agent SDK with OpenAIChatCompletionsModel and Gemini Integration

**Feature**: Backend Chat Communication Service
**Branch**: `001-fastapi-chat-endpoint`
**Date**: 2025-12-14
**Status**: Completed

## Executive Summary

This research resolves all technical unknowns for implementing a FastAPI chat endpoint using the **OpenAI Agent SDK** configured with **OpenAIChatCompletionsModel** and **Gemini 2.0 Flash**. The OpenAI Agent SDK provides a production-ready, Python-first framework for agent orchestration, while OpenAIChatCompletionsModel enables direct model configuration with Gemini.

## 1. OpenAI Agent SDK Architecture

### Decision: Use OpenAI Agent SDK for Agent Orchestration

**What was chosen**: OpenAI Agent SDK (openai-agents) as the primary framework for building the educational AI tutor agent, using OpenAIChatCompletionsModel for Gemini integration.

**Rationale**:
- **Production-Ready**: Described as "a production-ready upgrade" from the earlier Swarm framework
- **Python-First Design**: Leverages native Python features for orchestration rather than proprietary abstractions
- **Built-in Primitives**: Provides Agents, Handoffs, Guardrails, Sessions, and Tracing out of the box
- **Provider Agnostic**: Supports 100+ LLMs through direct model configuration
- **Educational Fit**: Instructions-based configuration aligns with injecting Global Constitution principles

**Alternatives Considered**:
- **Direct OpenAI SDK**: Rejected because it lacks agent orchestration primitives and ties us to OpenAI models
- **Langchain**: Rejected due to higher complexity and less alignment with our simple chat use case
- **Custom Agent Implementation**: Rejected due to development time and lack of production-ready features (session management, tracing, guardrails)

### Core Components

#### 1. Agents
```python
from agents import Agent

agent = Agent(
    name="Educational Tutor",
    instructions="You are an educational AI tutor specializing in Physical AI and Humanoid Robotics..."
)
```

**Key Features**:
- Instructions-based configuration (replaces system messages)
- Tool integration via `@function_tool` decorator
- Handoff support for multi-agent orchestration
- Guardrails for input/output validation

#### 2. Runner (Execution Layer)
```python
from agents import Runner

# Synchronous execution
result = Runner.run_sync(agent, "What is Physical AI?")
print(result.final_output)

# Asynchronous execution
result = await Runner.run(agent, "Explain ROS 2 nodes")
```

**Key Features**:
- `Runner.run_sync()`: Blocking execution for simple use cases
- `Runner.run()`: Async execution for production workloads
- Automatic conversation history management via Sessions
- Built-in tracing for debugging and optimization

#### 3. Sessions (Conversation Management)
- Automatic conversation history tracking across agent runs
- Optional Redis backend for distributed session storage
- In-memory sessions for development and testing

#### 4. Guardrails (Validation Layer)
- Configurable input/output validation
- Safety checks for educational content quality
- Custom guardrails can be implemented as needed

## 2. OpenAIChatCompletionsModel + Gemini Integration

### Decision: Use OpenAIChatCompletionsModel to Configure Gemini 2.0 Flash

**What was chosen**: OpenAIChatCompletionsModel with direct Gemini 2.0 Flash (gemini-2.0-flash) configuration as the underlying language model.

**Rationale**:
- **Direct Integration**: Provides clean, direct access to Gemini models without additional abstraction layers
- **Cost Optimization**: Gemini 2.0 Flash provides excellent performance at lower cost than GPT-4
- **Performance**: Direct model integration offers lower latency than multi-provider solutions
- **OpenAI Agents Compatibility**: Native integration with OpenAI Agents SDK ecosystem
- **Gemini Capabilities**: Supports structured output, tool use, and high token limits

**Alternatives Considered**:
- **OpenAI GPT-4**: Rejected due to higher cost and vendor lock-in
- **Anthropic Claude**: Rejected due to lack of production requirements for multi-provider support
- **LiteLLM**: Rejected because it adds unnecessary abstraction layer when direct integration is available

### Configuration Approach

#### Installation
```bash
pip install openai-agents
```

#### Environment Setup
```bash
export GEMINI_API_KEY="your-api-key-from-google-ai-studio"
```

#### Agent Configuration with OpenAIChatCompletionsModel
```python
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel

# Create AsyncOpenAI client configured for Gemini
gemini_client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY")
)

# Wrap client in OpenAIChatCompletionsModel
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=gemini_client
)

# Initialize agent with Gemini via OpenAIChatCompletionsModel
agent = Agent(
    name="Educational Tutor",
    instructions="You are an educational AI tutor...",
    model=model
)

# Execute
result = await Runner.run(agent, "What is Physical AI?")
```

## 3. Educational Principles Injection

### Decision: Use Agent Instructions for Constitution Integration

**What was chosen**: Load Global Constitution principles and inject them into the Agent's `instructions` parameter.

**Rationale**:
- **Native Support**: OpenAI Agent SDK's instructions parameter is designed for this use case
- **Persistent Context**: Instructions persist across all agent interactions
- **No Token Waste**: Unlike per-message system prompts, instructions are set once
- **Testable**: Easy to validate that responses align with constitutional principles

**Implementation Pattern**:
```python
# Load constitution
constitution_path = ".specify/memory/constitution.md"
with open(constitution_path, "r") as f:
    constitution = f.read()

# Extract educational principles
educational_principles = extract_educational_principles(constitution)

# Create instructions
instructions = f"""
You are an educational AI tutor specializing in Physical AI and Humanoid Robotics.

## Educational Principles (from Global Constitution)
{educational_principles}

## Response Guidelines
- Provide accessible explanations for learners with varying backgrounds
- Use progressive difficulty (foundational concepts before advanced topics)
- Include practical examples, simulations, and hands-on exercises
- Align responses with course modules: ROS 2, Gazebo/Unity, NVIDIA Isaac, and VLA
"""

agent = Agent(name="Educational Tutor", instructions=instructions)
```

## 4. Streaming vs Non-Streaming Responses

### Decision: Start with Non-Streaming, Add Streaming Later

**What was chosen**: Implement non-streaming responses (`Runner.run_sync()`) for MVP, plan for streaming in Phase 2.

**Rationale**:
- **Simplicity First**: Non-streaming is easier to test and debug
- **Success Criteria Alignment**: SC-002 requires responses within 10 seconds, non-streaming meets this
- **Incremental Value**: Can add streaming later without breaking existing functionality
- **Frontend Independence**: Simple JSON response works with any frontend framework

**Non-Streaming Implementation**:
```python
result = Runner.run_sync(agent, question)
response = result.final_output
```

**Future Streaming Implementation**:
```python
async for event in Runner.run_stream(agent, question):
    if event.type == "message":
        yield event.content
```

## 5. FastAPI Integration Pattern

### Decision: Async FastAPI with Pydantic Validation

**What was chosen**: FastAPI with async route handlers, Pydantic models for validation, and structured error responses.

**Rationale**:
- **Async Support**: FastAPI's async capabilities align with `Runner.run()` async API
- **Validation Built-In**: Pydantic models enforce FR-002 (character limits)
- **OpenAPI Documentation**: Auto-generated API docs for frontend developers
- **Error Handling**: Structured exception handling for FR-007 (informative errors)

**Implementation Pattern**:
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=10000)

class QuestionResponse(BaseModel):
    response: str
    agent_name: str

# Initialize agent at startup
@app.on_event("startup")
async def initialize_agent():
    global tutor_agent

    # Create Gemini-configured client
    gemini_client = AsyncOpenAI(
        api_key=settings.gemini_api_key,
        base_url=settings.gemini_base_url,
    )

    # Wrap in OpenAIChatCompletionsModel
    model = OpenAIChatCompletionsModel(
        model=settings.gemini_model,
        openai_client=gemini_client
    )

    # Create agent with instructions (system prompt)
    constitution = load_educational_instructions()
    tutor_agent = Agent(
        name="Educational Tutor",
        instructions=constitution,
        model=model
    )

@app.post("/chat", response_model=QuestionResponse)
async def chat(request: QuestionRequest):
    try:
        result = await Runner.run(tutor_agent, request.question)
        return QuestionResponse(
            response=result.final_output,
            agent_name=tutor_agent.name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## 6. Error Handling Strategy

### Decision: Multi-Layer Error Handling

**What was chosen**: FastAPI validation + Agent-level error handling + Service-level fallbacks.

**Layers**:
1. **Pydantic Validation**: Catch FR-002 violations (character limits)
2. **Agent Guardrails**: Validate educational content quality
3. **Service Exception Handling**: Catch API failures, timeouts, empty responses
4. **Timeout Enforcement**: 30-second timeout via asyncio.wait_for()

**Implementation Pattern**:
```python
import asyncio

@app.post("/chat")
async def chat(request: QuestionRequest):
    try:
        # FR-008: 30-second timeout
        result = await asyncio.wait_for(
            Runner.run(tutor_agent, request.question),
            timeout=30.0
        )

        # FR-009: Check for empty/unusable responses
        if not result.final_output or len(result.final_output.strip()) == 0:
            raise HTTPException(
                status_code=500,
                detail="The tutor service returned an empty response. Please rephrase your question and try again."
            )

        return QuestionResponse(response=result.final_output)

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="The request timed out after 30 seconds. Please try again later."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"The tutor service is temporarily unavailable: {str(e)}"
        )
```

## 7. Rate Limiting Implementation

### Decision: Use slowapi for FastAPI Rate Limiting

**What was chosen**: slowapi library with in-memory storage for MVP, Redis for production.

**Rationale**:
- **FastAPI Native**: Designed specifically for FastAPI applications
- **Simple Integration**: Decorator-based approach
- **FR-013 Compliance**: Enforces 10 requests/minute per student
- **Production Ready**: Supports Redis backend for distributed systems

**Implementation Pattern**:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/chat")
@limiter.limit("10/minute")
async def chat(request: Request, question_request: QuestionRequest):
    # ... implementation
```

## 8. Dependencies and Installation

### Final Dependency List

**Core Dependencies**:
```txt
fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.10.0
openai-agents==0.6.0  # Replaces openai package
slowapi==0.1.9
python-dotenv==1.0.0
```

**Development Dependencies**:
```txt
pytest==8.3.0
pytest-asyncio==0.24.0
httpx==0.28.0
```

**Optional (for future phases)**:
```txt
openai-agents[redis]  # For distributed session management
openai-agents[voice]  # For voice capabilities
```

## 9. Testing Strategy

### Decision: Pytest with Async Support + Contract Testing

**Testing Layers**:

1. **Unit Tests**: Agent initialization, instruction loading, validation logic
2. **Integration Tests**: End-to-end chat flow with mocked Gemini responses
3. **Contract Tests**: Verify Pydantic models match API contracts
4. **Load Tests**: 10 concurrent users (SC-005) using pytest-asyncio

**Example Test Pattern**:
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_valid_question_returns_response():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/chat",
            json={"question": "What is Physical AI?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert len(data["response"]) > 0

@pytest.mark.asyncio
async def test_rate_limiting_enforced():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Make 11 requests rapidly
        for i in range(11):
            response = await client.post(
                "/chat",
                json={"question": f"Question {i}"}
            )
            if i < 10:
                assert response.status_code == 200
            else:
                assert response.status_code == 429  # Rate limit exceeded
```

## 10. Migration from AsyncOpenAI to OpenAIChatCompletionsModel

### Key Implementation Differences

| Aspect | Previous (AsyncOpenAI) | New (OpenAIChatCompletionsModel) |
|--------|----------------------|------------------|
| **Package** | `openai` | `openai-agents` |
| **Import** | `from openai import AsyncOpenAI` | `from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel` |
| **Client** | Direct AsyncOpenAI | AsyncOpenAI wrapped in OpenAIChatCompletionsModel |
| **System Prompt** | Passed in messages array | Agent `instructions` parameter |
| **Execution** | `client.chat.completions.create()` | `Runner.run(agent, input=message)` |
| **Response** | `response.choices[0].message.content` | `result.final_output` |
| **Error Handling** | Custom exceptions | Custom exceptions (wrap SDK errors) |

### Migration Pattern

#### Current Implementation (AsyncOpenAI)
```python
# backend/src/backend/agent.py
from openai import AsyncOpenAI

class AITutor:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.gemini_api_key,
            base_url=settings.gemini_base_url,
        )
        self.model = settings.gemini_model
        self.system_prompt = self._load_constitution()

    async def generate_response(self, message: str) -> str:
        response = await asyncio.wait_for(
            self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": message},
                ],
            ),
            timeout=settings.request_timeout,
        )
        return response.choices[0].message.content.strip()
```

#### Migrated Implementation (OpenAIChatCompletionsModel)
```python
# backend/src/backend/agent.py
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel

class AITutor:
    def __init__(self):
        # Create Gemini-configured client
        gemini_client = AsyncOpenAI(
            api_key=settings.gemini_api_key,
            base_url=settings.gemini_base_url,
        )

        # Wrap in OpenAIChatCompletionsModel
        model = OpenAIChatCompletionsModel(
            model=settings.gemini_model,
            openai_client=gemini_client
        )

        # Create agent with instructions (system prompt)
        constitution = self._load_constitution()
        self.agent = Agent(
            name="Educational Tutor",
            instructions=constitution,
            model=model
        )

    async def generate_response(self, message: str) -> str:
        result = await asyncio.wait_for(
            Runner.run(
                starting_agent=self.agent,
                input=message
            ),
            timeout=settings.request_timeout
        )
        return result.final_output.strip()
```

## 11. Context7 MCP Server Integration

### Decision: Use Context7 for Documentation Access

**What was chosen**: Leverage Context7 MCP server for accessing latest OpenAI Agent SDK documentation during development.

**Rationale**:
- **Always Up-to-Date**: MCP server provides real-time access to latest docs
- **Development Efficiency**: Reduces context switching to browser documentation
- **AI-Native Workflow**: Aligns with Constitution Principle II (AI-Native Content Creation)

**Usage Pattern**:
- Query Context7 during implementation for specific SDK features
- Validate API usage against latest documentation
- Reference official examples for complex patterns (guardrails, multi-agent handoffs)

## Summary of Key Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| **Agent Framework** | OpenAI Agent SDK | Production-ready, Python-first, provider-agnostic |
| **LLM Provider** | Gemini 2.0 Flash via OpenAIChatCompletionsModel | Cost-effective, high performance, direct integration |
| **Backend Framework** | FastAPI with async | Native async support, auto documentation, validation |
| **Constitution Injection** | Agent instructions parameter | Native support, persistent context, testable |
| **Response Mode** | Non-streaming (MVP) | Simplicity, meets success criteria, easy to test |
| **Rate Limiting** | slowapi library | FastAPI native, decorator-based, production-ready |
| **Error Handling** | Multi-layer (validation + agent + service) | Comprehensive, informative, meets FR-006/FR-007 |
| **Testing** | Pytest async + contract tests | Aligns with Python ecosystem, async support |
| **Documentation Source** | Context7 MCP server | Always current, AI-native workflow |
| **Migration** | OpenAIChatCompletionsModel instead of AsyncOpenAI | Better SDK integration, future agent features |

## References

- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents SDK - GitHub](https://github.com/openai/openai-agents-python)
- [Models - OpenAI Agents SDK](https://openai.github.io/openai-agents-python/models/)
- [Runner - OpenAI Agents SDK](https://openai.github.io/openai-agents-python/ref/run/)
- [Agents - OpenAI Agents SDK](https://openai.github.io/openai-agents-python/ref/agent/)
- [openai-agents · PyPI](https://pypi.org/project/openai-agents/)

## Next Steps

1. Generate data-model.md with entity definitions
2. Generate API contracts in /contracts/
3. Create quickstart.md for developers
4. Update plan.md with architectural decisions
5. Update agent context with new technologies (OpenAI Agent SDK, OpenAIChatCompletionsModel)