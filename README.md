# Refactory 🔍

![Refactory Logo](refactory_logo_white_bg.png)

**⚠️ ALPHA SOFTWARE - EXPERIMENTAL PROOF OF CONCEPT**

**Multi-agent AI code analysis system** - Experimental system exploring comprehensive code reviews from specialized AI agents.

## Overview

Refactory is a prototype that deploys three specialized AI agents to analyze your code:

- **🏗️ Architect** - Design patterns, SOLID principles, code structure
- **🔒 Security** - Vulnerabilities, injection attacks, secure practices
- **⚡ Performance** - Algorithmic complexity, optimization opportunities

Each agent provides scored feedback (0-100) with actionable recommendations.

## Status

**⚠️ Under Active Development:** This is experimental alpha software
**Currently Available:** Architect, Security, and Performance agents
**In Development:** Hybrid local + cloud architecture for cost reduction

## Quick Start

### Installation
```bash
git clone <repository-url>
cd refactory
uv venv .venv && uv pip install -e .
```

### Configuration
Create a `.env` file:
```bash
# Recommended: Best value for most users
REFACTORY_MODEL=gemini-2.0-flash-exp
GEMINI_API_KEY=your_api_key_here
```

**Supported Models:**
- **Google Gemini**: `gemini-2.0-flash-exp`, `gemini-1.5-pro`, `gemini-1.5-flash`
- **Anthropic Claude**: `anthropic:claude-4-opus`, `anthropic:claude-4-sonnet`
- **OpenAI GPT**: `openai:gpt-4`, `openai:gpt-4.1`, `openai:gpt-4o`
- **Groq**: `groq:llama-3.3-70b`, `groq:deepseek-r1`

### Usage (Experimental)
```bash
# Analyze a single file
refactory analyze examples/sample_code.py

# Analyze entire codebase (experimental)
refactory analyze src/ --include "*.py" --exclude ".venv"

# Security-focused analysis
refactory analyze . --focus security --format detailed

# Multiple agents
refactory analyze code.py --focus security --focus performance

# Show available models
refactory models
```

### Example Output
```
🔍 Refactory Analysis Results
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ File           ┃ Overall Score ┃ Issues ┃ Top Issue                                             ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ sample_code.py │      45       │   3    │ Missing input validation                              │
│ auth.py        │      25       │   8    │ SQL injection vulnerability                          │
│ utils.py       │      75       │   1    │ Inefficient algorithm complexity                     │
└────────────────┴───────────────┴────────┴───────────────────────────────────────────────────────┘
```

## Features (Experimental)

### Analysis Capabilities
- **Single Files**: Analyze individual Python files
- **Entire Codebases**: Recursive directory analysis with filtering (experimental)
- **Selective Agents**: Choose specific agents (security, performance, architecture)
- **Multiple Formats**: Table, JSON, or detailed output

### Agent Specializations (Prototype)
- **🏗️ Architect**: SOLID principles, design patterns, code organization
- **🔒 Security**: SQL injection, XSS, hardcoded secrets, authentication flaws
- **⚡ Performance**: Algorithmic complexity, memory efficiency, optimization opportunities

## Documentation

- **[CLI Reference](docs/CLI.md)** - Complete command-line interface guide
- **[User Guide](docs/README.md)** - Getting started and configuration
- **[Design Document](DESIGN.md)** - Technical architecture and roadmap

## Examples (Experimental)

```bash
# Security audit of web application (experimental)
refactory analyze webapp/ --focus security --format detailed

# Performance review of algorithms (experimental)
refactory analyze algorithms/ --focus performance --include "*.py"

# Full analysis with custom output (experimental)
refactory analyze src/ --format json --output report.json
```

---

**⚠️ Experimental software for code improvement and security analysis research.**