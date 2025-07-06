"""
Refactory: Multi-Agent Code Analysis System

A comprehensive code review system using specialized AI agents for different
aspects of code quality analysis.
"""

__version__ = "0.1.0"
__author__ = "Evan Volgas"

from .core.review_engine import ReviewEngine
from .core.models import (
    ReviewResult,
    AgentScore,
    RecommendationPriority,
    AnalysisRequest,
    CodeContext,
    AgentType,
)
from .agents import ArchitectAgent

__all__ = [
    "__version__",
    "__author__",
    "ReviewEngine",
    "ReviewResult",
    "AgentScore",
    "RecommendationPriority",
    "AnalysisRequest",
    "CodeContext",
    "AgentType",
    "ArchitectAgent",
]
