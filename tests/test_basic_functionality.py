"""
Basic functionality tests for the Refactory system.

These tests verify that the core components work correctly.
"""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import Mock, patch

from refactory.core.models import (
    AgentType,
    CodeContext,
    AgentScore,
    AnalysisRequest,
    SeverityLevel,
    EffortLevel,
    CodeIssue,
)
from refactory.core.review_engine import ReviewEngine
from refactory.agents.architect_agent import ArchitectAgent
from refactory.agents.security_agent import SecurityAgent
from refactory.agents.performance_agent import PerformanceAgent


class TestModels:
    """Test the core data models."""

    def test_code_context_creation(self):
        """Test creating a CodeContext object."""
        context = CodeContext(
            file_path=Path("test.py"),
            content="print('hello')",
            language="python",
            file_size=13,
            line_count=1,
        )

        assert context.file_path == Path("test.py")
        assert context.content == "print('hello')"
        assert context.language == "python"
        assert context.file_size == 13
        assert context.line_count == 1

    def test_code_issue_creation(self):
        """Test creating a CodeIssue object."""
        issue = CodeIssue(
            title="Test Issue",
            description="This is a test issue",
            severity=SeverityLevel.HIGH,
            line_number=10,
            effort_estimate=EffortLevel.MEDIUM,
            tags=["test", "example"],
        )

        assert issue.title == "Test Issue"
        assert issue.severity == SeverityLevel.HIGH
        assert issue.line_number == 10
        assert issue.effort_estimate == EffortLevel.MEDIUM
        assert "test" in issue.tags

    def test_agent_score_creation(self):
        """Test creating an AgentScore object."""
        score = AgentScore(
            agent_type=AgentType.ARCHITECT,
            overall_score=75,
            domain_scores={"design_quality": 80, "modularity": 70},
            issues=[],
            recommendations=["Improve naming"],
            analysis_notes="Good overall structure",
        )

        assert score.agent_type == AgentType.ARCHITECT
        assert score.overall_score == 75
        assert score.domain_scores["design_quality"] == 80
        assert "Improve naming" in score.recommendations


class TestArchitectAgent:
    """Test the Architect Agent."""

    def test_agent_initialization(self):
        """Test that the Architect Agent initializes correctly."""
        agent = ArchitectAgent()

        assert agent.agent_type == AgentType.ARCHITECT
        # Model name should come from config or default
        assert agent.model_name is not None
        assert ":" in agent.model_name or agent.model_name.startswith(
            ("gemini", "gpt", "claude")
        )  # Should be valid model format

        # Test domain areas
        domains = agent._get_domain_areas()
        expected_domains = [
            "design_quality",
            "modularity",
            "solid_adherence",
            "maintainability",
            "dependency_management",
        ]

        assert all(domain in domains for domain in expected_domains)


class TestSecurityAgent:
    """Test the Security Agent."""

    def test_agent_initialization(self):
        """Test that the Security Agent initializes correctly."""
        agent = SecurityAgent()

        assert agent.agent_type == AgentType.SECURITY
        # Model name should come from config or default
        assert agent.model_name is not None
        assert ":" in agent.model_name or agent.model_name.startswith(("gemini", "gpt", "claude"))

        # Test domain areas
        domains = agent._get_domain_areas()
        expected_domains = [
            "input_validation",
            "authentication_authorization",
            "injection_vulnerabilities",
            "cryptographic_security",
            "secret_management",
            "data_protection",
            "error_handling",
            "dependency_security",
        ]

        assert all(domain in domains for domain in expected_domains)

    def test_system_prompt_generation(self):
        """Test that the Security Agent generates appropriate system prompts."""
        agent = SecurityAgent()
        prompt = agent._get_system_prompt()

        # Check that security-specific terms are in the prompt
        security_terms = [
            "security",
            "vulnerability",
            "OWASP",
            "injection",
            "authentication",
            "cryptographic",
            "input validation",
        ]

        prompt_lower = prompt.lower()
        for term in security_terms:
            assert term.lower() in prompt_lower

    def test_focus_description(self):
        """Test that the Security Agent has appropriate focus description."""
        agent = SecurityAgent()
        focus = agent._get_focus_description()

        # Should mention key security concepts
        focus_lower = focus.lower()
        assert "security" in focus_lower
        assert "vulnerabilities" in focus_lower or "vulnerability" in focus_lower


class TestPerformanceAgent:
    """Test the Performance Agent."""

    def test_agent_initialization(self):
        """Test that the Performance Agent initializes correctly."""
        agent = PerformanceAgent()

        assert agent.agent_type == AgentType.PERFORMANCE
        # Model name should come from config or default
        assert agent.model_name is not None
        assert ":" in agent.model_name or agent.model_name.startswith(
            ("gemini", "gpt", "claude")
        )  # Should be valid model format

        # Test domain areas
        domains = agent._get_domain_areas()
        expected_domains = [
            "algorithmic_complexity",
            "memory_efficiency",
            "cpu_optimization",
            "io_performance",
            "data_structures",
            "caching_strategy",
            "concurrency_utilization",
            "resource_management",
        ]

        assert all(domain in domains for domain in expected_domains)

    def test_system_prompt_generation(self):
        """Test that the Performance Agent generates appropriate system prompts."""
        agent = PerformanceAgent()
        prompt = agent._get_system_prompt()

        # Check that performance-specific terms are in the prompt
        performance_terms = [
            "performance",
            "optimization",
            "complexity",
            "algorithm",
            "memory",
            "cpu",
            "bottleneck",
            "efficiency",
        ]

        prompt_lower = prompt.lower()
        for term in performance_terms:
            assert term.lower() in prompt_lower

    def test_focus_description(self):
        """Test that the Performance Agent has appropriate focus description."""
        agent = PerformanceAgent()
        focus = agent._get_focus_description()

        # Should mention key performance concepts
        focus_lower = focus.lower()
        assert "performance" in focus_lower or "optimization" in focus_lower
        assert "complexity" in focus_lower or "efficiency" in focus_lower


class TestReviewEngine:
    """Test the Review Engine."""

    def test_engine_initialization(self):
        """Test that the Review Engine initializes correctly."""
        engine = ReviewEngine()

        assert AgentType.ARCHITECT in engine.agents
        assert AgentType.SECURITY in engine.agents
        assert AgentType.PERFORMANCE in engine.agents
        assert len(engine.agents) == 3  # Architect, Security, and Performance Agents

    def test_language_detection(self):
        """Test language detection from file extensions."""
        engine = ReviewEngine()

        assert engine._detect_language(Path("test.py")) == "python"
        assert engine._detect_language(Path("test.js")) == "javascript"
        assert engine._detect_language(Path("test.java")) == "java"
        assert engine._detect_language(Path("test.unknown")) == "unknown"

    def test_file_filtering(self):
        """Test file filtering logic."""
        engine = ReviewEngine()

        request = AnalysisRequest(
            file_path=Path("."),
            include_patterns=["*.py"],
            exclude_patterns=["__pycache__", "*.pyc"],
        )

        # Test should analyze Python files
        assert engine._should_analyze_file(Path("test.py"), request)

        # Test should not analyze excluded patterns
        assert not engine._should_analyze_file(Path("__pycache__/test.py"), request)
        assert not engine._should_analyze_file(Path("test.pyc"), request)

        # Test should not analyze non-matching files
        assert not engine._should_analyze_file(Path("test.js"), request)

    @pytest.mark.asyncio
    async def test_code_context_preparation(self, tmp_path):
        """Test preparing code context from a file."""
        engine = ReviewEngine()

        # Create a temporary Python file
        test_file = tmp_path / "test.py"
        test_content = "def hello():\n    print('Hello, World!')\n"
        test_file.write_text(test_content)

        context = await engine._prepare_code_context(test_file)

        assert context.file_path == test_file
        assert context.content == test_content
        assert context.language == "python"
        assert context.line_count == 2
        assert context.file_size == len(test_content.encode("utf-8"))


class TestIntegration:
    """Integration tests for the complete system."""

    @pytest.mark.asyncio
    async def test_end_to_end_analysis(self, tmp_path):
        """Test complete analysis workflow."""
        # Create a test file with some issues
        test_file = tmp_path / "test_code.py"
        test_content = """
def bad_function(x, y, z):
    # Poor naming and no type hints
    result = x + y + z
    print(result)  # Side effect in function
    return result

# Global variable
GLOBAL_VAR = "bad practice"
"""
        test_file.write_text(test_content)

        # Mock the PydanticAI agent to avoid API calls in tests
        mock_score = AgentScore(
            agent_type=AgentType.ARCHITECT,
            overall_score=60,
            domain_scores={
                "design_quality": 60,
                "modularity": 65,
                "solid_adherence": 55,
                "maintainability": 60,
                "dependency_management": 70,
            },
            issues=[
                CodeIssue(
                    title="Poor Function Naming",
                    description="Function name 'bad_function' is not descriptive",
                    severity=SeverityLevel.MEDIUM,
                    line_number=2,
                    effort_estimate=EffortLevel.LOW,
                    tags=["naming", "readability"],
                )
            ],
            recommendations=["Improve function naming", "Add type hints"],
            analysis_notes="Function has basic issues but structure is okay",
        )

        # Mock all three agents to avoid API calls
        mock_security_score = AgentScore(
            agent_type=AgentType.SECURITY,
            overall_score=70,
            domain_scores={
                "input_validation": 70,
                "authentication_authorization": 70,
                "injection_vulnerabilities": 70,
                "cryptographic_security": 70,
                "secret_management": 70,
                "data_protection": 70,
                "error_handling": 70,
                "dependency_security": 70,
            },
            issues=[],
            recommendations=["Add input validation"],
            analysis_notes="Basic security practices followed",
        )

        mock_performance_score = AgentScore(
            agent_type=AgentType.PERFORMANCE,
            overall_score=80,
            domain_scores={
                "algorithmic_complexity": 80,
                "memory_efficiency": 80,
                "cpu_optimization": 80,
                "io_performance": 80,
                "data_structures": 80,
                "caching_strategy": 80,
                "concurrency_utilization": 80,
                "resource_management": 80,
            },
            issues=[],
            recommendations=["Consider optimization opportunities"],
            analysis_notes="Good performance characteristics",
        )

        with (
            patch.object(ArchitectAgent, "analyze_code", return_value=mock_score),
            patch.object(SecurityAgent, "analyze_code", return_value=mock_security_score),
            patch.object(PerformanceAgent, "analyze_code", return_value=mock_performance_score),
        ):
            engine = ReviewEngine()
            result = await engine.analyze_file(test_file)

            assert result.file_path == test_file
            # Overall score should be average of all agents: (60 + 70 + 80) / 3 = 70
            assert result.overall_score == 70
            assert len(result.agent_scores) == 3
            assert any(score.agent_type == AgentType.ARCHITECT for score in result.agent_scores)
            assert any(score.agent_type == AgentType.SECURITY for score in result.agent_scores)
            assert any(score.agent_type == AgentType.PERFORMANCE for score in result.agent_scores)
            assert len(result.priority_issues) > 0
            assert "Improve function naming" in result.action_plan


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
