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

def setup_git_config():
    """Set up Git configuration"""
    print("Setting up Git configuration...")
    try:
        # Check if git config exists
        run_command('git config user.name "Bitcoin Bot"')
        run_command('git config user.email "bot@example.com"')
        print("Git configuration completed")
        return True
    except Exception as e:
        print(f"Error setting up git config: {str(e)}")
        return False

def sync_repository(repo_url=None, branch='main'):
    """Sync local repository with GitHub"""
    if not repo_url:
        # Default to the Bitcoin bot Lambda repository
        repo_url = "https://github.com/foozy74/bitcoinbot-lambda.git"

    print("Starting repository synchronization...")

    # Set up git configuration
    if not setup_git_config():
        print("Failed to set up git configuration")
        return False

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

    # Add all files
    print("Adding files to repository...")
    run_command('git add .')

    # Commit changes
    print("Committing changes...")
    try:
        run_command('git commit -m "Initial commit: Lambda implementation of Bitcoin Trading Bot"')
    except subprocess.CalledProcessError:
        print("No changes to commit")

    # Push to remote
    print("Pushing to remote repository...")
    print("\nIMPORTANT: To push to GitHub, you need to:")
    print("1. Create the repository on GitHub first")
    print("2. Use a personal access token for authentication")
    print("3. Set the token as an environment variable:")
    print("   export GITHUB_TOKEN=your_token_here\n")

    try:
        # Check if we have a token
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            print("ERROR: GITHUB_TOKEN environment variable not set")
            print("Please set up your GitHub token and try again")
            return False

        # Use token in remote URL
        token_url = f"https://{github_token}@github.com/foozy74/bitcoinbot-lambda.git"
        run_command(f'git remote set-url origin {token_url}')

        try:
            run_command(f'git push -u origin {branch}')
            print("Successfully synchronized repository!")
        except subprocess.CalledProcessError as e:
            if "remote repository is empty" in str(e.stderr):
                run_command(f'git push -u origin {branch}')
                print("Successfully synchronized repository!")
            else:
                raise
    except Exception as e:
        print(f"Error pushing to repository: {str(e)}")
        return False

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sync Bitcoin Trading Bot Lambda repository')
    parser.add_argument('--repo', help='GitHub repository URL')
    parser.add_argument('--branch', default='main', help='Branch to sync (default: main)')

    args = parser.parse_args()
    sync_repository(args.repo, args.branch)