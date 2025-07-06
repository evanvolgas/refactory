"""
Command Line Interface for the Refactory multi-agent code analysis system.

This module provides a CLI for running code analysis from the command line.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .core.review_engine import ReviewEngine
from .core.models import AnalysisRequest, AgentType
from .config import config

console = Console()
logger = logging.getLogger(__name__)


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.option("--model", help="AI model to use for analysis (overrides .env config)")
@click.pass_context
def main(ctx, verbose: bool, model: Optional[str]):
    """
    Refactory: Multi-Agent Code Analysis System

    Analyze your code with specialized AI agents for comprehensive reviews.

    Configure your preferred AI model in .env file or use --model option.
    """
    # Set up logging based on config and CLI options
    log_level = config.get_log_level() if not verbose else "DEBUG"
    level = getattr(logging, log_level)
    logging.basicConfig(level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Store context
    ctx.ensure_object(dict)
    ctx.obj["model"] = model  # CLI override, None if not provided
    ctx.obj["verbose"] = verbose or config.is_debug_mode()


@main.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file for results")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "table", "detailed"]),
    default="table",
    help="Output format",
)
@click.option("--include", multiple=True, default=["*.py"], help="File patterns to include")
@click.option(
    "--exclude",
    multiple=True,
    default=["__pycache__", "*.pyc", ".git"],
    help="File patterns to exclude",
)
@click.option(
    "--depth",
    type=click.Choice(["quick", "standard", "thorough"]),
    default="standard",
    help="Analysis depth",
)
@click.option(
    "--focus",
    type=click.Choice([t.value for t in AgentType]),
    multiple=True,
    help="Focus on specific agent types",
)
@click.pass_context
def analyze(
    ctx,
    path: Path,
    output: Optional[Path],
    output_format: str,
    include: tuple,
    exclude: tuple,
    depth: str,
    focus: tuple,
):
    """
    Analyze code files or directories.

    PATH: File or directory to analyze
    """
    # Run the async analysis
    asyncio.run(_run_analysis(ctx, path, output, output_format, include, exclude, depth, focus))


async def _run_analysis(
    ctx,
    path: Path,
    output: Optional[Path],
    output_format: str,
    include: tuple,
    exclude: tuple,
    depth: str,
    focus: tuple,
):
    """Run the actual analysis (async function)."""
    # Get model from CLI override or config
    cli_model = ctx.obj["model"]
    actual_model = cli_model or config.get_model()

    console.print(f"🔍 Starting Refactory analysis of: {path}")
    console.print(f"📊 Using model: {actual_model}")

    # Show model info if available
    supported_models = config.get_supported_models()
    if actual_model in supported_models:
        model_info = supported_models[actual_model]
        console.print(
            f"💡 Model info: {model_info['best_for']} (${model_info['input_cost_per_mtok']:.2f}/${model_info['output_cost_per_mtok']:.2f} per MTok)"
        )

    # Check API key availability
    provider = config.get_provider_from_model(actual_model)
    if not config.get_api_key(provider):
        console.print(
            f"⚠️  Warning: No API key found for {provider}. Please set the appropriate environment variable.",
            style="yellow",
        )

    # Convert focus to AgentType enums
    focus_agents = [AgentType(f) for f in focus] if focus else []

    # Create analysis request
    request = AnalysisRequest(
        file_path=path,
        include_patterns=list(include),
        exclude_patterns=list(exclude),
        analysis_depth=depth,
        focus_areas=focus_agents,
    )

    # Run analysis with progress indicator
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing code...", total=None)

        try:
            engine = ReviewEngine(cli_model)  # Pass CLI override or None to use config
            results = await engine.analyze(request)
            progress.update(task, description="Analysis complete!")

        except Exception as e:
            console.print(f"❌ Analysis failed: {str(e)}", style="red")
            raise click.Abort()

    if not results:
        console.print("⚠️  No files were analyzed", style="yellow")
        return

    # Display results
    if output_format == "json":
        await _output_json(results, output)
    elif output_format == "detailed":
        await _output_detailed(results, output)
    else:
        await _output_table(results, output)

    console.print(f"✅ Analysis complete! Processed {len(results)} files.")


async def _output_table(results, output_file):
    """Output results in table format."""
    table = Table(title="🔍 Refactory Analysis Results")

    table.add_column("File", style="cyan", no_wrap=True)
    table.add_column("Overall Score", justify="center", style="magenta")
    table.add_column("Issues", justify="center", style="red")
    table.add_column("Top Issue", style="yellow")

    for result in results:
        file_name = result.file_path.name
        score = str(result.overall_score)
        issue_count = str(len(result.priority_issues))
        top_issue = result.priority_issues[0].title if result.priority_issues else "None"

        # Color code the score
        if result.overall_score >= 80:
            score_style = "green"
        elif result.overall_score >= 60:
            score_style = "yellow"
        else:
            score_style = "red"

        table.add_row(
            file_name,
            f"[{score_style}]{score}[/{score_style}]",
            issue_count,
            top_issue[:50] + "..." if len(top_issue) > 50 else top_issue,
        )

    console.print(table)

    if output_file:
        with open(output_file, "w") as f:
            console.print(table, file=f)


async def _output_detailed(results, output_file):
    """Output detailed results."""
    for result in results:
        # File header
        panel_title = f"📁 {result.file_path.name} (Score: {result.overall_score}/100)"

        content = []

        # Agent scores
        if result.agent_scores:
            content.append("🤖 Agent Scores:")
            for agent_score in result.agent_scores:
                content.append(
                    f"  • {agent_score.agent_type.value.title()}: {agent_score.overall_score}/100"
                )

        # Top issues
        if result.priority_issues:
            content.append("\n🚨 Priority Issues:")
            for i, issue in enumerate(result.priority_issues[:5], 1):
                content.append(f"  {i}. [{issue.severity.value.upper()}] {issue.title}")
                if issue.line_number:
                    content.append(f"     Line {issue.line_number}: {issue.description[:100]}...")

        # Action plan
        if result.action_plan:
            content.append("\n📋 Action Plan:")
            for i, action in enumerate(result.action_plan[:3], 1):
                content.append(f"  {i}. {action}")

        panel = Panel("\n".join(content), title=panel_title, border_style="blue")
        console.print(panel)

    if output_file:
        with open(output_file, "w") as f:
            for result in results:
                console.print(f"File: {result.file_path}", file=f)
                console.print(f"Score: {result.overall_score}/100", file=f)
                console.print("Issues:", file=f)
                for issue in result.priority_issues:
                    console.print(f"  - {issue.title}", file=f)
                console.print("", file=f)


async def _output_json(results, output_file):
    """Output results in JSON format."""
    # Convert results to JSON-serializable format
    json_results = []
    for result in results:
        json_result = {
            "file_path": str(result.file_path),
            "overall_score": result.overall_score,
            "agent_scores": [
                {
                    "agent_type": score.agent_type.value,
                    "overall_score": score.overall_score,
                    "domain_scores": score.domain_scores,
                    "issues_count": len(score.issues),
                    "recommendations": score.recommendations,
                }
                for score in result.agent_scores
            ],
            "priority_issues": [
                {
                    "title": issue.title,
                    "severity": issue.severity.value,
                    "line_number": issue.line_number,
                    "description": issue.description,
                }
                for issue in result.priority_issues
            ],
            "action_plan": result.action_plan,
            "metadata": result.analysis_metadata,
        }
        json_results.append(json_result)

    json_output = json.dumps(json_results, indent=2)

    if output_file:
        output_file.write_text(json_output)
        console.print(f"📄 Results saved to: {output_file}")
    else:
        console.print(json_output)


@main.command()
def info():
    """Show information about available agents and capabilities."""
    console.print("🤖 Available Agents:", style="bold blue")

    agents_info = [
        ("🏗️  Architect", "Design patterns, SOLID principles, code structure"),
        ("🔒 Security", "Vulnerabilities, secure coding practices (Coming Soon)"),
        ("⚡ Performance", "Efficiency, complexity, scalability (Coming Soon)"),
        ("📚 Documentation", "Code clarity, comments, API docs (Coming Soon)"),
        ("🎨 Style", "Consistency, naming, formatting (Coming Soon)"),
    ]

    for name, description in agents_info:
        console.print(f"  {name}: {description}")

    console.print("\n📋 Supported Languages:", style="bold blue")
    console.print("  • Python (Full support)")
    console.print("  • JavaScript, TypeScript, Java, C++, Go (Coming Soon)")


@main.command()
def models():
    """Show available AI models and current configuration."""
    console.print("\n🤖 Available AI Models", style="bold blue")

    # Show current configuration
    current_model = config.get_model()
    provider = config.get_provider_from_model(current_model)
    has_api_key = bool(config.get_api_key(provider))

    console.print(f"\n📊 Current Configuration:")
    console.print(f"  Model: {current_model}")
    console.print(f"  Provider: {provider}")
    console.print(f"  API Key: {'✅ Set' if has_api_key else '❌ Missing'}")

    # Create models table
    table = Table(title="\nSupported Models")
    table.add_column("Model", style="cyan", no_wrap=True)
    table.add_column("Provider", style="magenta")
    table.add_column("Context", justify="right")
    table.add_column("Input Cost", justify="right")
    table.add_column("Output Cost", justify="right")
    table.add_column("Best For", style="green")
    table.add_column("Tier", style="yellow")

    supported_models = config.get_supported_models()

    # Group by provider for better organization
    providers = {}
    for model_name, info in supported_models.items():
        provider_name = info["provider"]
        if provider_name not in providers:
            providers[provider_name] = []
        providers[provider_name].append((model_name, info))

    # Add rows grouped by provider
    for provider_name in sorted(providers.keys()):
        for model_name, info in sorted(providers[provider_name]):
            # Format context window
            context = (
                f"{info['context_window']:,}"
                if info["context_window"] < 1000000
                else f"{info['context_window']/1000000:.1f}M"
            )

            # Format costs
            input_cost = f"${info['input_cost_per_mtok']:.2f}"
            output_cost = f"${info['output_cost_per_mtok']:.2f}"

            # Highlight current model
            model_display = (
                f"[bold]{model_name}[/bold]" if model_name == current_model else model_name
            )

            table.add_row(
                model_display,
                provider_name.title(),
                context,
                input_cost,
                output_cost,
                info["best_for"],
                info["performance_tier"].title(),
            )

    console.print(table)

    # Show configuration instructions
    console.print(f"\n💡 Configuration:")
    console.print(f"  • Set REFACTORY_MODEL in .env file to change default model")
    console.print(
        f"  • Set API keys: OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, GROQ_API_KEY"
    )
    console.print(f"  • Use --model option to override for single analysis")
    console.print(f"  • Agent-specific models: REFACTORY_ARCHITECT_MODEL, etc.")


if __name__ == "__main__":
    main()
