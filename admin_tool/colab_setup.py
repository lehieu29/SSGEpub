"""
Google Colab Setup Script
Script để setup môi trường Google Colab cho SSG Epub Admin Tool
"""

import os
import subprocess
import sys
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    packages = [
        "streamlit>=1.28.0",
        "requests>=2.31.0",
        "PyYAML>=6.0",
        "pyngrok>=6.0.0"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")

def setup_ngrok():
    """Setup ngrok for public URL"""
    print("🌐 Setting up ngrok...")
    
    try:
        from pyngrok import ngrok
        
        # Get ngrok auth token from user
        auth_token = input("Enter your ngrok auth token (get from https://dashboard.ngrok.com/get-started/your-authtoken): ")
        
        if auth_token:
            ngrok.set_auth_token(auth_token)
            print("✅ Ngrok auth token set successfully")
        else:
            print("⚠️ No ngrok token provided. You can set it later.")
            
    except ImportError:
        print("❌ pyngrok not installed")
    except Exception as e:
        print(f"❌ Error setting up ngrok: {e}")

def clone_repository():
    """Clone the SSG Epub repository"""
    print("📂 Cloning repository...")
    
    repo_url = input("Enter your repository URL (e.g., https://github.com/username/SSGEpub.git): ")
    
    if not repo_url:
        print("❌ No repository URL provided")
        return None
    
    try:
        # Clone repository
        subprocess.check_call(["git", "clone", repo_url, "/content/SSGEpub"])
        print("✅ Repository cloned successfully")
        return "/content/SSGEpub"
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to clone repository: {e}")
        return None

def setup_git_config():
    """Setup git configuration"""
    print("⚙️ Setting up git configuration...")
    
    try:
        git_name = input("Enter your git user name: ") or "Admin Bot"
        git_email = input("Enter your git email: ") or "admin@ssgepub.com"
        
        subprocess.check_call(["git", "config", "--global", "user.name", git_name])
        subprocess.check_call(["git", "config", "--global", "user.email", git_email])
        
        print("✅ Git configuration set successfully")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to setup git config: {e}")

def setup_github_token():
    """Setup GitHub token for authentication"""
    print("🔑 Setting up GitHub authentication...")
    
    github_token = input("Enter your GitHub Personal Access Token: ")
    
    if github_token:
        # Store in environment variable
        os.environ['GITHUB_TOKEN'] = github_token
        print("✅ GitHub token set successfully")
        return github_token
    else:
        print("⚠️ No GitHub token provided. You can set it later in the admin tool.")
        return None

def create_streamlit_config():
    """Create Streamlit configuration"""
    print("🎨 Creating Streamlit configuration...")
    
    try:
        # Create .streamlit directory
        streamlit_dir = Path.home() / ".streamlit"
        streamlit_dir.mkdir(exist_ok=True)
        
        # Create config.toml
        config_content = """
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
"""
        
        config_file = streamlit_dir / "config.toml"
        with open(config_file, 'w') as f:
            f.write(config_content)
        
        print("✅ Streamlit configuration created")
        
    except Exception as e:
        print(f"❌ Failed to create Streamlit config: {e}")

def start_admin_tool(repo_path):
    """Start the admin tool"""
    print("🚀 Starting SSG Epub Admin Tool...")
    
    if not repo_path:
        repo_path = "/content/SSGEpub"
    
    admin_tool_path = os.path.join(repo_path, "admin_tool", "main.py")
    
    if not os.path.exists(admin_tool_path):
        print(f"❌ Admin tool not found at {admin_tool_path}")
        return
    
    try:
        # Change to repository directory
        os.chdir(repo_path)
        
        # Start ngrok tunnel
        from pyngrok import ngrok
        public_url = ngrok.connect(8501)
        print(f"🌐 Admin Tool URL: {public_url}")
        
        # Start Streamlit
        print("🎯 Starting Streamlit app...")
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            admin_tool_path, 
            "--server.port", "8501",
            "--server.headless", "true"
        ])
        
    except Exception as e:
        print(f"❌ Failed to start admin tool: {e}")

def main():
    """Main setup function"""
    print("🎯 SSG Epub Admin Tool - Google Colab Setup")
    print("=" * 50)
    
    # Step 1: Install requirements
    install_requirements()
    print()
    
    # Step 2: Setup ngrok
    setup_ngrok()
    print()
    
    # Step 3: Clone repository
    repo_path = clone_repository()
    print()
    
    # Step 4: Setup git config
    setup_git_config()
    print()
    
    # Step 5: Setup GitHub token
    github_token = setup_github_token()
    print()
    
    # Step 6: Create Streamlit config
    create_streamlit_config()
    print()
    
    # Step 7: Start admin tool
    start_choice = input("Do you want to start the admin tool now? (y/n): ").lower()
    if start_choice == 'y':
        start_admin_tool(repo_path)
    else:
        print("✅ Setup completed! You can start the admin tool later by running:")
        print(f"cd {repo_path}")
        print("python -m streamlit run admin_tool/main.py --server.port 8501 --server.headless true")

if __name__ == "__main__":
    main()
