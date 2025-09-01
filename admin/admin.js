// Admin Panel JavaScript

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
                downloadLinks.push({
                    platform: platforms[i],
                    url: urls[i],
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
    
    function generateFilename(title) {
        return title
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
    }
    
    function showGeneratedMarkdown(filename, markdown) {
        const modal = document.getElementById('markdownModal');
        document.getElementById('generatedFilename').textContent = filename;
        document.getElementById('generatedPath').textContent = filename;
        document.getElementById('generatedMarkdown').value = markdown;
        modal.style.display = 'block';
    }
    
    // Modal functionality
    document.querySelectorAll('.modal .close').forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            this.closest('.modal').style.display = 'none';
        });
    });
    
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
        }
    });
    
    // Copy to clipboard
    document.getElementById('copyMarkdown').addEventListener('click', function() {
        const textarea = document.getElementById('generatedMarkdown');
        textarea.select();
        document.execCommand('copy');
        alert('Đã copy markdown vào clipboard!');
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
