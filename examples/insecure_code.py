#!/usr/bin/env python3
"""
Example of insecure Python code with various security vulnerabilities.

This file demonstrates common security anti-patterns that the Security Agent
should detect and flag for remediation.

WARNING: This code contains intentional security vulnerabilities.
DO NOT use any of these patterns in production code!
"""

import os
import sqlite3
import subprocess
import hashlib
import pickle
import yaml
import random
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Security Issue #1: Hardcoded secrets
API_KEY = "sk-1234567890abcdef1234567890abcdef"
DATABASE_PASSWORD = "super_secret_password_123"
JWT_SECRET = "my-jwt-secret-key-that-should-not-be-hardcoded"

# Security Issue #2: Weak cryptographic practices
def hash_password(password):
    """Hash password using weak MD5 algorithm."""
    return hashlib.md5(password.encode()).hexdigest()

def generate_session_token():
    """Generate session token using weak random."""
    return str(random.random())

# Security Issue #3: SQL Injection vulnerabilities
def get_user_by_id(user_id):
    """Retrieve user data - vulnerable to SQL injection."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Vulnerable: Direct string formatting
    query = "SELECT * FROM users WHERE id = '%s'" % user_id
    cursor.execute(query)
    
    result = cursor.fetchone()
    conn.close()
    return result

def search_users(search_term):
    """Search users - another SQL injection vulnerability."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Vulnerable: f-string interpolation
    query = f"SELECT * FROM users WHERE name LIKE '%{search_term}%'"
    cursor.execute(query)
    
    results = cursor.fetchall()
    conn.close()
    return results

# Security Issue #4: Command injection
def backup_database(backup_name):
    """Backup database - vulnerable to command injection."""
    # Vulnerable: Shell command with user input
    command = f"mysqldump -u root -p{DATABASE_PASSWORD} mydb > {backup_name}.sql"
    os.system(command)

def process_file(filename):
    """Process uploaded file - command injection risk."""
    # Vulnerable: subprocess with shell=True and user input
    result = subprocess.run(f"file {filename}", shell=True, capture_output=True)
    return result.stdout

# Security Issue #5: Path traversal
def read_user_file(filename):
    """Read user file - vulnerable to path traversal."""
    # Vulnerable: No path validation
    file_path = "/var/uploads/" + filename
    with open(file_path, 'r') as f:
        return f.read()

def serve_static_file(file_path):
    """Serve static file - path traversal vulnerability."""
    # Vulnerable: Direct path concatenation
    full_path = os.path.join("/var/www/static", file_path)
    with open(full_path, 'rb') as f:
        return f.read()

# Security Issue #6: Insecure deserialization
def load_user_preferences(data):
    """Load user preferences - pickle deserialization vulnerability."""
    # Vulnerable: Pickle can execute arbitrary code
    return pickle.loads(data)

def parse_config(config_data):
    """Parse YAML config - unsafe loading."""
    # Vulnerable: yaml.load can execute arbitrary code
    return yaml.load(config_data)

# Security Issue #7: Code injection
def evaluate_expression(expression):
    """Evaluate mathematical expression - code injection."""
    # Vulnerable: eval can execute arbitrary code
    return eval(expression)

def execute_user_code(code):
    """Execute user-provided code - extremely dangerous."""
    # Vulnerable: exec allows arbitrary code execution
    exec(code)

# Security Issue #8: Flask web vulnerabilities
@app.route('/user/<user_id>')
def get_user(user_id):
    """Get user endpoint - multiple vulnerabilities."""
    # SQL injection via get_user_by_id
    user = get_user_by_id(user_id)
    
    if user:
        # XSS vulnerability: Direct template rendering
        template = f"<h1>Welcome {user[1]}!</h1><p>Email: {user[2]}</p>"
        return render_template_string(template)
    else:
        return "User not found", 404

@app.route('/search')
def search():
    """Search endpoint - XSS and SQL injection."""
    query = request.args.get('q', '')
    
    # SQL injection via search_users
    results = search_users(query)
    
    # XSS vulnerability: Unescaped user input
    html = f"<h2>Search results for: {query}</h2><ul>"
    for user in results:
        html += f"<li>{user[1]} - {user[2]}</li>"
    html += "</ul>"
    
    return html

@app.route('/backup', methods=['POST'])
def create_backup():
    """Create backup endpoint - command injection."""
    backup_name = request.form.get('name', 'default')
    
    # Command injection via backup_database
    backup_database(backup_name)
    
    return f"Backup {backup_name} created successfully"

# Security Issue #9: Insecure error handling
def divide_numbers(a, b):
    """Divide numbers with insecure error handling."""
    try:
        result = a / b
        return result
    except Exception as e:
        # Vulnerable: Exposing internal error details
        return f"Error occurred: {str(e)}, Database password: {DATABASE_PASSWORD}"

# Security Issue #10: Insecure session management
user_sessions = {}

def create_session(user_id):
    """Create user session with weak token."""
    # Vulnerable: Predictable session token
    session_token = f"session_{user_id}_{random.randint(1000, 9999)}"
    user_sessions[session_token] = user_id
    return session_token

def validate_session(token):
    """Validate session without proper checks."""
    # Vulnerable: No expiration, weak validation
    return user_sessions.get(token)

# Security Issue #11: Missing input validation
def update_user_profile(user_id, name, email, bio):
    """Update user profile without validation."""
    # Vulnerable: No input validation or sanitization
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Multiple vulnerabilities: SQL injection + no validation
    query = f"UPDATE users SET name='{name}', email='{email}', bio='{bio}' WHERE id={user_id}"
    cursor.execute(query)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Security Issue #12: Debug mode in production
    app.run(debug=True, host='0.0.0.0', port=5000)
