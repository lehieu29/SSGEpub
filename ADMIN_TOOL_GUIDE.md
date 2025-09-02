# 📚 SSG Epub Admin Tool - Hướng dẫn đầy đủ

## 🎯 Tổng quan

SSG Epub Admin Tool là công cụ quản lý sách điện tử được xây dựng bằng Python và Streamlit, cho phép:

- ✅ **Tạo sách mới** với tự động rút gọn link hoặc nhập thủ công
- ✅ **Quản lý platforms** rút gọn URL (TinyURL, Is.gd, v.v.)
- ✅ **Convert hàng loạt** sách cũ sang platform mới
- ✅ **Tự động Git operations** (add, commit, push)
- ✅ **Chạy trên Google Colab** với ngrok tunnel
- ✅ **Giao diện thân thiện** với Streamlit

## 🚀 Cách sử dụng

### 📱 Option 1: Google Colab (Khuyến nghị)

#### Cách 1: Sử dụng Notebook có sẵn
1. **Mở Google Colab**: https://colab.research.google.com
2. **Upload notebook**: Upload file `admin_tool/colab_notebook.ipynb`
3. **Chạy từng cell** theo thứ tự và nhập thông tin khi được yêu cầu
4. **Truy cập URL** được tạo bởi ngrok

#### Cách 2: Setup thủ công
```python
# Cell 1: Install packages
!pip install streamlit requests PyYAML pyngrok

# Cell 2: Clone repository
!git clone https://github.com/your-username/SSGEpub.git
%cd SSGEpub

# Cell 3: Setup ngrok
from pyngrok import ngrok
ngrok.set_auth_token("your_ngrok_token")  # Lấy từ ngrok.com

# Cell 4: Setup environment
import os
os.environ['GITHUB_TOKEN'] = 'your_github_token'

# Cell 5: Start admin tool
public_url = ngrok.connect(8501)
print(f"Admin Tool URL: {public_url}")
!streamlit run admin_tool/main.py --server.port 8501 --server.headless true
```

#### Cách 3: Quick start script
```python
# Download và chạy script setup
!wget https://raw.githubusercontent.com/your-username/SSGEpub/main/admin_tool/run_colab.py
!python run_colab.py
```

### 💻 Option 2: Local Development

```bash
# Clone repository
git clone https://github.com/your-username/SSGEpub.git
cd SSGEpub

# Install dependencies
pip install -r admin_tool/requirements.txt

# Start admin tool
streamlit run admin_tool/main.py
```

Truy cập: http://localhost:8501

## 🔧 Cấu hình cần thiết

### 1. GitHub Personal Access Token
- Vào GitHub Settings > Developer settings > Personal access tokens
- Tạo token mới với quyền `repo`
- Copy token và nhập vào admin tool

### 2. Ngrok Auth Token (cho Colab)
- Đăng ký tại https://ngrok.com
- Lấy auth token từ dashboard
- Nhập token khi setup

## 📖 Hướng dẫn sử dụng từng tính năng

### ➕ Thêm Sách Mới

1. **Nhập thông tin cơ bản:**
   - Tên sách (bắt buộc)
   - Tác giả (bắt buộc)
   - URL ảnh bìa (bắt buộc)
   - Mô tả (bắt buộc)
   - Các thông tin khác (tùy chọn)

2. **Chọn phương thức link download:**

   **🤖 Tự động rút gọn:**
   - Nhập link Google Drive
   - Chọn platform rút gọn
   - Hệ thống tự động rút gọn và tạo sách

   **✋ Nhập thủ công:**
   - Nhập số lượng link
   - Nhập từng link đã được rút gọn
   - Nhập tên platform và logo

3. **Tạo sách:**
   - Nhấn "Tạo Sách"
   - Hệ thống tự động:
     - Tạo file markdown
     - Commit và push lên GitHub
     - Trigger Jekyll build

### 🔗 Quản lý Platform Rút gọn

#### Platforms có sẵn:
- **TinyURL**: Miễn phí, không cần API key
- **Is.gd**: Miễn phí, không cần API key
- **V.gd**: Miễn phí, không cần API key

#### Thêm platform mới:
1. Vào tab "Quản lý Platform"
2. Điền thông tin:
   - **Tên Platform**: Tên hiển thị
   - **URL Logo**: Link logo platform
   - **API Endpoint**: URL API của platform
   - **cURL Template**: Template để gọi API
   - **Response Format**: text hoặc json
   - **JSON Path**: Đường dẫn đến short URL (nếu JSON)

#### Ví dụ cURL Template:
```bash
# Text response
curl -X POST "https://tinyurl.com/api-create.php" -d "url=${link_download}"

# JSON response với API key
curl -X POST "https://api-ssl.bitly.com/v4/shorten" -H "Authorization: Bearer ${api_key}" -H "Content-Type: application/json" -d "{\"long_url\": \"${link_download}\"}"
```

### 🔄 Convert Sách Cũ

1. **Chọn platform đích** từ danh sách platforms active
2. **Chọn chế độ convert:**
   - **Convert tất cả**: Convert tất cả links
   - **Convert từ Google Drive**: Chỉ convert Google Drive links
3. **Nhấn "Bắt đầu Convert"**
4. **Hệ thống sẽ:**
   - Đọc tất cả file markdown
   - Extract download links
   - Convert links sang platform mới
   - Update file markdown
   - Batch commit và push

### ⚙️ Cài Đặt

- **Git Settings**: Cấu hình user name, email, GitHub token
- **Data Management**: Refresh cache, export data
- **Statistics**: Xem thống kê hệ thống

## 🎨 Cấu trúc File

### Markdown Template
```yaml
---
layout: epub
title: "Tên sách"
author: "Tác giả"
cover_image: "URL ảnh bìa"
preview_image: "URL ảnh preview"
isbn: "ISBN"
published_date: "YYYY-MM-DD"
genre: ["Thể loại 1", "Thể loại 2"]
description: "Mô tả sách"
rating: 4.5
pages: 280
language: "Tiếng Việt"
publisher: "Nhà xuất bản"
preview_content: |
  Nội dung preview...
download_links:
  - platform: "Platform Name"
    url: "https://short.url"
    index: 1
    icon: "fas fa-download"
tags: ["tag1", "tag2"]
---

Đây là trang chi tiết của cuốn sách "{{ page.title }}" của tác giả {{ page.author }}.
```

### Platform Configuration
```json
{
  "id": 1,
  "name": "TinyURL",
  "logo_url": "https://tinyurl.com/logo.svg",
  "api_endpoint": "https://tinyurl.com/api-create.php",
  "curl_template": "curl -X POST \"https://tinyurl.com/api-create.php\" -d \"url=${link_download}\"",
  "response_format": "text",
  "response_path": "",
  "active": true,
  "icon": "fas fa-link"
}
```

## 🛠️ Troubleshooting

### Lỗi thường gặp:

#### 1. Git operations failed
**Nguyên nhân:** GitHub token không đúng hoặc không có quyền
**Giải pháp:**
- Kiểm tra GitHub token có quyền `repo`
- Verify repository URL
- Kiểm tra git config (user.name, user.email)

#### 2. Platform rút gọn không hoạt động
**Nguyên nhân:** cURL template sai hoặc API thay đổi
**Giải pháp:**
- Test platform trước khi sử dụng
- Kiểm tra cURL template syntax
- Verify response format và path

#### 3. Streamlit không khởi động
**Nguyên nhân:** Package chưa cài đặt hoặc port bị chiếm
**Giải pháp:**
- Reinstall packages: `pip install -r requirements.txt`
- Thử port khác: `--server.port 8502`
- Restart runtime (Colab)

#### 4. Ngrok không hoạt động
**Nguyên nhân:** Auth token không đúng
**Giải pháp:**
- Lấy token mới từ ngrok.com
- Set token: `ngrok.set_auth_token("your_token")`

### Debug commands:

```python
# Kiểm tra trạng thái
import os
print(f"Current dir: {os.getcwd()}")
print(f"Admin tool exists: {os.path.exists('admin_tool/main.py')}")
print(f"GitHub token: {'✅' if os.environ.get('GITHUB_TOKEN') else '❌'}")

# Test git
!git status

# Test packages
!pip list | grep streamlit
```

## 🧪 Testing

Chạy test suite để kiểm tra:
```bash
cd admin_tool
python test_admin_tool.py
```

Test sẽ kiểm tra:
- ✅ EpubManager functionality
- ✅ ShortenerManager functionality  
- ✅ GitManager functionality
- ✅ Integration between components

## 📊 Workflow hoàn chỉnh

### Tạo sách mới:
1. User nhập thông tin sách
2. Chọn phương thức link (auto/manual)
3. Nếu auto: nhập Google Drive link + chọn platform
4. Hệ thống rút gọn URL (nếu cần)
5. Generate markdown file
6. Save vào `_epubs/`
7. Git add + commit + push
8. Jekyll build tự động trigger

### Convert sách cũ:
1. User chọn platform đích
2. Hệ thống scan tất cả file markdown
3. Extract download links từ mỗi file
4. Convert Google Drive links sang platform mới
5. Update markdown files
6. Batch git commit + push
7. Jekyll rebuild toàn bộ site

## 🎯 Best Practices

1. **Backup trước khi convert**: Luôn backup repository trước khi convert hàng loạt
2. **Test platform**: Test platform mới trước khi sử dụng
3. **Commit messages**: Sử dụng commit messages có ý nghĩa
4. **Regular updates**: Cập nhật admin tool thường xuyên
5. **Monitor builds**: Theo dõi GitHub Actions builds

## 🔮 Tính năng tương lai

- [ ] **Batch import** từ CSV/Excel
- [ ] **Advanced search** và filter
- [ ] **Book templates** cho các thể loại khác nhau
- [ ] **Analytics dashboard** với charts
- [ ] **Multi-language support**
- [ ] **API integration** với các book databases
- [ ] **Automated testing** với GitHub Actions
- [ ] **Docker deployment** option

---

**🎉 Chúc bạn sử dụng admin tool hiệu quả!**
