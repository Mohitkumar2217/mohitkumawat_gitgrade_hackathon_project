#!/usr/bin/env python3
"""
GitHub Repository Analyzer (Refactored)
-------------------------------------
Evaluates a public GitHub repository and produces:
- Score (0–100)
- Level (Beginner / Intermediate / Advanced)
- Summary
- Personalized Roadmap

Robust features:
- GitHub API analysis
- Graceful error handling
- Network-safe design (ready for clone fallback)

Run:
  python repo_analyzer.py <github_repo_url>
"""

import os
import sys
import re
import requests
from typing import List, Tuple

# ===================== CONFIG =====================

GITHUB_API = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
TIMEOUT = 10

# ===================== UTILITIES =====================

def parse_repo(url: str) -> Tuple[str, str]:
    url = url.strip().replace(".git", "")
    match = re.search(r"github.com/([^/]+)/([^/]+)", url)
    if not match:
        raise ValueError("Invalid GitHub repository URL")
    return match.group(1), match.group(2)


def gh_get(endpoint: str):
    try:
        r = requests.get(
            f"{GITHUB_API}{endpoint}",
            headers=HEADERS,
            timeout=TIMEOUT
        )
        if r.status_code == 404:
            raise RuntimeError("Repository not found or private")
        if r.status_code == 403:
            raise RuntimeError("GitHub API rate limit exceeded")
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectTimeout:
        raise RuntimeError("GitHub API timed out (network/firewall issue)")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"GitHub API error: {e}")

# ===================== ANALYSIS =====================

def fetch_repo_data(owner: str, repo: str):
    repo_info = gh_get(f"/repos/{owner}/{repo}")
    contents = gh_get(f"/repos/{owner}/{repo}/contents")
    commits = gh_get(f"/repos/{owner}/{repo}/commits?per_page=100")
    languages = gh_get(f"/repos/{owner}/{repo}/languages")
    return repo_info, contents, commits, languages


def analyze_structure(contents: List[dict]):
    files, folders = 0, 0
    has_tests = False
    for item in contents:
        if item["type"] == "file":
            files += 1
            if "test" in item["name"].lower():
                has_tests = True
        elif item["type"] == "dir":
            folders += 1
            if item["name"].lower() in {"test", "tests", "__tests__"}:
                has_tests = True
    return files, folders, has_tests


def has_readme(contents: List[dict]) -> bool:
    return any(item["name"].lower() == "readme.md" for item in contents)


def analyze_commits(commits: List[dict]):
    total = len(commits)
    consistency = min(1.0, total / 30)  # heuristic
    return total, consistency


def language_score(languages: dict) -> float:
    return min(1.0, len(languages) / 3)

# ===================== SCORING =====================

def calculate_score(files: int, readme: bool, tests: bool,
                    commit_consistency: float, lang_score: float) -> float:
    score = 0.0
    score += min(files / 10, 1) * 20        # structure
    score += readme * 15                    # docs
    score += tests * 20                     # testing
    score += commit_consistency * 20        # commits
    score += lang_score * 25                # tech stack
    return round(score, 2)


def level(score: float) -> str:
    if score < 40:
        return "Beginner"
    elif score < 70:
        return "Intermediate"
    return "Advanced"

# ===================== ROADMAP =====================

def generate_roadmap(readme: bool, tests: bool, commits: int, score: float):
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
    steps.append("Add CI/CD using GitHub Actions")
    return steps

# ===================== OUTPUT =====================

def print_report(repo_name: str, score: float, files: int,
                 readme: bool, tests: bool, roadmap: List[str]):

    print("\n===== Repository Evaluation =====")
    print(f"Project       : {repo_name}")
    print(f"Score         : {score}/100")
    print(f"Level         : {level(score)}")

    print("\n--- Summary ---")
    summary = "Clean structure" if files > 5 else "Small or early-stage project"
    summary += ", documentation present" if readme else ", documentation missing"
    summary += ", tests included" if tests else ", tests missing"
    print(summary)

    print("\n--- Personalized Roadmap ---")
    for i, step in enumerate(roadmap, 1):
        print(f"{i}. {step}")

# ===================== MAIN =====================

def main():
    if len(sys.argv) != 2:
        print("Usage: python repo_analyzer.py <github_repo_url>")
        sys.exit(1)

    try:
        owner, repo = parse_repo(sys.argv[1])
        repo_info, contents, commits, languages = fetch_repo_data(owner, repo)

        files, folders, tests = analyze_structure(contents)
        readme = has_readme(contents)
        total_commits, consistency = analyze_commits(commits)
        lang_score = language_score(languages)

        score = calculate_score(files, readme, tests, consistency, lang_score)
        roadmap = generate_roadmap(readme, tests, total_commits, score)

        print_report(repo_info["name"], score, files, readme, tests, roadmap)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()