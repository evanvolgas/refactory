"""
Base agent class for the Refactory multi-agent code analysis system.

This module provides the abstract base class that all specialized agents inherit from,
defining the common interface and shared functionality.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging
from pydantic_ai import Agent, RunContext

from ..core.models import AgentScore, AgentType, CodeContext, CodeIssue, SeverityLevel, EffortLevel
from ..config import config


logger = logging.getLogger(__name__)


class BaseCodeAgent(ABC):
    """
    Abstract base class for all code analysis agents.

    Each specialized agent (Architect, Security, Performance, Documentation, Style)
    inherits from this class and implements the analyze_code method.
    """

    def __init__(self, agent_type: AgentType, model_name: Optional[str] = None):
        """
        Initialize the base agent.

        Args:
            agent_type: The type of agent (from AgentType enum)
            model_name: The AI model to use for analysis (if None, uses config)
        """
        self.agent_type = agent_type
        # Use provided model or get from config (with agent-specific override)
        self.model_name = model_name or config.get_model(agent_type.value)
        self.model_params = config.get_model_params()
        self._setup_pydantic_agent()

    def _setup_pydantic_agent(self) -> None:
        """Set up the PydanticAI agent with appropriate system prompt and parameters."""
        system_prompt = self._get_system_prompt()

        # Prepare agent configuration
        agent_config = {
            "model": self.model_name,
            "system_prompt": system_prompt,
            "output_type": AgentScore,
        }

        # Add model-specific parameters if available
        agent_config.update(self.model_params)

        self.agent = Agent(**agent_config)

        logger.debug(f"Initialized {self.agent_type.value} agent with model: {self.model_name}")

    @abstractmethod
    def _get_system_prompt(self) -> str:
        """
        Get the system prompt for this agent type.

        Returns:
            System prompt string tailored to the agent's specialization
        """
        pass

    @abstractmethod
    def _get_domain_areas(self) -> List[str]:
        """
        Get the domain areas this agent scores.

        Returns:
            List of domain area names for scoring
        """
        pass

    async def analyze_code(self, context: CodeContext) -> AgentScore:
        """
        Analyze code from this agent's specialized perspective.

        Args:
            context: Code context containing file content and metadata

        Returns:
            AgentScore with analysis results
        """
        try:
            logger.info(f"Starting {self.agent_type.value} analysis for {context.file_path}")

            # Prepare the analysis prompt
            analysis_prompt = self._prepare_analysis_prompt(context)

            # Run the PydanticAI agent
            result = await self.agent.run(analysis_prompt)

            # Validate and enhance the result
            agent_score = self._process_agent_result(result.output, context)

            logger.info(
                f"Completed {self.agent_type.value} analysis with score: {agent_score.overall_score}"
            )
            return agent_score

        except Exception as e:
            logger.error(f"Error in {self.agent_type.value} analysis: {str(e)}")
            return self._create_error_score(str(e))

    def _prepare_analysis_prompt(self, context: CodeContext) -> str:
        """
        Prepare the analysis prompt for the AI agent.

        Args:
            context: Code context to analyze

        Returns:
            Formatted prompt string
        """
        prompt = f"""
Analyze the following {context.language} code from the perspective of a {self.agent_type.value} expert.

File: {context.file_path}
Language: {context.language}
Lines: {context.line_count}

Code:
```{context.language}
{context.content}
```

Please provide:
1. An overall score (0-100) for {self.agent_type.value} quality
2. Specific domain scores for: {', '.join(self._get_domain_areas())}
3. Detailed issues with severity levels and line numbers
4. Concrete recommendations for improvement
5. Analysis notes explaining your assessment

Focus on {self._get_focus_description()} and provide actionable, specific feedback.
"""
        return prompt

    @abstractmethod
    def _get_focus_description(self) -> str:
        """
        Get a description of what this agent focuses on.

        Returns:
            Description of the agent's focus areas
        """
        pass

    def _process_agent_result(self, result: AgentScore, context: CodeContext) -> AgentScore:
        """
        Process and validate the agent result.

        Args:
            result: Raw result from the AI agent
            context: Original code context

        Returns:
            Processed and validated AgentScore
        """
        # Ensure the agent type is set correctly
        if result.agent_type != self.agent_type:
            result = result.model_copy(update={"agent_type": self.agent_type})

        # Validate domain scores
        expected_domains = self._get_domain_areas()
        for domain in expected_domains:
            if domain not in result.domain_scores:
                result.domain_scores[domain] = result.overall_score

        # Validate issues have required fields
        validated_issues = []
        for issue in result.issues:
            if not issue.effort_estimate:
                issue = issue.model_copy(update={"effort_estimate": EffortLevel.MEDIUM})
            validated_issues.append(issue)

        result = result.model_copy(update={"issues": validated_issues})

        return result

    def _create_error_score(self, error_message: str) -> AgentScore:
        """
        Create an error score when analysis fails.

        Args:
            error_message: Error message to include

        Returns:
            AgentScore indicating analysis failure
        """
        return AgentScore(
            agent_type=self.agent_type,
            overall_score=0,
            domain_scores={domain: 0 for domain in self._get_domain_areas()},
            issues=[
                CodeIssue(
                    title="Analysis Error",
                    description=f"Failed to analyze code: {error_message}",
                    severity=SeverityLevel.CRITICAL,
                    effort_estimate=EffortLevel.HIGH,
                    tags=["error", "analysis-failure"],
                )
            ],
            recommendations=[f"Fix analysis error: {error_message}"],
            analysis_notes=f"Analysis failed due to error: {error_message}",
        )

    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get information about this agent.

        Returns:
            Dictionary with agent information
        """
        return {
            "type": self.agent_type.value,
            "model": self.model_name,
            "domain_areas": self._get_domain_areas(),
            "focus": self._get_focus_description(),
        }
