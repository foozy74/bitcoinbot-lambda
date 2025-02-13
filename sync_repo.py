import os
import subprocess
import argparse
from pathlib import Path

def run_command(command):
    """Execute a shell command and return output"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.cmd}")
        print(f"Error output: {e.stderr}")
        raise

def sync_repository(repo_url=None, branch='main'):
    """Sync local repository with GitHub"""
    if not repo_url:
        # Default to the Bitcoin bot repository
        repo_url = "https://github.com/foozy74/Bitcoinbot.git"
    
    print("Starting repository synchronization...")
    
    # Check if git is initialized
    if not Path('.git').exists():
        print("Initializing git repository...")
        run_command('git init')
    
    # Check if remote exists
    try:
        current_remote = run_command('git remote get-url origin')
    except subprocess.CalledProcessError:
        current_remote = None
    
    if current_remote is None or current_remote.strip() != repo_url:
        if current_remote:
            print("Updating remote URL...")
            run_command('git remote remove origin')
        run_command(f'git remote add origin {repo_url}')
    
    # Fetch latest changes
    print("Fetching latest changes...")
    run_command('git fetch origin')
    
    # Check current branch
    try:
        current_branch = run_command('git branch --show-current').strip()
    except subprocess.CalledProcessError:
        current_branch = None
    
    if current_branch != branch:
        print(f"Switching to {branch} branch...")
        try:
            run_command(f'git checkout {branch}')
        except subprocess.CalledProcessError:
            run_command(f'git checkout -b {branch}')
            run_command(f'git branch --set-upstream-to=origin/{branch} {branch}')
    
    # Pull latest changes
    print("Pulling latest changes...")
    try:
        run_command('git pull origin main')
        print("Successfully synchronized repository!")
    except subprocess.CalledProcessError as e:
        if "resolve conflicts" in str(e.stderr):
            print("Merge conflicts detected. Please resolve conflicts manually.")
            return False
        raise
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sync Bitcoin Trading Bot repository')
    parser.add_argument('--repo', help='GitHub repository URL')
    parser.add_argument('--branch', default='main', help='Branch to sync (default: main)')
    
    args = parser.parse_args()
    sync_repository(args.repo, args.branch)
