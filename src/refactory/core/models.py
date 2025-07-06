"""
Core data models for the Refactory multi-agent code analysis system.

This module defines the Pydantic models used throughout the system for
structured data validation and serialization.
"""

from enum import Enum
from typing import List, Dict, Optional, Any
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict


class SeverityLevel(str, Enum):
    """Severity levels for code issues."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecommendationPriority(str, Enum):
    """Priority levels for recommendations."""
    URGENT = "urgent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class EffortLevel(str, Enum):
    """Effort levels for implementing fixes."""
    MINIMAL = "minimal"      # < 30 minutes
    LOW = "low"             # 30 minutes - 2 hours
    MEDIUM = "medium"       # 2 hours - 1 day
    HIGH = "high"           # 1-3 days
    EXTENSIVE = "extensive"  # > 3 days


class AgentType(str, Enum):
    """Types of specialized agents."""
    ARCHITECT = "architect"
    SECURITY = "security"
    PERFORMANCE = "performance"
    DOCUMENTATION = "documentation"
    STYLE = "style"


class CodeIssue(BaseModel):
    """Represents a specific code issue identified by an agent."""
    model_config = ConfigDict(frozen=True)
    
    title: str = Field(..., description="Brief title of the issue")
    description: str = Field(..., description="Detailed description of the issue")
    severity: SeverityLevel = Field(..., description="Severity level of the issue")
    line_number: Optional[int] = Field(None, description="Line number where issue occurs")
    column_number: Optional[int] = Field(None, description="Column number where issue occurs")
    code_snippet: Optional[str] = Field(None, description="Relevant code snippet")
    suggested_fix: Optional[str] = Field(None, description="Suggested code fix")
    effort_estimate: EffortLevel = Field(..., description="Estimated effort to fix")
    tags: List[str] = Field(default_factory=list, description="Categorization tags")


class AgentScore(BaseModel):
    """Score and analysis from a specific agent."""
    model_config = ConfigDict(frozen=True)
    
    agent_type: AgentType = Field(..., description="Type of agent that generated this score")
    overall_score: int = Field(..., ge=0, le=100, description="Overall score (0-100)")
    domain_scores: Dict[str, int] = Field(
        default_factory=dict, 
        description="Scores for specific domain areas"
    )
    issues: List[CodeIssue] = Field(default_factory=list, description="Issues identified")
    recommendations: List[str] = Field(
        default_factory=list, 
        description="High-level recommendations"
    )
    analysis_notes: str = Field(default="", description="Additional analysis notes")


class CodeContext(BaseModel):
    """Context information about the code being analyzed."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    file_path: Path = Field(..., description="Path to the code file")
    content: str = Field(..., description="Raw code content")
    language: str = Field(..., description="Programming language")
    file_size: int = Field(..., description="File size in bytes")
    line_count: int = Field(..., description="Number of lines")
    ast_data: Optional[Any] = Field(None, description="Abstract Syntax Tree data")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Additional metadata"
    )


class ConflictResolution(BaseModel):
    """Resolution of conflicts between agent recommendations."""
    model_config = ConfigDict(frozen=True)
    
    conflicting_agents: List[AgentType] = Field(..., description="Agents with conflicting recommendations")
    conflict_description: str = Field(..., description="Description of the conflict")
    resolution_strategy: str = Field(..., description="How the conflict was resolved")
    final_recommendation: str = Field(..., description="Final unified recommendation")
    trade_offs: List[str] = Field(default_factory=list, description="Trade-offs considered")


class ReviewResult(BaseModel):
    """Complete review result from all agents."""
    model_config = ConfigDict(frozen=True)
    
    file_path: Path = Field(..., description="Path to the analyzed file")
    overall_score: int = Field(..., ge=0, le=100, description="Composite overall score")
    agent_scores: List[AgentScore] = Field(..., description="Individual agent scores")
    priority_issues: List[CodeIssue] = Field(
        default_factory=list, 
        description="Top priority issues across all agents"
    )
    conflict_resolutions: List[ConflictResolution] = Field(
        default_factory=list, 
        description="Resolved conflicts between agents"
    )
    action_plan: List[str] = Field(
        default_factory=list, 
        description="Step-by-step improvement plan"
    )
    analysis_metadata: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Analysis metadata and statistics"
    )


class AnalysisRequest(BaseModel):
    """Request for code analysis."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    file_path: Path = Field(..., description="Path to file or directory to analyze")
    include_patterns: List[str] = Field(
        default_factory=lambda: ["*.py"], 
        description="File patterns to include"
    )
    exclude_patterns: List[str] = Field(
        default_factory=lambda: ["__pycache__", "*.pyc", ".git"], 
        description="File patterns to exclude"
    )
    analysis_depth: str = Field(
        default="standard", 
        description="Analysis depth: quick, standard, thorough"
    )
    focus_areas: List[AgentType] = Field(
        default_factory=list, 
        description="Specific agents to focus on (empty = all agents)"
    )
    custom_rules: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Custom analysis rules and configurations"
    )
