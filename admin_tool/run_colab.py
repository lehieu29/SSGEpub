#!/usr/bin/env python3
"""
Quick start script for Google Colab
Chạy script này để khởi động nhanh admin tool trên Colab
"""

import os
import sys
import subprocess
import time

def main():
    """Main function for Colab quick start"""
    print("🎯 SSG Epub Admin Tool - Quick Start for Google Colab")
    print("=" * 60)
    
    # Check if we're in Colab
    try:
        import google.colab
        print("✅ Detected Google Colab environment")
    except ImportError:
        print("⚠️ Not running in Google Colab")
    
    # Install packages
    print("\n📦 Installing packages...")
    packages = ["streamlit", "requests", "PyYAML", "pyngrok"]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
            print(f"✅ {package}")
        except:
            print(f"❌ Failed to install {package}")
    
    # Setup ngrok
    print("\n🌐 Setting up ngrok...")
    try:
        from pyngrok import ngrok

        # Try to get auth token from Colab userdata first
        ngrok_token = None
        try:
            from google.colab import userdata
            ngrok_token = userdata.get('NGROK_TOKEN')
            print("✅ Loaded ngrok token from Colab secrets")
        except ImportError:
            # Not in Colab
            ngrok_token = os.environ.get('NGROK_TOKEN')
        except Exception:
            # Colab userdata not available
            pass

        if not ngrok_token:
            print("Get your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken")
            ngrok_token = input("Enter ngrok auth token (or press Enter to skip): ")

        if ngrok_token:
            ngrok.set_auth_token(ngrok_token)
            print("✅ Ngrok configured")
        else:
            print("⚠️ Ngrok not configured - will run on localhost only")
            print("💡 Tip: Add NGROK_TOKEN to Colab Secrets to avoid entering it each time")
    except Exception as e:
        print(f"❌ Ngrok setup failed: {e}")
    
    # Setup git
    print("\n⚙️ Setting up git...")
    try:
        # Try to get git config from Colab userdata
        git_name = "Admin Bot"
        git_email = "admin@ssgepub.com"

        try:
            from google.colab import userdata
            git_name = userdata.get('GITHUB_USERNAME', 'Admin Bot')
            git_email = userdata.get('GITHUB_EMAIL', 'admin@ssgepub.com')
            print(f"✅ Loaded git config from Colab secrets: {git_name} <{git_email}>")
        except ImportError:
            # Not in Colab
            pass
        except Exception:
            # Colab userdata not available
            pass

        subprocess.run(["git", "config", "--global", "user.name", git_name], check=True)
        subprocess.run(["git", "config", "--global", "user.email", git_email], check=True)

        # For Colab
        if '/content' in os.getcwd():
            subprocess.run(["git", "config", "--global", "--add", "safe.directory", "/content/SSGEpub"], check=False)

        print("✅ Git configured")
    except Exception as e:
        print(f"❌ Git setup failed: {e}")
    
    # Check for repository
    repo_path = None
    possible_paths = ["/content/SSGEpub", "./SSGEpub", "."]
    
    for path in possible_paths:
        if os.path.exists(os.path.join(path, "admin_tool", "main.py")):
            repo_path = path
            break
    
    if not repo_path:
        print("\n📂 Repository not found. Please clone it first:")
        print("!git clone https://github.com/your-username/SSGEpub.git /content/SSGEpub")
        return
    
    print(f"✅ Found repository at: {repo_path}")
    
    # Change to repo directory
    os.chdir(repo_path)
    
    # Setup GitHub token
    github_token = None
    try:
        from google.colab import userdata
        github_token = userdata.get('GITHUB_TOKEN')
        os.environ['GITHUB_TOKEN'] = github_token
        print("✅ Loaded GitHub token from Colab secrets")
    except ImportError:
        # Not in Colab
        github_token = os.environ.get('GITHUB_TOKEN')
    except Exception:
        # Colab userdata not available
        pass

    if not github_token:
        github_token = input("Enter GitHub token (or press Enter to skip): ")
        if github_token:
            os.environ['GITHUB_TOKEN'] = github_token

    if github_token:
        print("✅ GitHub token configured")
    else:
        print("⚠️ No GitHub token - git operations will be limited")
        print("💡 Tip: Add GITHUB_TOKEN to Colab Secrets to avoid entering it each time")
    
    # Create Streamlit config
    print("\n🎨 Setting up Streamlit...")
    try:
        from pathlib import Path
        
        streamlit_dir = Path.home() / ".streamlit"
        streamlit_dir.mkdir(exist_ok=True)
        
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
        
        print("✅ Streamlit configured")
    except Exception as e:
        print(f"❌ Streamlit setup failed: {e}")
    
    # Start admin tool
    print("\n🚀 Starting Admin Tool...")
    
    admin_tool_path = os.path.join(repo_path, "admin_tool", "main.py")
    
    if not os.path.exists(admin_tool_path):
        print(f"❌ Admin tool not found at {admin_tool_path}")
        return
    
    try:
        # Setup ngrok tunnel
        from pyngrok import ngrok
        public_url = ngrok.connect(8501)
        print(f"\n🌐 Public URL: {public_url}")
        print("📱 Click the URL above to access the admin tool")
        print("⏰ Starting Streamlit app...\n")
    except:
        print("⚠️ Running on localhost:8501 only")
    
    # Start Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            admin_tool_path,
            "--server.port", "8501",
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n👋 Admin tool stopped")
    except Exception as e:
        print(f"❌ Error starting admin tool: {e}")

if __name__ == "__main__":
    main()
