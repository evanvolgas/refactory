"""
Security Agent for the Refactory multi-agent code analysis system.

This agent focuses on security vulnerabilities, authentication issues,
input validation, and security best practices.
"""

from typing import List, Optional
from ..core.models import AgentType
from .base_agent import BaseCodeAgent


class SecurityAgent(BaseCodeAgent):
    """
    Security Agent specializing in vulnerability detection and security best practices.
    
    Key focus areas:
    - Input validation and sanitization
    - Authentication and authorization flaws
    - Injection vulnerabilities (SQL, XSS, Command, etc.)
    - Cryptographic issues and weak encryption
    - Hardcoded secrets and credentials
    - Insecure data handling and storage
    - Security configuration issues
    - Access control and privilege escalation
    """
    
    def __init__(self, model_name: Optional[str] = None):
        """Initialize the Security Agent."""
        super().__init__(AgentType.SECURITY, model_name)
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Security Agent."""
        return """
You are a Senior Security Engineer with 15+ years of experience in application security, 
penetration testing, and secure code review. You specialize in:

**Core Security Areas:**
- OWASP Top 10 vulnerabilities and mitigation strategies
- Input validation, sanitization, and encoding techniques
- Authentication, authorization, and session management
- Cryptographic implementations and key management
- Secure coding practices and defensive programming

**Vulnerability Detection:**
- SQL Injection, XSS, CSRF, and other injection attacks
- Insecure direct object references and broken access control
- Security misconfigurations and exposed sensitive data
- Insecure cryptographic storage and transmission
- Command injection and path traversal vulnerabilities

**Security Best Practices:**
- Principle of least privilege and defense in depth
- Secure error handling and logging practices
- Input validation at all trust boundaries
- Proper secret management and credential handling
- Secure communication protocols and data protection

**Analysis Guidelines:**
1. **Prioritize Critical Vulnerabilities**: Focus on exploitable security flaws first
2. **Consider Attack Vectors**: Think like an attacker - how could this be exploited?
3. **Validate Input Handling**: Check all user inputs, file uploads, and external data
4. **Review Authentication**: Examine login, session, and access control mechanisms
5. **Check Cryptography**: Verify proper use of encryption, hashing, and random generation
6. **Identify Secrets**: Look for hardcoded passwords, API keys, and sensitive data
7. **Assess Error Handling**: Ensure errors don't leak sensitive information
8. **Evaluate Dependencies**: Consider security of third-party libraries and components

**Scoring Criteria:**
- 90-100: Excellent security posture with comprehensive protections
- 70-89: Good security with minor issues or missing best practices
- 50-69: Moderate security with several vulnerabilities or weak practices
- 30-49: Poor security with significant vulnerabilities requiring immediate attention
- 0-29: Critical security flaws that pose immediate risk to the application

**Output Requirements:**
- Identify specific security vulnerabilities with CVE references when applicable
- Provide clear exploitation scenarios and impact assessments
- Suggest concrete remediation steps with code examples
- Prioritize fixes based on risk level and exploitability
- Include references to security standards (OWASP, NIST, etc.)

Focus on actionable security improvements that developers can implement immediately.
Be thorough but practical - security should enhance, not hinder, development productivity.
"""
    
    def _get_domain_areas(self) -> List[str]:
        """
        Get the domain areas this agent scores.
        
        Returns:
            List of security domain area names
        """
        return [
            "input_validation",
            "authentication_authorization", 
            "injection_vulnerabilities",
            "cryptographic_security",
            "secret_management",
            "data_protection",
            "error_handling",
            "dependency_security"
        ]
    
    def _get_focus_description(self) -> str:
        """
        Get a description of what this agent focuses on.
        
        Returns:
            Description of the agent's security focus areas
        """
        return """security vulnerabilities, input validation, authentication flaws, 
injection attacks, cryptographic issues, hardcoded secrets, insecure data handling, 
and security best practices compliance"""


# Security patterns and common vulnerabilities to detect
SECURITY_PATTERNS = {
    "sql_injection": [
        r"execute\s*\(\s*[\"'].*%.*[\"']\s*%",  # String formatting in SQL
        r"cursor\.execute\s*\(\s*f[\"']",        # f-strings in SQL
        r"\.format\s*\(\s*\)\s*\)",              # .format() in SQL queries
    ],
    
    "hardcoded_secrets": [
        r"password\s*=\s*[\"'][^\"']{8,}[\"']",   # Hardcoded passwords
        r"api_key\s*=\s*[\"'][^\"']{20,}[\"']",   # API keys
        r"secret\s*=\s*[\"'][^\"']{16,}[\"']",    # Secret keys
        r"token\s*=\s*[\"'][^\"']{20,}[\"']",     # Access tokens
    ],
    
    "command_injection": [
        r"os\.system\s*\(\s*.*\+",               # Command concatenation
        r"subprocess\.\w+\s*\(\s*.*\+",          # Subprocess with concatenation
        r"shell=True.*\+",                       # Shell=True with concatenation
    ],
    
    "path_traversal": [
        r"open\s*\(\s*.*\+.*[\"']\.\./",         # Path traversal in file operations
        r"os\.path\.join\s*\(\s*.*input",        # User input in path joins
    ],
    
    "weak_crypto": [
        r"hashlib\.md5\s*\(",                    # Weak MD5 hashing
        r"hashlib\.sha1\s*\(",                   # Weak SHA1 hashing
        r"random\.random\s*\(",                  # Weak random for security
    ],
    
    "insecure_deserialization": [
        r"pickle\.loads?\s*\(",                  # Pickle deserialization
        r"yaml\.load\s*\(",                      # Unsafe YAML loading
        r"eval\s*\(",                            # Code evaluation
        r"exec\s*\(",                            # Code execution
    ]
}
