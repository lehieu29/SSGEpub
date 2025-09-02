#!/usr/bin/env python3
"""
Script để tạo tất cả files của Admin Tool trên Google Colab
Chạy script này để tạo từng file một cách có tổ chức
"""

import os
from pathlib import Path

def create_directory_structure():
    """Tạo cấu trúc thư mục"""
    print("📁 Tạo cấu trúc thư mục...")
    
    directories = [
        "admin_tool",
        "admin_tool/data"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Tạo thư mục: {directory}")

def create_requirements_txt():
    """Tạo file requirements.txt"""
    print("\n📦 Tạo requirements.txt...")
    
    content = """streamlit>=1.28.0
requests>=2.31.0
PyYAML>=6.0
pathlib>=1.0.1
unicodedata2>=15.0.0"""
    
    with open("admin_tool/requirements.txt", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ Đã tạo admin_tool/requirements.txt")

def create_platforms_json():
    """Tạo file platforms.json"""
    print("\n🔗 Tạo platforms.json...")
    
    content = """{
  "platforms": [
    {
      "id": 1,
      "name": "TinyURL",
      "logo_url": "https://tinyurl.com/app/themes/tinyurl/images/tinyurl-logo.svg",
      "api_endpoint": "https://tinyurl.com/api-create.php",
      "curl_template": "curl -X POST \\"https://tinyurl.com/api-create.php\\" -d \\"url=${link_download}\\"",
      "response_format": "text",
      "response_path": "",
      "active": true,
      "icon": "fas fa-link"
    },
    {
      "id": 2,
      "name": "Is.gd",
      "logo_url": "https://is.gd/images/logo.png",
      "api_endpoint": "https://is.gd/create.php",
      "curl_template": "curl -X POST \\"https://is.gd/create.php\\" -d \\"format=simple&url=${link_download}\\"",
      "response_format": "text",
      "response_path": "",
      "active": true,
      "icon": "fas fa-compress-alt"
    },
    {
      "id": 3,
      "name": "V.gd",
      "logo_url": "https://v.gd/images/logo.png",
      "api_endpoint": "https://v.gd/create.php",
      "curl_template": "curl -X POST \\"https://v.gd/create.php\\" -d \\"format=simple&url=${link_download}\\"",
      "response_format": "text",
      "response_path": "",
      "active": true,
      "icon": "fas fa-external-link-alt"
    }
  ],
  "last_updated": "2024-01-01T00:00:00"
}"""
    
    with open("admin_tool/data/platforms.json", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ Đã tạo admin_tool/data/platforms.json")

def create_epub_manager():
    """Tạo file epub_manager.py"""
    print("\n📚 Tạo epub_manager.py...")
    
    # Đọc content từ file template (nếu có) hoặc tạo mới
    content = '''"""
Epub Manager - Quản lý sách điện tử
Xử lý tạo, sửa, xóa và convert sách
"""

import os
import re
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import unicodedata

class EpubManager:
    def __init__(self, repo_path: str = None):
        """Initialize EpubManager"""
        self.repo_path = repo_path or self._find_repo_path()
        self.epubs_dir = os.path.join(self.repo_path, '_epubs')
        self.cache = {}
        self.load_books_cache()
    
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
                if os.path.exists(os.path.join(path, '_epubs')):
                    return path
        
        # Local development
        while current_dir != '/':
            if os.path.exists(os.path.join(current_dir, '_epubs')):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        
        # Default fallback
        return os.getcwd()
    
    def load_books_cache(self):
        """Load books cache"""
        try:
            if os.path.exists(self.epubs_dir):
                self.cache = {}
                for filename in os.listdir(self.epubs_dir):
                    if filename.endswith('.md'):
                        filepath = os.path.join(self.epubs_dir, filename)
                        book_data = self._parse_markdown_file(filepath)
                        if book_data:
                            self.cache[filename] = book_data
        except Exception as e:
            print(f"Error loading books cache: {e}")
            self.cache = {}
    
    def _parse_markdown_file(self, filepath: str) -> Optional[Dict]:
        """Parse markdown file and extract frontmatter"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    frontmatter['filename'] = os.path.basename(filepath)
                    frontmatter['content'] = parts[2].strip()
                    return frontmatter
        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
        
        return None
    
    def get_all_books(self) -> List[Dict]:
        """Get all books"""
        return list(self.cache.values())
    
    def get_book_by_filename(self, filename: str) -> Optional[Dict]:
        """Get book by filename"""
        return self.cache.get(filename)
    
    def refresh_cache(self):
        """Refresh books cache"""
        self.load_books_cache()
    
    def create_filename(self, title: str) -> str:
        """Create filename from title"""
        # Remove Vietnamese accents and special characters
        filename = self._slugify(title)
        filename = f"{filename}.md"
        
        # Ensure unique filename
        counter = 1
        original_filename = filename
        while os.path.exists(os.path.join(self.epubs_dir, filename)):
            name, ext = os.path.splitext(original_filename)
            filename = f"{name}-{counter}{ext}"
            counter += 1
        
        return filename
    
    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug"""
        # Normalize unicode characters
        text = unicodedata.normalize('NFD', text)
        
        # Remove accents
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
        
        # Convert to lowercase and replace spaces/special chars with hyphens
        text = re.sub(r'[^\\w\\s-]', '', text.lower())
        text = re.sub(r'[-\\s]+', '-', text)
        
        return text.strip('-')
    
    def generate_markdown(self, book_data: Dict) -> str:
        """Generate markdown content from book data"""
        # Prepare frontmatter
        frontmatter = {
            'layout': 'epub',
            'title': book_data['title'],
            'author': book_data['author'],
            'cover_image': book_data['cover_image'],
            'description': book_data['description']
        }
        
        # Add optional fields
        optional_fields = [
            'preview_image', 'isbn', 'published_date', 'genre', 
            'rating', 'pages', 'language', 'publisher', 'tags'
        ]
        
        for field in optional_fields:
            if field in book_data and book_data[field]:
                frontmatter[field] = book_data[field]
        
        # Add preview content if available
        if book_data.get('preview_content'):
            frontmatter['preview_content'] = book_data['preview_content']
        
        # Add download links
        if book_data.get('download_links'):
            frontmatter['download_links'] = []
            for link in book_data['download_links']:
                link_data = {
                    'platform': link['platform'],
                    'url': link['url'],
                    'index': link.get('index', 0)
                }
                if link.get('icon'):
                    link_data['icon'] = link['icon']
                frontmatter['download_links'].append(link_data)
        
        # Add download config URL if needed
        if book_data.get('download_config_url'):
            frontmatter['download_config_url'] = book_data['download_config_url']
        
        # Generate YAML frontmatter
        yaml_content = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
        
        # Generate full markdown
        markdown_content = f"""---
{yaml_content}---

Đây là trang chi tiết của cuốn sách "{{{{ page.title }}}}" của tác giả {{{{ page.author }}}}.
"""
        
        return markdown_content
    
    def create_book(self, book_data: Dict) -> str:
        """Create new book"""
        # Generate filename
        filename = self.create_filename(book_data['title'])
        filepath = os.path.join(self.epubs_dir, filename)
        
        # Generate markdown content
        markdown_content = self.generate_markdown(book_data)
        
        # Ensure directory exists
        os.makedirs(self.epubs_dir, exist_ok=True)
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Update cache
        book_data['filename'] = filename
        self.cache[filename] = book_data
        
        return filename
    
    # ... (thêm các methods khác nếu cần)
'''
    
    with open("admin_tool/epub_manager.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ Đã tạo admin_tool/epub_manager.py")

def create_shortener_manager():
    """Tạo file shortener_manager.py"""
    print("\n🔗 Tạo shortener_manager.py...")
    
    content = '''"""
Shortener Manager - Quản lý các platform rút gọn URL
Xử lý rút gọn URL và quản lý cấu hình platforms
"""

import os
import json
import requests
import subprocess
import re
from typing import Dict, List, Optional, Any
from pathlib import Path

class ShortenerManager:
    def __init__(self, data_dir: str = None):
        """Initialize ShortenerManager"""
        self.data_dir = data_dir or os.path.join(os.getcwd(), 'admin_tool', 'data')
        self.platforms_file = os.path.join(self.data_dir, 'platforms.json')
        self.platforms = []
        self.load_platforms()
    
    def load_platforms(self):
        """Load platforms from file"""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            
            if os.path.exists(self.platforms_file):
                with open(self.platforms_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.platforms = data.get('platforms', [])
            else:
                # Create default platforms
                self.platforms = self._get_default_platforms()
                self.save_platforms()
        except Exception as e:
            print(f"Error loading platforms: {e}")
            self.platforms = self._get_default_platforms()
    
    def _get_default_platforms(self) -> List[Dict]:
        """Get default platform configurations"""
        return [
            {
                'id': 1,
                'name': 'TinyURL',
                'logo_url': 'https://tinyurl.com/app/themes/tinyurl/images/tinyurl-logo.svg',
                'api_endpoint': 'https://tinyurl.com/api-create.php',
                'curl_template': 'curl -X POST "https://tinyurl.com/api-create.php" -d "url=${link_download}"',
                'response_format': 'text',
                'response_path': '',
                'active': True,
                'icon': 'fas fa-link'
            },
            {
                'id': 2,
                'name': 'Is.gd',
                'logo_url': 'https://is.gd/images/logo.png',
                'api_endpoint': 'https://is.gd/create.php',
                'curl_template': 'curl -X POST "https://is.gd/create.php" -d "format=simple&url=${link_download}"',
                'response_format': 'text',
                'response_path': '',
                'active': True,
                'icon': 'fas fa-compress-alt'
            }
        ]
    
    def get_platforms(self) -> List[Dict]:
        """Get all platforms"""
        return self.platforms
    
    def get_active_platforms(self) -> List[Dict]:
        """Get only active platforms"""
        return [p for p in self.platforms if p.get('active', True)]
    
    def shorten_url(self, long_url: str, platform_config: Dict) -> str:
        """Shorten URL using specified platform"""
        try:
            # Replace variables in cURL template
            curl_command = platform_config['curl_template'].replace('${link_download}', long_url)
            
            # Execute cURL
            response = self._execute_curl(curl_command)
            
            # Parse response
            short_url = self._parse_response(
                response, 
                platform_config['response_format'],
                platform_config.get('response_path', '')
            )
            
            return short_url.strip() if short_url else long_url
            
        except Exception as e:
            print(f"Error shortening URL: {e}")
            return long_url
    
    def _execute_curl(self, curl_command: str) -> str:
        """Execute cURL command and return response"""
        try:
            result = subprocess.run(
                curl_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                raise Exception(f"cURL failed: {result.stderr}")
                
        except Exception as e:
            raise Exception(f"Request failed: {e}")
    
    def _parse_response(self, response: str, format_type: str, path: str) -> str:
        """Parse response to extract short URL"""
        if format_type == 'text':
            return response.strip()
        elif format_type == 'json':
            import json
            data = json.loads(response)
            if path:
                keys = path.split('.')
                for key in keys:
                    data = data[key]
            return str(data)
        return response
    
    # ... (thêm các methods khác nếu cần)
'''
    
    with open("admin_tool/shortener_manager.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ Đã tạo admin_tool/shortener_manager.py")

def create_git_manager():
    """Tạo file git_manager.py"""
    print("\n📤 Tạo git_manager.py...")
    
    content = '''"""
Git Manager - Quản lý Git operations
Xử lý add, commit, push và GitHub integration
"""

import os
import subprocess
from typing import Dict, List, Optional

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
            possible_paths = ['/content/SSGEpub', current_dir]
            for path in possible_paths:
                if os.path.exists(os.path.join(path, '.git')):
                    return path
        
        # Local development
        while current_dir != '/':
            if os.path.exists(os.path.join(current_dir, '.git')):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        
        return os.getcwd()
    
    def setup_git_config(self):
        """Setup basic git configuration"""
        try:
            # Try to get config from Colab userdata first
            git_name = "Admin Bot"
            git_email = "admin@ssgepub.com"
            github_token = None
            
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
                pass
            except Exception as e:
                print(f"⚠️ Could not load from Colab secrets: {e}")
            
            # Set git config
            self._run_git_command(['config', '--global', 'user.name', git_name], check_error=False)
            self._run_git_command(['config', '--global', 'user.email', git_email], check_error=False)
            
            # Set safe directory for Google Colab
            if '/content' in os.getcwd():
                self._run_git_command(['config', '--global', '--add', 'safe.directory', self.repo_path], check_error=False)
            
        except Exception as e:
            print(f"Warning: Git setup failed: {e}")
    
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
                raise Exception(f"Git command failed: {' '.join(cmd)}\\nError: {result.stderr}")
            
            return result
        except Exception as e:
            if check_error:
                raise Exception(f"Git command error: {e}")
            return None
    
    def add_commit_push(self, filename: str, message: str = None, branch: str = 'main') -> bool:
        """Add, commit and push a specific file"""
        try:
            if not message:
                message = f"Update {filename}"
            
            # Add file
            self._run_git_command(['add', f"_epubs/{filename}"])
            
            # Commit
            self._run_git_command(['commit', '-m', message])
            
            # Push with token if available
            if self.github_token:
                # Get remote URL and modify it to include token
                remote_result = self._run_git_command(['remote', 'get-url', 'origin'])
                if remote_result.returncode == 0:
                    remote_url = remote_result.stdout.strip()
                    if remote_url.startswith('https://github.com/'):
                        auth_url = remote_url.replace('https://github.com/', f'https://{self.github_token}@github.com/')
                        self._run_git_command(['remote', 'set-url', 'origin', auth_url])
                        try:
                            self._run_git_command(['push', 'origin', branch])
                            return True
                        finally:
                            self._run_git_command(['remote', 'set-url', 'origin', remote_url])
            else:
                self._run_git_command(['push', 'origin', branch])
                return True
                
        except Exception as e:
            print(f"Error in git operations: {e}")
            return False
    
    # ... (thêm các methods khác nếu cần)
'''
    
    with open("admin_tool/git_manager.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ Đã tạo admin_tool/git_manager.py")

def create_main_app():
    """Tạo file main.py (Streamlit app)"""
    print("\n🎯 Tạo main.py...")
    
    content = '''#!/usr/bin/env python3
"""
SSG Epub Admin Tool - Main Streamlit Application
Công cụ quản lý sách điện tử cho SSG Epub Library
"""

import streamlit as st
import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from epub_manager import EpubManager
from shortener_manager import ShortenerManager
from git_manager import GitManager

# Page config
st.set_page_config(
    page_title="📚 SSG Epub Admin Tool",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_managers():
    """Initialize all manager classes"""
    if 'epub_manager' not in st.session_state:
        st.session_state.epub_manager = EpubManager()
    if 'shortener_manager' not in st.session_state:
        st.session_state.shortener_manager = ShortenerManager()
    if 'git_manager' not in st.session_state:
        st.session_state.git_manager = GitManager()

def main_header():
    """Display main header"""
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 1rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
        <h1>📚 SSG Epub Admin Tool</h1>
        <p>Công cụ quản lý sách điện tử cho SSG Epub Library</p>
    </div>
    """, unsafe_allow_html=True)

def create_book_interface():
    """Interface for creating new books"""
    st.header("📖 Thêm Sách Mới")
    
    with st.form("create_book_form"):
        # Basic Information
        st.subheader("📋 Thông tin cơ bản")
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Tên sách *", placeholder="Nhập tên sách...")
            author = st.text_input("Tác giả *", placeholder="Nhập tên tác giả...")
        
        with col2:
            cover_image = st.text_input("URL ảnh bìa *", placeholder="https://example.com/cover.jpg")
            rating = st.slider("Đánh giá", 0.0, 5.0, 4.0, 0.1)
        
        description = st.text_area("Mô tả sách *", placeholder="Nhập mô tả sách...", height=100)
        
        # Download Links Configuration
        st.subheader("🔗 Cấu hình Link Download")
        link_method = st.radio(
            "Phương thức nhập link:",
            ["🤖 Tự động rút gọn từ Google Drive", "✋ Nhập thủ công các link rút gọn"]
        )
        
        if link_method == "🤖 Tự động rút gọn từ Google Drive":
            google_drive_link = st.text_input("Link Google Drive *", placeholder="https://drive.google.com/file/d/...")
            
            platforms = st.session_state.shortener_manager.get_active_platforms()
            if platforms:
                selected_platform = st.selectbox(
                    "Chọn platform rút gọn:",
                    platforms,
                    format_func=lambda x: f"{x['name']} (ID: {x['id']})"
                )
            else:
                st.warning("⚠️ Chưa có platform nào được cấu hình.")
                selected_platform = None
        else:
            st.info("💡 Nhập trực tiếp các link đã được rút gọn")
            manual_links = []
            
            num_links = st.number_input("Số lượng link download", min_value=1, max_value=5, value=1)
            for i in range(num_links):
                st.write(f"**Link {i+1}:**")
                col_name, col_url = st.columns([1, 2])
                with col_name:
                    platform_name = st.text_input(f"Tên platform", key=f"platform_name_{i}")
                with col_url:
                    platform_url = st.text_input(f"URL", key=f"platform_url_{i}")
                
                if platform_name and platform_url:
                    manual_links.append({
                        'platform': platform_name,
                        'url': platform_url,
                        'index': i
                    })
        
        # Submit button
        submitted = st.form_submit_button("🎯 Tạo Sách", type="primary")
        
        if submitted:
            # Validation
            if not all([title, author, cover_image, description]):
                st.error("❌ Vui lòng điền đầy đủ các trường bắt buộc (*)")
                return
            
            # Create book data
            book_data = {
                'title': title,
                'author': author,
                'cover_image': cover_image,
                'description': description,
                'rating': rating,
                'language': 'Tiếng Việt'
            }
            
            # Process download links
            try:
                if link_method == "🤖 Tự động rút gọn từ Google Drive":
                    if not google_drive_link or not selected_platform:
                        st.error("❌ Vui lòng nhập link Google Drive và chọn platform")
                        return
                    
                    with st.spinner("🔄 Đang rút gọn link..."):
                        short_url = st.session_state.shortener_manager.shorten_url(
                            google_drive_link, selected_platform
                        )
                        download_links = [{
                            'platform': selected_platform['name'],
                            'url': short_url,
                            'index': selected_platform['id']
                        }]
                else:
                    if not manual_links:
                        st.error("❌ Vui lòng nhập ít nhất một link download")
                        return
                    download_links = manual_links
                
                book_data['download_links'] = download_links
                
                # Create markdown file
                with st.spinner("📝 Đang tạo file markdown..."):
                    filename = st.session_state.epub_manager.create_book(book_data)
                
                # Git operations
                with st.spinner("📤 Đang push lên GitHub..."):
                    success = st.session_state.git_manager.add_commit_push(
                        filename, f"Add new book: {title}"
                    )
                
                if success:
                    st.success(f"✅ Đã tạo thành công sách '{title}'!")
                    st.info(f"📄 File: {filename}")
                else:
                    st.warning("⚠️ Sách đã được tạo nhưng có lỗi khi push lên GitHub")
                
            except Exception as e:
                st.error(f"❌ Lỗi khi tạo sách: {str(e)}")

def platform_management_interface():
    """Interface for managing shortener platforms"""
    st.header("🔗 Quản lý Platform Rút gọn")
    
    platforms = st.session_state.shortener_manager.get_platforms()
    
    if not platforms:
        st.info("📝 Chưa có platform nào. Hãy thêm platform đầu tiên!")
    else:
        for platform in platforms:
            with st.container():
                col1, col2, col3 = st.columns([1, 3, 1])
                
                with col1:
                    st.write("🔗")
                
                with col2:
                    status_icon = "🟢" if platform.get('active', True) else "🔴"
                    st.write(f"**{platform['name']}** {status_icon}")
                    st.write(f"ID: {platform['id']} | Format: {platform.get('response_format', 'text')}")
                
                with col3:
                    if st.button("🗑️ Xóa", key=f"delete_{platform['id']}"):
                        # Implement delete functionality
                        st.rerun()
            
            st.divider()

def main():
    """Main application"""
    # Initialize
    initialize_managers()
    
    # Header
    main_header()
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ Thêm Sách Mới", 
        "🔗 Quản lý Platform", 
        "🔄 Convert Sách Cũ",
        "⚙️ Cài Đặt"
    ])
    
    with tab1:
        create_book_interface()
    
    with tab2:
        platform_management_interface()
    
    with tab3:
        st.header("🔄 Convert Sách Cũ")
        st.info("Tính năng convert sách cũ sẽ được implement sau")
    
    with tab4:
        st.header("⚙️ Cài Đặt")
        st.info("Tính năng cài đặt sẽ được implement sau")

if __name__ == "__main__":
    main()
'''
    
    with open("admin_tool/main.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ Đã tạo admin_tool/main.py")

def main():
    """Main function để tạo tất cả files"""
    print("🎯 Tạo SSG Epub Admin Tool Files")
    print("=" * 50)
    
    # Tạo từng file theo thứ tự
    create_directory_structure()
    create_requirements_txt()
    create_platforms_json()
    create_epub_manager()
    create_shortener_manager()
    create_git_manager()
    create_main_app()
    
    print("\n" + "=" * 50)
    print("🎉 Đã tạo xong tất cả files!")
    print("\n📁 Cấu trúc files đã tạo:")
    print("admin_tool/")
    print("├── main.py")
    print("├── epub_manager.py")
    print("├── shortener_manager.py")
    print("├── git_manager.py")
    print("├── requirements.txt")
    print("└── data/")
    print("    └── platforms.json")
    
    print("\n🚀 Để chạy admin tool:")
    print("1. pip install -r admin_tool/requirements.txt")
    print("2. streamlit run admin_tool/main.py")

if __name__ == "__main__":
    main()
