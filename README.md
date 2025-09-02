# 📚 SSG Epub Library - Thư viện Sách Điện tử

Một trang web tĩnh (Static Site Generator) được xây dựng bằng Jekyll để hiển thị và chia sẻ sách điện tử Epub với preview nội dung và download links từ nhiều platform.

![SSG Epub Library](https://via.placeholder.com/800x400/007bff/ffffff?text=SSG+Epub+Library)

## ✨ Tính năng chính

### 📖 Quản lý Epub
- Hiển thị thông tin chi tiết sách (tác giả, thể loại, mô tả, rating...)
- Preview nội dung sách với hỗ trợ Markdown
- Ảnh bìa và ảnh preview từ các dịch vụ cloud storage
- Phân loại theo tags và thể loại

### 🔗 Download Links Động
- Hỗ trợ nhiều platform: Google Drive, OneDrive, Mega, MediaFire, Dropbox
- Cấu hình động qua API để hiển thị link download theo ý muốn
- Fallback tự động khi API không khả dụng
- Caching thông minh để tối ưu performance

### 🎨 Giao diện đẹp & Responsive
- Thiết kế responsive cho mọi thiết bị (mobile, tablet, desktop)
- Hỗ trợ Dark mode tự động
- Grid/List view cho danh sách sách
- Tìm kiếm và lọc theo thể loại, tác giả
- Animations mượt mà và transitions đẹp mắt

### ⚡ Tính năng nâng cao
- Thanh tiến trình đọc (scroll progress bar)
- Ước tính thời gian đọc preview
- Copy link và in trang
- Phím tắt (Ctrl+P, Ctrl+K, Esc)
- Nút quay lên đầu trang
- Lazy loading cho hình ảnh

### 👨‍💼 Admin Panel
- Form thêm sách mới với validation đầy đủ
- Preview Markdown trước khi tạo
- Tự động generate file markdown
- Quản lý nhiều download links
- Export và download file markdown

## 🚀 Hướng dẫn cài đặt chi tiết

### Bước 1: Cài đặt Ruby

#### Trên Windows:
1. Tải và cài đặt [Ruby+Devkit](https://rubyinstaller.org/downloads/) (khuyến nghị phiên bản 3.0+)
2. Trong quá trình cài đặt, chọn "Add Ruby executables to your PATH"
3. Mở Command Prompt hoặc PowerShell và kiểm tra:
```bash
ruby --version
gem --version
```

#### Trên macOS:
```bash
# Sử dụng Homebrew (khuyến nghị)
brew install ruby

# Hoặc sử dụng rbenv
brew install rbenv
rbenv install 3.0.0
rbenv global 3.0.0
```

#### Trên Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ruby-full build-essential zlib1g-dev

# Thêm vào ~/.bashrc
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Bước 2: Cài đặt Jekyll và Bundler
```bash
gem install jekyll bundler
```

### Bước 3: Clone và setup project
```bash
# Clone repository
git clone https://github.com/your-username/SSGEpub.git
cd SSGEpub

# Cài đặt dependencies
bundle install
```

### Bước 4: Chạy development server
```bash
# Chạy server với live reload
bundle exec jekyll serve --livereload

# Hoặc chạy trên tất cả network interfaces
bundle exec jekyll serve --host 0.0.0.0 --port 4000

# Truy cập trang web tại: http://localhost:4000
```

## 📁 Cấu trúc thư mục

```
SSGEpub/
├── _config.yml              # Cấu hình Jekyll
├── _epubs/                  # Collection chứa các sách
│   ├── sample-book.md       # Sách mẫu
│   ├── mat-biec.md
│   ├── toi-thay-hoa-vang.md
│   └── harry-potter.md
├── _layouts/
│   └── epub.html           # Layout cho trang chi tiết sách
├── _includes/
│   └── epub-card.html      # Component hiển thị card sách
├── admin/                  # Trang quản trị
│   ├── index.html          # Giao diện admin
│   └── admin.js           # JavaScript cho admin
├── assets/
│   ├── css/
│   │   └── epub-styles.scss # CSS tùy chỉnh
│   └── js/
│       ├── download-config.js    # Quản lý cấu hình download
│       └── epub-enhancements.js  # Tính năng nâng cao
├── epubs.html              # Trang danh sách tất cả sách
├── index.html              # Trang chủ
├── api-example.md          # Hướng dẫn tạo API
└── README.md               # File này
```

## 🌐 Các trang chính của website

Sau khi chạy `bundle exec jekyll serve`, bạn có thể truy cập:

### 🏠 [Trang chủ](http://localhost:4000/)
- Hiển thị sách nổi bật (rating >= 4.0)
- Thống kê tổng quan (số sách, thể loại, tác giả)
- Sách mới thêm gần đây
- Thể loại phổ biến

### 📚 [Thư viện sách](http://localhost:4000/epubs/)
- Danh sách tất cả sách dạng grid/list
- Tìm kiếm theo tên sách, tác giả
- Lọc theo thể loại
- Sắp xếp theo tên, tác giả, năm xuất bản, rating

### 👨‍💼 [Admin Panel](http://localhost:4000/admin/)
- Form thêm sách mới
- Quản lý thông tin sách
- Preview nội dung Markdown
- Generate và download file markdown

### 📖 Trang chi tiết sách
- Ví dụ: [http://localhost:4000/epubs/sample-book/](http://localhost:4000/epubs/sample-book/)
- Thông tin đầy đủ về sách
- Preview nội dung
- Download links từ nhiều platform
- Ước tính thời gian đọc

## 📝 Hướng dẫn thêm sách mới

### Cách 1: Sử dụng Admin Panel (Khuyến nghị)

1. **Truy cập Admin Panel**: [http://localhost:4000/admin/](http://localhost:4000/admin/)

2. **Điền thông tin sách**:
   - Thông tin cơ bản: Tên sách, tác giả, ISBN, ngày xuất bản...
   - Upload ảnh bìa và ảnh preview lên cloud storage (Google Drive, S3, etc.)
   - Dán URL ảnh vào form
   - Nhập thể loại (phân cách bằng dấu phẩy)
   - Viết mô tả sách
   - Nhập nội dung preview (hỗ trợ Markdown)

3. **Thêm download links**:
   - Chọn platform (Google Drive, OneDrive, Mega, etc.)
   - Dán URL download
   - Đặt index (0, 1, 2...) để phân biệt thứ tự

4. **Preview và tạo file**:
   - Click "Preview" để xem trước nội dung Markdown
   - Click "Tạo sách" để generate file markdown
   - Download file và copy vào thư mục `_epubs/`

5. **Rebuild website**:
```bash
# Dừng server (Ctrl+C) và chạy lại
bundle exec jekyll serve --livereload
```

### Cách 2: Tạo file markdown thủ công

Tạo file `.md` mới trong thư mục `_epubs/` với format:

```yaml
---
layout: epub
title: "Tên sách"
author: "Tác giả"
cover_image: "https://example.com/cover.jpg"
preview_image: "https://example.com/preview.jpg"
isbn: "978-xxx-xxx-xxx"
published_date: "2024-01-01"
genre: ["Thể loại 1", "Thể loại 2"]
description: "Mô tả ngắn gọn về sách"
rating: 4.5
pages: 300
language: "Tiếng Việt"
publisher: "NXB Trẻ"
preview_content: |
  Nội dung preview của sách...
  Hỗ trợ **Markdown** formatting.
download_links:
  - platform: "Google Drive"
    url: "https://drive.google.com/file/d/xxx/view"
    index: 0
    icon: "fab fa-google-drive"
  - platform: "OneDrive"
    url: "https://onedrive.live.com/download?cid=xxx"
    index: 1
    icon: "fab fa-microsoft"
download_config_url: "https://api.example.com/config/book-id"
tags: ["tag1", "tag2", "tag3"]
---

Nội dung bổ sung (tùy chọn)
```

## 🔧 Cấu hình API cho Download Links động

Để sử dụng tính năng hiển thị download links theo cấu hình động, bạn cần tạo API endpoint.

### Format JSON Response:
```json
{
  "activeIndices": [0, 1, 2]
}
```

### Ví dụ API đơn giản với PHP:
```php
<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$bookId = $_GET['book'] ?? '';

$configs = [
    'mat-biec' => ['activeIndices' => [0, 1]], // Chỉ hiển thị Google Drive và OneDrive
    'harry-potter' => ['activeIndices' => [2]], // Chỉ hiển thị Mega
    'default' => ['activeIndices' => [0, 1, 2]] // Hiển thị tất cả
];

$config = $configs[$bookId] ?? $configs['default'];
echo json_encode($config);
?>
```

### Cập nhật URL trong sách:
```yaml
download_config_url: "https://your-api.com/config.php?book=mat-biec"
```

**Lưu ý**: Nếu API không khả dụng, hệ thống sẽ tự động hiển thị tất cả download links.

## 🎨 Tùy chỉnh giao diện

### Thay đổi màu sắc chủ đạo:
Chỉnh sửa file `assets/css/epub-styles.scss`:

```scss
// Thay đổi màu primary
:root {
  --primary-color: #007bff;    // Màu xanh dương
  --success-color: #28a745;    // Màu xanh lá
  --danger-color: #dc3545;     // Màu đỏ
}
```

### Thêm CSS tùy chỉnh:
Thêm CSS vào file `_sass/custom.scss`:

```scss
/* Custom styles */
.my-custom-class {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
}
```

## 🚀 Deploy lên hosting

### GitHub Pages:
1. Push code lên GitHub repository
2. Vào Settings > Pages
3. Chọn source branch (thường là `main`)
4. Website sẽ có địa chỉ: `https://username.github.io/repository-name`

### Netlify:
1. Kết nối repository với Netlify
2. Build command: `bundle exec jekyll build`
3. Publish directory: `_site`
4. Deploy tự động khi push code

### Vercel:
1. Import project từ GitHub
2. Framework preset: Jekyll
3. Deploy

## 🛠 Lệnh hữu ích

```bash
# Chạy development server
bundle exec jekyll serve --livereload

# Build production
JEKYLL_ENV=production bundle exec jekyll build

# Chạy trên network (để test từ điện thoại)
bundle exec jekyll serve --host 0.0.0.0

# Clean build files
bundle exec jekyll clean

# Update dependencies
bundle update
```

## 🔍 Troubleshooting

### Lỗi "bundle: command not found":
```bash
gem install bundler
```

### Lỗi permission trên macOS/Linux:
```bash
sudo gem install bundler jekyll
```

### Lỗi encoding trên Windows:
Thêm vào đầu file `_config.yml`:
```yaml
encoding: utf-8
```

### Website không load CSS:
Kiểm tra file `_sass/custom.scss` có import đúng:
```scss
@import url('/assets/css/epub-styles.css');
```

## 📄 License

Dự án này sử dụng MIT License. Xem file `LICENSE` để biết chi tiết.

## 🙏 Credits

- **Base Theme**: [Jekyll TeXt Theme](https://github.com/kitian616/jekyll-TeXt-theme)
- **Icons**: [Font Awesome](https://fontawesome.com/)
- **Static Site Generator**: [Jekyll](https://jekyllrb.com/)

---

## 📞 Hỗ trợ

Nếu bạn gặp vấn đề:
1. Kiểm tra [Issues](../../issues) đã có
2. Tạo issue mới với mô tả chi tiết
3. Hoặc liên hệ qua email

**Happy reading! 📚✨**
