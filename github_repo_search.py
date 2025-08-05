#!/usr/bin/env python3
"""
GitHub Repository Search Script

This script searches for specific strings across all repositories in the my-org organization
and returns the URLs of repositories where the strings are found.

Requirements:
- GitHub personal access token
- PyGithub library (pip install PyGithub)

Usage:
    python github_repo_search.py --strings "search_term1" "search_term2"
    python github_repo_search.py --strings "search_term1" --ignore "md" "json" ".circleci"
"""

import os
import sys
import time
from typing import List, Set, Dict
from github import Github, GithubException
import argparse


class GitHubRepoSearcher:
    def __init__(self, token: str, ignore_patterns: List[str] = None):
        """
        Initialize the GitHub searcher with authentication token.
        
        Args:
            token (str): GitHub personal access token
            ignore_patterns (List[str]): List of patterns to ignore (file extensions, paths, etc.)
        """
        self.github = Github(token)
        self.org_name = "my-org"
        self.ignore_patterns = ignore_patterns or []
        
    def _build_ignore_query(self) -> str:
        """
        Build the ignore query string from ignore patterns.
        
        Returns:
            str: Query string with exclusions
        """
        ignore_query = ""
        for pattern in self.ignore_patterns:
            pattern = pattern.strip()
            if not pattern:
                continue
                
            # Handle file extensions (e.g., "md", ".md", "*.md")
            if pattern.startswith('*.') or pattern.startswith('.'):
                ext = pattern.lstrip('*.')
                ignore_query += f' -extension:{ext}'
            elif '.' not in pattern and not pattern.startswith('/'):
                # Assume it's a file extension without dot
                ignore_query += f' -extension:{pattern}'
            else:
                # Handle paths and folders
                ignore_query += f' -path:{pattern}'
        
        return ignore_query
        
    def get_organization_repos(self) -> List:
        """
        Get all repositories from the my-org organization.
        
        Returns:
            List of repository objects
        """
        try:
            org = self.github.get_organization(self.org_name)
            repos = list(org.get_repos())
            print(f"Found {len(repos)} repositories in {self.org_name} organization")
            return repos
        except GithubException as e:
            print(f"Error accessing organization {self.org_name}: {e}")
            return []
    
    def search_string_in_repo(self, repo, search_string: str) -> bool:
        """
        Search for a specific string within a repository using GitHub's search API.
        
        Args:
            repo: Repository object
            search_string (str): String to search for
            
        Returns:
            bool: True if string is found, False otherwise
        """
        try:
            # Use GitHub's code search API with ignore patterns
            ignore_query = self._build_ignore_query()
            query = f'"{search_string}" repo:{repo.full_name}{ignore_query}'
            search_results = self.github.search_code(query)
            
            # Check if any results were found
            return search_results.totalCount > 0
            
        except GithubException as e:
            if e.status == 403:
                print(f"Rate limit exceeded or search not available for {repo.name}")
                # Wait a bit and try again
                time.sleep(60)
                return False
            elif e.status == 422:
                # Repository might be empty or search not available
                print(f"Search not available for repository {repo.name}")
                return False
            else:
                print(f"Error searching in {repo.name}: {e}")
                return False
        except Exception as e:
            print(f"Unexpected error searching in {repo.name}: {e}")
            return False
    
    def search_strings_in_repos(self, search_strings: List[str]) -> Dict[str, Set[str]]:
        """
        Search for multiple strings across all repositories in the organization.
        
        Args:
            search_strings (List[str]): List of strings to search for
            
        Returns:
            Dict[str, Set[str]]: Dictionary mapping repo URLs to found strings
        """
        repos = self.get_organization_repos()
        if not repos:
            return {}
        
        results = {}
        
        for i, repo in enumerate(repos, 1):
            print(f"Searching repository {i}/{len(repos)}: {repo.name}")
            
            found_strings = set()
            
            for search_string in search_strings:
                print(f"  Searching for: '{search_string}'")
                
                if self.search_string_in_repo(repo, search_string):
                    found_strings.add(search_string)
                    print(f"    ✓ Found '{search_string}' in {repo.name}")
                
                # Add a small delay to avoid hitting rate limits
                time.sleep(1)
            
            if found_strings:
                results[repo.html_url] = found_strings
            
            print(f"  Completed {repo.name} - Found {len(found_strings)} strings")
            print("-" * 50)
        
        return results
    
    def display_results(self, results: Dict[str, Set[str]]):
        """
        Display the search results in a formatted way.
        
        Args:
            results (Dict[str, Set[str]]): Search results
        """
        if not results:
            print("No repositories found containing the specified strings.")
            return
        
        print("\n" + "=" * 80)
        print("SEARCH RESULTS")
        print("=" * 80)
        
        for repo_url, found_strings in results.items():
            print(f"\nRepository: {repo_url}")
            print(f"Found strings: {', '.join(sorted(found_strings))}")
        
        print(f"\nTotal repositories with matches: {len(results)}")


def main():
    parser = argparse.ArgumentParser(description="Search for strings in my-org GitHub repositories")
    parser.add_argument("--token", help="GitHub personal access token (or set GITHUB_TOKEN env var)")
    parser.add_argument("--strings", nargs="+", required=True, 
                       help="Strings to search for (space-separated)")
    parser.add_argument("--ignore", nargs="*", default=[], 
                       help="Patterns to ignore (file extensions like 'md' 'json', or paths like '.circleci')")
    
    args = parser.parse_args()
    
    # Get GitHub token
    token = args.token or os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GitHub token is required. Set GITHUB_TOKEN environment variable or use --token")
        print("To create a token: https://github.com/settings/tokens")
        sys.exit(1)
    
    # Get search strings and ignore patterns
    search_strings = args.strings
    ignore_patterns = args.ignore
    
    print(f"Searching for strings: {search_strings}")
    print("Organization: my-org")
    if ignore_patterns:
        print(f"Ignoring patterns: {ignore_patterns}")
    print("=" * 50)
    
    try:
        searcher = GitHubRepoSearcher(token, ignore_patterns)
        results = searcher.search_strings_in_repos(search_strings)
        searcher.display_results(results)
        
    except KeyboardInterrupt:
        print("\nSearch interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()