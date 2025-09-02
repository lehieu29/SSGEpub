# 📚 SSG Epub Admin Tool

Công cụ quản lý sách điện tử cho SSG Epub Library được xây dựng bằng Python và Streamlit.

## 🎯 Tính năng chính

### ➕ Thêm Sách Mới
- Form nhập thông tin sách đầy đủ (tên, tác giả, mô tả, ảnh bìa, v.v.)
- Hỗ trợ 2 phương thức nhập link download:
  - **Tự động rút gọn**: Nhập link Google Drive, tự động rút gọn bằng platform đã chọn
  - **Nhập thủ công**: Nhập trực tiếp các link đã được rút gọn
- Tự động tạo file markdown trong thư mục `_epubs/`
- Tự động commit và push lên GitHub
- Trigger Jekyll build tự động

### 🔗 Quản lý Platform Rút gọn
- Thêm/sửa/xóa các platform rút gọn URL
- Cấu hình cURL template và response format
- Test platform trước khi sử dụng
- Hỗ trợ cả text và JSON response
- Quản lý logo và icon cho từng platform

### 🔄 Convert Sách Cũ
- Convert hàng loạt tất cả sách cũ sang platform mới
- Chọn convert tất cả hoặc chỉ Google Drive links
- Batch commit và push sau khi convert
- Báo cáo chi tiết kết quả convert

### ⚙️ Cài Đặt
- Cấu hình Git user và GitHub token
- Quản lý dữ liệu và cache
- Export/Import cấu hình
- Thống kê hệ thống

## 🚀 Cài đặt và Sử dụng

### 📱 Google Colab (Khuyến nghị)

1. **Tạo notebook mới trên Google Colab**

2. **Chạy setup script:**
```python
# Cell 1: Download và chạy setup
!wget https://raw.githubusercontent.com/your-username/SSGEpub/main/admin_tool/colab_setup.py
!python colab_setup.py
```

3. **Hoặc setup thủ công:**
```python
# Cell 1: Install packages
!pip install streamlit requests PyYAML pyngrok

# Cell 2: Clone repository
!git clone https://github.com/your-username/SSGEpub.git
%cd SSGEpub

# Cell 3: Setup ngrok (cần auth token từ ngrok.com)
from pyngrok import ngrok
ngrok.set_auth_token("your_ngrok_token")

# Cell 4: Setup environment
import os
os.environ['GITHUB_TOKEN'] = 'your_github_token'

# Cell 5: Start admin tool
public_url = ngrok.connect(8501)
print(f"Admin Tool URL: {public_url}")
!streamlit run admin_tool/main.py --server.port 8501 --server.headless true
```

### 💻 Local Development

1. **Clone repository:**
```bash
git clone https://github.com/your-username/SSGEpub.git
cd SSGEpub
```

2. **Install dependencies:**
```bash
pip install -r admin_tool/requirements.txt
```

3. **Start admin tool:**
```bash
streamlit run admin_tool/main.py
```

4. **Mở browser:** http://localhost:8501

## 🔧 Cấu hình

### GitHub Token
1. Vào GitHub Settings > Developer settings > Personal access tokens
2. Tạo token mới với quyền `repo`
3. Nhập token vào phần Cài đặt trong admin tool

### Ngrok Token (cho Colab)
1. Đăng ký tài khoản tại https://ngrok.com
2. Lấy auth token từ dashboard
3. Nhập token khi setup

### Platform Rút gọn
Admin tool đã có sẵn 3 platform mặc định:
- **TinyURL**: Miễn phí, không cần API key
- **Is.gd**: Miễn phí, không cần API key  
- **V.gd**: Miễn phí, không cần API key

Bạn có thể thêm platform khác bằng cách:
1. Vào tab "Quản lý Platform"
2. Điền thông tin platform mới
3. Cấu hình cURL template và response format

## 📁 Cấu trúc File

```
admin_tool/
├── main.py              # Streamlit app chính
├── epub_manager.py      # Quản lý sách
├── shortener_manager.py # Quản lý platform rút gọn
├── git_manager.py       # Quản lý Git operations
├── colab_setup.py       # Setup script cho Colab
├── requirements.txt     # Dependencies
├── README.md           # Documentation
└── data/
    ├── platforms.json   # Cấu hình platforms
    └── books_cache.json # Cache sách (tự động tạo)
```

## 🔗 Platform Configuration

### Text Response Platform
```json
{
  "name": "TinyURL",
  "api_endpoint": "https://tinyurl.com/api-create.php",
  "curl_template": "curl -X POST \"https://tinyurl.com/api-create.php\" -d \"url=${link_download}\"",
  "response_format": "text",
  "response_path": ""
}
```

### JSON Response Platform
```json
{
  "name": "Bit.ly",
  "api_endpoint": "https://api-ssl.bitly.com/v4/shorten",
  "curl_template": "curl -X POST \"https://api-ssl.bitly.com/v4/shorten\" -H \"Authorization: Bearer ${api_key}\" -H \"Content-Type: application/json\" -d \"{\\\"long_url\\\": \\\"${link_download}\\\"}\"",
  "response_format": "json",
  "response_path": "link"
}
```

## 🎨 Markdown Template

Sách được tạo theo template:

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

## 🔄 Workflow

### Tạo Sách Mới
1. Nhập thông tin sách
2. Chọn phương thức link download
3. Nếu tự động: nhập Google Drive link + chọn platform
4. Nếu thủ công: nhập các link đã rút gọn
5. Preview markdown
6. Tạo file và push lên GitHub

### Convert Sách Cũ
1. Chọn platform đích
2. Chọn chế độ convert (tất cả hoặc chỉ Google Drive)
3. Hệ thống tự động:
   - Đọc tất cả file markdown
   - Extract download links
   - Convert links sang platform mới
   - Update file markdown
   - Batch commit và push

## 🛠️ Troubleshooting

### Lỗi Git
- Kiểm tra GitHub token có đúng quyền
- Đảm bảo repository URL chính xác
- Kiểm tra git config (user.name, user.email)

### Lỗi Platform Rút gọn
- Test platform trước khi sử dụng
- Kiểm tra cURL template syntax
- Verify response format và path

### Lỗi Colab
- Restart runtime nếu có lỗi package
- Kiểm tra ngrok token
- Đảm bảo repository được clone đúng

## 📊 Thống kê

Admin tool cung cấp thống kê:
- Tổng số sách
- Số platform active
- Thống kê theo thể loại, tác giả
- Lịch sử convert

## 🔒 Bảo mật

- GitHub token được lưu trong environment variable
- Không commit token vào repository
- Sử dụng HTTPS cho tất cả API calls
- Validate input trước khi xử lý

## 🆘 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra logs trong Streamlit
2. Verify cấu hình Git và GitHub
3. Test platform configuration
4. Restart admin tool

## 📝 Changelog

### v1.0.0
- ✅ Tạo sách mới với auto/manual link input
- ✅ Quản lý platform rút gọn
- ✅ Batch convert sách cũ
- ✅ Git integration
- ✅ Google Colab support
- ✅ Streamlit UI
