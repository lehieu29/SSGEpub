#!/usr/bin/env python3
"""
Script để tạo Google Colab notebook hoàn chỉnh
"""

import json

def create_colab_notebook():
    """Tạo notebook hoàn chỉnh cho Google Colab"""
    
    notebook = {
        "nbformat": 4,
        "nbformat_minor": 0,
        "metadata": {
            "colab": {
                "provenance": [],
                "collapsed_sections": []
            },
            "kernelspec": {
                "name": "python3",
                "display_name": "Python 3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "cells": [
            # Header cell
            {
                "cell_type": "markdown",
                "source": [
                    "# 📚 SSG Epub Admin Tool - Google Colab\n\n",
                    "**Công cụ quản lý sách điện tử cho SSG Epub Library**\n\n",
                    "## 🚀 Hướng dẫn sử dụng:\n",
                    "1. **Chạy từng cell theo thứ tự** (Ctrl+Enter hoặc Shift+Enter)\n",
                    "2. **Lần đầu**: Nhập thông tin khi được yêu cầu\n",
                    "3. **Lần sau**: Tự động lấy từ Colab Secrets\n",
                    "4. **Sử dụng URL public** để truy cập admin tool\n\n",
                    "## 🔑 Setup Colab Secrets (khuyến nghị):\n",
                    "Để không phải nhập lại thông tin mỗi lần:\n",
                    "1. Click vào icon 🔑 **Secrets** ở sidebar trái\n",
                    "2. Thêm các secrets:\n",
                    "   - `GITHUB_REPO_URL`: https://github.com/username/SSGEpub.git\n",
                    "   - `GITHUB_TOKEN`: Personal Access Token từ GitHub\n",
                    "   - `GITHUB_USERNAME`: Tên GitHub của bạn\n",
                    "   - `GITHUB_EMAIL`: Email GitHub của bạn\n",
                    "   - `NGROK_TOKEN`: Auth token từ ngrok.com (tùy chọn)\n\n",
                    "---"
                ],
                "metadata": {"id": "header"}
            },
            
            # Step 1: Install packages
            {
                "cell_type": "markdown",
                "source": ["## 📦 Bước 1: Cài đặt packages"],
                "metadata": {"id": "step1"}
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {"id": "install_packages"},
                "outputs": [],
                "source": [
                    "# Cài đặt các package cần thiết\n",
                    "!pip install streamlit requests PyYAML pyngrok -q\n\n",
                    "print(\"✅ Đã cài đặt xong các packages!\")\n",
                    "print(\"📦 Packages: streamlit, requests, PyYAML, pyngrok\")"
                ]
            },
            
            # Step 2: Clone repository
            {
                "cell_type": "markdown",
                "source": ["## 📂 Bước 2: Clone repository"],
                "metadata": {"id": "step2"}
            },
            {
                "cell_type": "code",
                "source": [
                    "import os\n",
                    "from google.colab import userdata\n\n",
                    "# Lấy URL repository từ Colab Secrets hoặc nhập thủ công\n",
                    "try:\n",
                    "    REPO_URL = userdata.get('GITHUB_REPO_URL')\n",
                    "    print(f\"✅ Lấy được repository URL từ secrets: {REPO_URL}\")\n",
                    "except:\n",
                    "    REPO_URL = input(\"Nhập URL repository (ví dụ: https://github.com/username/SSGEpub.git): \")\n\n",
                    "if REPO_URL:\n",
                    "    # Xóa thư mục cũ nếu có\n",
                    "    !rm -rf /content/SSGEpub\n",
                    "    \n",
                    "    # Clone repository\n",
                    "    !git clone {REPO_URL} /content/SSGEpub\n",
                    "    \n",
                    "    # Chuyển đến thư mục repository\n",
                    "    %cd /content/SSGEpub\n",
                    "    \n",
                    "    print(\"✅ Đã clone repository thành công!\")\n",
                    "    print(f\"📂 Repository: {REPO_URL}\")\n",
                    "    \n",
                    "    # Kiểm tra admin_tool có tồn tại không\n",
                    "    if os.path.exists('/content/SSGEpub/admin_tool/main.py'):\n",
                    "        print(\"✅ Tìm thấy admin_tool\")\n",
                    "    else:\n",
                    "        print(\"⚠️ Không tìm thấy admin_tool, sẽ tạo mới\")\n",
                    "        # Tạo admin_tool nếu chưa có\n",
                    "        !mkdir -p admin_tool/data\n",
                    "        print(\"📁 Đã tạo thư mục admin_tool\")\n",
                    "else:\n",
                    "    print(\"❌ Vui lòng nhập URL repository!\")\n",
                    "    print(\"💡 Tip: Thêm GITHUB_REPO_URL vào Colab Secrets để không phải nhập lại\")"
                ],
                "metadata": {"id": "clone_repo"},
                "execution_count": None,
                "outputs": []
            },
            
            # Step 3: Setup authentication
            {
                "cell_type": "markdown",
                "source": ["## 🔑 Bước 3: Cấu hình authentication"],
                "metadata": {"id": "step3"}
            },
            {
                "cell_type": "code",
                "source": [
                    "from google.colab import userdata\n",
                    "import os\n\n",
                    "# Lấy thông tin từ Colab Secrets hoặc nhập thủ công\n",
                    "try:\n",
                    "    git_name = userdata.get('GITHUB_USERNAME')\n",
                    "    print(f\"✅ Lấy được GitHub username từ secrets: {git_name}\")\n",
                    "except:\n",
                    "    git_name = input(\"Nhập Git user name (mặc định: Admin Bot): \") or \"Admin Bot\"\n\n",
                    "try:\n",
                    "    git_email = userdata.get('GITHUB_EMAIL')\n",
                    "    print(f\"✅ Lấy được GitHub email từ secrets: {git_email}\")\n",
                    "except:\n",
                    "    git_email = input(\"Nhập Git email (mặc định: admin@ssgepub.com): \") or \"admin@ssgepub.com\"\n\n",
                    "# Cấu hình Git\n",
                    "!git config --global user.name \"{git_name}\"\n",
                    "!git config --global user.email \"{git_email}\"\n",
                    "!git config --global --add safe.directory /content/SSGEpub\n\n",
                    "print(f\"✅ Đã cấu hình Git: {git_name} <{git_email}>\")\n\n",
                    "# GitHub Token\n",
                    "try:\n",
                    "    github_token = userdata.get('GITHUB_TOKEN')\n",
                    "    os.environ['GITHUB_TOKEN'] = github_token\n",
                    "    print(\"✅ Lấy được GitHub token từ secrets!\")\n",
                    "except:\n",
                    "    github_token = input(\"Nhập GitHub Personal Access Token: \")\n",
                    "    if github_token:\n",
                    "        os.environ['GITHUB_TOKEN'] = github_token\n",
                    "        print(\"✅ Đã lưu GitHub token!\")\n",
                    "    else:\n",
                    "        print(\"⚠️ Không có GitHub token. Bạn có thể cấu hình sau trong admin tool.\")\n\n",
                    "print(\"\\n💡 Tip: Để không phải nhập lại, hãy thêm vào Colab Secrets:\")\n",
                    "print(\"   - GITHUB_TOKEN: Personal Access Token\")\n",
                    "print(\"   - GITHUB_USERNAME: Tên GitHub của bạn\")\n",
                    "print(\"   - GITHUB_EMAIL: Email GitHub của bạn\")\n",
                    "print(\"   - NGROK_TOKEN: Auth token từ ngrok.com (tùy chọn)\")"
                ],
                "metadata": {"id": "setup_auth"},
                "execution_count": None,
                "outputs": []
            },
            
            # Step 4: Setup ngrok
            {
                "cell_type": "markdown",
                "source": ["## 🌐 Bước 4: Setup ngrok (để tạo URL public)"],
                "metadata": {"id": "step4"}
            },
            {
                "cell_type": "code",
                "source": [
                    "from pyngrok import ngrok\n",
                    "from google.colab import userdata\n\n",
                    "# Lấy ngrok token từ secrets hoặc nhập thủ công\n",
                    "try:\n",
                    "    ngrok_token = userdata.get('NGROK_TOKEN')\n",
                    "    ngrok.set_auth_token(ngrok_token)\n",
                    "    print(\"✅ Lấy được ngrok token từ secrets!\")\n",
                    "except:\n",
                    "    ngrok_token = input(\"Nhập ngrok auth token (lấy từ https://dashboard.ngrok.com/get-started/your-authtoken): \")\n",
                    "    if ngrok_token:\n",
                    "        ngrok.set_auth_token(ngrok_token)\n",
                    "        print(\"✅ Đã cấu hình ngrok!\")\n",
                    "    else:\n",
                    "        print(\"⚠️ Không có ngrok token. Admin tool sẽ chỉ chạy local.\")\n\n",
                    "print(\"\\n📝 Lưu ý về ngrok:\")\n",
                    "print(\"🎯 Ngrok tạo URL public để truy cập Streamlit app từ browser\")\n",
                    "print(\"🔗 Ví dụ: https://abc123.ngrok.io -> localhost:8501 trên Colab\")\n",
                    "print(\"✨ Nếu chạy local trên máy bạn thì KHÔNG CẦN ngrok!\")"
                ],
                "metadata": {"id": "setup_ngrok"},
                "execution_count": None,
                "outputs": []
            },
            
            # Step 5: Streamlit config
            {
                "cell_type": "markdown",
                "source": ["## 🎨 Bước 5: Cấu hình Streamlit"],
                "metadata": {"id": "step5"}
            },
            {
                "cell_type": "code",
                "source": [
                    "# Tạo cấu hình Streamlit\n",
                    "import os\n",
                    "from pathlib import Path\n\n",
                    "# Tạo thư mục .streamlit\n",
                    "streamlit_dir = Path.home() / \".streamlit\"\n",
                    "streamlit_dir.mkdir(exist_ok=True)\n\n",
                    "# Tạo file config.toml\n",
                    "config_content = \"\"\"\n",
                    "[server]\n",
                    "headless = true\n",
                    "port = 8501\n",
                    "enableCORS = false\n",
                    "enableXsrfProtection = false\n\n",
                    "[browser]\n",
                    "gatherUsageStats = false\n",
                    "\"\"\"\n\n",
                    "config_file = streamlit_dir / \"config.toml\"\n",
                    "with open(config_file, 'w') as f:\n",
                    "    f.write(config_content)\n\n",
                    "print(\"✅ Đã cấu hình Streamlit!\")"
                ],
                "metadata": {"id": "setup_streamlit"},
                "execution_count": None,
                "outputs": []
            },

            # Step 6: Create admin tool files
            {
                "cell_type": "markdown",
                "source": ["## 📝 Bước 6: Tạo Admin Tool Files (nếu chưa có)"],
                "metadata": {"id": "step6"}
            },
            {
                "cell_type": "code",
                "source": [
                    "# Kiểm tra và tạo admin tool files nếu cần\n",
                    "import os\n",
                    "import json\n\n",
                    "def create_admin_tool_files():\n",
                    "    \"\"\"Tạo các file cần thiết cho admin tool\"\"\"\n",
                    "    \n",
                    "    # Kiểm tra xem có file main.py chưa\n",
                    "    if os.path.exists('admin_tool/main.py'):\n",
                    "        print(\"✅ Admin tool files đã tồn tại\")\n",
                    "        return\n",
                    "    \n",
                    "    print(\"📁 Tạo admin tool files...\")\n",
                    "    \n",
                    "    # Tạo thư mục\n",
                    "    os.makedirs('admin_tool/data', exist_ok=True)\n",
                    "    \n",
                    "    # Tạo requirements.txt\n",
                    "    requirements = \"\"\"streamlit>=1.28.0\n",
                    "requests>=2.31.0\n",
                    "PyYAML>=6.0\n",
                    "pathlib>=1.0.1\n",
                    "unicodedata2>=15.0.0\"\"\"\n",
                    "    \n",
                    "    with open('admin_tool/requirements.txt', 'w') as f:\n",
                    "        f.write(requirements)\n",
                    "    print(\"✅ Tạo requirements.txt\")\n",
                    "    \n",
                    "    # Tạo platforms.json\n",
                    "    platforms_data = {\n",
                    "        \"platforms\": [\n",
                    "            {\n",
                    "                \"id\": 1,\n",
                    "                \"name\": \"TinyURL\",\n",
                    "                \"logo_url\": \"https://tinyurl.com/app/themes/tinyurl/images/tinyurl-logo.svg\",\n",
                    "                \"api_endpoint\": \"https://tinyurl.com/api-create.php\",\n",
                    "                \"curl_template\": \"curl -X POST \\\"https://tinyurl.com/api-create.php\\\" -d \\\"url=${link_download}\\\"\",\n",
                    "                \"response_format\": \"text\",\n",
                    "                \"response_path\": \"\",\n",
                    "                \"active\": True,\n",
                    "                \"icon\": \"fas fa-link\"\n",
                    "            },\n",
                    "            {\n",
                    "                \"id\": 2,\n",
                    "                \"name\": \"Is.gd\",\n",
                    "                \"logo_url\": \"https://is.gd/images/logo.png\",\n",
                    "                \"api_endpoint\": \"https://is.gd/create.php\",\n",
                    "                \"curl_template\": \"curl -X POST \\\"https://is.gd/create.php\\\" -d \\\"format=simple&url=${link_download}\\\"\",\n",
                    "                \"response_format\": \"text\",\n",
                    "                \"response_path\": \"\",\n",
                    "                \"active\": True,\n",
                    "                \"icon\": \"fas fa-compress-alt\"\n",
                    "            }\n",
                    "        ],\n",
                    "        \"last_updated\": \"2024-01-01T00:00:00\"\n",
                    "    }\n",
                    "    \n",
                    "    with open('admin_tool/data/platforms.json', 'w', encoding='utf-8') as f:\n",
                    "        json.dump(platforms_data, f, indent=2, ensure_ascii=False)\n",
                    "    print(\"✅ Tạo platforms.json\")\n",
                    "    \n",
                    "    print(\"✅ Đã tạo xong các file cần thiết!\")\n\n",
                    "# Chạy function\n",
                    "create_admin_tool_files()"
                ],
                "metadata": {"id": "create_files"},
                "execution_count": None,
                "outputs": []
            },

            # Step 7: Start admin tool
            {
                "cell_type": "markdown",
                "source": ["## 🚀 Bước 7: Khởi động Admin Tool"],
                "metadata": {"id": "step7"}
            },
            {
                "cell_type": "code",
                "source": [
                    "import subprocess\n",
                    "import threading\n",
                    "import time\n",
                    "from pyngrok import ngrok\n\n",
                    "# Kiểm tra admin tool có tồn tại không\n",
                    "admin_tool_path = \"/content/SSGEpub/admin_tool/main.py\"\n\n",
                    "if not os.path.exists(admin_tool_path):\n",
                    "    print(f\"❌ Không tìm thấy admin tool tại {admin_tool_path}\")\n",
                    "    print(\"🔄 Tạo file main.py cơ bản...\")\n",
                    "    \n",
                    "    # Tạo file main.py cơ bản\n",
                    "    main_py_content = '''import streamlit as st\n\n",
                    "st.set_page_config(\n",
                    "    page_title=\"📚 SSG Epub Admin Tool\",\n",
                    "    page_icon=\"📚\",\n",
                    "    layout=\"wide\"\n",
                    ")\n\n",
                    "st.markdown(\"\"\"\n",
                    "<div style=\"background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); \n",
                    "            padding: 1rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;\">\n",
                    "    <h1>📚 SSG Epub Admin Tool</h1>\n",
                    "    <p>Công cụ quản lý sách điện tử cho SSG Epub Library</p>\n",
                    "</div>\n",
                    "\"\"\", unsafe_allow_html=True)\n\n",
                    "st.success(\"🎉 Admin Tool đã khởi động thành công!\")\n",
                    "st.info(\"⚠️ Đây là phiên bản cơ bản. Vui lòng upload các file đầy đủ để sử dụng tất cả tính năng.\")\n\n",
                    "st.markdown(\"\"\"\n",
                    "## 📋 Tính năng sẽ có:\n",
                    "- ➕ **Thêm sách mới** với tự động rút gọn link\n",
                    "- 🔗 **Quản lý platforms** rút gọn URL\n",
                    "- 🔄 **Convert hàng loạt** sách cũ\n",
                    "- 📤 **Tự động Git operations**\n",
                    "- ⚙️ **Cài đặt và quản lý**\n\n",
                    "## 🔧 Để sử dụng đầy đủ:\n",
                    "1. Upload các file: `epub_manager.py`, `shortener_manager.py`, `git_manager.py`\n",
                    "2. Hoặc clone repository có đầy đủ files\n",
                    "3. Restart admin tool\n",
                    "\"\"\")\n",
                    "'''\n",
                    "    \n",
                    "    with open(admin_tool_path, 'w', encoding='utf-8') as f:\n",
                    "        f.write(main_py_content)\n",
                    "    \n",
                    "    print(\"✅ Đã tạo file main.py cơ bản\")\n\n",
                    "print(\"🚀 Đang khởi động Admin Tool...\")\n\n",
                    "# Tạo ngrok tunnel\n",
                    "try:\n",
                    "    public_url = ngrok.connect(8501)\n",
                    "    print(f\"\\n🌐 Admin Tool URL: {public_url}\")\n",
                    "    print(f\"📱 Truy cập URL trên để sử dụng admin tool\")\n",
                    "    print(f\"⏰ Tool sẽ khởi động trong vài giây...\\n\")\n",
                    "except Exception as e:\n",
                    "    print(f\"⚠️ Không thể tạo ngrok tunnel: {e}\")\n",
                    "    print(\"Admin tool sẽ chạy trên localhost:8501\")\n\n",
                    "# Khởi động Streamlit\n",
                    "!streamlit run {admin_tool_path} --server.port 8501 --server.headless true"
                ],
                "metadata": {"id": "start_admin_tool"},
                "execution_count": None,
                "outputs": []
            }
        ]
    }
    
    return notebook

def main():
    """Tạo và lưu notebook"""
    print("📝 Tạo Google Colab notebook...")
    
    notebook = create_colab_notebook()
    
    # Lưu notebook với custom JSON encoder
    notebook_json = json.dumps(notebook, indent=2, ensure_ascii=False)
    # Replace None with null for proper JSON
    notebook_json = notebook_json.replace(': None,', ': null,')

    with open('SSG_Epub_Admin_Tool_Ready.ipynb', 'w', encoding='utf-8') as f:
        f.write(notebook_json)

    print("✅ Đã tạo notebook: SSG_Epub_Admin_Tool_Ready.ipynb")
    print("\n🚀 Cách sử dụng:")
    print("1. Upload file này lên Google Colab")
    print("2. Chạy từng cell theo thứ tự")
    print("3. Truy cập URL được tạo bởi ngrok")

if __name__ == "__main__":
    main()
