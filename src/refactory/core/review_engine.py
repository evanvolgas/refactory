"""
Review Engine for the Refactory multi-agent code analysis system.

This module orchestrates the analysis process, coordinating between multiple
agents and producing unified results.
"""

import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from .models import (
    AnalysisRequest,
    ReviewResult,
    CodeContext,
    AgentScore,
    AgentType,
    CodeIssue,
    ConflictResolution,
    RecommendationPriority,
)
from ..agents import BaseCodeAgent, ArchitectAgent, SecurityAgent, PerformanceAgent
from ..config import config

logger = logging.getLogger(__name__)


class ReviewEngine:
    """
    Main engine that orchestrates the multi-agent code analysis process.

    The engine:
    1. Processes analysis requests
    2. Prepares code context for agents
    3. Coordinates agent execution
    4. Resolves conflicts between agent recommendations
    5. Produces unified review results
    """

    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize the Review Engine.

        Args:
            model_name: AI model to use for all agents (if None, uses config)
        """
        self.model_name = model_name or config.get_model()
        self.agents: Dict[AgentType, BaseCodeAgent] = {}
        self._initialize_agents()

    def _initialize_agents(self) -> None:
        """Initialize all available agents."""
        # Initialize core agents
        self.agents[AgentType.ARCHITECT] = ArchitectAgent(self.model_name)
        self.agents[AgentType.SECURITY] = SecurityAgent(self.model_name)
        self.agents[AgentType.PERFORMANCE] = PerformanceAgent(self.model_name)

        logger.info(f"Initialized {len(self.agents)} agents: {list(self.agents.keys())}")

    async def analyze_file(self, file_path: Path, **kwargs) -> ReviewResult:
        """
        Analyze a single file.

        Args:
            file_path: Path to the file to analyze
            **kwargs: Additional analysis options

        Returns:
            ReviewResult with complete analysis
        """
        request = AnalysisRequest(file_path=file_path, **kwargs)
        results = await self.analyze(request)
        return results[0] if results else self._create_empty_result(file_path)

    async def analyze(self, request: AnalysisRequest) -> List[ReviewResult]:
        """
        Analyze code based on the analysis request.

        Args:
            request: Analysis request with configuration

        Returns:
            List of ReviewResult objects (one per file analyzed)
        """
        logger.info(f"Starting analysis for: {request.file_path}")

        # Get files to analyze
        files_to_analyze = self._get_files_to_analyze(request)

        if not files_to_analyze:
            logger.warning(f"No files found to analyze in: {request.file_path}")
            return []

        # Analyze each file
        results = []
        for file_path in files_to_analyze:
            try:
                result = await self._analyze_single_file(file_path, request)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to analyze {file_path}: {str(e)}")
                results.append(self._create_error_result(file_path, str(e)))

        logger.info(f"Completed analysis of {len(results)} files")
        return results

    async def _analyze_single_file(self, file_path: Path, request: AnalysisRequest) -> ReviewResult:
        """
        Analyze a single file with all relevant agents.

        Args:
            file_path: Path to the file to analyze
            request: Original analysis request

        Returns:
            ReviewResult for the file
        """
        # Prepare code context
        context = await self._prepare_code_context(file_path)

        # Determine which agents to use
        agents_to_use = self._get_agents_for_analysis(request.focus_areas)

        # Run agents in parallel
        agent_tasks = [agent.analyze_code(context) for agent in agents_to_use]

        agent_scores = await asyncio.gather(*agent_tasks, return_exceptions=True)

        # Filter out exceptions and log errors
        valid_scores = []
        for i, score in enumerate(agent_scores):
            if isinstance(score, Exception):
                logger.error(f"Agent {list(agents_to_use)[i].agent_type} failed: {str(score)}")
            else:
                valid_scores.append(score)

        # Create unified result
        return self._create_review_result(file_path, valid_scores, context)

    def _get_files_to_analyze(self, request: AnalysisRequest) -> List[Path]:
        """
        Get list of files to analyze based on the request.

        Args:
            request: Analysis request

        Returns:
            List of file paths to analyze
        """
        path = request.file_path

        if path.is_file():
            return [path] if self._should_analyze_file(path, request) else []

        if path.is_dir():
            files = []
            for pattern in request.include_patterns:
                files.extend(path.rglob(pattern))

            # Filter out excluded files
            filtered_files = []
            for file_path in files:
                if self._should_analyze_file(file_path, request):
                    filtered_files.append(file_path)

            return filtered_files

        return []

    def _should_analyze_file(self, file_path: Path, request: AnalysisRequest) -> bool:
        """
        Check if a file should be analyzed based on include/exclude patterns.

        Args:
            file_path: Path to check
            request: Analysis request with patterns

        Returns:
            True if file should be analyzed
        """
        # Check exclude patterns
        for pattern in request.exclude_patterns:
            # Check if any part of the path matches the exclude pattern
            if (
                file_path.match(pattern)
                or any(part.startswith(".") for part in file_path.parts)
                or any(str(file_path).find(pattern) != -1 for _ in [pattern])
            ):
                return False

        # Check include patterns
        for pattern in request.include_patterns:
            if file_path.match(pattern):
                return True

        return False

    async def _prepare_code_context(self, file_path: Path) -> CodeContext:
        """
        Prepare code context for analysis.

        Args:
            file_path: Path to the code file

        Returns:
            CodeContext with file information
        """
        try:
            content = file_path.read_text(encoding="utf-8")

            return CodeContext(
                file_path=file_path,
                content=content,
                language=self._detect_language(file_path),
                file_size=len(content.encode("utf-8")),
                line_count=len(content.splitlines()),
                metadata={
                    "analyzed_at": datetime.now().isoformat(),
                    "file_extension": file_path.suffix,
                },
            )
        except Exception as e:
            logger.error(f"Failed to prepare context for {file_path}: {str(e)}")
            raise

    def _detect_language(self, file_path: Path) -> str:
        """
        Detect programming language from file extension.

        Args:
            file_path: Path to the file

        Returns:
            Language name
        """
        extension_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".cpp": "cpp",
            ".c": "c",
            ".go": "go",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php",
        }

        return extension_map.get(file_path.suffix.lower(), "unknown")

    def _get_agents_for_analysis(self, focus_areas: List[AgentType]) -> List[BaseCodeAgent]:
        """
        Get agents to use for analysis.

        Args:
            focus_areas: Specific agents to focus on (empty = all agents)

        Returns:
            List of agents to use
        """
        if focus_areas:
            return [
                self.agents[agent_type] for agent_type in focus_areas if agent_type in self.agents
            ]
        else:
            return list(self.agents.values())

    def _create_review_result(
        self, file_path: Path, agent_scores: List[AgentScore], context: CodeContext
    ) -> ReviewResult:
        """
        Create a unified review result from agent scores.

        Args:
            file_path: Path to the analyzed file
            agent_scores: Scores from all agents
            context: Code context

        Returns:
            Unified ReviewResult
        """
        if not agent_scores:
            return self._create_empty_result(file_path)

        # Calculate overall score (weighted average)
        overall_score = sum(score.overall_score for score in agent_scores) // len(agent_scores)

        # Collect all issues and sort by priority
        all_issues = []
        for score in agent_scores:
            all_issues.extend(score.issues)

        # Sort issues by severity and score impact
        priority_issues = sorted(
            all_issues,
            key=lambda issue: (
                {"critical": 0, "high": 1, "medium": 2, "low": 3}[issue.severity.value],
                -len(issue.description),  # Longer descriptions might be more detailed
            ),
        )[
            :10
        ]  # Top 10 issues

        # Create action plan from recommendations
        action_plan = []
        for score in agent_scores:
            action_plan.extend(score.recommendations)

        return ReviewResult(
            file_path=file_path,
            overall_score=overall_score,
            agent_scores=agent_scores,
            priority_issues=priority_issues,
            conflict_resolutions=[],  # TODO: Implement conflict resolution
            action_plan=action_plan,
            analysis_metadata={
                "agents_used": [score.agent_type.value for score in agent_scores],
                "total_issues": len(all_issues),
                "analysis_timestamp": datetime.now().isoformat(),
                "file_language": context.language,
                "file_size": context.file_size,
                "line_count": context.line_count,
            },
        )

    def _create_empty_result(self, file_path: Path) -> ReviewResult:
        """Create an empty result for when no analysis is possible."""
        return ReviewResult(
            file_path=file_path,
            overall_score=0,
            agent_scores=[],
            priority_issues=[],
            conflict_resolutions=[],
            action_plan=["No analysis performed"],
            analysis_metadata={"error": "No agents available or file not analyzable"},
        )

    def _create_error_result(self, file_path: Path, error_message: str) -> ReviewResult:
        """Create an error result when analysis fails."""
        return ReviewResult(
            file_path=file_path,
            overall_score=0,
            agent_scores=[],
            priority_issues=[],
            conflict_resolutions=[],
            action_plan=[f"Fix analysis error: {error_message}"],
            analysis_metadata={"error": error_message, "analysis_failed": True},
        )
