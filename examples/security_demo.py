#!/usr/bin/env python3
"""
Security Agent Demonstration

This script demonstrates the Security Agent's capabilities by analyzing
different types of code - from secure to highly vulnerable.

Run this with:
    python examples/security_demo.py
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the path so we can import refactory
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from refactory.core import ReviewEngine
from refactory.core.models import AnalysisRequest


async def analyze_security_examples():
    """Analyze different security examples and show the results."""
    
    print("🔒 Refactory Security Agent Demonstration")
    print("=" * 50)
    
    # Initialize the review engine
    engine = ReviewEngine()
    
    examples = [
        {
            "name": "Secure Code Example",
            "file": "examples/sample_code.py",
            "description": "Well-structured code with basic security practices"
        },
        {
            "name": "Highly Vulnerable Code",
            "file": "examples/insecure_code.py", 
            "description": "Code with multiple critical security vulnerabilities"
        }
    ]
    
    for example in examples:
        print(f"\n🔍 Analyzing: {example['name']}")
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
                if agent_score.agent_type.value == "security":
                    print(f"🔒 Security Score: {agent_score.overall_score}/100")
                    
                    # Show security domain scores
                    if agent_score.domain_scores:
                        print("\n🎯 Security Domain Scores:")
                        for domain, score in agent_score.domain_scores.items():
                            domain_name = domain.replace("_", " ").title()
                            print(f"   • {domain_name}: {score}/100")
                    
                    # Show security issues
                    security_issues = [issue for issue in agent_score.issues 
                                     if issue.severity.value in ["critical", "high"]]
                    
                    if security_issues:
                        print(f"\n🚨 Critical/High Security Issues ({len(security_issues)}):")
                        for i, issue in enumerate(security_issues[:3], 1):  # Show top 3
                            severity_emoji = "🔴" if issue.severity.value == "critical" else "🟠"
                            print(f"   {i}. {severity_emoji} {issue.title}")
                            if issue.line_number:
                                print(f"      Line {issue.line_number}: {issue.description[:100]}...")
                    
                    # Show security recommendations
                    if agent_score.recommendations:
                        print(f"\n💡 Security Recommendations:")
                        for i, rec in enumerate(agent_score.recommendations[:3], 1):
                            print(f"   {i}. {rec}")
                    
                    break
            
            print()
            
        except Exception as e:
            print(f"❌ Error analyzing {example['file']}: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Security Analysis Summary")
    print("=" * 50)
    
    print("""
The Security Agent evaluates code across multiple security domains:

🔍 **Input Validation**: Checks for proper sanitization and validation
🔐 **Authentication/Authorization**: Reviews access control mechanisms  
💉 **Injection Vulnerabilities**: Detects SQL, command, and code injection risks
🔒 **Cryptographic Security**: Validates encryption and hashing practices
🗝️  **Secret Management**: Identifies hardcoded credentials and API keys
🛡️  **Data Protection**: Reviews secure data handling and storage
⚠️  **Error Handling**: Ensures errors don't leak sensitive information
📦 **Dependency Security**: Evaluates third-party library security

**Scoring Guide:**
• 90-100: Excellent security posture
• 70-89:  Good security with minor issues
• 50-69:  Moderate security concerns
• 30-49:  Poor security requiring attention
• 0-29:   Critical security flaws

**Next Steps:**
1. Run: `refactory analyze your_code.py --focus security`
2. Review detailed security recommendations
3. Implement suggested fixes based on priority
4. Re-analyze to verify improvements
""")


def show_security_patterns():
    """Show examples of security patterns the agent can detect."""
    
    print("\n🔍 Security Patterns Detected")
    print("=" * 30)
    
    patterns = {
        "SQL Injection": [
            "cursor.execute(f\"SELECT * FROM users WHERE id = {user_id}\")",
            "query = \"SELECT * FROM users WHERE name = '%s'\" % username"
        ],
        "Hardcoded Secrets": [
            "API_KEY = 'sk-1234567890abcdef'",
            "password = 'super_secret_password_123'"
        ],
        "Command Injection": [
            "os.system(f'rm {filename}')",
            "subprocess.run(f'ping {host}', shell=True)"
        ],
        "Weak Cryptography": [
            "hashlib.md5(password.encode()).hexdigest()",
            "random.random()  # for security tokens"
        ],
        "Insecure Deserialization": [
            "pickle.loads(user_data)",
            "eval(user_expression)"
        ]
    }
    
    for category, examples in patterns.items():
        print(f"\n🚨 {category}:")
        for example in examples:
            print(f"   ❌ {example}")


if __name__ == "__main__":
    # Run the security demonstration
    asyncio.run(analyze_security_examples())
    show_security_patterns()
    
    print("\n🚀 Try analyzing your own code:")
    print("   refactory analyze your_file.py --format detailed")
    print("   refactory analyze your_project/ --focus security")
