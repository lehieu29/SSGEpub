# API Configuration Example

Đây là ví dụ về cách cấu hình API endpoint để quản lý download links động.

## Format API Response

API endpoint cần trả về JSON với format sau:

### Hiển thị một link duy nhất:
```json
{
  "activeIndex": 0
}
```

### Hiển thị nhiều links:
```json
{
  "activeIndices": [0, 2]
}
```

### Response với metadata (tùy chọn):
```json
{
  "activeIndices": [1, 2],
  "message": "Showing OneDrive and Mega links",
  "timestamp": "2024-01-01T00:00:00Z",
  "bookId": "mat-biec"
}
```

## Ví dụ Implementation

### 1. Static JSON Files
Tạo file JSON tĩnh cho mỗi sách:

**config/mat-biec.json:**
```json
{
  "activeIndices": [0, 1],
  "message": "Google Drive và OneDrive available"
}
```

### 2. Simple PHP API
```php
<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$bookId = $_GET['book'] ?? '';

// Simple configuration based on book ID
$configs = [
    'mat-biec' => ['activeIndices' => [0, 1]],
    'toi-thay-hoa-vang' => ['activeIndices' => [0, 2]],
    'harry-potter-1' => ['activeIndices' => [1]]
];

if (isset($configs[$bookId])) {
    echo json_encode($configs[$bookId]);
} else {
    http_response_code(404);
    echo json_encode(['error' => 'Book not found']);
}
?>
```

### 3. Node.js Express API
```javascript
const express = require('express');
const app = express();

app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    next();
});

const configs = {
    'mat-biec': { activeIndices: [0, 1] },
    'toi-thay-hoa-vang': { activeIndices: [0, 2] },
    'harry-potter-1': { activeIndices: [1] }
};

app.get('/config/:bookId', (req, res) => {
    const bookId = req.params.bookId;
    const config = configs[bookId];
    
    if (config) {
        res.json(config);
    } else {
        res.status(404).json({ error: 'Book not found' });
    }
});

app.listen(3000, () => {
    console.log('API server running on port 3000');
});
```

### 4. Firebase Functions
```javascript
const functions = require('firebase-functions');

exports.getDownloadConfig = functions.https.onRequest((req, res) => {
    res.set('Access-Control-Allow-Origin', '*');
    
    const bookId = req.query.book;
    
    // Your logic here
    const config = getConfigForBook(bookId);
    
    res.json(config);
});
```

## Cách sử dụng

1. Deploy API endpoint của bạn
2. Cập nhật `download_config_url` trong file markdown của sách
3. Hệ thống sẽ tự động gọi API và hiển thị links theo cấu hình

## Error Handling

Nếu API không available hoặc trả về lỗi, hệ thống sẽ tự động fallback để hiển thị tất cả download links.

## Caching

Hệ thống có built-in caching 5 phút để tránh gọi API quá nhiều lần.
