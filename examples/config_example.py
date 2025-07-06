#!/usr/bin/env python3
"""
Example demonstrating Refactory's AI model configuration system.

This example shows how to:
1. Use different AI models for analysis
2. Configure models via environment variables
3. Override models programmatically
4. Check model availability and costs
"""

import asyncio
import os
from pathlib import Path

# Add the src directory to the path so we can import refactory
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from refactory.config import config
from refactory.core import ReviewEngine
from refactory.agents import ArchitectAgent


async def demonstrate_model_configuration():
    """Demonstrate different ways to configure AI models."""

    print("🤖 Refactory AI Model Configuration Demo")
    print("=" * 50)

    # 1. Show current configuration
    print("\n📊 Current Configuration:")
    current_model = config.get_model()
    provider = config.get_provider_from_model(current_model)
    has_api_key = bool(config.get_api_key(provider))

    print(f"  Default Model: {current_model}")
    print(f"  Provider: {provider}")
    print(f"  API Key Available: {'✅' if has_api_key else '❌'}")

    # 2. Show available models
    print("\n🎯 Available Models:")
    supported_models = config.get_supported_models()

    # Show top 3 models by category
    categories = {
        "Best for Coding": ["anthropic:claude-4-opus", "anthropic:claude-4-sonnet"],
        "Best Value": ["google:gemini-2.5-flash", "google:gemini-2.5-flash-lite"],
        "Fastest": ["groq:llama-3.3-70b", "groq:deepseek-r1"],
    }

    for category, models in categories.items():
        print(f"\n  {category}:")
        for model in models:
            if model in supported_models:
                info = supported_models[model]
                print(f"    • {model}")
                print(
                    f"      Cost: ${info['input_cost_per_mtok']:.2f}/${info['output_cost_per_mtok']:.2f} per MTok"
                )
                print(f"      Best for: {info['best_for']}")

    # 3. Demonstrate agent-specific model configuration
    print("\n🎭 Agent-Specific Configuration:")

    # Show how different agents can use different models
    agent_models = {
        "architect": config.get_model("architect"),
        "security": config.get_model("security"),
        "performance": config.get_model("performance"),
    }

    for agent_type, model in agent_models.items():
        print(f"  {agent_type.title()} Agent: {model}")

    # 4. Demonstrate programmatic model override
    print("\n🔧 Programmatic Model Override:")

    # Create agents with different models
    if has_api_key:
        print("  Creating agents with current configuration...")

        # Default agent (uses config)
        default_agent = ArchitectAgent()
        print(f"  Default Agent Model: {default_agent.model_name}")

        # Override agent model
        if "anthropic:claude-4-sonnet" in supported_models:
            override_agent = ArchitectAgent("anthropic:claude-4-sonnet")
            print(f"  Override Agent Model: {override_agent.model_name}")

        # Create review engine with model override
        engine = ReviewEngine()
        print(f"  Review Engine Model: {engine.model_name}")

    else:
        print("  ⚠️  Skipping agent creation - no API key available")

    # 5. Show configuration tips
    print("\n💡 Configuration Tips:")
    print("  1. Set REFACTORY_MODEL in .env file for default model")
    print("  2. Use agent-specific variables like REFACTORY_ARCHITECT_MODEL")
    print("  3. Set appropriate API keys: OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, etc.")
    print("  4. Use --model CLI option for one-time overrides")
    print("  5. Check costs before running large analyses!")

    # 6. Show sample .env configuration
    print("\n📝 Sample .env Configuration:")
    print("  # Choose your preferred model")
    print("  REFACTORY_MODEL=google:gemini-2.5-flash")
    print("  ")
    print("  # Set API key for your chosen provider")
    print("  GEMINI_API_KEY=your_gemini_api_key_here")
    print("  ")
    print("  # Optional: Use different models for different agents")
    print("  REFACTORY_ARCHITECT_MODEL=anthropic:claude-4-sonnet")
    print("  REFACTORY_SECURITY_MODEL=anthropic:claude-4-opus")
    print("  REFACTORY_PERFORMANCE_MODEL=groq:llama-3.3-70b")


def demonstrate_cost_estimation():
    """Show cost estimation for different models."""
    print("\n💰 Cost Estimation Example:")
    print("=" * 30)

    # Estimate costs for analyzing a typical Python file
    typical_file_tokens = 2000  # ~500 lines of Python
    expected_response_tokens = 1000  # Detailed analysis

    supported_models = config.get_supported_models()

    print(
        f"Analyzing a typical file (~{typical_file_tokens} input tokens, ~{expected_response_tokens} output tokens):"
    )
    print()

    # Show costs for different model tiers
    budget_models = [
        m for m, info in supported_models.items() if info["performance_tier"] == "budget"
    ]
    standard_models = [
        m for m, info in supported_models.items() if info["performance_tier"] == "standard"
    ]
    premium_models = [
        m for m, info in supported_models.items() if info["performance_tier"] == "premium"
    ]

    for tier, models in [
        ("Budget", budget_models[:2]),
        ("Standard", standard_models[:2]),
        ("Premium", premium_models[:1]),
    ]:
        if models:
            print(f"{tier} Options:")
            for model in models:
                info = supported_models[model]
                input_cost = (typical_file_tokens / 1_000_000) * info["input_cost_per_mtok"]
                output_cost = (expected_response_tokens / 1_000_000) * info["output_cost_per_mtok"]
                total_cost = input_cost + output_cost

                print(f"  • {model}: ${total_cost:.4f} per analysis")
            print()


if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(demonstrate_model_configuration())
    demonstrate_cost_estimation()

    print("\n🚀 Ready to analyze code with your preferred AI model!")
    print("Run 'refactory models' to see all available options.")
