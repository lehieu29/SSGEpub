/**
 * Epub Library Enhancements
 * Additional JavaScript functionality for better UX
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Scroll Progress Bar
    function initScrollProgress() {
        const progressBar = document.createElement('div');
        progressBar.className = 'scroll-progress';
        document.body.appendChild(progressBar);
        
        function updateProgress() {
            const scrollTop = window.pageYOffset;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const scrollPercent = (scrollTop / docHeight) * 100;
            progressBar.style.width = scrollPercent + '%';
        }
        
        window.addEventListener('scroll', updateProgress);
        updateProgress();
    }
    
    // Smooth Scrolling for Anchor Links
    function initSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    // Image Lazy Loading Enhancement
    function initImageLazyLoading() {
        const images = document.querySelectorAll('img[loading="lazy"]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.classList.add('fade-in');
                        observer.unobserve(img);
                    }
                });
            });
            
            images.forEach(img => imageObserver.observe(img));
        }
    }
    
    // Reading Time Estimation
    function addReadingTime() {
        const previewContent = document.querySelector('.preview-content');
        if (previewContent) {
            const text = previewContent.textContent || previewContent.innerText;
            const wordsPerMinute = 200;
            const words = text.trim().split(/\s+/).length;
            const readingTime = Math.ceil(words / wordsPerMinute);
            
            const readingTimeElement = document.createElement('div');
            readingTimeElement.className = 'reading-time';
            readingTimeElement.innerHTML = `
                <i class="fas fa-clock"></i>
                <span>Thời gian đọc preview: ~${readingTime} phút</span>
            `;
            
            previewContent.parentNode.insertBefore(readingTimeElement, previewContent);
        }
    }
    
    // Copy Link Functionality
    function initCopyLink() {
        const copyBtn = document.createElement('button');
        copyBtn.className = 'nav-btn copy-link-btn';
        copyBtn.innerHTML = '<i class="fas fa-link"></i>';
        copyBtn.title = 'Copy link to this book';
        
        copyBtn.addEventListener('click', async function() {
            try {
                await navigator.clipboard.writeText(window.location.href);
                
                // Visual feedback
                const icon = this.querySelector('i');
                const originalClass = icon.className;
                icon.className = 'fas fa-check';
                this.style.color = '#28a745';
                
                setTimeout(() => {
                    icon.className = originalClass;
                    this.style.color = '';
                }, 2000);
                
            } catch (err) {
                console.error('Failed to copy link:', err);
            }
        });
        
        const navActions = document.querySelector('.nav-actions');
        if (navActions) {
            navActions.appendChild(copyBtn);
        }
    }
    
    // Print Functionality
    function initPrintButton() {
        const printBtn = document.createElement('button');
        printBtn.className = 'nav-btn print-btn';
        printBtn.innerHTML = '<i class="fas fa-print"></i>';
        printBtn.title = 'Print this page';
        
        printBtn.addEventListener('click', function() {
            window.print();
        });
        
        const navActions = document.querySelector('.nav-actions');
        if (navActions) {
            navActions.appendChild(printBtn);
        }
    }
    
    // Search Highlight
    function initSearchHighlight() {
        const urlParams = new URLSearchParams(window.location.search);
        const searchTerm = urlParams.get('highlight');
        
        if (searchTerm) {
            highlightText(searchTerm);
        }
    }
    
    function highlightText(term) {
        const content = document.querySelector('.epub-container');
        if (!content) return;
        
        const walker = document.createTreeWalker(
            content,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );
        
        const textNodes = [];
        let node;
        
        while (node = walker.nextNode()) {
            textNodes.push(node);
        }
        
        textNodes.forEach(textNode => {
            const parent = textNode.parentNode;
            if (parent.tagName === 'SCRIPT' || parent.tagName === 'STYLE') return;
            
            const text = textNode.textContent;
            const regex = new RegExp(`(${term})`, 'gi');
            
            if (regex.test(text)) {
                const highlightedHTML = text.replace(regex, '<mark class="search-highlight">$1</mark>');
                const wrapper = document.createElement('span');
                wrapper.innerHTML = highlightedHTML;
                parent.replaceChild(wrapper, textNode);
            }
        });
    }
    
    // Keyboard Shortcuts
    function initKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + P for print
            if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
                e.preventDefault();
                window.print();
            }
            
            // Ctrl/Cmd + K for copy link
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const copyBtn = document.querySelector('.copy-link-btn');
                if (copyBtn) copyBtn.click();
            }
            
            // Escape to close modals
            if (e.key === 'Escape') {
                const openModal = document.querySelector('.modal[style*="block"]');
                if (openModal) {
                    openModal.style.display = 'none';
                }
            }
        });
    }
    
    // Back to Top Button
    function initBackToTop() {
        const backToTopBtn = document.createElement('button');
        backToTopBtn.className = 'back-to-top';
        backToTopBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
        backToTopBtn.title = 'Back to top';
        
        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        
        document.body.appendChild(backToTopBtn);
        
        // Show/hide based on scroll position
        function toggleBackToTop() {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        }
        
        window.addEventListener('scroll', toggleBackToTop);
        toggleBackToTop();
    }
    
    // Initialize all enhancements
    function init() {
        initScrollProgress();
        initSmoothScrolling();
        initImageLazyLoading();
        addReadingTime();
        initSearchHighlight();
        initKeyboardShortcuts();
        initBackToTop();
        
        // Only add navigation buttons on epub pages
        if (document.querySelector('.layout--epub')) {
            // Create navigation if it doesn't exist
            if (!document.querySelector('.epub-navigation')) {
                const nav = document.createElement('div');
                nav.className = 'epub-navigation';
                nav.innerHTML = `
                    <div class="nav-container">
                        <div class="nav-links">
                            <a href="/epubs/">← Quay lại thư viện</a>
                        </div>
                        <div class="nav-actions">
                            <!-- Buttons will be added here -->
                        </div>
                    </div>
                `;
                
                const container = document.querySelector('.epub-container');
                if (container) {
                    container.parentNode.insertBefore(nav, container);
                }
            }
            
            initCopyLink();
            initPrintButton();
        }
    }
    
    // Run initialization
    init();
    
    // Add CSS for enhancements
    const style = document.createElement('style');
    style.textContent = `
        .fade-in {
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .reading-time {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #6c757d;
            font-size: 0.9rem;
            margin-bottom: 1rem;
            padding: 0.5rem 1rem;
            background: #f8f9fa;
            border-radius: 6px;
            border-left: 3px solid #007bff;
        }
        
        .search-highlight {
            background: #ffeb3b;
            padding: 0.1rem 0.2rem;
            border-radius: 3px;
        }
        
        .back-to-top {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 50px;
            height: 50px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 2px 10px rgba(0, 123, 255, 0.3);
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
            z-index: 1000;
        }
        
        .back-to-top.visible {
            opacity: 1;
            visibility: visible;
        }
        
        .back-to-top:hover {
            background: #0056b3;
            transform: translateY(-2px);
        }
        
        @media (max-width: 768px) {
            .back-to-top {
                bottom: 1rem;
                right: 1rem;
                width: 45px;
                height: 45px;
            }
        }
    `;
    
    document.head.appendChild(style);
});
