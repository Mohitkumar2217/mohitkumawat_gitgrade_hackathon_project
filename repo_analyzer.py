#!/usr/bin/env python3
"""
GitHub Repository Analyzer
-------------------------
Input  : Public GitHub Repository URL
Output : Score + Summary + Personalized Roadmap

How to run:
1. pip install requests radon pygments
2. python repo_analyzer.py https://github.com/username/repo

Optional:
- Set GITHUB_TOKEN env variable to avoid rate limits
"""

import os
import sys
import re
import math
import requests
from collections import defaultdict
from radon.complexity import cc_visit
from radon.metrics import mi_visit

GITHUB_API = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

# ---------------------- Utilities ----------------------

def parse_repo(url: str):
    match = re.search(r"github.com/([^/]+)/([^/]+)", url)
    if not match:
        raise ValueError("Invalid GitHub repository URL")
    return match.group(1), match.group(2)


def gh_get(endpoint):
    try:
        r = requests.get(
            f"{GITHUB_API}{endpoint}",
            headers=HEADERS,
            timeout=10
        )
        if r.status_code == 404:
            raise RuntimeError("Repository not found or private")
        if r.status_code == 403:
            raise RuntimeError("Rate limit exceeded or token invalid")
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectTimeout:
        raise RuntimeError("GitHub API timed out. Check internet or firewall.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"GitHub API error: {e}")


# ---------------------- Analysis ----------------------

def fetch_repo_data(owner, repo):
    repo_info = gh_get(f"/repos/{owner}/{repo}")
    contents = gh_get(f"/repos/{owner}/{repo}/contents")
    commits = gh_get(f"/repos/{owner}/{repo}/commits?per_page=100")
    return repo_info, contents, commits


def analyze_structure(contents):
    files = 0
    folders = 0
    has_tests = False
    for item in contents:
        if item['type'] == 'file':
            files += 1
            if 'test' in item['name'].lower():
                has_tests = True
        elif item['type'] == 'dir':
            folders += 1
            if item['name'].lower() in ['test', 'tests', '__tests__']:
                has_tests = True
    return files, folders, has_tests


def analyze_readme(contents):
    for item in contents:
        if item['name'].lower() == 'readme.md':
            return True
    return False


def analyze_commits(commits):
    total = len(commits)
    consistency = min(1.0, total / 30)  # heuristic
    return total, consistency


def language_score(languages):
    return min(1.0, len(languages) / 3)

# ---------------------- Scoring ----------------------

def calculate_score(structure, readme, tests, commits, lang_score):
    score = 0
    score += min(structure[0] / 10, 1) * 20
    score += readme * 15
    score += tests * 20
    score += commits[1] * 20
    score += lang_score * 25
    return round(score, 2)


def level(score):
    if score < 40:
        return "Beginner"
    elif score < 70:
        return "Intermediate"
    return "Advanced"

# ---------------------- Roadmap ----------------------

def roadmap(readme, tests, commits, score):
    steps = []
    if not readme:
        steps.append("Add a clear README.md with setup, usage, and screenshots")
    if not tests:
        steps.append("Introduce unit tests and basic test coverage")
    if commits < 10:
        steps.append("Commit more frequently with meaningful messages")
    if score < 70:
        steps.append("Refactor code for readability and modularity")
        steps.append("Apply linting and formatting tools")
    steps.append("Add CI/CD (GitHub Actions) for automated checks")
    return steps

# ---------------------- Main ----------------------

def main():
    if len(sys.argv) != 2:
        print("Usage: python repo_analyzer.py <github_repo_url>")
        sys.exit(1)

    owner, repo = parse_repo(sys.argv[1])
    repo_info, contents, commits = fetch_repo_data(owner, repo)

    files, folders, has_tests = analyze_structure(contents)
    has_readme = analyze_readme(contents)
    total_commits, commit_consistency = analyze_commits(commits)
    langs = gh_get(f"/repos/{owner}/{repo}/languages")

    score = calculate_score(
        (files, folders),
        has_readme,
        has_tests,
        (total_commits, commit_consistency),
        language_score(langs)
    )

    print("\n===== Repository Evaluation =====")
    print(f"Project       : {repo_info['name']}")
    print(f"Score         : {score}/100")
    print(f"Level         : {level(score)}")

    print("\n--- Summary ---")
    summary = "Clean structure" if files > 5 else "Small or incomplete project"
    summary += ", documentation present" if has_readme else ", documentation missing"
    summary += ", tests included" if has_tests else ", tests missing"
    print(summary)

    print("\n--- Personalized Roadmap ---")
    for i, step in enumerate(roadmap(has_readme, has_tests, total_commits, score), 1):
        print(f"{i}. {step}")


if __name__ == "__main__":
    main()
