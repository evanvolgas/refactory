"""
Architect Agent for the Refactory multi-agent code analysis system.

This agent focuses on design patterns, code structure, SOLID principles,
and overall architectural quality of the code.
"""

from typing import List, Optional
from ..core.models import AgentType
from .base_agent import BaseCodeAgent


class ArchitectAgent(BaseCodeAgent):
    """
    Architect Agent specializing in design patterns, code structure, and SOLID principles.

    Key focus areas:
    - Design patterns and architectural patterns
    - SOLID principles adherence
    - Code modularity and separation of concerns
    - Maintainability and extensibility
    - Class and module design
    - Dependency management
    """

    def __init__(self, model_name: Optional[str] = None):
        """Initialize the Architect Agent."""
        super().__init__(AgentType.ARCHITECT, model_name)

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Architect Agent."""
        return """
You are a Senior Software Architect with 15+ years of experience in designing
maintainable, scalable software systems. You specialize in:

- Design patterns (GoF, architectural patterns)
- SOLID principles and clean architecture
- Code structure and modularity
- Maintainability and extensibility
- Dependency management and inversion
- Domain-driven design principles

Your role is to analyze code from an architectural perspective and provide
specific, actionable recommendations for improving:

1. **Design Quality**: How well does the code follow established design patterns?
2. **Modularity**: Is the code properly separated into cohesive modules?
3. **SOLID Adherence**: Does the code follow SOLID principles?
4. **Maintainability**: How easy is it to modify and extend this code?
5. **Dependency Management**: Are dependencies properly managed and abstracted?

For each issue you identify:
- Provide the specific line number where possible
- Explain WHY it's an architectural concern
- Suggest a concrete improvement with before/after examples
- Estimate the effort required to implement the fix
- Consider the impact on the overall system design

Focus on structural improvements that will make the code more maintainable,
testable, and extensible in the long term. Prioritize issues that affect
the fundamental design and architecture of the system.

Always provide specific, actionable recommendations with clear examples.
"""

    def _get_domain_areas(self) -> List[str]:
        """Get the domain areas this agent scores."""
        return [
            "design_quality",
            "modularity",
            "solid_adherence",
            "maintainability",
            "dependency_management",
        ]

    def _get_focus_description(self) -> str:
        """Get a description of what this agent focuses on."""
        return """design patterns, code structure, SOLID principles, modularity,
maintainability, and overall architectural quality. Consider how the code
can be better engineered for long-term maintenance and extension."""


class ArchitectAgentPrompts:
    """
    Additional prompts and templates for the Architect Agent.
    """

    DESIGN_PATTERN_ANALYSIS = """
    Analyze the code for design pattern opportunities:

    1. Are there repeated code structures that could benefit from patterns?
    2. Could creational patterns (Factory, Builder, Singleton) improve object creation?
    3. Would structural patterns (Adapter, Decorator, Facade) improve code organization?
    4. Could behavioral patterns (Strategy, Observer, Command) improve flexibility?

    For each pattern opportunity, explain:
    - Which pattern would help
    - Where to apply it
    - What benefits it would provide
    - Implementation approach
    """

    SOLID_PRINCIPLES_CHECK = """
    Evaluate SOLID principles adherence:

    **Single Responsibility Principle (SRP)**:
    - Does each class have only one reason to change?
    - Are responsibilities clearly separated?

    **Open/Closed Principle (OCP)**:
    - Is the code open for extension but closed for modification?
    - Are there extension points for new functionality?

    **Liskov Substitution Principle (LSP)**:
    - Can derived classes be substituted for base classes?
    - Do inheritance relationships make logical sense?

    **Interface Segregation Principle (ISP)**:
    - Are interfaces focused and cohesive?
    - Do clients depend only on methods they use?

    **Dependency Inversion Principle (DIP)**:
    - Do high-level modules depend on abstractions?
    - Are dependencies properly inverted?
    """

    REFACTORING_SUGGESTIONS = """
    Provide specific refactoring suggestions:

    1. **Extract Method**: Long methods that do multiple things
    2. **Extract Class**: Classes with too many responsibilities
    3. **Move Method**: Methods in the wrong class
    4. **Replace Conditional with Polymorphism**: Complex if/else chains
    5. **Introduce Parameter Object**: Methods with many parameters
    6. **Replace Magic Numbers**: Hard-coded values that should be constants
    7. **Encapsulate Field**: Direct field access that should use methods

    For each suggestion:
    - Show the current problematic code
    - Explain why it's problematic
    - Provide the refactored version
    - Explain the benefits of the change
    """
