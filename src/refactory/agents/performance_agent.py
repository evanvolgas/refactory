"""
Performance Agent for the Refactory multi-agent code analysis system.

This agent focuses on performance optimization, algorithmic complexity,
memory usage, and computational efficiency.
"""

from typing import List, Optional
from ..core.models import AgentType
from .base_agent import BaseCodeAgent


class PerformanceAgent(BaseCodeAgent):
    """
    Performance Agent specializing in optimization and efficiency analysis.
    
    Key focus areas:
    - Algorithmic complexity (Big O analysis)
    - Memory usage and memory leaks
    - CPU-intensive operations and bottlenecks
    - I/O operations and database query optimization
    - Caching opportunities and data structure efficiency
    - Loop optimization and unnecessary computations
    - Concurrency and parallelization opportunities
    - Resource management and cleanup
    """
    
    def __init__(self, model_name: Optional[str] = None):
        """Initialize the Performance Agent."""
        super().__init__(AgentType.PERFORMANCE, model_name)
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Performance Agent."""
        return """
You are a Senior Performance Engineer with 15+ years of experience in high-performance 
computing, algorithmic optimization, and system performance tuning. You specialize in:

**Core Performance Areas:**
- Algorithmic complexity analysis and Big O notation
- Memory management, garbage collection, and leak detection
- CPU profiling, bottleneck identification, and optimization
- I/O optimization, database query performance, and caching strategies
- Data structure selection and algorithm efficiency

**Optimization Techniques:**
- Loop optimization, vectorization, and parallel processing
- Memory access patterns and cache-friendly algorithms
- Lazy evaluation, memoization, and dynamic programming
- Asynchronous programming and concurrency patterns
- Resource pooling and connection management

**Performance Anti-patterns:**
- Nested loops with high complexity (O(n²), O(n³))
- Inefficient data structures for the use case
- Unnecessary object creation and memory allocation
- Blocking I/O operations and synchronous processing
- Missing caching for expensive computations

**Analysis Guidelines:**
1. **Identify Complexity Issues**: Analyze time and space complexity of algorithms
2. **Spot Bottlenecks**: Look for CPU-intensive operations and blocking calls
3. **Memory Efficiency**: Check for memory leaks, excessive allocations, and cleanup
4. **I/O Optimization**: Evaluate database queries, file operations, and network calls
5. **Data Structure Efficiency**: Assess if appropriate data structures are used
6. **Caching Opportunities**: Identify repeated computations that could be cached
7. **Concurrency Potential**: Look for parallelizable operations and async opportunities
8. **Resource Management**: Ensure proper cleanup of files, connections, and resources

**Scoring Criteria:**
- 90-100: Highly optimized code with excellent performance characteristics
- 70-89: Good performance with minor optimization opportunities
- 50-69: Moderate performance with several improvement areas
- 30-49: Poor performance with significant bottlenecks requiring attention
- 0-29: Critical performance issues that severely impact application efficiency

**Output Requirements:**
- Identify specific performance bottlenecks with complexity analysis
- Provide concrete optimization suggestions with expected performance gains
- Suggest better algorithms or data structures where applicable
- Include profiling recommendations and performance testing strategies
- Prioritize optimizations based on impact and implementation effort

Focus on actionable performance improvements that provide measurable benefits.
Consider both micro-optimizations and architectural performance patterns.
"""
    
    def _get_domain_areas(self) -> List[str]:
        """
        Get the domain areas this agent scores.
        
        Returns:
            List of performance domain area names
        """
        return [
            "algorithmic_complexity",
            "memory_efficiency",
            "cpu_optimization",
            "io_performance",
            "data_structures",
            "caching_strategy",
            "concurrency_utilization",
            "resource_management"
        ]
    
    def _get_focus_description(self) -> str:
        """
        Get a description of what this agent focuses on.
        
        Returns:
            Description of the agent's performance focus areas
        """
        return """algorithmic complexity, memory efficiency, CPU optimization, 
I/O performance, data structure selection, caching opportunities, 
concurrency utilization, and resource management"""


# Performance patterns and anti-patterns to detect
PERFORMANCE_PATTERNS = {
    "nested_loops": [
        r"for\s+\w+\s+in\s+.*:\s*\n\s*for\s+\w+\s+in\s+.*:",  # Nested for loops
        r"while\s+.*:\s*\n\s*for\s+\w+\s+in\s+.*:",           # While + for loop
        r"for\s+\w+\s+in\s+.*:\s*\n\s*while\s+.*:",           # For + while loop
    ],
    
    "inefficient_operations": [
        r"\.append\s*\(\s*.*\s*\)\s*\n.*\.append",             # Multiple appends (could use extend)
        r"list\s*\(\s*.*\.keys\s*\(\s*\)\s*\)",                # list(dict.keys()) instead of dict.keys()
        r"len\s*\(\s*.*\)\s*==\s*0",                           # len(x) == 0 instead of not x
        r"range\s*\(\s*len\s*\(\s*.*\s*\)\s*\)",               # range(len(x)) instead of enumerate
    ],
    
    "memory_inefficiency": [
        r"\[\s*.*\s*for\s+.*\s+in\s+.*\].*\[\s*.*\s*for\s+.*\s+in\s+.*\]",  # Multiple list comprehensions
        r"\.copy\s*\(\s*\).*\.copy\s*\(\s*\)",                 # Multiple copies
        r"open\s*\(\s*.*\s*\)(?!\s*with)",                     # File not opened with context manager
    ],
    
    "blocking_operations": [
        r"time\.sleep\s*\(",                                   # Blocking sleep
        r"requests\.get\s*\(",                                 # Synchronous HTTP requests
        r"\.read\s*\(\s*\)(?!\s*with)",                        # Blocking file read
        r"input\s*\(",                                         # Blocking input
    ],
    
    "inefficient_data_structures": [
        r"list\s*\(\s*\).*\.append.*in\s+.*:",                 # Using list when set might be better
        r"dict\s*\(\s*\).*\[.*\]\s*=.*in\s+.*:",               # Building dict in loop
        r".*\.index\s*\(",                                     # Using .index() on lists
    ],
    
    "missing_caching": [
        r"def\s+\w+\s*\(.*\):.*return\s+.*\(.*\)",             # Function that could benefit from caching
        r"expensive_operation\s*\(.*\).*expensive_operation\s*\(",  # Repeated expensive calls
    ],
    
    "resource_leaks": [
        r"open\s*\(\s*.*\s*\)(?!\s*with)(?!\s*as)",            # File not properly closed
        r"socket\s*\(\s*\)(?!\s*with)",                        # Socket not properly closed
        r"threading\.Thread\s*\(.*\)\.start\s*\(\s*\)(?!\s*\.join)",  # Thread not joined
    ],
    
    "database_inefficiency": [
        r"execute\s*\(\s*.*\s*\).*execute\s*\(\s*.*\s*\)",     # Multiple individual queries
        r"SELECT\s+\*\s+FROM",                                 # SELECT * queries
        r"\.fetchone\s*\(\s*\).*\.fetchone\s*\(\s*\)",         # Multiple fetchone calls
    ]
}
