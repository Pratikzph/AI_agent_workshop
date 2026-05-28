# AI Agent Workshop

A test project for exploring and building agentic applications powered by large language models.

## Overview

This repository serves as a sandbox for experimenting with agentic AI patterns — systems where an LLM autonomously plans, reasons, and takes actions using tools to accomplish goals. It is intended as a hands-on workshop for learning how to design, build, and evaluate AI agents.

## Goals

- Understand the core concepts behind agentic AI (reasoning, tool use, memory, planning)
- Prototype and test different agent architectures (ReAct, multi-agent, autonomous loops)
- Explore integrations with external tools and APIs
- Evaluate agent behavior and outputs

## Concepts Covered

- **Tool Use** — giving agents the ability to call external functions or APIs
- **Memory** — short-term (context window) and long-term (vector store / file-based) memory
- **Planning** — step-by-step task decomposition
- **Multi-agent Systems** — orchestrating multiple specialized agents
- **Evaluation** — measuring agent performance and reliability

## Tech Stack

> To be defined as the workshop progresses. Likely candidates:
> - Python or Node.js
> - Anthropic Claude API (claude-sonnet-4-6 / claude-opus-4-7)
> - LangChain / custom agent loop
> - Vector database for memory (e.g., ChromaDB, Pinecone)

## Getting Started

```bash
# Clone the repository
git clone https://github.com/Pratikzph/AI_agent_workshop.git
cd AI_agent_workshop

# Install dependencies (once added)
pip install -r requirements.txt   # Python
# or
npm install                        # Node.js
```

## Status

This project is in early/experimental stage. Structure and code will evolve as new agent patterns are tested.

## Author

Pratik Budhathoki
