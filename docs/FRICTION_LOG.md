# Product Feedback & Developer Friction Log
**Project:** OmniFlow (Alexa+ Track & AWS Builder Mini Challenge)  
**Hackathon:** Build, Ship, Shape: Amazon Developer Hackathon 2026

---

## 1. Product Feedback Summary

### Which developer tools, APIs, and SDKs did you use and for what?
- **Model Context Protocol (MCP) Streamable HTTP Transport (Spec v2025-11-25)**: Used to build a self-hosted MCP server exposing travel planning, Amazon product search, budget optimization, and 1-click order execution tools.
- **Amazon Bedrock Runtime SDK (`@aws-sdk/client-bedrock-runtime`)**: Used to orchestrate tool selection, synthesize reasoning chains, and generate multi-turn conversational responses with Claude 3.5 Sonnet.
- **Amazon Alexa+ Multi-Modal UX Standards**: Used to structure rich media cards (horizontal product carousels, itinerary tabs, and interactive touch triggers).

### What worked well?
- **Streamable HTTP Specification**: The move towards Streamable HTTP (over legacy STDIO or raw WebSockets) makes hosting MCP servers behind standard web infrastructure (Express, Lambda, ECS, CloudFront) significantly easier.
- **Bedrock Converse API & Tool Use**: Bedrock's function-calling format maps smoothly to JSONSchema tool parameters, making MCP tool ingestion relatively straightforward.
- **Agent Skill Interoperability**: The decoupled design of MCP allows tools to be developed independently and wired dynamically into Alexa+.

### What needs work?
- **Streamable HTTP Disconnect & Reconnect Semantics**: In low-latency voice environments, long-lived Server-Sent Events (SSE) connections can drop silently when network conditions fluctuate. Better built-in reconnection headers or standard session recovery tokens in the MCP client library would save developers hours of boilerplate.
- **Rich Media / UI Card Standard in MCP**: MCP excels at returning raw text and JSON blobs, but lacks a standardized specification for interactive visual components (e.g., adaptive cards, carousels, action triggers). We had to design custom schemas for Alexa+ screens.
- **Bedrock Streaming Tool Call Latency**: When chaining 3 or 4 sequential tool invocations (itinerary -> catalog search -> cart calculation), time-to-first-token can exceed 3 seconds. Providing server-side speculative parallel execution would enhance real-time voice UX.

### How was your onboarding experience (getting from zero to hello world)?
- Rating: **8.5 / 10**. Getting a basic MCP server up and running took under 30 minutes thanks to clear JSON-RPC documentation. The hardest part was discovering official reference implementations for Streamable HTTP headers compared to older STDIO samples.

### Would you build with these devices and services again?
- **Yes, absolutely.** The combination of Alexa+ ambient screen devices and open-standard MCP server tooling is the future of autonomous personal AI.

---

## 2. Detailed Friction Log Entries

### Entry 1: Streamable HTTP Header Negotiation & Content-Type
- **Task Attempted**: Establishing an SSE stream from the Alexa+ web client to the MCP server.
- **Steps Taken**: Implemented `GET /mcp/stream` returning `text/event-stream`.
- **Expected Result**: Immediate bi-directional channel recognition.
- **Actual Result**: Some reverse proxies buffered chunks because `X-Accel-Buffering: no` and explicit cache-control headers were not explicitly documented in the early spec drafts.
- **Severity**: Medium
- **Workaround Used**: Added explicit `res.setHeader("X-Accel-Buffering", "no")` and `res.flushHeaders()` immediately upon connection.
- **Actionable Suggestion**: Include a standardized Express/Fastify/Next.js middleware snippet directly in the official MCP documentation.

### Entry 2: Bedrock Tool Response Schema Validation Mismatch
- **Task Attempted**: Passing MCP tool output back into Amazon Bedrock Converse stream.
- **Steps Taken**: Sent raw JSON string in toolResult.
- **Expected Result**: Bedrock accepts standard JSON object.
- **Actual Result**: Bedrock expects a specific array of content blocks with `json` or `text` keys.
- **Severity**: Low
- **Workaround Used**: Built an adapter function mapping MCP `content: [{ type: "text", text: ... }]` to Bedrock's content block format.
- **Actionable Suggestion**: Provide an official `@aws-sdk/mcp-adapter` package that natively converts between MCP tool schemas and Bedrock Converse APIs.

---

## 3. Feature Requests

1. **Native UI Card Specification for MCP (Critical)**:
   - *Why it matters*: Alexa+ devices (Echo Show, Fire TV) are visual. Having an official MCP standard for interactive components (Cards, Carousels, Action Buttons) would standardize multi-modal skills across the entire ecosystem.
2. **Built-in Session State Synchronization (Important)**:
   - *Why it matters*: Agents need to remember preferences and cart state across multiple conversational turns without relying on client-side cookie hacking.
3. **AWS Bedrock Managed MCP Gateway (Nice-to-have)**:
   - *Why it matters*: Allowing Bedrock Agents to connect directly to registered MCP server endpoints with zero custom code would accelerate developer adoption by 10x.
