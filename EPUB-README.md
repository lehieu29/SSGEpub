# SSG Epub Library

Một trang web tĩnh (SSG) được xây dựng bằng Jekyll để hiển thị và chia sẻ sách điện tử Epub với preview và download links từ nhiều platform.

## ✨ Tính năng

### 📚 Quản lý Epub
- Hiển thị thông tin chi tiết sách (tác giả, thể loại, mô tả, rating...)
- Preview nội dung sách với hỗ trợ Markdown
- Ảnh bìa và ảnh preview từ các dịch vụ cloud
- Tags và thể loại để phân loại

### 🔗 Download Links Động
- Hỗ trợ nhiều platform: Google Drive, OneDrive, Mega, MediaFire, Dropbox
- Cấu hình động qua API để hiển thị link theo ý muốn
- Fallback tự động khi API không available
- Caching để tối ưu performance

### 🎨 Giao diện đẹp
- Responsive design cho mọi thiết bị
- Dark mode support
- Grid/List view cho danh sách sách
- Search và filter theo thể loại, tác giả
- Smooth animations và transitions

### ⚡ Tính năng nâng cao
- Scroll progress bar
- Reading time estimation
- Copy link và print functionality
- Keyboard shortcuts
- Back to top button
- Image lazy loading

### 👨‍💼 Admin Panel
- Form thêm sách mới với validation
- Preview Markdown trước khi tạo
- Generate file markdown tự động
- Quản lý download links
- Export/download file markdown

## 🚀 Cài đặt

### Yêu cầu
- Ruby 2.7+
- Jekyll 4.0+
- Node.js (cho development)

### Cài đặt cơ bản
```bash
# Clone repository
git clone <your-repo-url>
cd SSGEpub

# Cài đặt dependencies
bundle install

# Chạy development server
bundle exec jekyll serve

# Truy cập http://localhost:4000
```

## 📁 Cấu trúc thư mục

```
├── _config.yml              # Cấu hình Jekyll
├── _epubs/                  # Collection chứa các sách
│   ├── sample-book.md
│   └── ...
├── _layouts/
│   └── epub.html           # Layout cho trang sách
├── _includes/
│   └── epub-card.html      # Component card sách
├── admin/                  # Trang admin
│   ├── index.html
│   └── admin.js
├── assets/
│   ├── css/
│   │   └── epub-styles.scss
│   └── js/
│       ├── download-config.js
│       └── epub-enhancements.js
├── epubs.html              # Trang danh sách sách
├── index.html              # Trang chủ
└── api-example.md          # Hướng dẫn API
```

## 📝 Thêm sách mới

### Cách 1: Sử dụng Admin Panel
1. Truy cập `/admin/`
2. Điền form thông tin sách
3. Preview nội dung
4. Generate và download file markdown
5. Upload file vào thư mục `_epubs/`

### Cách 2: Tạo file markdown thủ công
Tạo file `.md` trong thư mục `_epubs/` với format:

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
description: "Mô tả sách"
rating: 4.5
pages: 300
language: "Tiếng Việt"
publisher: "NXB"
preview_content: |
  Nội dung preview...
download_links:
  - platform: "Google Drive"
    url: "https://drive.google.com/..."
    index: 0
    icon: "fab fa-google-drive"
download_config_url: "https://api.example.com/config/book-id"
tags: ["tag1", "tag2"]
---

Nội dung bổ sung (tùy chọn)
```

## 🔧 Cấu hình API

Để sử dụng tính năng download links động, bạn cần tạo API endpoint trả về JSON:

### Format response:
```json
{
  "activeIndices": [0, 1, 2]
}
```

### Ví dụ implementation:
Xem file `api-example.md` để biết chi tiết cách implement API với PHP, Node.js, Firebase Functions...

## 🎨 Tùy chỉnh giao diện

### Thay đổi theme colors
Chỉnh sửa file `assets/css/epub-styles.scss`:

```scss
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --success-color: #28a745;
  // ...
}
```

### Thêm custom CSS
Thêm CSS vào file `_sass/custom.scss`

### Thay đổi layout
Chỉnh sửa các file trong `_layouts/` và `_includes/`

## 📱 Responsive Design

Trang web được thiết kế responsive với breakpoints:
- Mobile: < 768px
- Tablet: 768px - 1024px  
- Desktop: > 1024px

## 🔍 SEO Optimization

- Meta tags tự động từ thông tin sách
- Open Graph tags cho social sharing
- Structured data cho search engines
- Sitemap tự động generate
- RSS feed cho sách mới

## 🚀 Deploy

### GitHub Pages
1. Push code lên GitHub repository
2. Enable GitHub Pages trong Settings
3. Chọn source branch (thường là `main`)

### Netlify
1. Connect repository với Netlify
2. Build command: `bundle exec jekyll build`
3. Publish directory: `_site`

### Vercel
1. Import project từ GitHub
2. Framework preset: Jekyll
3. Deploy

## 🛠 Development

### Chạy development server
```bash
bundle exec jekyll serve --livereload
```

### Build production
```bash
JEKYLL_ENV=production bundle exec jekyll build
```

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Tạo Pull Request

## 📄 License

Dự án này sử dụng MIT License. Xem file `LICENSE` để biết chi tiết.

## 🙏 Credits

- [Jekyll TeXt Theme](https://github.com/kitian616/jekyll-TeXt-theme) - Base theme
- [Font Awesome](https://fontawesome.com/) - Icons
- [Jekyll](https://jekyllrb.com/) - Static site generator

---

**Happy reading! 📚✨**
