#!/usr/bin/env python3
"""
Performance Agent Demonstration

This script demonstrates the Performance Agent's capabilities by analyzing
different types of code - from efficient to highly inefficient.

Run this with:
    python examples/performance_demo.py
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the path so we can import refactory
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from refactory.core import ReviewEngine
from refactory.core.models import AnalysisRequest


async def analyze_performance_examples():
    """Analyze different performance examples and show the results."""
    
    print("⚡ Refactory Performance Agent Demonstration")
    print("=" * 50)
    
    # Initialize the review engine
    engine = ReviewEngine()
    
    examples = [
        {
            "name": "Regular Code Example",
            "file": "examples/sample_code.py",
            "description": "Well-structured code with reasonable performance"
        },
        {
            "name": "Performance-Critical Code",
            "file": "examples/slow_code.py", 
            "description": "Code with multiple performance bottlenecks and inefficiencies"
        }
    ]
    
    for example in examples:
        print(f"\n⚡ Analyzing: {example['name']}")
        print(f"📄 File: {example['file']}")
        print(f"📝 Description: {example['description']}")
        print("-" * 50)
        
        try:
            file_path = Path(example['file'])
            if not file_path.exists():
                print(f"❌ File not found: {file_path}")
                continue
                
            # Analyze the file
            result = await engine.analyze_file(file_path)
            
            # Display results
            print(f"📊 Overall Score: {result.overall_score}/100")
            
            # Show agent scores
            for agent_score in result.agent_scores:
                if agent_score.agent_type.value == "performance":
                    print(f"⚡ Performance Score: {agent_score.overall_score}/100")
                    
                    # Show performance domain scores
                    if agent_score.domain_scores:
                        print("\n🎯 Performance Domain Scores:")
                        for domain, score in agent_score.domain_scores.items():
                            domain_name = domain.replace("_", " ").title()
                            print(f"   • {domain_name}: {score}/100")
                    
                    # Show performance issues
                    performance_issues = [issue for issue in agent_score.issues 
                                        if issue.severity.value in ["critical", "high"]]
                    
                    if performance_issues:
                        print(f"\n🚨 Critical/High Performance Issues ({len(performance_issues)}):")
                        for i, issue in enumerate(performance_issues[:3], 1):  # Show top 3
                            severity_emoji = "🔴" if issue.severity.value == "critical" else "🟠"
                            print(f"   {i}. {severity_emoji} {issue.title}")
                            if issue.line_number:
                                print(f"      Line {issue.line_number}: {issue.description[:100]}...")
                    
                    # Show performance recommendations
                    if agent_score.recommendations:
                        print(f"\n💡 Performance Recommendations:")
                        for i, rec in enumerate(agent_score.recommendations[:3], 1):
                            print(f"   {i}. {rec}")
                    
                    break
            
            print()
            
        except Exception as e:
            print(f"❌ Error analyzing {example['file']}: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Performance Analysis Summary")
    print("=" * 50)
    
    print("""
The Performance Agent evaluates code across multiple performance domains:

⚡ **Algorithmic Complexity**: Analyzes time and space complexity (Big O)
🧠 **Memory Efficiency**: Checks for memory leaks and efficient allocation
🔥 **CPU Optimization**: Identifies CPU-intensive operations and bottlenecks
💾 **I/O Performance**: Reviews database queries, file operations, and network calls
📊 **Data Structures**: Evaluates if appropriate data structures are used
🗄️  **Caching Strategy**: Identifies opportunities for memoization and caching
🔄 **Concurrency Utilization**: Looks for parallelization opportunities
🛠️  **Resource Management**: Ensures proper cleanup and resource handling

**Scoring Guide:**
• 90-100: Highly optimized with excellent performance characteristics
• 70-89:  Good performance with minor optimization opportunities
• 50-69:  Moderate performance with several improvement areas
• 30-49:  Poor performance with significant bottlenecks
• 0-29:   Critical performance issues severely impacting efficiency

**Next Steps:**
1. Run: `refactory analyze your_code.py --focus performance`
2. Review algorithmic complexity recommendations
3. Implement suggested optimizations based on priority
4. Profile and benchmark before/after changes
""")


def show_performance_patterns():
    """Show examples of performance patterns the agent can detect."""
    
    print("\n⚡ Performance Patterns Detected")
    print("=" * 35)
    
    patterns = {
        "Algorithmic Complexity Issues": [
            "# O(n²) nested loops",
            "for i in range(len(data)):",
            "    for j in range(len(data)):",
            "",
            "# Inefficient search in unsorted data",
            "if target in large_list:  # O(n) when O(log n) possible"
        ],
        "Memory Inefficiency": [
            "# Multiple unnecessary copies",
            "data1 = original.copy()",
            "data2 = data1.copy()",
            "data3 = data2.copy()",
            "",
            "# Inefficient string concatenation",
            "result = ''",
            "for item in items:",
            "    result += item  # Creates new string each time"
        ],
        "Missing Caching": [
            "# Expensive computation without memoization",
            "def fibonacci(n):",
            "    if n <= 1: return n",
            "    return fibonacci(n-1) + fibonacci(n-2)  # Exponential time",
            "",
            "# Repeated expensive operations",
            "for item in data:",
            "    expensive_calculation(item)  # Same inputs, same outputs"
        ],
        "Blocking I/O Operations": [
            "# Synchronous HTTP requests",
            "for url in urls:",
            "    response = requests.get(url)  # Blocks for each request",
            "",
            "# Blocking file operations",
            "for filename in files:",
            "    with open(filename) as f:",
            "        content = f.read()  # Sequential, not parallel"
        ],
        "Inefficient Data Structures": [
            "# Using list when set is better",
            "if item in large_list:  # O(n) instead of O(1)",
            "",
            "# Wrong data structure for use case",
            "data = []",
            "for item in items:",
            "    data.append(item)",
            "    if target in data:  # O(n) search repeatedly"
        ]
    }
    
    for category, examples in patterns.items():
        print(f"\n🚨 {category}:")
        for example in examples:
            if example.startswith("#"):
                print(f"   {example}")
            elif example == "":
                print()
            else:
                print(f"   ❌ {example}")


def show_optimization_examples():
    """Show before/after optimization examples."""
    
    print("\n🔧 Optimization Examples")
    print("=" * 25)
    
    optimizations = [
        {
            "title": "Fibonacci with Memoization",
            "before": [
                "def fibonacci(n):",
                "    if n <= 1: return n",
                "    return fibonacci(n-1) + fibonacci(n-2)"
            ],
            "after": [
                "from functools import lru_cache",
                "",
                "@lru_cache(maxsize=None)",
                "def fibonacci(n):",
                "    if n <= 1: return n",
                "    return fibonacci(n-1) + fibonacci(n-2)"
            ],
            "improvement": "Exponential → Linear time complexity"
        },
        {
            "title": "Efficient String Concatenation",
            "before": [
                "result = ''",
                "for item in items:",
                "    result += item"
            ],
            "after": [
                "result = ''.join(items)"
            ],
            "improvement": "O(n²) → O(n) time complexity"
        },
        {
            "title": "Set-based Membership Testing",
            "before": [
                "valid_items = []",
                "for item in data:",
                "    if item in allowed_list:  # O(n)",
                "        valid_items.append(item)"
            ],
            "after": [
                "allowed_set = set(allowed_list)",
                "valid_items = [item for item in data",
                "              if item in allowed_set]  # O(1)"
            ],
            "improvement": "O(n²) → O(n) time complexity"
        }
    ]
    
    for opt in optimizations:
        print(f"\n📈 {opt['title']}")
        print("   Before (Inefficient):")
        for line in opt['before']:
            print(f"     {line}")
        
        print("   After (Optimized):")
        for line in opt['after']:
            print(f"     {line}")
        
        print(f"   💡 Improvement: {opt['improvement']}")


if __name__ == "__main__":
    # Run the performance demonstration
    asyncio.run(analyze_performance_examples())
    show_performance_patterns()
    show_optimization_examples()
    
    print("\n🚀 Try analyzing your own code:")
    print("   refactory analyze your_file.py --format detailed")
    print("   refactory analyze your_project/ --focus performance")
    print("   refactory analyze slow_algorithm.py  # Get specific optimization suggestions")
