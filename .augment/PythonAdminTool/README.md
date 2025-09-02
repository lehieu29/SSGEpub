Tôi hiểu rõ yêu cầu của bạn! Đây là một kế hoạch chi tiết để chuyển từ trang admin HTML sang Python admin tool chạy trên Google Colab với các tính năng nâng cao:

## 📋 **KẾ HOẠCH CHI TIẾT - PYTHON ADMIN TOOL**

### 🎯 **1. PHÂN TÍCH YÊU CẦU**

#### **Hạn chế của trang HTML hiện tại:**
- ❌ Không thể tự động tạo file vào `_epubs/`
- ❌ Không thể trigger Jekyll build
- ❌ Không thể push lên GitHub
- ❌ Không thể xử lý API calls cho link rút gọn
- ❌ Không thể convert hàng loạt sách cũ

#### **Ưu điểm của Python solution:**
- ✅ Full file system access
- ✅ Git operations
- ✅ API integration
- ✅ Batch processing
- ✅ Data persistence
- ✅ Google Colab compatibility

### 🏗️ **2. KIẾN TRÚC HỆ THỐNG MỚI**

```
📁 Python Admin Tool
├── 📄 main.py (Streamlit/Gradio UI)
├── 📄 epub_manager.py (Core logic)
├── 📄 shortener_manager.py (URL shortening)
├── 📄 git_manager.py (Git operations)
├── 📄 config.json (Platform configs)
└── 📁 data/
    ├── platforms.json (Shortener platforms)
    └── books_cache.json (Books metadata)
```

### 🔧 **3. TÍNH NĂNG CHI TIẾT**

#### **3.1 Quản lý Platform Rút gọn**
```python
# Platform Configuration
{
    "platforms": [
        {
            "id": 1,
            "name": "TinyURL",
            "logo_url": "https://tinyurl.com/logo.png",
            "api_endpoint": "https://tinyurl.com/api-create.php",
            "curl_template": "curl -X POST 'https://tinyurl.com/api-create.php' -d 'url=${link_download}'",
            "response_format": "text", # or "json"
            "response_path": "", # for JSON: "data.short_url"
            "active": true
        },
        {
            "id": 2,
            "name": "Bit.ly",
            "logo_url": "https://bit.ly/logo.png",
            "api_endpoint": "https://api-ssl.bitly.com/v4/shorten",
            "curl_template": "curl -X POST 'https://api-ssl.bitly.com/v4/shorten' -H 'Authorization: Bearer ${api_key}' -H 'Content-Type: application/json' -d '{\"long_url\": \"${link_download}\"}'",
            "response_format": "json",
            "response_path": "link",
            "active": true
        }
    ]
}
```

#### **3.2 Workflow Tạo Sách Mới**
```python
def create_new_book():
    # 1. Thu thập thông tin sách
    book_data = collect_book_info()
    
    # 2. Xử lý link download
    if use_auto_shortening:
        short_links = []
        for original_link in book_data['download_links']:
            short_link = shorten_url(original_link, selected_platform)
            short_links.append({
                'platform': selected_platform['name'],
                'url': short_link,
                'logo': selected_platform['logo_url'],
                'index': selected_platform['id']
            })
    else:
        # Manual input
        short_links = manual_input_links()
    
    # 3. Generate markdown
    markdown_content = generate_markdown(book_data, short_links)
    
    # 4. Save to _epubs/
    filename = create_filename(book_data['title'])
    save_markdown_file(filename, markdown_content)
    
    # 5. Git operations
    git_add_commit_push(filename)
    
    # 6. Trigger Jekyll build (GitHub Actions)
    trigger_github_build()
```

#### **3.3 Conversion Tool cho Sách Cũ**
```python
def convert_old_books():
    # 1. Load all existing books
    existing_books = load_all_epub_files()
    
    # 2. Get new platform config
    new_platform = get_new_platform_config()
    
    # 3. Convert each book
    for book in existing_books:
        # Extract current download links
        current_links = extract_download_links(book)
        
        # Convert to new platform
        new_links = []
        for link in current_links:
            if is_google_drive_link(link['url']):
                new_short_link = shorten_url(link['url'], new_platform)
                new_links.append({
                    'platform': new_platform['name'],
                    'url': new_short_link,
                    'logo': new_platform['logo_url'],
                    'index': new_platform['id']
                })
        
        # Update markdown
        updated_content = update_markdown_content(book, new_links)
        save_markdown_file(book['filename'], updated_content)
    
    # 4. Batch git operations
    git_add_all_commit_push("Convert all books to new platform")
    trigger_github_build()
```

### 🖥️ **4. GIAO DIỆN NGƯỜI DÙNG (STREAMLIT)**

#### **4.1 Main Dashboard**
```python
import streamlit as st

def main_dashboard():
    st.title("📚 SSG Epub Admin Tool")
    
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
        conversion_interface()
    
    with tab4:
        settings_interface()
```

#### **4.2 Thêm Sách Mới Interface**
```python
def create_book_interface():
    st.header("📖 Thêm Sách Mới")
    
    # Basic Info
    with st.expander("📋 Thông tin cơ bản", expanded=True):
        title = st.text_input("Tên sách *")
        author = st.text_input("Tác giả *")
        cover_image = st.text_input("URL ảnh bìa *")
        description = st.text_area("Mô tả sách *")
    
    # Download Links
    with st.expander("🔗 Link Download", expanded=True):
        link_method = st.radio(
            "Phương thức nhập link:",
            ["🤖 Tự động rút gọn", "✋ Nhập thủ công"]
        )
        
        if link_method == "🤖 Tự động rút gọn":
            auto_shortening_interface()
        else:
            manual_input_interface()
    
    # Preview & Create
    if st.button("🎯 Tạo Sách", type="primary"):
        create_book_workflow()
```

#### **4.3 Platform Management Interface**
```python
def platform_management_interface():
    st.header("🔗 Quản lý Platform Rút gọn")
    
    # Current Platforms
    platforms = load_platforms()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Danh sách Platform")
        for platform in platforms:
            with st.container():
                col_logo, col_info, col_actions = st.columns([1, 3, 1])
                
                with col_logo:
                    st.image(platform['logo_url'], width=50)
                
                with col_info:
                    st.write(f"**{platform['name']}** (ID: {platform['id']})")
                    st.write(f"Status: {'🟢 Active' if platform['active'] else '🔴 Inactive'}")
                
                with col_actions:
                    if st.button("✏️", key=f"edit_{platform['id']}"):
                        edit_platform(platform)
    
    with col2:
        st.subheader("➕ Thêm Platform Mới")
        add_new_platform_form()
```

### 🔧 **5. CORE MODULES**

#### **5.1 URL Shortener Manager**
```python
class ShortenerManager:
    def __init__(self):
        self.platforms = self.load_platforms()
    
    def shorten_url(self, long_url, platform_config):
        """Rút gọn URL sử dụng platform được chọn"""
        try:
            # Replace variables in cURL template
            curl_command = platform_config['curl_template'].replace(
                '${link_download}', long_url
            )
            
            # Execute cURL
            response = self.execute_curl(curl_command)
            
            # Parse response
            short_url = self.parse_response(
                response, 
                platform_config['response_format'],
                platform_config['response_path']
            )
            
            return short_url
            
        except Exception as e:
            st.error(f"Lỗi rút gọn URL: {e}")
            return long_url
    
    def parse_response(self, response, format_type, path):
        """Parse response để lấy short URL"""
        if format_type == "text":
            return response.strip()
        elif format_type == "json":
            import json
            data = json.loads(response)
            # Navigate JSON path: "data.short_url" -> data['data']['short_url']
            keys = path.split('.')
            for key in keys:
                data = data[key]
            return data
```

#### **5.2 Git Manager**
```python
class GitManager:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.setup_git()
    
    def setup_git(self):
        """Setup Git credentials for Google Colab"""
        # Configure git user
        os.system('git config --global user.name "Admin Bot"')
        os.system('git config --global user.email "admin@example.com"')
        
        # Setup GitHub token
        github_token = st.secrets["GITHUB_TOKEN"]
        self.setup_github_auth(github_token)
    
    def add_commit_push(self, filename, message=None):
        """Add, commit và push file"""
        if not message:
            message = f"Add new book: {filename}"
        
        os.system(f'cd {self.repo_path} && git add _epubs/{filename}')
        os.system(f'cd {self.repo_path} && git commit -m "{message}"')
        os.system(f'cd {self.repo_path} && git push origin main')
    
    def batch_commit_push(self, message):
        """Commit tất cả thay đổi"""
        os.system(f'cd {self.repo_path} && git add .')
        os.system(f'cd {self.repo_path} && git commit -m "{message}"')
        os.system(f'cd {self.repo_path} && git push origin main')
```

### 📱 **6. GOOGLE COLAB SETUP**

#### **6.1 Colab Notebook Structure**
```python
# Cell 1: Setup
!pip install streamlit requests gitpython

# Cell 2: Clone Repository
!git clone https://github.com/username/SSGEpub.git
%cd SSGEpub

# Cell 3: Setup Secrets
import os
os.environ['GITHUB_TOKEN'] = 'your_github_token'

# Cell 4: Run Admin Tool
!streamlit run admin_tool.py --server.port 8501 --server.headless true
```

#### **6.2 Colab-specific Features**
```python
def setup_colab_environment():
    """Setup môi trường Google Colab"""
    # Mount Google Drive for persistent storage
    from google.colab import drive
    drive.mount('/content/drive')
    
    # Setup ngrok for public URL
    !pip install pyngrok
    from pyngrok import ngrok
    public_url = ngrok.connect(8501)
    print(f"Admin Tool URL: {public_url}")
    
    # Load persistent data from Drive
    load_persistent_data()
```

### 🎯 **7. MIGRATION PLAN**

#### **Phase 1: Core Development (1-2 tuần)**
- ✅ Tạo basic Streamlit interface
- ✅ Implement file operations
- ✅ Git integration
- ✅ Basic URL shortening

#### **Phase 2: Advanced Features (1 tuần)**
- ✅ Platform management
- ✅ Batch conversion tool
- ✅ Data persistence
- ✅ Error handling

#### **Phase 3: Testing & Deployment (3-5 ngày)**
- ✅ Google Colab optimization
- ✅ UI/UX improvements
- ✅ Documentation
- ✅ Final testing

### 💡 **8. BENEFITS**

#### **Immediate Benefits:**
- 🚀 **Tự động hóa hoàn toàn**: Từ tạo file đến push GitHub
- 🔗 **URL shortening tích hợp**: Không cần copy/paste manual
- 📊 **Batch operations**: Convert hàng loạt sách cũ
- 💾 **Data persistence**: Lưu trữ cấu hình platforms

#### **Long-term Benefits:**
- 🔧 **Extensible**: Dễ thêm platforms mới
- 🛡️ **Reliable**: Error handling và validation
- 📈 **Scalable**: Xử lý được hàng nghìn sách
- 🌐 **Cloud-based**: Chạy mọi lúc mọi nơi

### 🚀 **9. NEXT STEPS**

1. **Confirm approach**: Bạn có muốn proceed với Python solution?
2. **Choose UI framework**: Streamlit vs Gradio vs Jupyter widgets?
3. **Platform priorities**: Platforms rút gọn nào cần support đầu tiên?
4. **Start development**: Tôi có thể bắt đầu code ngay!

**Bạn có muốn tôi bắt đầu implement Python admin tool này không?** 🎯
