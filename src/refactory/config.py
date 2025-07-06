"""
Configuration management for Refactory.

This module handles loading configuration from environment variables,
including AI model selection and API keys.
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class RefactoryConfig:
    """Configuration manager for Refactory settings."""

    def __init__(self):
        """Initialize configuration by loading from environment."""
        self._load_dotenv()
        self._validate_config()

    def _load_dotenv(self) -> None:
        """
        Load environment variables from .env file if it exists.

        System environment variables (from .zshrc, .bashrc, etc.) take precedence
        over .env file variables.
        """
        env_file = Path(".env")
        if env_file.exists():
            try:
                with open(env_file, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")  # Remove quotes
                            # Only set if not already in system environment
                            if key not in os.environ:
                                os.environ[key] = value
                logger.debug(f"Loaded configuration from {env_file}")
            except Exception as e:
                logger.warning(f"Failed to load .env file: {e}")
        else:
            logger.debug("No .env file found, using system environment variables only")

    def _validate_config(self) -> None:
        """Validate that required configuration is present."""
        model = self.get_model()
        provider = self.get_provider_from_model(model)

        # Check if API key is available for the selected provider
        api_key = self.get_api_key(provider)
        if not api_key:
            logger.warning(
                f"No API key found for provider '{provider}'. "
                f"Please set the appropriate environment variable."
            )

    @property
    def default_model(self) -> str:
        """Get the default model if none is specified."""
        return "gemini-2.0-flash-exp"

    def get_model(self, agent_type: Optional[str] = None) -> str:
        """
        Get the AI model to use.

        Args:
            agent_type: Optional specific agent type (architect, security, etc.)

        Returns:
            Model string in format "provider:model-name"
        """
        # Check for agent-specific model override
        if agent_type:
            agent_model = os.getenv(f"REFACTORY_{agent_type.upper()}_MODEL")
            if agent_model:
                return agent_model

        # Check for general model setting
        model = os.getenv("REFACTORY_MODEL")
        if model:
            return model

        return self.default_model

    def get_provider_from_model(self, model: str) -> str:
        """
        Extract provider name from model string.

        Args:
            model: Model string in format "provider:model-name" or just "model-name"

        Returns:
            Provider name (e.g., "openai", "anthropic", "google", "groq")
        """
        if ":" in model:
            return model.split(":", 1)[0].lower()

        # For models without provider prefix, detect from model name
        model_lower = model.lower()
        if model_lower.startswith("gemini"):
            return "google"
        elif model_lower.startswith("claude"):
            return "anthropic"
        elif model_lower.startswith("gpt") or model_lower.startswith("o"):
            return "openai"
        elif model_lower.startswith("llama") or model_lower.startswith("deepseek"):
            return "groq"

        return "openai"  # Default fallback

    def get_api_key(self, provider: str) -> Optional[str]:
        """
        Get API key for the specified provider.

        Args:
            provider: Provider name (openai, anthropic, google, groq)

        Returns:
            API key string or None if not found
        """
        key_mapping = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "google": "GEMINI_API_KEY",
            "groq": "GROQ_API_KEY",
        }

        env_var = key_mapping.get(provider.lower())
        if env_var:
            return os.getenv(env_var)

        logger.warning(f"Unknown provider: {provider}")
        return None

    def get_model_params(self) -> Dict[str, Any]:
        """
        Get model-specific parameters.

        Returns:
            Dictionary of model parameters
        """
        params = {}

        # Temperature setting
        temp = os.getenv("REFACTORY_TEMPERATURE")
        if temp:
            try:
                params["temperature"] = float(temp)
            except ValueError:
                logger.warning(f"Invalid temperature value: {temp}")

        # Max tokens setting
        max_tokens = os.getenv("REFACTORY_MAX_TOKENS")
        if max_tokens:
            try:
                params["max_tokens"] = int(max_tokens)
            except ValueError:
                logger.warning(f"Invalid max_tokens value: {max_tokens}")

        # Timeout setting
        timeout = os.getenv("REFACTORY_TIMEOUT")
        if timeout:
            try:
                params["timeout"] = int(timeout)
            except ValueError:
                logger.warning(f"Invalid timeout value: {timeout}")

        return params

    def get_log_level(self) -> str:
        """Get the logging level."""
        return os.getenv("REFACTORY_LOG_LEVEL", "INFO").upper()

    def is_debug_mode(self) -> bool:
        """Check if debug mode is enabled."""
        return os.getenv("REFACTORY_DEBUG_MODE", "false").lower() == "true"

    def is_cache_enabled(self) -> bool:
        """Check if caching is enabled."""
        return os.getenv("REFACTORY_CACHE_ENABLED", "true").lower() == "true"

    def get_supported_models(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about supported models.

        Returns:
            Dictionary with model information including costs and capabilities
        """
        return {
            # Anthropic Claude Models
            "anthropic:claude-4-opus": {
                "provider": "anthropic",
                "context_window": 200000,
                "input_cost_per_mtok": 15.0,
                "output_cost_per_mtok": 75.0,
                "best_for": "Complex coding, autonomous tasks",
                "performance_tier": "premium",
            },
            "anthropic:claude-4-sonnet": {
                "provider": "anthropic",
                "context_window": 200000,
                "input_cost_per_mtok": 3.0,
                "output_cost_per_mtok": 15.0,
                "best_for": "Balanced performance",
                "performance_tier": "high",
            },
            "anthropic:claude-3.5-haiku": {
                "provider": "anthropic",
                "context_window": 200000,
                "input_cost_per_mtok": 0.8,
                "output_cost_per_mtok": 4.0,
                "best_for": "Fast responses",
                "performance_tier": "standard",
            },
            # OpenAI GPT Models
            "openai:gpt-4.1": {
                "provider": "openai",
                "context_window": 1000000,
                "input_cost_per_mtok": 2.0,
                "output_cost_per_mtok": 8.0,
                "best_for": "Large context tasks",
                "performance_tier": "high",
            },
            "openai:gpt-4o": {
                "provider": "openai",
                "context_window": 128000,
                "input_cost_per_mtok": 5.0,
                "output_cost_per_mtok": 15.0,
                "best_for": "Multimodal (text/image/audio)",
                "performance_tier": "high",
            },
            "openai:gpt-4": {
                "provider": "openai",
                "context_window": 128000,
                "input_cost_per_mtok": 30.0,  # Approximate
                "output_cost_per_mtok": 60.0,  # Approximate
                "best_for": "Reliable general purpose",
                "performance_tier": "high",
            },
            "openai:o4-mini": {
                "provider": "openai",
                "context_window": 200000,
                "input_cost_per_mtok": 0.5,
                "output_cost_per_mtok": 2.0,
                "best_for": "Budget reasoning",
                "performance_tier": "standard",
            },
            # Google Gemini Models (using PydanticAI model names)
            "gemini-2.0-flash-exp": {
                "provider": "google",
                "context_window": 1000000,
                "input_cost_per_mtok": 0.15,
                "output_cost_per_mtok": 0.6,
                "best_for": "Best value (experimental)",
                "performance_tier": "standard",
            },
            "gemini-1.5-flash": {
                "provider": "google",
                "context_window": 1000000,
                "input_cost_per_mtok": 0.075,
                "output_cost_per_mtok": 0.3,
                "best_for": "Fast and efficient",
                "performance_tier": "standard",
            },
            "gemini-1.5-pro": {
                "provider": "google",
                "context_window": 2000000,
                "input_cost_per_mtok": 1.25,
                "output_cost_per_mtok": 10.0,
                "best_for": "Complex reasoning",
                "performance_tier": "high",
            },
            # Groq Models
            "groq:llama-3.3-70b": {
                "provider": "groq",
                "context_window": 128000,
                "input_cost_per_mtok": 0.59,
                "output_cost_per_mtok": 0.79,
                "best_for": "Ultra-fast inference (276 tok/s)",
                "performance_tier": "standard",
            },
            "groq:deepseek-r1": {
                "provider": "groq",
                "context_window": 128000,
                "input_cost_per_mtok": 0.6,
                "output_cost_per_mtok": 1.2,
                "best_for": "Fast reasoning",
                "performance_tier": "standard",
            },
        }


# Global configuration instance
config = RefactoryConfig()
