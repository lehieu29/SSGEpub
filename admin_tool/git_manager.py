"""
Git Manager - Quản lý Git operations
Xử lý add, commit, push và GitHub integration
"""

import os
import subprocess
import json
from typing import Dict, List, Optional
from pathlib import Path

class GitManager:
    def __init__(self, repo_path: str = None):
        """Initialize GitManager"""
        self.repo_path = repo_path or self._find_repo_path()
        self.github_token = None
        self.setup_git_config()
    
    def _find_repo_path(self) -> str:
        """Tìm đường dẫn repository"""
        current_dir = os.getcwd()
        
        # Check if we're in Google Colab
        if '/content' in current_dir:
            # Look for cloned repo in Colab
            possible_paths = [
                '/content/SSGEpub',
                '/content/ssg-epub',
                current_dir
            ]
            for path in possible_paths:
                if os.path.exists(os.path.join(path, '.git')):
                    return path
        
        # Local development - find git root
        while current_dir != '/':
            if os.path.exists(os.path.join(current_dir, '.git')):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        
        # Default fallback
        return os.getcwd()
    
    def setup_git_config(self):
        """Setup basic git configuration"""
        try:
            # Check if git is available
            result = subprocess.run(['git', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception("Git is not installed or not available")

            # Try to get config from Colab userdata first
            git_name = "Admin Bot"
            git_email = "admin@ssgepub.com"
            github_token = None

            # Check if we're in Colab and try to get userdata
            try:
                from google.colab import userdata
                git_name = userdata.get('GITHUB_USERNAME', 'Admin Bot')
                git_email = userdata.get('GITHUB_EMAIL', 'admin@ssgepub.com')
                github_token = userdata.get('GITHUB_TOKEN', None)
                print(f"✅ Loaded git config from Colab secrets: {git_name} <{git_email}>")
                if github_token:
                    self.github_token = github_token
                    print("✅ Loaded GitHub token from Colab secrets")
            except ImportError:
                # Not in Colab, use defaults
                pass
            except Exception as e:
                # Colab userdata not available, use defaults
                print(f"⚠️ Could not load from Colab secrets: {e}")

            # Set git config
            self._run_git_command(['config', '--global', 'user.name', git_name], check_error=False)
            self._run_git_command(['config', '--global', 'user.email', git_email], check_error=False)

            # Set safe directory for Google Colab
            if '/content' in os.getcwd():
                self._run_git_command(['config', '--global', '--add', 'safe.directory', self.repo_path], check_error=False)

        except Exception as e:
            print(f"Warning: Git setup failed: {e}")
    
    def configure_git(self, user_name: str, user_email: str, github_token: str = None):
        """Configure git user and GitHub token"""
        try:
            # Set user config
            self._run_git_command(['config', '--global', 'user.name', user_name])
            self._run_git_command(['config', '--global', 'user.email', user_email])
            
            # Store GitHub token
            if github_token:
                self.github_token = github_token
                self._setup_github_auth(github_token)
            
            return True
        except Exception as e:
            raise Exception(f"Failed to configure git: {e}")
    
    def _setup_github_auth(self, token: str):
        """Setup GitHub authentication"""
        try:
            # For HTTPS URLs, we'll use token in the URL
            # This is handled in the push operation
            self.github_token = token
            
            # Test authentication
            result = subprocess.run([
                'curl', '-H', f'Authorization: token {token}',
                'https://api.github.com/user'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                user_info = json.loads(result.stdout)
                print(f"GitHub authentication successful for user: {user_info.get('login', 'Unknown')}")
            else:
                print("Warning: GitHub token validation failed")
                
        except Exception as e:
            print(f"Warning: GitHub auth setup failed: {e}")
    
    def _run_git_command(self, args: List[str], check_error: bool = True) -> subprocess.CompletedProcess:
        """Run git command in repository directory"""
        try:
            cmd = ['git'] + args
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if check_error and result.returncode != 0:
                raise Exception(f"Git command failed: {' '.join(cmd)}\nError: {result.stderr}")
            
            return result
        except subprocess.TimeoutExpired:
            raise Exception(f"Git command timed out: {' '.join(args)}")
        except Exception as e:
            if check_error:
                raise Exception(f"Git command error: {e}")
            return None
    
    def get_repo_status(self) -> Dict:
        """Get repository status"""
        try:
            # Check if we're in a git repository
            result = self._run_git_command(['rev-parse', '--git-dir'])
            if result.returncode != 0:
                return {'error': 'Not a git repository'}
            
            # Get current branch
            branch_result = self._run_git_command(['branch', '--show-current'])
            current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else 'unknown'
            
            # Get status
            status_result = self._run_git_command(['status', '--porcelain'])
            has_changes = bool(status_result.stdout.strip())
            
            # Get last commit
            log_result = self._run_git_command(['log', '-1', '--pretty=format:%H|%s|%an|%ad', '--date=short'])
            last_commit = {}
            if log_result.returncode == 0 and log_result.stdout:
                parts = log_result.stdout.split('|')
                if len(parts) >= 4:
                    last_commit = {
                        'hash': parts[0][:8],
                        'message': parts[1],
                        'author': parts[2],
                        'date': parts[3]
                    }
            
            # Get remote URL
            remote_result = self._run_git_command(['remote', 'get-url', 'origin'], check_error=False)
            remote_url = remote_result.stdout.strip() if remote_result and remote_result.returncode == 0 else 'No remote'
            
            return {
                'current_branch': current_branch,
                'has_changes': has_changes,
                'last_commit': last_commit,
                'remote_url': remote_url,
                'repo_path': self.repo_path
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def add_file(self, filename: str) -> bool:
        """Add specific file to git"""
        try:
            self._run_git_command(['add', filename])
            return True
        except Exception as e:
            print(f"Error adding file {filename}: {e}")
            return False
    
    def add_all(self) -> bool:
        """Add all changes to git"""
        try:
            self._run_git_command(['add', '.'])
            return True
        except Exception as e:
            print(f"Error adding all files: {e}")
            return False
    
    def commit(self, message: str) -> bool:
        """Commit changes"""
        try:
            self._run_git_command(['commit', '-m', message])
            return True
        except Exception as e:
            print(f"Error committing: {e}")
            return False
    
    def push(self, branch: str = 'main') -> bool:
        """Push changes to remote repository"""
        try:
            if self.github_token:
                # Get remote URL and modify it to include token
                remote_result = self._run_git_command(['remote', 'get-url', 'origin'])
                if remote_result.returncode == 0:
                    remote_url = remote_result.stdout.strip()
                    
                    # Convert to authenticated URL
                    if remote_url.startswith('https://github.com/'):
                        auth_url = remote_url.replace('https://github.com/', f'https://{self.github_token}@github.com/')
                        
                        # Temporarily set the remote URL
                        self._run_git_command(['remote', 'set-url', 'origin', auth_url])
                        
                        try:
                            # Push
                            self._run_git_command(['push', 'origin', branch])
                            return True
                        finally:
                            # Restore original URL
                            self._run_git_command(['remote', 'set-url', 'origin', remote_url])
                    else:
                        # For SSH or other URLs, try direct push
                        self._run_git_command(['push', 'origin', branch])
                        return True
            else:
                # Try push without authentication (might work if SSH keys are set up)
                self._run_git_command(['push', 'origin', branch])
                return True
                
        except Exception as e:
            print(f"Error pushing: {e}")
            return False
    
    def add_commit_push(self, filename: str, message: str = None, branch: str = 'main') -> bool:
        """Add, commit and push a specific file"""
        try:
            if not message:
                message = f"Update {filename}"
            
            # Add file
            if not self.add_file(f"_epubs/{filename}"):
                return False
            
            # Commit
            if not self.commit(message):
                return False
            
            # Push
            if not self.push(branch):
                return False
            
            return True
            
        except Exception as e:
            print(f"Error in add_commit_push: {e}")
            return False
    
    def batch_commit_push(self, message: str, branch: str = 'main') -> bool:
        """Add all changes, commit and push"""
        try:
            # Add all changes
            if not self.add_all():
                return False
            
            # Commit
            if not self.commit(message):
                return False
            
            # Push
            if not self.push(branch):
                return False
            
            return True
            
        except Exception as e:
            print(f"Error in batch_commit_push: {e}")
            return False
    
    def pull(self, branch: str = 'main') -> bool:
        """Pull latest changes from remote"""
        try:
            self._run_git_command(['pull', 'origin', branch])
            return True
        except Exception as e:
            print(f"Error pulling: {e}")
            return False
    
    def create_branch(self, branch_name: str) -> bool:
        """Create and switch to new branch"""
        try:
            self._run_git_command(['checkout', '-b', branch_name])
            return True
        except Exception as e:
            print(f"Error creating branch {branch_name}: {e}")
            return False
    
    def switch_branch(self, branch_name: str) -> bool:
        """Switch to existing branch"""
        try:
            self._run_git_command(['checkout', branch_name])
            return True
        except Exception as e:
            print(f"Error switching to branch {branch_name}: {e}")
            return False
    
    def get_branches(self) -> List[str]:
        """Get list of branches"""
        try:
            result = self._run_git_command(['branch', '-a'])
            if result.returncode == 0:
                branches = []
                for line in result.stdout.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('*'):
                        # Remove 'remotes/origin/' prefix if present
                        branch = line.replace('remotes/origin/', '')
                        if branch not in branches:
                            branches.append(branch)
                return branches
        except Exception as e:
            print(f"Error getting branches: {e}")
        
        return []
    
    def trigger_github_build(self) -> bool:
        """Trigger GitHub Actions build (if configured)"""
        try:
            if not self.github_token:
                print("No GitHub token configured")
                return False
            
            # This would trigger a workflow dispatch if you have one configured
            # For Jekyll sites, usually just pushing triggers the build automatically
            print("GitHub build will be triggered automatically by the push")
            return True
            
        except Exception as e:
            print(f"Error triggering GitHub build: {e}")
            return False
