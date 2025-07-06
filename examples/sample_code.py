"""
Sample Python code for demonstrating Refactory analysis.

This file contains intentional code quality issues to showcase
the different types of problems the Architect Agent can identify.
"""

import os
import json
from typing import List


class UserManager:
    """Manages user data with various architectural issues."""
    
    def __init__(self, data_file):
        # Poor naming and doing too much in constructor
        self.df = data_file
        self.users = []
        
        # File I/O in constructor without error handling
        if os.path.exists(data_file):
            with open(data_file, 'r') as f:
                self.users = json.load(f)
    
    def add_user(self, name, email, age):
        """Add user with validation and saving mixed together."""
        # No input validation
        user = {
            "id": len(self.users) + 1,
            "name": name,
            "email": email,
            "age": age
        }
        
        self.users.append(user)
        
        # Side effect - saving in add method
        self.save_users()
        
        # Also sending email notification here (mixed responsibilities)
        print(f"Welcome email sent to {email}")
        
        return user
    
    def save_users(self):
        """Save users without proper error handling."""
        with open(self.df, 'w') as f:
            json.dump(self.users, f)
    
    def get_adult_users(self):
        """Get adult users with hardcoded age limit."""
        adults = []
        for user in self.users:
            if user["age"] >= 18:  # Magic number
                adults.append(user)
        return adults


def process_user_data(file_path, output_path):
    """Global function doing too many things."""
    
    # No input validation
    manager = UserManager(file_path)
    
    # Mixed logic - processing and formatting
    adults = manager.get_adult_users()
    
    # Hardcoded formatting logic
    report = {
        "total_users": len(manager.users),
        "adult_users": len(adults),
        "adult_percentage": len(adults) / len(manager.users) * 100 if manager.users else 0
    }
    
    # File I/O mixed with business logic
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    return report


# Global variable (poor practice)
DEFAULT_DATA_FILE = "users.json"


if __name__ == "__main__":
    # Poor command line handling
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python sample_code.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Direct execution without proper main function
    result = process_user_data(input_file, output_file)
    print(f"Report generated: {result}")
