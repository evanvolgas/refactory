# Refactory 🔍

> **⚠️ UNDER ACTIVE DEVELOPMENT**  
> This project is currently in early development stages. Features are being actively implemented and the API may change frequently. Not recommended for production use yet.

A multi-agent code analysis system that performs comprehensive code reviews using AI agents specialized in different aspects of code quality.

## 🎯 What It Does

Refactory simulates a senior engineering team by deploying five specialized AI agents that analyze your code from different perspectives:

- **🏗️ Architect Agent** - Design patterns, structure, SOLID principles
- **🔒 Security Agent** - Vulnerabilities, secure coding practices  
- **⚡ Performance Agent** - Efficiency, complexity, scalability
- **📚 Documentation Agent** - Code clarity, comments, API docs
- **🎨 Style Agent** - Consistency, naming, formatting

Each agent provides scored feedback (0-100) with specific, actionable recommendations.

## 🚧 Current Status

**Phase 1: Foundation** (In Progress)
- [x] Project design and architecture planning
- [x] Core documentation
- [ ] PydanticAI framework setup
- [ ] Basic agent structure
- [ ] Python language support
- [ ] Initial scoring system

## 📋 Planned Features

### Core Functionality
- Multi-language support (Python, JavaScript, TypeScript, Java, C++, Go)
- Intelligent conflict resolution between agent recommendations
- Comprehensive scoring and reporting system
- Before/after code examples with improvement suggestions

### Integration Options
- CLI tool for local development
- GitHub Actions for CI/CD
- REST API for custom integrations
- Multiple export formats (JSON, Markdown, PDF)

### Advanced Capabilities
- Context-aware analysis based on project type
- Framework-specific best practices
- Incremental analysis for large codebases
- Configurable analysis depth

## 🛠️ Technology Stack

- **Framework**: PydanticAI for agent orchestration
- **Code Analysis**: Tree-sitter for AST parsing
- **Output**: Structured Pydantic models
- **Languages**: Python (expanding to others)

## 📖 Documentation

- [Design Document](./DESIGN.md) - Comprehensive technical specification
- [Architecture Overview](./DESIGN.md#architecture) - System design and agent roles
- [Implementation Roadmap](./DESIGN.md#implementation-roadmap) - Development phases

## 🤝 Contributing

This project is in early development. While we're not ready for external contributions yet, we welcome:

- Feedback on the design and architecture
- Suggestions for additional analysis capabilities
- Ideas for integration improvements

## 📄 License

[License to be determined]

## 🔄 Development Updates

This README will be updated regularly as development progresses. Check back for:
- Implementation milestones
- API documentation
- Installation instructions
- Usage examples

---

**Built for defensive security and code improvement purposes only.**