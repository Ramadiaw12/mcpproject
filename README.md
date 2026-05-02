# ⚙️ MCP Orchestration Hub — Streamable HTTP Agent Platform

> A production-ready **Model Context Protocol (MCP) server** exposing custom AI tools, integrated with **LangChain/LangGraph** and **n8n** via the `streamable-http` transport protocol.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-20%2B-green.svg)](https://nodejs.org)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/Protocol-MCP%201.x-purple.svg)](https://modelcontextprotocol.io)

---

## 📌 Table of Contents

1. [Project Description](#-project-description)
2. [Architecture](#-architecture)
3. [Tech Stack](#-tech-stack)
4. [Installation](#-installation)
5. [Configuration](#-configuration)
6. [Usage](#-usage)
7. [MCP Tools Reference](#-mcp-tools-reference)
8. [Testing with MCP Inspector](#-testing-with-mcp-inspector)
9. [LangChain / LangGraph Integration](#-langchain--langgraph-integration)
10. [n8n Integration](#-n8n-integration)
11. [Workflow Example](#-workflow-example)
12. [Design Choices & Best Practices](#-design-choices--best-practices)
13. [Future Improvements](#-future-improvements)
14. [Author](#-author)

---

## 🚀 Project Description

**MCP Orchestration Hub** is a modular, extensible platform built around the [Model Context Protocol](https://modelcontextprotocol.io) — an open standard for exposing tools and resources to LLM-powered agents.

This project demonstrates a complete integration pipeline:

- **A custom MCP server** written in TypeScript/Node.js that exposes two specialized tools over `streamable-http`
- **An AI agent built with LangChain/LangGraph** (Python) that dynamically discovers and invokes those tools
- **An n8n workflow** that connects to the same MCP server for no-code/low-code automation

### 🎯 Use Cases

| Use Case | Description |
|---|---|
| **Agentic RAG pipeline** | An LLM agent calls MCP tools to fetch documents, summarize, and return structured answers |
| **Automated data enrichment** | n8n triggers the MCP server on webhook events to enrich CRM records via AI |
| **Multi-agent orchestration** | LangGraph coordinates multiple specialized agents, each consuming MCP tools |
| **DevOps automation** | An agent reads CI/CD logs, performs root-cause analysis, and posts Slack alerts |

---

## 🏗️ Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                                 │
│                                                                     │
│   ┌──────────────────────┐      ┌──────────────────────────────┐   │
│   │  LangChain / LangGraph│      │          n8n Workflow        │   │
│   │  (Python Agent)       │      │  (No-code Automation Engine) │   │
│   └──────────┬───────────┘      └──────────────┬───────────────┘   │
│              │                                  │                   │
│              │  HTTP POST (streamable-http)      │                   │
│              └──────────────┬───────────────────┘                   │
└─────────────────────────────┼───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    MCP SERVER (Node.js / TypeScript)                 │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                  Transport Layer                            │   │
│   │              streamable-http  (POST /mcp)                   │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│              ┌───────────────┴───────────────┐                      │
│              ▼                               ▼                      │
│   ┌─────────────────────┐       ┌─────────────────────────┐        │
│   │    Tool: search_web  │       │  Tool: summarize_text    │        │
│   │  (SerpAPI / Tavily)  │       │  (Anthropic / OpenAI)   │        │
│   └─────────────────────┘       └─────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     EXTERNAL SERVICES                               │
│                                                                     │
│     Search API          LLM Provider         Vector Store           │
│   (Tavily/SerpAPI)   (Anthropic/OpenAI)    (Optional/Future)       │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Agent ──[Tool Call Request]──▶ MCP Server
       ◀──[JSON-RPC Stream]──  MCP Server ──▶ External API
```

The `streamable-http` transport allows chunked, streaming responses over a standard HTTP POST endpoint — no WebSocket or persistent connection required. Each request carries a full JSON-RPC 2.0 payload, and the server streams back results as NDJSON (newline-delimited JSON).

---

## 🛠️ Tech Stack

### MCP Server
| Component | Technology |
|---|---|
| Runtime | Node.js 20+ |
| Language | TypeScript 5 |
| MCP SDK | `@modelcontextprotocol/sdk` |
| Transport | `streamable-http` |
| Bundler | `tsx` / `esbuild` |

### Python Agent
| Component | Technology |
|---|---|
| Agent Framework | LangChain 0.3+ / LangGraph 0.2+ |
| MCP Client | `mcp` Python SDK (`langchain-mcp-adapters`) |
| LLM | Anthropic Claude / OpenAI GPT-4 |
| Async runtime | `asyncio` + `httpx` |

### Automation
| Component | Technology |
|---|---|
| Workflow Engine | n8n (self-hosted or cloud) |
| MCP Node | Native HTTP Request node |
| Auth | Bearer token / API key |

---

## 📦 Installation

### Prerequisites

- Node.js `>= 20.x`
- Python `>= 3.11`
- npm or pnpm
- n8n instance (local or cloud)

### 1. Clone the repository

```bash
git clone https://github.com/Ramadiaw12/mcpproject.git
cd mcp-orchestration-hub
```

### 2. Install MCP Server dependencies

```bash
cd mcp-server
npm install
```

### 3. Install Python agent dependencies

```bash
cd ../agent
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. (Optional) Install MCP Inspector globally

```bash
npm install -g @modelcontextprotocol/inspector
```

---

## ⚙️ Configuration

### MCP Server — `.env`

```bash
cp mcp-server/.env.example mcpserver/.env
```

```env
# Server
PORT=24000
HOST=0.0.0.0
LOG_LEVEL=info

# Tool: search_web
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxx

# Tool: summarize_text
OPENAI_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx
```

### Python Agent — `.env`

```bash
cp agent/.env.example agent/.env
```

```env
# LLM Provider
OPENAI_API_KET=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# MCP Server endpoint
MCP_SERVER_URL=http://localhost:24000/mcp
```

### n8n — Environment Variables

In your n8n instance settings, define:

```
MCP_SERVER_URL=http://localhost:24000/mcp
MCP_API_KEY=your-optional-bearer-token
```

---

## ▶️ Usage

### Start the MCP Server

```bash
cd mcp-server
npm run build
npm start
```

The server is now listening at `http://localhost:24000/mcp`.



### Development mode (hot reload)

```bash
cd mcpserver
uv run agentmcp
```

---

## 🔧 MCP Tools Reference

The server exposes two tools compliant with the MCP specification.

---

### `search_web`

Performs a real-time web search and returns structured results.

**Input Schema:**

```json
{
  "name": "search_web",
  "description": "Search the web for recent and relevant information on a given topic.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The search query to run"
      },
      "max_results": {
        "type": "integer",
        "description": "Maximum number of results to return (default: 5)",
        "default": 5
      }
    },
    "required": ["query"]
  }
}
```

**Example Response:**

```json
{
  "content": [
    {
      "type": "text",
      "text": "[{\"title\": \"...\", \"url\": \"...\", \"snippet\": \"...\"}]"
    }
  ]
}
```

---

### `summarize_text`

Generates a concise, structured summary of a given text using an LLM.

**Input Schema:**

```json
{
  "name": "summarize_text",
  "description": "Summarize a long piece of text into concise bullet points or a short paragraph.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "text": {
        "type": "string",
        "description": "The text content to summarize"
      },
      "format": {
        "type": "string",
        "enum": ["bullets", "paragraph"],
        "description": "Output format for the summary",
        "default": "paragraph"
      },
      "max_words": {
        "type": "integer",
        "description": "Approximate maximum word count for the summary",
        "default": 150
      }
    },
    "required": ["text"]
  }
}
```

---


### Launch the inspector against your running server

```bash
npx @modelcontextprotocol/inspector http://localhost:24000/mcp
```

This opens a local web UI where you can:

- Browse all available tools and their schemas
- Execute tool calls interactively with custom inputs
- Inspect raw JSON-RPC request/response pairs
- Validate streaming behavior

### Expected output in Inspector

```
Connected to MCP server at http://localhost:24000/mcp
Protocol version: 1.0
Available tools: search_web, summarize_text
```

### Manual HTTP test (streamable-http)

```bash
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/x-ndjson" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "search_web",
      "arguments": {
        "query": "Model Context Protocol 2025",
        "max_results": 3
      }
    }
  }'
```

**Streamed NDJSON response:**

```ndjson
{"jsonrpc":"2.0","id":1,"result":{"content":[{"type":"text","text":"[{\"title\":\"Introducing MCP...\",\"url\":\"https://...\"}]"}]}}
```

---

## 🧠 LangChain / LangGraph Integration

### Architecture

```
LangGraph Agent
     │
     ├── Node: agent  (LLM reasoning)
     │       └── Decides which MCP tool to call
     │
     └── Node: tools  (MCP tool executor)
             └── Sends JSON-RPC via streamable-http
                 └── MCP Server responds with results
```

### Installation

```bash
pip install langchain langgraph langchain-anthropic mcp langchain-mcp-adapters
```

### Agent implementation (`agentgraph.py`)

```python
import asyncio
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

async def run_agent(query: str):
    # Connect to the MCP server via streamable-http
    async with MultiServerMCPClient(
        {
            "orchestration_hub": {
                "url": "http://localhost:3000/mcp",
                "transport": "streamable_http",
            }
        }
    ) as client:
        tools = await client.get_tools()

        llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
        agent = create_react_agent(llm, tools)

        response = await agent.ainvoke({"messages": [{"role": "user", "content": query}]})
        return response["messages"][-1].content

if __name__ == "__main__":
    result = asyncio.run(run_agent("Search for recent AI news and summarize the top result."))
    print(result)
```

### LangGraph State Machine (multi-step)

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    search_results: list
    final_summary: str

# Build graph
builder = StateGraph(AgentState)
builder.add_node("search", search_node)       # Calls search_web MCP tool
builder.add_node("summarize", summarize_node) # Calls summarize_text MCP tool
builder.add_node("respond", respond_node)     # Formats final response

builder.set_entry_point("search")
builder.add_edge("search", "summarize")
builder.add_edge("summarize", "respond")
builder.add_edge("respond", END)

graph = builder.compile()
```

---

## 🔄 n8n Integration

### Overview

n8n connects to the MCP server using its native **HTTP Request** node over the `streamable-http` protocol.

### Workflow Setup

1. Open your n8n instance and create a new workflow
2. Add a **Webhook** trigger node (or any trigger)
3. Add an **HTTP Request** node with these settings:

```
Method:        POST
URL:           {{ $env.MCP_SERVER_URL }}
Headers:
  Content-Type:  application/json
  Accept:        application/x-ndjson
  Authorization: Bearer {{ $env.MCP_API_KEY }}
Body (JSON):
{
  "jsonrpc": "2.0",
  "id": "{{ $now }}",
  "method": "tools/call",
  "params": {
    "name": "search_web",
    "arguments": {
      "query": "{{ $json.topic }}",
      "max_results": 5
    }
  }
}
```

4. Add a **Code** node to parse the NDJSON streamed response:

```javascript
// Parse NDJSON response from MCP server
const rawBody = $input.first().json.body;
const lines = rawBody.split('\n').filter(l => l.trim());
const parsed = lines.map(line => JSON.parse(line));
const results = parsed[0]?.result?.content?.[0]?.text;
return [{ json: { results: JSON.parse(results) } }];
```

5. Connect to a **Slack** or **Email** node to deliver results

### Example n8n Workflow JSON (importable)

```json
{
  "name": "MCP Search & Summarize",
  "nodes": [
    { "type": "n8n-nodes-base.webhook", "name": "Trigger" },
    { "type": "n8n-nodes-base.httpRequest", "name": "Call MCP: search_web" },
    { "type": "n8n-nodes-base.code", "name": "Parse NDJSON" },
    { "type": "n8n-nodes-base.httpRequest", "name": "Call MCP: summarize_text" },
    { "type": "n8n-nodes-base.slack", "name": "Post to Slack" }
  ]
}
```

---

## 💡 Workflow Example

### End-to-end scenario: "AI News Briefing"

```
1. User sends query: "Latest news on AI agents"
        │
        ▼
2. LangGraph agent receives query
        │
        ▼
3. Agent invokes tool: search_web("Latest news on AI agents", max_results=5)
        │  ──── HTTP POST /mcp ────▶  MCP Server
        │  ◀──── NDJSON stream ────   MCP Server ──▶ Tavily API
        │
        ▼
4. Agent receives 5 search results
        │
        ▼
5. Agent invokes tool: summarize_text(results[0].snippet, format="bullets")
        │  ──── HTTP POST /mcp ────▶  MCP Server
        │  ◀──── NDJSON stream ────   MCP Server ──▶ Anthropic API
        │
        ▼
6. Agent formats final answer and returns to user
```

---

## 📐 Design Choices & Best Practices

### Why `streamable-http` over `stdio` or WebSocket?

`streamable-http` is the preferred transport for production deployments:

- **Stateless**: no persistent connection management overhead
- **Firewall-friendly**: standard HTTP POST, works with any API gateway or load balancer
- **Observable**: easy to log, trace, and debug with standard HTTP tooling
- **Streaming**: NDJSON chunked responses allow partial results without buffering the full payload

### Tool design principles

- **Single responsibility**: each tool does exactly one thing well
- **Typed schemas**: all inputs use strict JSON Schema with `required` fields and `enum` constraints where applicable
- **Idempotency**: tools are stateless — calling them twice with the same arguments yields the same result
- **Error propagation**: errors are returned as MCP-compliant error objects (never thrown silently)

```typescript
// Proper MCP error handling in tool handler
if (!result.ok) {
  return {
    content: [{ type: "text", text: `Error: ${result.statusText}` }],
    isError: true,
  };
}
```

### Agent architecture choices

- **LangGraph over simple LangChain**: state machines provide better control flow, observability, and human-in-the-loop support
- **Async-first**: all MCP client calls use `async/await` to avoid blocking the event loop
- **Tool discovery at runtime**: tools are fetched from the MCP server on agent startup, not hardcoded — enabling zero-downtime tool updates

---

## 🔮 Future Improvements

- [ ] **Authentication**: Add OAuth2 / JWT middleware to the MCP server endpoint
- [ ] **Tool registry**: Dynamic tool registration without server restart
- [ ] **Observability**: OpenTelemetry tracing across agent → MCP server → external API
- [ ] **Caching**: Redis-backed result cache for `search_web` to reduce API costs
- [ ] **Vector Store tool**: Add a `semantic_search` tool backed by Qdrant or Pinecone
- [ ] **Multi-server routing**: LangGraph agent capable of routing calls across multiple MCP servers
- [ ] **Docker Compose**: One-command deployment of MCP server + n8n + monitoring stack
- [ ] **Evaluation harness**: Automated test suite for tool correctness using `pytest` + MCP client

---

## 👤 Author

**DIAWANE Ramatoulaye**
Staff Engineer — AI Systems & Distributed Platforms

- GitHub: [@your-handle](https://github.com/Ramadiaw12)
- LinkedIn: [linkedin.com/in/your-profile](Ramatoulaye Diawane)
- Email: rdiawane2001@gmail.com

---

> Built with ⚙️ precision and 🧠 intent. Contributions welcome — open an issue or submit a PR.