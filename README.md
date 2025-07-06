# Refactory 🔍

**Multi-agent AI code analysis system** - Get comprehensive code reviews from specialized AI agents.

## Overview

Refactory deploys three specialized AI agents that analyze your code like a senior engineering team:

- **🏗️ Architect** - Design patterns, SOLID principles, code structure
- **🔒 Security** - Vulnerabilities, injection attacks, secure practices
- **⚡ Performance** - Algorithmic complexity, optimization opportunities

Each agent provides scored feedback (0-100) with actionable recommendations.

## Status

**Currently Available:** Architect, Security, and Performance agents
**Coming Soon:** Documentation and Style agents

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

### Usage
```bash
# Analyze a single file
refactory analyze examples/sample_code.py

# Analyze entire codebase
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

## Features

### Analysis Capabilities
- **Single Files**: Analyze individual Python files
- **Entire Codebases**: Recursive directory analysis with filtering
- **Selective Agents**: Choose specific agents (security, performance, architecture)
- **Multiple Formats**: Table, JSON, or detailed output

### Agent Specializations
- **🏗️ Architect**: SOLID principles, design patterns, code organization
- **🔒 Security**: SQL injection, XSS, hardcoded secrets, authentication flaws
- **⚡ Performance**: Algorithmic complexity, memory efficiency, optimization opportunities

## Documentation

- **[CLI Reference](docs/CLI.md)** - Complete command-line interface guide
- **[User Guide](docs/README.md)** - Getting started and configuration
- **[Design Document](DESIGN.md)** - Technical architecture and roadmap

## Examples

```bash
# Security audit of web application
refactory analyze webapp/ --focus security --format detailed

# Performance review of algorithms
refactory analyze algorithms/ --focus performance --include "*.py"

# Full analysis with custom output
refactory analyze src/ --format json --output report.json
```

---

**Built for code improvement and security analysis.**