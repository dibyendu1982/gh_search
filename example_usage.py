#!/usr/bin/env python3
"""
Example usage of the GitHub Repository Search Tool

This demonstrates how to use the GitHubRepoSearcher class programmatically.
"""

import os
from github_repo_search import GitHubRepoSearcher


def main():
    # Get GitHub token from environment variable
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Please set the GITHUB_TOKEN environment variable")
        return
    
    # Define strings to search for
    search_strings = [
        'python:3.8',
        'python = ^3.8', 
        "python3.8",
    ]
    
    # Define patterns to ignore (file types and paths)
    ignore_patterns = [
        "md",           # Ignore markdown files
        "json",         # Ignore JSON files
        ".circleci"    # Ignore .circleci folder
    ]
    
    print("Starting search for configuration-related strings in Vacasa repositories...")
    print(f"Search terms: {search_strings}")
    print(f"Ignoring patterns: {ignore_patterns}")
    print("=" * 60)
    
    # Initialize the searcher with ignore patterns
    searcher = GitHubRepoSearcher(token, ignore_patterns)
    
    # Perform the search
    results = searcher.search_strings_in_repos(search_strings)
    
    # Display results
    searcher.display_results(results)
    
    # Additional processing of results
    if results:
        print("\n" + "=" * 60)
        print("SUMMARY BY STRING")
        print("=" * 60)
        
        # Count occurrences of each string
        string_counts = {}
        for repo_url, found_strings in results.items():
            for string in found_strings:
                string_counts[string] = string_counts.get(string, 0) + 1
        
        for string, count in sorted(string_counts.items()):
            print(f"'{string}' found in {count} repositories")


if __name__ == "__main__":
    main()