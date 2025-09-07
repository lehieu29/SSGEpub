// Admin Panel JavaScript

/**
 * Simple obfuscation utilities (shared with frontend)
 * Purpose: Hide download URLs from basic inspection
 */
class LinkObfuscator {
    static encode(url) {
        try {
            // Simple XOR with key + Base64
            const key = 'SSGEpub2024';
            let result = '';
            for (let i = 0; i < url.length; i++) {
                result += String.fromCharCode(
                    url.charCodeAt(i) ^ key.charCodeAt(i % key.length)
                );
            }
            return btoa(result);
        } catch (e) {
            console.error('Failed to encode URL:', e);
            return url;
        }
    }
    
    static decode(encoded) {
        try {
            const key = 'SSGEpub2024';
            const decoded = atob(encoded);
            let result = '';
            for (let i = 0; i < decoded.length; i++) {
                result += String.fromCharCode(
                    decoded.charCodeAt(i) ^ key.charCodeAt(i % key.length)
                );
            }
            return result;
        } catch (e) {
            console.error('Failed to decode URL:', e);
            return null;
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetTab = this.dataset.tab;
            
            // Remove active class from all tabs and contents
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            this.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
    
    // Download links management
    let downloadLinkIndex = 1;
    
    function addDownloadLink() {
        const container = document.getElementById('downloadLinksContainer');
        const newLink = document.createElement('div');
        newLink.className = 'download-link-item';
        newLink.innerHTML = `
            <div class="form-row">
                <div class="form-group">
                    <label>Platform</label>
                    <select name="platform[]" required>
                        <option value="">Chọn platform</option>
                        <option value="Google Drive">Google Drive</option>
                        <option value="OneDrive">OneDrive</option>
                        <option value="Mega">Mega</option>
                        <option value="MediaFire">MediaFire</option>
                        <option value="Dropbox">Dropbox</option>
                        <option value="Other">Khác</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>URL</label>
                    <input type="url" name="download_url[]" required placeholder="https://...">
                </div>
                <div class="form-group">
                    <label>Index</label>
                    <input type="number" name="download_index[]" min="0" required placeholder="${downloadLinkIndex}">
                </div>
                <div class="form-group">
                    <button type="button" class="btn-remove-link">Xóa</button>
                </div>
            </div>
        `;
        container.appendChild(newLink);
        downloadLinkIndex++;
        
        // Add event listener to remove button
        newLink.querySelector('.btn-remove-link').addEventListener('click', function() {
            newLink.remove();
        });
    }
    
    // Add download link button
    document.getElementById('addDownloadLink').addEventListener('click', addDownloadLink);
    
    // Remove download link buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-remove-link')) {
            const linkItem = e.target.closest('.download-link-item');
            if (document.querySelectorAll('.download-link-item').length > 1) {
                linkItem.remove();
            } else {
                alert('Phải có ít nhất một link tải xuống');
            }
        }
    });
    
    // Form submission
    document.getElementById('addBookForm').addEventListener('submit', function(e) {
        e.preventDefault();
        generateMarkdownFile();
    });
    
    // Preview button
    document.getElementById('previewBtn').addEventListener('click', function() {
        const previewContent = document.getElementById('preview_content').value;
        showPreview(previewContent);
    });
    
    // Reset button
    document.getElementById('resetBtn').addEventListener('click', function() {
        if (confirm('Bạn có chắc muốn reset form? Tất cả dữ liệu sẽ bị mất.')) {
            document.getElementById('addBookForm').reset();
            // Reset download links to just one
            const container = document.getElementById('downloadLinksContainer');
            const links = container.querySelectorAll('.download-link-item');
            for (let i = 1; i < links.length; i++) {
                links[i].remove();
            }
            downloadLinkIndex = 1;
        }
    });
    
    // Generate markdown file
    function generateMarkdownFile() {
        const form = document.getElementById('addBookForm');
        const formData = new FormData(form);
        
        // Validate required fields
        const requiredFields = ['title', 'author', 'cover_image', 'description', 'preview_content'];
        for (let field of requiredFields) {
            if (!formData.get(field)) {
                alert(`Vui lòng điền ${field}`);
                return;
            }
        }
        
        // Generate filename
        const title = formData.get('title');
        const filename = generateFilename(title);
        
        // Build download links array
        const platforms = formData.getAll('platform[]');
        const urls = formData.getAll('download_url[]');
        const indices = formData.getAll('download_index[]');
        
        const downloadLinks = [];
        for (let i = 0; i < platforms.length; i++) {
            if (platforms[i] && urls[i]) {
                
                // Encode URL for obfuscation
                const encodedUrl = `data:encoded,${LinkObfuscator.encode(urls[i])}`;
                
                downloadLinks.push({
                    platform: platforms[i],
                    url: encodedUrl,  // Use encoded URL
                    index: parseInt(indices[i]) || i,
                    icon: getIconForPlatform(platforms[i])
                });
            }
        }
        
        // Build genres array
        const genresStr = formData.get('genres') || '';
        const genres = genresStr.split(',').map(g => g.trim()).filter(g => g);
        
        // Build tags array
        const tagsStr = formData.get('tags') || '';
        const tags = tagsStr.split(',').map(t => t.trim()).filter(t => t);
        
        // Generate YAML front matter
        const frontMatter = {
            layout: 'epub',
            title: formData.get('title'),
            author: formData.get('author'),
            cover_image: formData.get('cover_image'),
            preview_image: formData.get('preview_image') || null,
            isbn: formData.get('isbn') || null,
            published_date: formData.get('published_date') || null,
            genre: genres,
            description: formData.get('description'),
            rating: parseFloat(formData.get('rating')) || null,
            pages: parseInt(formData.get('pages')) || null,
            language: formData.get('language') || null,
            publisher: formData.get('publisher') || null,
            preview_content: formData.get('preview_content'),
            download_links: downloadLinks,
            download_config_url: formData.get('config_url') || null,
            tags: tags
        };
        
        // Generate markdown content
        const markdown = generateMarkdown(frontMatter);
        
        // Show generated markdown
        showGeneratedMarkdown(filename, markdown);
    }
    
    function removeVietnameseTones(str) {
        str = str.replace(/à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ/g, 'a');
        str = str.replace(/è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ/g, 'e');
        str = str.replace(/ì|í|ị|ỉ|ĩ/g, 'i');
        str = str.replace(/ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ/g, 'o');
        str = str.replace(/ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ/g, 'u');
        str = str.replace(/ỳ|ý|ỵ|ỷ|ỹ/g, 'y');
        str = str.replace(/đ/g, 'd');
        str = str.replace(/À|Á|Ạ|Ả|Ã|Â|Ầ|Ấ|Ậ|Ẩ|Ẫ|Ă|Ằ|Ắ|Ặ|Ẳ|Ẵ/g, 'A');
        str = str.replace(/È|É|Ẹ|Ẻ|Ẽ|Ê|Ề|Ế|Ệ|Ể|Ễ/g, 'E');
        str = str.replace(/Ì|Í|Ị|Ỉ|Ĩ/g, 'I');
        str = str.replace(/Ò|Ó|Ọ|Ỏ|Õ|Ô|Ồ|Ố|Ộ|Ổ|Ỗ|Ơ|Ờ|Ớ|Ợ|Ở|Ỡ/g, 'O');
        str = str.replace(/Ù|Ú|Ụ|Ủ|Ũ|Ư|Ừ|Ứ|Ự|Ử|Ữ/g, 'U');
        str = str.replace(/Ỳ|Ý|Ỵ|Ỷ|Ỹ/g, 'Y');
        str = str.replace(/Đ/g, 'D');
        // Some system encode vietnamese combining accent as individual utf-8 characters
        str = str.replace(/\u0300|\u0301|\u0303|\u0309|\u0323/g, ''); // ̀ ́ ̃ ̉ ̣  huyền, sắc, ngã, hỏi, nặng
        str = str.replace(/\u02C6|\u0306|\u031B/g, ''); // ˆ ̆ ̛  Â, Ê, Ă, Ơ, Ư
        // Remove extra spaces
        str = str.replace(/ + /g, ' ');
        str = str.trim();
        return str;
    }

    function generateFilename(title) {
        // Remove Vietnamese tones first
        const cleanTitle = removeVietnameseTones(title);
        return cleanTitle
            .toLowerCase()
            .replace(/[^a-z0-9\s]/g, '')
            .replace(/\s+/g, '-')
            .substring(0, 50) + '.md';
    }
    
    function getIconForPlatform(platform) {
        const icons = {
            'Google Drive': 'fab fa-google-drive',
            'OneDrive': 'fab fa-microsoft',
            'Mega': 'fas fa-cloud-download-alt',
            'MediaFire': 'fas fa-fire',
            'Dropbox': 'fab fa-dropbox'
        };
        return icons[platform] || 'fas fa-download';
    }
    
    function generateMarkdown(data) {
        let yaml = '---\n';
        
        // Add each field to YAML
        for (const [key, value] of Object.entries(data)) {
            if (value === null || value === undefined) continue;
            
            if (Array.isArray(value)) {
                if (value.length > 0) {
                    yaml += `${key}:\n`;
                    value.forEach(item => {
                        if (typeof item === 'object') {
                            yaml += `  - platform: "${item.platform}"\n`;
                            yaml += `    url: "${item.url}"\n`;
                            yaml += `    index: ${item.index}\n`;
                            yaml += `    icon: "${item.icon}"\n`;
                        } else {
                            yaml += `  - "${item}"\n`;
                        }
                    });
                }
            } else if (key === 'preview_content') {
                yaml += `${key}: |\n`;
                const lines = value.split('\n');
                lines.forEach(line => {
                    yaml += `  ${line}\n`;
                });
            } else if (typeof value === 'string') {
                yaml += `${key}: "${value}"\n`;
            } else {
                yaml += `${key}: ${value}\n`;
            }
        }
        
        yaml += '---\n\n';
        yaml += `Đây là trang chi tiết của cuốn sách "{{ page.title }}" của tác giả {{ page.author }}.`;
        
        return yaml;
    }
    
    function showPreview(content) {
        const modal = document.getElementById('previewModal');
        const previewDiv = document.getElementById('previewContent');

        // Simple markdown to HTML conversion (basic)
        let html = content
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');

        html = '<p>' + html + '</p>';
        previewDiv.innerHTML = html;
        modal.style.display = 'block';
        modal.classList.add('show');
    }
    
    function showGeneratedMarkdown(filename, markdown) {
        const modal = document.getElementById('markdownModal');
        document.getElementById('generatedFilename').textContent = filename;
        document.getElementById('generatedPath').textContent = filename;
        document.getElementById('generatedMarkdown').value = markdown;
        modal.style.display = 'block';
        modal.classList.add('show');
    }
    
    // Modal functionality
    document.querySelectorAll('.modal .close').forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            const modal = this.closest('.modal');
            modal.style.display = 'none';
            modal.classList.remove('show');
        });
    });

    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
            e.target.classList.remove('show');
        }
    });
    
    // Copy to clipboard
    document.getElementById('copyMarkdown').addEventListener('click', async function() {
        const textarea = document.getElementById('generatedMarkdown');
        try {
            await navigator.clipboard.writeText(textarea.value);
            alert('Đã copy markdown vào clipboard!');
        } catch (err) {
            // Fallback for older browsers
            textarea.select();
            document.execCommand('copy');
            alert('Đã copy markdown vào clipboard!');
        }
    });
    
    // Download file
    document.getElementById('downloadMarkdown').addEventListener('click', function() {
        const filename = document.getElementById('generatedFilename').textContent;
        const content = document.getElementById('generatedMarkdown').value;
        
        const blob = new Blob([content], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
    
    // Load existing books for management
    function loadExistingBooks() {
        // This would typically fetch from an API or parse existing files
        // For now, we'll show a placeholder
        const booksList = document.getElementById('booksList');
        booksList.innerHTML = '<p>Chức năng quản lý sách sẽ được phát triển trong phiên bản tiếp theo.</p>';
    }
    
    // Initialize
    loadExistingBooks();
});
