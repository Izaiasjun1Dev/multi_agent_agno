# INNER AI Technical Test: Applied AI Engineer

## 1. Overview & Challenge

Welcome! This technical test is designed to assess your ability to build complex, resilient, and intelligent generative AI systems.

Your challenge is to build the **"Assistant Core"**: a backend service that orchestrates LLMs and tools to power a conversational AI assistant. The service must be exposed via an API and manage all its state through a database, reflecting a real-world production environment.

We are more interested in your design choices, architectural thinking, and code quality than in a feature-complete but poorly engineered solution.

**Note on AI-powered Tools:** You are encouraged to use any AI coding assistants you are comfortable with (e.g., GitHub Copilot, Cursor). We view these as standard tools for modern development. The final design, implementation, and quality of the code are your responsibility.

---

## 2. Core Functional Requirements

*These are the mandatory features your solution must implement.*

-   **LLM Routing:** Based on the user's prompt, dynamically route the request to the most suitable provider:
    -   **OpenAI API:** For general-purpose, creative, or code-related tasks.
    -   **Anthropic API:** For tasks that require complex reasoning, handle long contexts, or demand higher safety levels.
    -   The routing logic itself must be powered by an LLM.

-   **Image Generation Tool:**
    -   Detect user intent to generate an image.
    -   Trigger a tool that calls an appropriate image generation model from the available APIs.
    -   The final API response must contain the URL of the generated image.

-   **Streaming with Server-Sent Events (SSE):** For text-based responses, the API must not wait for the full response from the LLM. It should stream the response back to the client token by token using SSE. Responses for tool calls (like image generation) can be sent as a single, non-streamed JSON object.

-   **Stateful Conversations:**
    -   **Conversation History:** Maintain a short-term memory of the conversation. Each new prompt must be contextualized with the recent message history.

---

## 3. Architecture & Engineering Best Practices

*A senior engineer doesn't just write code that works; they build systems that are robust, maintainable, and observable. Your submission will be heavily evaluated on these aspects.*

**Mandatory Stack:** The only strict requirements for the stack are **Python** for the language and a graph-based orchestration tool like **LangGraph** for the core logic. All other technology choices (web framework, database, etc.) are up to you.

-   **API Design:** Expose the service via a clear and simple REST API (Flask or FastAPI are good choices).
-   **Technology Choices:** Select your stack (database, LLM abstraction libraries like `LiteLLM` or `LangChain`, etc.) and provide a clear justification for each choice in your `README.md`. Focus not just on *what* the tool does, but *why* it was the right choice for *this specific problem*, considering its trade-offs (e.g., why FastAPI over Flask for an I/O-bound app?).
-   **Observability & Tracing:**
    -   Instrument your application to trace the lifecycle of a request. We need to understand the full flow: from the initial API call, through the router's decision, the final LLM call, and any tool usage.
    -   Using a free tier of a service like **Langfuse, LangSmith, or similar** is highly encouraged.

---

## 4. How to Impress Us (Bonus Points)

*Completing the core requirements is great. Demonstrating excellence will set you apart. Here are some ideas:*

-   **Dockerization:** Provide a `Dockerfile` or `docker-compose.yml` for one-command setup and execution.
-   **Unit & Integration Testing:** Write tests for your critical business logic (e.g., routing decisions, database interactions, API endpoints).
-   **Security Considerations:** In your `README.md`, briefly discuss how you would protect the system from malicious inputs (e.g., prompt injection). Implementing a simple "guardrail" check on the input before sending it to the LLM would be a great differentiator.
-   **Error Handling & Resilience:** Show how your system gracefully handles common failures, such as API timeouts from LLM providers or database connection issues.
-   **Async Implementation:** Implement the service using `asyncio` for better performance, especially in an I/O-bound application like this.

---

## 5. Deliverables & Evaluation

#### Deliverables

1.  **Source Code:** Create a **private Git repository** containing your full solution and share access with diogo@innerai.com and henrique.januario@innerai.com.
2.  **README.md:** This is a critical part of your submission. It must include:
    -   A high-level overview of your architecture.
    -   Clear justifications for your technology and design choices.
    -   Detailed, step-by-step instructions for setting up and running the project locally.
    -   `curl` or other examples of how to interact with your API.

#### Evaluation Criteria

-   **System & Architecture Design:** Is the solution well-structured, scalable, and maintainable?
-   **Generative AI Logic:** How effective is your implementation of routing, tool use, and memory?
-   **Software Engineering Craftsmanship:** Is the code clean, well-documented, and robust? Is there evidence of good practices like testing and observability?
-   **Clarity of Communication:** How well do you explain your work and your decisions in the `README.md`?
 