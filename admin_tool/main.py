#!/usr/bin/env python3
"""
SSG Epub Admin Tool - Main Streamlit Application
Công cụ quản lý sách điện tử cho SSG Epub Library
"""

import streamlit as st
import os
import sys
import json
from datetime import datetime
from pathlib import Path

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

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .platform-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #f9f9f9;
    }
</style>
""", unsafe_allow_html=True)

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
    <div class="main-header">
        <h1>📚 SSG Epub Admin Tool</h1>
        <p>Công cụ quản lý sách điện tử cho SSG Epub Library</p>
    </div>
    """, unsafe_allow_html=True)

def sidebar_info():
    """Display sidebar information"""
    with st.sidebar:
        st.header("ℹ️ Thông tin hệ thống")
        
        # Repository status
        repo_path = st.session_state.git_manager.repo_path
        if os.path.exists(repo_path):
            st.success(f"✅ Repository: {repo_path}")
        else:
            st.error("❌ Repository không tìm thấy")
        
        # Statistics
        epub_count = len(st.session_state.epub_manager.get_all_books())
        platform_count = len(st.session_state.shortener_manager.get_platforms())
        
        st.metric("📚 Tổng số sách", epub_count)
        st.metric("🔗 Platforms", platform_count)
        
        # Quick actions
        st.header("⚡ Thao tác nhanh")
        if st.button("🔄 Refresh Data"):
            st.session_state.epub_manager.refresh_cache()
            st.session_state.shortener_manager.load_platforms()
            st.rerun()

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
            isbn = st.text_input("ISBN", placeholder="978-604-2-12345-6")
            published_date = st.date_input("Ngày xuất bản")
        
        with col2:
            cover_image = st.text_input("URL ảnh bìa *", placeholder="https://example.com/cover.jpg")
            preview_image = st.text_input("URL ảnh preview", placeholder="https://example.com/preview.jpg")
            pages = st.number_input("Số trang", min_value=1, value=100)
            rating = st.slider("Đánh giá", 0.0, 5.0, 4.0, 0.1)
        
        # Additional Information
        st.subheader("📝 Thông tin bổ sung")
        description = st.text_area("Mô tả sách *", placeholder="Nhập mô tả sách...", height=100)
        
        col3, col4 = st.columns(2)
        with col3:
            genre = st.text_input("Thể loại (phân cách bằng dấu phẩy)", placeholder="Văn học, Tiểu thuyết")
            language = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English", "中文", "日本語"])
        
        with col4:
            publisher = st.text_input("Nhà xuất bản", placeholder="NXB Trẻ")
            tags = st.text_input("Tags (phân cách bằng dấu phẩy)", placeholder="epub, văn học việt nam")
        
        # Preview Content
        st.subheader("👁️ Nội dung preview")
        preview_content = st.text_area("Nội dung preview", placeholder="Nhập đoạn trích...", height=150)
        
        # Download Links Configuration
        st.subheader("🔗 Cấu hình Link Download")
        link_method = st.radio(
            "Phương thức nhập link:",
            ["🤖 Tự động rút gọn từ Google Drive", "✋ Nhập thủ công các link rút gọn"]
        )
        
        if link_method == "🤖 Tự động rút gọn từ Google Drive":
            st.info("💡 Nhập link Google Drive, hệ thống sẽ tự động rút gọn bằng platform đã chọn")
            google_drive_link = st.text_input("Link Google Drive *", placeholder="https://drive.google.com/file/d/...")
            
            platforms = st.session_state.shortener_manager.get_active_platforms()
            if platforms:
                selected_platform = st.selectbox(
                    "Chọn platform rút gọn:",
                    platforms,
                    format_func=lambda x: f"{x['name']} (ID: {x['id']})"
                )
            else:
                st.warning("⚠️ Chưa có platform nào được cấu hình. Vui lòng thêm platform trước.")
                selected_platform = None
        else:
            st.info("💡 Nhập trực tiếp các link đã được rút gọn")
            manual_links = []
            
            num_links = st.number_input("Số lượng link download", min_value=1, max_value=10, value=1)
            for i in range(num_links):
                st.write(f"**Link {i+1}:**")
                col_name, col_url, col_logo = st.columns([2, 3, 2])
                with col_name:
                    platform_name = st.text_input(f"Tên platform", key=f"platform_name_{i}")
                with col_url:
                    platform_url = st.text_input(f"URL", key=f"platform_url_{i}")
                with col_logo:
                    platform_logo = st.text_input(f"Logo URL", key=f"platform_logo_{i}")
                
                if platform_name and platform_url:
                    manual_links.append({
                        'platform': platform_name,
                        'url': platform_url,
                        'logo': platform_logo or "",
                        'index': i
                    })
        
        # Submit button
        submitted = st.form_submit_button("🎯 Tạo Sách", type="primary")
        
        if submitted:
            # Validation
            if not all([title, author, cover_image, description]):
                st.error("❌ Vui lòng điền đầy đủ các trường bắt buộc (*)")
                return
            
            if link_method == "🤖 Tự động rút gọn từ Google Drive":
                if not google_drive_link or not selected_platform:
                    st.error("❌ Vui lòng nhập link Google Drive và chọn platform")
                    return
            else:
                if not manual_links:
                    st.error("❌ Vui lòng nhập ít nhất một link download")
                    return
            
            # Create book data
            book_data = {
                'title': title,
                'author': author,
                'cover_image': cover_image,
                'preview_image': preview_image,
                'isbn': isbn,
                'published_date': published_date.strftime('%Y-%m-%d'),
                'genre': [g.strip() for g in genre.split(',') if g.strip()],
                'description': description,
                'rating': rating,
                'pages': pages,
                'language': language,
                'publisher': publisher,
                'preview_content': preview_content,
                'tags': [t.strip() for t in tags.split(',') if t.strip()]
            }
            
            # Process download links
            try:
                if link_method == "🤖 Tự động rút gọn từ Google Drive":
                    with st.spinner("🔄 Đang rút gọn link..."):
                        short_url = st.session_state.shortener_manager.shorten_url(
                            google_drive_link, selected_platform
                        )
                        download_links = [{
                            'platform': selected_platform['name'],
                            'url': short_url,
                            'index': selected_platform['id'],
                            'icon': selected_platform.get('icon', 'fas fa-download')
                        }]
                else:
                    download_links = manual_links
                
                book_data['download_links'] = download_links
                
                # Create markdown file
                with st.spinner("📝 Đang tạo file markdown..."):
                    filename = st.session_state.epub_manager.create_book(book_data)
                
                # Git operations
                with st.spinner("📤 Đang push lên GitHub..."):
                    st.session_state.git_manager.add_commit_push(
                        filename, f"Add new book: {title}"
                    )
                
                st.success(f"✅ Đã tạo thành công sách '{title}'!")
                st.info(f"📄 File: {filename}")
                
                # Show preview
                with st.expander("👁️ Preview markdown"):
                    markdown_content = st.session_state.epub_manager.generate_markdown(book_data)
                    st.code(markdown_content, language='markdown')
                
            except Exception as e:
                st.error(f"❌ Lỗi khi tạo sách: {str(e)}")

def platform_management_interface():
    """Interface for managing shortener platforms"""
    st.header("🔗 Quản lý Platform Rút gọn")
    
    # Current platforms
    platforms = st.session_state.shortener_manager.get_platforms()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Danh sách Platform")
        
        if not platforms:
            st.info("📝 Chưa có platform nào. Hãy thêm platform đầu tiên!")
        else:
            for platform in platforms:
                with st.container():
                    platform_col1, platform_col2, platform_col3 = st.columns([1, 3, 1])
                    
                    with platform_col1:
                        if platform.get('logo_url'):
                            try:
                                st.image(platform['logo_url'], width=50)
                            except:
                                st.write("🔗")
                        else:
                            st.write("🔗")
                    
                    with platform_col2:
                        status_icon = "🟢" if platform.get('active', True) else "🔴"
                        st.write(f"**{platform['name']}** {status_icon}")
                        st.write(f"ID: {platform['id']} | Endpoint: {platform.get('api_endpoint', 'N/A')}")
                        if platform.get('response_format'):
                            st.write(f"Response: {platform['response_format']}")
                    
                    with platform_col3:
                        if st.button("✏️ Sửa", key=f"edit_{platform['id']}"):
                            st.session_state.edit_platform_id = platform['id']
                        if st.button("🗑️ Xóa", key=f"delete_{platform['id']}"):
                            st.session_state.shortener_manager.delete_platform(platform['id'])
                            st.rerun()
                
                st.divider()
    
    with col2:
        st.subheader("➕ Thêm Platform Mới")
        
        with st.form("add_platform_form"):
            name = st.text_input("Tên Platform *")
            logo_url = st.text_input("URL Logo")
            api_endpoint = st.text_input("API Endpoint *")
            
            st.write("**cURL Template:**")
            curl_template = st.text_area(
                "Template",
                placeholder="curl -X POST 'https://api.example.com/shorten' -d 'url=${link_download}'",
                height=100
            )
            
            response_format = st.selectbox("Response Format", ["text", "json"])
            
            if response_format == "json":
                response_path = st.text_input(
                    "JSON Path",
                    placeholder="data.short_url",
                    help="Đường dẫn đến short URL trong JSON response"
                )
            else:
                response_path = ""
            
            active = st.checkbox("Kích hoạt", value=True)
            
            if st.form_submit_button("➕ Thêm Platform"):
                if name and api_endpoint and curl_template:
                    platform_data = {
                        'name': name,
                        'logo_url': logo_url,
                        'api_endpoint': api_endpoint,
                        'curl_template': curl_template,
                        'response_format': response_format,
                        'response_path': response_path,
                        'active': active
                    }
                    
                    try:
                        st.session_state.shortener_manager.add_platform(platform_data)
                        st.success(f"✅ Đã thêm platform '{name}'!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Lỗi: {str(e)}")
                else:
                    st.error("❌ Vui lòng điền đầy đủ thông tin bắt buộc")

def conversion_interface():
    """Interface for batch conversion"""
    st.header("🔄 Convert Sách Cũ")
    
    st.info("💡 Chuyển đổi tất cả sách cũ sang platform rút gọn mới")
    
    # Get all books
    books = st.session_state.epub_manager.get_all_books()
    platforms = st.session_state.shortener_manager.get_active_platforms()
    
    if not books:
        st.warning("📚 Không có sách nào để convert")
        return
    
    if not platforms:
        st.warning("🔗 Không có platform nào được kích hoạt")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Thống kê")
        st.metric("Tổng số sách", len(books))
        
        # Show sample books
        st.write("**Danh sách sách:**")
        for book in books[:5]:
            st.write(f"• {book.get('title', 'Unknown')}")
        if len(books) > 5:
            st.write(f"... và {len(books) - 5} sách khác")
    
    with col2:
        st.subheader("⚙️ Cấu hình Convert")
        
        selected_platform = st.selectbox(
            "Platform đích:",
            platforms,
            format_func=lambda x: f"{x['name']} (ID: {x['id']})"
        )
        
        convert_mode = st.radio(
            "Chế độ convert:",
            ["🔄 Convert tất cả", "🎯 Convert từ Google Drive links"]
        )
        
        if st.button("🚀 Bắt đầu Convert", type="primary"):
            if selected_platform:
                try:
                    with st.spinner("🔄 Đang convert..."):
                        result = st.session_state.epub_manager.batch_convert_books(
                            selected_platform, convert_mode == "🎯 Convert từ Google Drive links"
                        )
                    
                    st.success(f"✅ Convert thành công {result['converted']} sách!")
                    
                    if result['errors']:
                        st.warning(f"⚠️ Có {len(result['errors'])} lỗi:")
                        for error in result['errors']:
                            st.write(f"• {error}")
                    
                    # Git commit
                    with st.spinner("📤 Đang push lên GitHub..."):
                        st.session_state.git_manager.batch_commit_push(
                            f"Convert {result['converted']} books to {selected_platform['name']}"
                        )
                    
                    st.success("✅ Đã push lên GitHub!")
                    
                except Exception as e:
                    st.error(f"❌ Lỗi convert: {str(e)}")

def settings_interface():
    """Interface for settings"""
    st.header("⚙️ Cài Đặt")
    
    # Git settings
    st.subheader("🔧 Cài đặt Git")
    
    col1, col2 = st.columns(2)
    with col1:
        git_user = st.text_input("Git User Name", value="Admin Bot")
        git_email = st.text_input("Git Email", value="admin@example.com")
    
    with col2:
        github_token = st.text_input("GitHub Token", type="password")
        repo_url = st.text_input("Repository URL")
    
    if st.button("💾 Lưu cài đặt Git"):
        try:
            st.session_state.git_manager.configure_git(git_user, git_email, github_token)
            st.success("✅ Đã lưu cài đặt Git!")
        except Exception as e:
            st.error(f"❌ Lỗi: {str(e)}")
    
    st.divider()
    
    # Data management
    st.subheader("📊 Quản lý dữ liệu")
    
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("🔄 Refresh Cache"):
            st.session_state.epub_manager.refresh_cache()
            st.session_state.shortener_manager.load_platforms()
            st.success("✅ Đã refresh cache!")
    
    with col4:
        if st.button("📤 Export Data"):
            data = {
                'platforms': st.session_state.shortener_manager.get_platforms(),
                'books_count': len(st.session_state.epub_manager.get_all_books()),
                'export_time': datetime.now().isoformat()
            }
            st.download_button(
                "💾 Download Export",
                json.dumps(data, indent=2, ensure_ascii=False),
                file_name=f"ssg_epub_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

def main():
    """Main application"""
    # Initialize
    initialize_managers()
    
    # Header
    main_header()
    
    # Sidebar
    sidebar_info()
    
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
        conversion_interface()
    
    with tab4:
        settings_interface()

if __name__ == "__main__":
    main()
