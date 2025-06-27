#!/usr/bin/env python3
"""
Git repository initialization and deployment script for CleanNet Shield
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=cwd
        )
        if result.returncode != 0:
            print(f"❌ Error running command: {command}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Exception running command: {command}")
        print(f"Error: {e}")
        return False

def check_git_installed():
    """Check if git is installed"""
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git is installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Git is not installed or not in PATH")
            return False
    except FileNotFoundError:
        print("❌ Git is not installed")
        return False

def initialize_git_repo():
    """Initialize git repository and prepare for deployment"""
    
    print("🚀 CleanNet Shield - Repository Deployment Script")
    print("=" * 50)
    
    # Check if git is installed
    if not check_git_installed():
        print("\n❌ Please install Git first:")
        print("   https://git-scm.com/download/win")
        return False
    
    # Get current directory
    project_dir = Path.cwd()
    print(f"📁 Project directory: {project_dir}")
    
    # Check if already a git repository
    if (project_dir / ".git").exists():
        print("⚠️  Git repository already exists")
        response = input("Continue anyway? (y/n): ").lower()
        if response != 'y':
            return False
    
    print("\n🔧 Initializing Git repository...")
    
    # Initialize git repository
    if not run_command("git init"):
        return False
    print("✅ Git repository initialized")
    
    # Configure git user if not set
    result = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
    if not result.stdout.strip():
        name = input("Enter your name for git commits: ")
        run_command(f'git config user.name "{name}"')
    
    result = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True)
    if not result.stdout.strip():
        email = input("Enter your email for git commits: ")
        run_command(f'git config user.email "{email}"')
    
    # Add all files
    print("\n📦 Adding files to repository...")
    if not run_command("git add ."):
        return False
    print("✅ Files added to staging area")
    
    # Create initial commit
    print("\n💾 Creating initial commit...")
    if not run_command('git commit -m "Initial commit: CleanNet Shield v2.0.0"'):
        return False
    print("✅ Initial commit created")
    
    # Check current branch and rename if necessary
    result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
    current_branch = result.stdout.strip()
    
    if current_branch != "main":
        print(f"\n🔄 Renaming branch from '{current_branch}' to 'main'...")
        if not run_command("git branch -M main"):
            return False
        print("✅ Branch renamed to 'main'")
    
    print("\n🎉 Git repository successfully initialized!")
    print("\n📋 Next steps:")
    print("1. Create a new repository on GitHub/GitLab")
    print("2. Copy the remote URL")
    print("3. Run the following commands:")
    print("   git remote add origin <YOUR_REPOSITORY_URL>")
    print("   git push -u origin main")
    
    # Ask if user wants to add remote now
    add_remote = input("\nDo you have a remote repository URL to add now? (y/n): ").lower()
    if add_remote == 'y':
        remote_url = input("Enter the remote repository URL: ").strip()
        if remote_url:
            print(f"\n🔗 Adding remote repository: {remote_url}")
            if run_command(f"git remote add origin {remote_url}"):
                print("✅ Remote repository added")
                
                # Ask if user wants to push now
                push_now = input("Push to remote repository now? (y/n): ").lower()
                if push_now == 'y':
                    print("\n⬆️  Pushing to remote repository...")
                    if run_command("git push -u origin main"):
                        print("✅ Successfully pushed to remote repository!")
                        print("🎉 CleanNet Shield is now deployed!")
                    else:
                        print("❌ Failed to push to remote repository")
                        print("You can try again later with: git push -u origin main")
    
    print("\n📊 Repository status:")
    run_command("git status")
    
    return True

def show_deployment_checklist():
    """Show final deployment checklist"""
    print("\n" + "=" * 50)
    print("📋 DEPLOYMENT CHECKLIST")
    print("=" * 50)
    
    checklist = [
        "✅ README.md created with project overview",
        "✅ .gitignore configured for Python project",
        "✅ LICENSE file added (MIT License)",
        "✅ CONTRIBUTING.md with contribution guidelines", 
        "✅ setup.py for Python package installation",
        "✅ RELEASE_NOTES.md with version information",
        "✅ Git repository initialized",
        "✅ Initial commit created",
        "⏳ Remote repository URL needed",
        "⏳ Push to remote repository",
    ]
    
    for item in checklist:
        print(f"  {item}")
    
    print("\n🚀 Your CleanNet Shield project is ready for deployment!")
    print("   Just add your remote repository and push!")

if __name__ == "__main__":
    try:
        if initialize_git_repo():
            show_deployment_checklist()
        else:
            print("\n❌ Repository initialization failed")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
