# Refactory CLI Documentation

**⚠️ Personal Research Project**

Basic guide to using the Refactory command-line interface for small codebase analysis.

## Table of Contents

- [Quick Start](#quick-start)
- [Commands](#commands)
- [Analysis Options](#analysis-options)
- [Agent Selection](#agent-selection)
- [File Filtering](#file-filtering)
- [Output Formats](#output-formats)
- [Examples](#examples)
- [Best Practices](#best-practices)

## Quick Start

```bash
# Analyze a single file
refactory analyze examples/sample_code.py

# Analyze small project
refactory analyze src/ --include "*.py"

# Security-focused analysis
refactory analyze auth.py --focus security

# Show available models
refactory models
```

## Commands

### `refactory analyze`

Analyze code files or small directories with AI agents.

```bash
refactory analyze [OPTIONS] PATH
```

**Arguments:**
- `PATH`: File or small directory to analyze (works best with ~100 files or less)

### `refactory models`

Display available AI models and current configuration.

```bash
refactory models
```

Shows:
- Current model configuration
- All supported models with costs
- API key status
- Configuration instructions

## Analysis Options

### Basic Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output PATH` | Save results to file | Console output |
| `--format FORMAT` | Output format | `table` |
| `--depth LEVEL` | Analysis thoroughness | `standard` |

### Output Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| `table` | Clean tabular display | Quick overview |
| `json` | Machine-readable JSON | Integration, storage |
| `detailed` | Comprehensive analysis | In-depth review |

### Analysis Depth

| Depth | Description | Speed | Detail |
|-------|-------------|-------|--------|
| `quick` | Fast overview | ⚡⚡⚡ | ⭐ |
| `standard` | Balanced analysis | ⚡⚡ | ⭐⭐ |
| `thorough` | Comprehensive review | ⚡ | ⭐⭐⭐ |

## Agent Selection

Control which agents analyze your code with the `--focus` option.

### Available Agents

| Agent | Focus Area | Use Case |
|-------|------------|----------|
| `architect` | Basic design patterns, obvious structure issues | Simple code structure review |
| `security` | Common vulnerabilities, obvious security issues | Basic security check |
| `performance` | Obvious inefficiencies, algorithmic complexity | Simple performance check |

### Usage

```bash
# Single agent
refactory analyze code.py --focus security

# Multiple agents
refactory analyze code.py --focus security --focus performance

# All agents (default)
refactory analyze code.py
```

## File Filtering

### Include Patterns

Specify which files to analyze:

```bash
# Python files only
refactory analyze src/ --include "*.py"

# Multiple patterns
refactory analyze src/ --include "*.py" --include "*.pyx"

# Specific directories
refactory analyze . --include "src/**/*.py"
```

### Exclude Patterns

Skip files and directories:

```bash
# Common exclusions
refactory analyze . --exclude ".venv" --exclude "__pycache__"

# Test files
refactory analyze src/ --exclude "test_*.py" --exclude "*_test.py"

# Multiple patterns
refactory analyze . --exclude "*.pyc" --exclude "build/" --exclude "dist/"
```

### Pattern Syntax

Uses glob patterns:
- `*.py` - All Python files
- `**/*.py` - Python files in all subdirectories
- `test_*` - Files starting with "test_"
- `*_test.py` - Files ending with "_test.py"
- `.venv/` - Entire .venv directory

## Examples

### Single File Analysis

```bash
# Basic analysis
refactory analyze app.py

# Security focus
refactory analyze app.py --focus security --format detailed

# Save results
refactory analyze app.py --output security_report.json --format json
```

### Small Project Analysis

```bash
# Small Python project
refactory analyze . --include "*.py" --exclude ".venv" --exclude "__pycache__"

# Source code only
refactory analyze src/ --include "*.py"

# Exclude tests
refactory analyze . --include "*.py" --exclude "test_*" --exclude "*_test.py"
```

### Focused Analysis

```bash
# Basic security check
refactory analyze auth.py \
  --focus security \
  --format detailed \
  --output security_check.json

# Simple performance review
refactory analyze data_processor.py \
  --focus performance \
  --include "*.py"

# Basic architecture check
refactory analyze new_feature/ \
  --focus architect \
  --exclude "tests/" \
  --format detailed
```

### Simple Automation

```bash
# Basic security check
refactory analyze auth.py \
  --focus security \
  --format json \
  --output security_report.json

# Simple check with exit code
if refactory analyze auth.py --focus security --format json > /dev/null; then
  echo "Basic security check passed"
else
  echo "Security issues found"
  exit 1
fi
```

## Best Practices

### For Large Codebases

```bash
# Use specific focus for faster analysis
refactory analyze large_project/ --focus security --depth quick

# Exclude unnecessary files
refactory analyze . \
  --include "*.py" \
  --exclude ".venv" \
  --exclude "__pycache__" \
  --exclude "build/" \
  --exclude "dist/"

# Save results for later review
refactory analyze src/ --format json --output analysis_$(date +%Y%m%d).json
```

### For Security Audits

```bash
# Comprehensive security review
refactory analyze . \
  --focus security \
  --include "*.py" \
  --exclude "tests/" \
  --format detailed \
  --depth thorough

# Quick security scan
refactory analyze src/ --focus security --depth quick
```

### For Performance Optimization

```bash
# Find performance bottlenecks
refactory analyze algorithms/ \
  --focus performance \
  --format detailed

# Check specific modules
refactory analyze core/processing.py --focus performance --format detailed
```

### For Code Reviews

```bash
# Full analysis for code review
refactory analyze feature_branch/ \
  --format detailed \
  --output code_review.json

# Architecture review
refactory analyze new_module/ --focus architect --format detailed
```

## Configuration

### Model Selection

Set your preferred AI model in `.env`:

```bash
# Best value (recommended)
REFACTORY_MODEL=gemini-2.0-flash-exp
GEMINI_API_KEY=your_api_key_here

# High performance
REFACTORY_MODEL=anthropic:claude-4-sonnet
ANTHROPIC_API_KEY=your_api_key_here
```

### Agent-Specific Models

Use different models for different agents:

```bash
REFACTORY_ARCHITECT_MODEL=anthropic:claude-4-sonnet
REFACTORY_SECURITY_MODEL=anthropic:claude-4-opus
REFACTORY_PERFORMANCE_MODEL=gemini-2.0-flash-exp
```

## Troubleshooting

### Common Issues

**API Rate Limits:**
```bash
# Use a different model with higher limits
refactory --model anthropic:claude-4-sonnet analyze src/

# Analyze smaller chunks
refactory analyze src/module1/ --focus security
refactory analyze src/module2/ --focus security
```

**Large Codebases:**
```bash
# Use quick depth for initial scan
refactory analyze . --depth quick --include "*.py"

# Focus on specific areas
refactory analyze src/critical/ --depth thorough
```

**File Filtering:**
```bash
# Debug what files are being analyzed
refactory analyze . --include "*.py" --exclude ".venv" --format table

# Check file patterns
ls src/**/*.py  # Verify your patterns match expected files
```

### Getting Help

```bash
# Command help
refactory analyze --help

# Show available models
refactory models

# Version information
refactory --version
```
