#!/usr/bin/env python3
"""
Example of inefficient Python code with various performance issues.

This file demonstrates common performance anti-patterns that the Performance Agent
should detect and suggest optimizations for.

WARNING: This code contains intentional performance issues.
DO NOT use any of these patterns in production code!
"""

import time
import requests
import threading
from typing import List, Dict, Any


# Performance Issue #1: Inefficient nested loops (O(n²) complexity)
def find_duplicates_slow(numbers: List[int]) -> List[int]:
    """Find duplicates using nested loops - O(n²) complexity."""
    duplicates = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j] and numbers[i] not in duplicates:
                duplicates.append(numbers[i])
    return duplicates


def matrix_multiply_naive(matrix_a: List[List[int]], matrix_b: List[List[int]]) -> List[List[int]]:
    """Naive matrix multiplication - O(n³) complexity."""
    rows_a, cols_a = len(matrix_a), len(matrix_a[0])
    rows_b, cols_b = len(matrix_b), len(matrix_b[0])
    
    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]
    
    # Triple nested loop - very inefficient for large matrices
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += matrix_a[i][k] * matrix_b[k][j]
    
    return result


# Performance Issue #2: Inefficient data structure usage
def count_items_slow(items: List[str]) -> Dict[str, int]:
    """Count items using inefficient list operations."""
    counts = {}
    unique_items = []
    
    # Inefficient: using 'in' operator on list repeatedly
    for item in items:
        if item not in unique_items:
            unique_items.append(item)
    
    # Inefficient: nested loop to count occurrences
    for unique_item in unique_items:
        count = 0
        for item in items:
            if item == unique_item:
                count += 1
        counts[unique_item] = count
    
    return counts


def search_in_list(data: List[int], target: int) -> bool:
    """Search using inefficient linear search when better options exist."""
    # Inefficient: linear search on potentially sorted data
    for item in data:
        if item == target:
            return True
    return False


# Performance Issue #3: Memory inefficiency
def process_large_dataset(data: List[int]) -> List[int]:
    """Process data with unnecessary memory allocations."""
    # Inefficient: creating multiple intermediate lists
    step1 = [x * 2 for x in data]
    step2 = [x + 1 for x in step1]
    step3 = [x ** 2 for x in step2]
    
    # Inefficient: unnecessary copying
    result = step3.copy()
    final_result = result.copy()
    
    return final_result


def concatenate_strings_slow(strings: List[str]) -> str:
    """Concatenate strings inefficiently."""
    result = ""
    # Inefficient: string concatenation in loop creates new objects
    for s in strings:
        result = result + s + " "
    return result.strip()


# Performance Issue #4: Blocking I/O operations
def fetch_urls_synchronously(urls: List[str]) -> List[str]:
    """Fetch URLs synchronously - blocking operations."""
    results = []
    for url in urls:
        try:
            # Blocking HTTP request
            response = requests.get(url, timeout=5)
            results.append(response.text)
            # Blocking sleep
            time.sleep(0.1)
        except Exception as e:
            results.append(f"Error: {e}")
    return results


def read_files_blocking(filenames: List[str]) -> List[str]:
    """Read files with blocking I/O."""
    contents = []
    for filename in filenames:
        # File not opened with context manager - potential resource leak
        file = open(filename, 'r')
        content = file.read()  # Blocking read
        contents.append(content)
        file.close()
    return contents


# Performance Issue #5: Missing caching for expensive operations
def fibonacci_no_cache(n: int) -> int:
    """Calculate Fibonacci without memoization - exponential complexity."""
    if n <= 1:
        return n
    # Inefficient: recalculating same values repeatedly
    return fibonacci_no_cache(n - 1) + fibonacci_no_cache(n - 2)


def expensive_calculation(x: int, y: int) -> float:
    """Expensive calculation that could benefit from caching."""
    # Simulate expensive computation
    time.sleep(0.01)
    result = 0
    for i in range(1000):
        result += (x * i + y) ** 0.5
    return result


def process_data_no_cache(data: List[int]) -> List[float]:
    """Process data without caching repeated calculations."""
    results = []
    for item in data:
        # Same expensive calculation might be repeated for same values
        result = expensive_calculation(item, item * 2)
        results.append(result)
    return results


# Performance Issue #6: Poor resource management
def create_threads_poorly(tasks: List[Any]) -> None:
    """Create threads without proper management."""
    threads = []
    for task in tasks:
        # Thread created but never joined - resource leak
        thread = threading.Thread(target=lambda: print(f"Processing {task}"))
        thread.start()
        threads.append(thread)
    # Missing: thread.join() calls


def database_queries_inefficient(user_ids: List[int]) -> List[Dict]:
    """Simulate inefficient database queries."""
    results = []
    
    # Inefficient: N+1 query problem simulation
    for user_id in user_ids:
        # Each iteration makes a separate "query"
        user_data = {"id": user_id, "name": f"User {user_id}"}
        
        # Another query for each user
        user_posts = [f"Post {i} by User {user_id}" for i in range(3)]
        user_data["posts"] = user_posts
        
        results.append(user_data)
    
    return results


# Performance Issue #7: Inefficient algorithms
def sort_bubble(arr: List[int]) -> List[int]:
    """Bubble sort - O(n²) when better algorithms exist."""
    n = len(arr)
    arr = arr.copy()  # Unnecessary copy
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    
    return arr


def find_max_inefficient(numbers: List[int]) -> int:
    """Find maximum using inefficient approach."""
    # Inefficient: sorting entire list just to find max
    sorted_numbers = sorted(numbers)
    return sorted_numbers[-1]


# Performance Issue #8: Unnecessary computations in loops
def calculate_averages_slow(data: List[List[int]]) -> List[float]:
    """Calculate averages with unnecessary repeated computations."""
    averages = []
    
    for row in data:
        total = 0
        count = 0
        
        # Inefficient: recalculating len() in each iteration
        for i in range(len(row)):
            total += row[i]
            count += 1
            
        # Could use len(row) directly instead of counting
        average = total / count if count > 0 else 0
        averages.append(average)
    
    return averages


def main():
    """Demonstrate performance issues."""
    # Large dataset for testing
    large_list = list(range(1000))
    
    print("Running performance-inefficient operations...")
    
    # This will be slow due to O(n²) complexity
    duplicates = find_duplicates_slow(large_list + large_list[:100])
    print(f"Found {len(duplicates)} duplicates")
    
    # This will be slow due to inefficient string operations
    strings = [f"String {i}" for i in range(100)]
    concatenated = concatenate_strings_slow(strings)
    print(f"Concatenated string length: {len(concatenated)}")
    
    # This will be slow due to lack of caching
    fib_result = fibonacci_no_cache(30)
    print(f"Fibonacci(30) = {fib_result}")


if __name__ == "__main__":
    main()
