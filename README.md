# GitHub Repository Search Tool

This Python script searches for specific strings across all repositories in the Vacasa GitHub organization and returns the URLs of repositories where the strings are found.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get a GitHub Personal Access Token:**
   - Go to https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Select the following scopes:
     - `public_repo` (for searching public repositories)
     - `repo` (if you need to search private repositories)
   - Copy the generated token

3. **Set your GitHub token:**
   ```bash
   export GITHUB_TOKEN="your_token_here"
   ```
   
   Or pass it directly to the script using the `--token` parameter.

## Usage

### Basic Usage
```bash
python github_repo_search.py --strings "search_term1" "search_term2"
```

### With Token Parameter
```bash
python github_repo_search.py --token "your_token_here" --strings "API_KEY" "database"
```

### Examples

Search for configuration-related terms:
```bash
python github_repo_search.py --strings "API_KEY" "DATABASE_URL" "SECRET_KEY"
```

Search for specific technology stacks:
```bash
python github_repo_search.py --strings "react" "django" "postgresql"
```

## Features

- ✅ Searches across all repositories in the Vacasa organization
- ✅ Uses GitHub's code search API for efficient searching
- ✅ Handles rate limiting and API errors gracefully
- ✅ Displays results with repository URLs and found strings
- ✅ Progress tracking during the search process

## Output

The script will display:
1. Progress information as it searches through repositories
2. A summary of results showing:
   - Repository URLs where strings were found
   - Which specific strings were found in each repository
   - Total count of repositories with matches

## Important Notes

- GitHub's search API has rate limits (10 searches per minute for authenticated requests)
- The script includes automatic delays to respect these limits
- Some repositories might not be searchable (empty repos, certain access restrictions)
- Large organizations with many repositories may take a while to search completely

## Troubleshooting

- **403 Error**: Usually indicates rate limiting. The script will wait and retry.
- **422 Error**: Repository might be empty or search not available for that repo.
- **Authentication Error**: Check that your GitHub token is valid and has the necessary permissions.