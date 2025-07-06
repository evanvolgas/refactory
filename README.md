# Refactory 🔍

![Refactory Logo](refactory_logo_white_bg.png)

**⚠️ EXPERIMENTAL ALPHA SOFTWARE**

**AI-assisted code review tool** - Personal experiment in using AI agents for focused code analysis.

## Overview

Refactory is a prototype tool that uses AI to review small codebases:

- **🏗️ Architect** - Basic design pattern and structure checks
- **🔒 Security** - Common vulnerability detection
- **⚡ Performance** - Obvious algorithmic issues

Provides scored feedback as a "second pair of eyes" for code review.

## Status

**⚠️ Personal Research Project:** Experimental software for small codebases
**Works For:** Individual files and small projects (~100 files)
**Experimenting With:** Cost reduction through local pattern matching

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

### Basic Usage
```bash
# Analyze a single file
refactory analyze examples/sample_code.py

# Analyze a small project
refactory analyze src/ --include "*.py" --exclude ".venv"

# Focus on security issues
refactory analyze auth.py --focus security

# Check multiple areas
refactory analyze code.py --focus security --focus performance
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

## What It Does

### Basic Capabilities
- **Single Files**: Analyze individual Python files
- **Small Projects**: Works best with ~100 files or less
- **Focused Analysis**: Choose specific areas (security, performance, architecture)
- **Simple Output**: Table or JSON format

### What Each Agent Checks
- **🏗️ Architect**: Basic SOLID principles, obvious design issues
- **🔒 Security**: Common vulnerabilities like SQL injection, hardcoded secrets
- **⚡ Performance**: Obvious inefficiencies, algorithmic complexity issues

## Documentation

- **[CLI Reference](docs/CLI.md)** - Complete command-line interface guide
- **[User Guide](docs/README.md)** - Getting started and configuration
- **[Design Document](DESIGN.md)** - Technical architecture and roadmap

## Example Use Cases

```bash
# Check auth code for security issues
refactory analyze auth.py --focus security

# Review new feature for design issues
refactory analyze new_feature/ --focus architect

# Quick performance check
refactory analyze data_processor.py --focus performance
```

---

**⚠️ Personal research project - use at your own risk.**