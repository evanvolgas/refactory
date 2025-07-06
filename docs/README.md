# Refactory Documentation

Complete documentation for the Refactory multi-agent code analysis system.

## Quick Links

- **[CLI Reference](CLI.md)** - Complete command-line interface guide
- **[Design Document](../DESIGN.md)** - Technical architecture and implementation details

## Getting Started

### 1. Installation
```bash
git clone <repository-url>
cd refactory
uv venv .venv && uv pip install -e .
```

### 2. Configuration
Create a `.env` file with your preferred AI model:
```bash
REFACTORY_MODEL=gemini-2.0-flash-exp
GEMINI_API_KEY=your_api_key_here
```

### 3. Basic Usage
```bash
# Analyze a single file
refactory analyze examples/sample_code.py

# Analyze entire project
refactory analyze src/ --include "*.py" --exclude ".venv"

# Security-focused analysis
refactory analyze . --focus security --format detailed
```

## Available Agents

### 🏗️ Architect Agent
**Focus**: Code structure, design patterns, SOLID principles

**Analyzes**:
- Design pattern usage and implementation
- SOLID principle adherence
- Code organization and modularity
- Separation of concerns
- Abstraction and encapsulation

**Example Issues**:
- Violation of Single Responsibility Principle
- Missing abstraction layers
- Poor separation of concerns
- Tight coupling between components

### 🔒 Security Agent
**Focus**: Vulnerabilities, secure coding practices

**Analyzes**:
- SQL injection vulnerabilities
- Cross-site scripting (XSS) risks
- Hardcoded secrets and credentials
- Authentication and authorization flaws
- Input validation and sanitization
- Insecure deserialization
- Command injection risks

**Example Issues**:
- SQL injection via string formatting
- Hardcoded API keys in source code
- Missing input validation
- Insecure password hashing

### ⚡ Performance Agent
**Focus**: Efficiency, optimization, algorithmic complexity

**Analyzes**:
- Algorithmic complexity (Big O analysis)
- Memory usage and efficiency
- CPU-intensive operations
- I/O performance bottlenecks
- Data structure selection
- Caching opportunities
- Concurrency utilization

**Example Issues**:
- O(n²) nested loops
- Inefficient data structure usage
- Missing caching for expensive operations
- Memory leaks and excessive allocations

## Output Formats

### Table Format (Default)
Clean, readable table showing file scores and top issues:
```
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ File           ┃ Overall Score ┃ Issues ┃ Top Issue                                             ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ sample_code.py │      45       │   3    │ Missing input validation                              │
└────────────────┴───────────────┴────────┴───────────────────────────────────────────────────────┘
```

### JSON Format
Machine-readable format for integration and storage:
```json
{
  "files": [
    {
      "file_path": "sample_code.py",
      "overall_score": 45,
      "agent_scores": [
        {
          "agent_type": "security",
          "overall_score": 30,
          "domain_scores": {
            "input_validation": 20,
            "authentication_authorization": 40
          },
          "issues": [
            {
              "title": "Missing input validation",
              "severity": "high",
              "line_number": 15
            }
          ]
        }
      ]
    }
  ]
}
```

### Detailed Format
Comprehensive analysis with full recommendations:
```
🔍 Security Analysis Results

📊 Overall Score: 30/100

🎯 Domain Scores:
   • Input Validation: 20/100
   • Authentication/Authorization: 40/100
   • Injection Vulnerabilities: 25/100

🚨 Critical Issues (2):
   1. 🔴 SQL Injection Vulnerability
      Line 45: Direct string formatting in SQL query
      Fix: Use parameterized queries

   2. 🔴 Hardcoded API Key
      Line 12: API key exposed in source code
      Fix: Move to environment variables

💡 Recommendations:
   1. Implement input validation for all user inputs
   2. Use parameterized SQL queries
   3. Store secrets in environment variables
```

## Configuration Options

### Model Selection
Choose from multiple AI providers and models:

```bash
# Google Gemini (recommended)
REFACTORY_MODEL=gemini-2.0-flash-exp
GEMINI_API_KEY=your_key

# Anthropic Claude (high performance)
REFACTORY_MODEL=anthropic:claude-4-sonnet
ANTHROPIC_API_KEY=your_key

# OpenAI GPT (reliable)
REFACTORY_MODEL=openai:gpt-4
OPENAI_API_KEY=your_key
```

### Agent-Specific Models
Use different models for different agents:
```bash
REFACTORY_ARCHITECT_MODEL=anthropic:claude-4-sonnet
REFACTORY_SECURITY_MODEL=anthropic:claude-4-opus
REFACTORY_PERFORMANCE_MODEL=gemini-2.0-flash-exp
```

### Analysis Parameters
```bash
REFACTORY_TEMPERATURE=0.1        # Lower = more deterministic
REFACTORY_MAX_TOKENS=4000        # Maximum response length
REFACTORY_TIMEOUT=60             # Request timeout in seconds
```

## Integration Examples

### CI/CD Pipeline
```yaml
# .github/workflows/code-analysis.yml
name: Code Analysis
on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Refactory
        run: |
          pip install uv
          uv venv .venv
          uv pip install -e .
      - name: Security Analysis
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          refactory analyze src/ \
            --focus security \
            --format json \
            --output security_report.json
      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: security-analysis
          path: security_report.json
```

### Pre-commit Hook
```bash
#!/bin/sh
# .git/hooks/pre-commit
refactory analyze --focus security $(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')
```

## Troubleshooting

### Common Issues

**API Rate Limits**:
- Switch to a model with higher limits
- Analyze smaller code chunks
- Use `--depth quick` for faster analysis

**Large Codebases**:
- Use file filtering: `--include "*.py" --exclude "tests/"`
- Focus on specific agents: `--focus security`
- Analyze incrementally by directory

**Configuration Issues**:
- Check API key environment variables
- Verify model name format
- Use `refactory models` to see available options

### Getting Help

```bash
refactory --help              # General help
refactory analyze --help      # Command-specific help
refactory models              # Show available models
```

For more detailed information, see the [CLI Reference](CLI.md).
