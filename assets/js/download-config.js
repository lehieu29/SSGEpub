/**
 * Download Configuration Manager
 * Handles dynamic loading of download link configurations
 */

class DownloadConfigManager {
    constructor() {
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
        this.retryAttempts = 3;
        this.retryDelay = 1000; // 1 second
    }

    /**
     * Load download configuration for a specific book
     * @param {string} configUrl - The API endpoint URL
     * @param {Array} fallbackLinks - Default links to show if config fails
     * @returns {Promise<Array>} Array of active download links
     */
    async loadConfig(configUrl, fallbackLinks = []) {
        if (!configUrl) {
            console.log('No config URL provided, using all links');
            return fallbackLinks;
        }

        // Check cache first
        const cached = this.getFromCache(configUrl);
        if (cached) {
            console.log('Using cached config for:', configUrl);
            return this.filterLinks(cached, fallbackLinks);
        }

        try {
            const config = await this.fetchWithRetry(configUrl);
            
            // Cache the result
            this.setCache(configUrl, config);
            
            return this.filterLinks(config, fallbackLinks);
        } catch (error) {
            console.warn('Failed to load download config:', error);
            console.log('Falling back to all links');
            return fallbackLinks;
        }
    }

    /**
     * Fetch configuration with retry logic
     * @param {string} url - The URL to fetch
     * @returns {Promise<Object>} The configuration object
     */
    async fetchWithRetry(url) {
        let lastError;
        
        for (let attempt = 1; attempt <= this.retryAttempts; attempt++) {
            try {
                console.log(`Fetching config (attempt ${attempt}/${this.retryAttempts}):`, url);
                
                const response = await fetch(url, {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                        'Cache-Control': 'no-cache'
                    },
                    timeout: 10000 // 10 seconds timeout
                });

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

                const config = await response.json();
                console.log('Config loaded successfully:', config);
                return config;
                
            } catch (error) {
                lastError = error;
                console.warn(`Attempt ${attempt} failed:`, error.message);
                
                if (attempt < this.retryAttempts) {
                    await this.delay(this.retryDelay * attempt);
                }
            }
        }
        
        throw lastError;
    }

    /**
     * Filter links based on configuration
     * @param {Object} config - The configuration object
     * @param {Array} allLinks - All available download links
     * @returns {Array} Filtered download links
     */
    filterLinks(config, allLinks) {
        if (!config || !allLinks || allLinks.length === 0) {
            return allLinks;
        }

        // Support both single index and multiple indices
        let activeIndices = [];
        
        if (Array.isArray(config.activeIndices)) {
            activeIndices = config.activeIndices;
        } else if (typeof config.activeIndex === 'number') {
            activeIndices = [config.activeIndex];
        } else if (typeof config.index === 'number') {
            activeIndices = [config.index];
        } else {
            console.warn('Invalid config format, using all links');
            return allLinks;
        }

        // Filter links by active indices
        const filteredLinks = allLinks.filter(link => 
            activeIndices.includes(link.index)
        );

        if (filteredLinks.length === 0) {
            console.warn('No links match the active indices, using all links');
            return allLinks;
        }

        console.log(`Filtered ${filteredLinks.length} links from ${allLinks.length} total`);
        return filteredLinks;
    }

    /**
     * Get configuration from cache
     * @param {string} url - The cache key
     * @returns {Object|null} Cached configuration or null
     */
    getFromCache(url) {
        const cached = this.cache.get(url);
        if (!cached) return null;

        const now = Date.now();
        if (now - cached.timestamp > this.cacheTimeout) {
            this.cache.delete(url);
            return null;
        }

        return cached.data;
    }

    /**
     * Set configuration in cache
     * @param {string} url - The cache key
     * @param {Object} data - The data to cache
     */
    setCache(url, data) {
        this.cache.set(url, {
            data: data,
            timestamp: Date.now()
        });
    }

    /**
     * Clear all cached configurations
     */
    clearCache() {
        this.cache.clear();
        console.log('Download config cache cleared');
    }

    /**
     * Delay execution for specified milliseconds
     * @param {number} ms - Milliseconds to delay
     * @returns {Promise} Promise that resolves after delay
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Render download buttons in the specified container
     * @param {HTMLElement} container - The container element
     * @param {Array} links - Array of download links
     */
    renderDownloadButtons(container, links) {
        if (!container || !links || links.length === 0) {
            console.warn('Invalid container or links for rendering');
            return;
        }

        // Clear existing content
        container.innerHTML = '';

        // Create buttons for each link
        links.forEach(link => {
            const button = document.createElement('a');
            button.href = link.url;
            button.className = 'download-btn';
            button.target = '_blank';
            button.rel = 'noopener noreferrer';
            button.setAttribute('data-platform', link.platform);
            
            // Add click tracking
            button.addEventListener('click', () => {
                this.trackDownload(link.platform, link.url);
            });
            
            button.innerHTML = `
                <i class="${link.icon || 'fas fa-download'}"></i>
                <span>${link.platform}</span>
            `;
            
            container.appendChild(button);
        });

        console.log(`Rendered ${links.length} download buttons`);
    }

    /**
     * Track download clicks for analytics
     * @param {string} platform - The download platform
     * @param {string} url - The download URL
     */
    trackDownload(platform, url) {
        console.log(`Download clicked: ${platform} - ${url}`);
        
        // You can integrate with analytics services here
        // Example: Google Analytics, Mixpanel, etc.
        if (typeof gtag !== 'undefined') {
            gtag('event', 'download_click', {
                'platform': platform,
                'url': url
            });
        }
    }

    /**
     * Initialize download configuration for a page
     * @param {Object} options - Configuration options
     */
    async initializePage(options = {}) {
        const {
            containerId = 'downloadButtons',
            configUrl = null,
            downloadLinks = [],
            showLoadingIndicator = true
        } = options;

        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container with ID '${containerId}' not found`);
            return;
        }

        // Show loading indicator
        if (showLoadingIndicator) {
            container.innerHTML = `
                <div class="loading-indicator">
                    <i class="fas fa-spinner fa-spin"></i>
                    <span>Đang tải cấu hình...</span>
                </div>
            `;
        }

        try {
            // Load configuration and render buttons
            const activeLinks = await this.loadConfig(configUrl, downloadLinks);
            this.renderDownloadButtons(container, activeLinks);
            
        } catch (error) {
            console.error('Failed to initialize download configuration:', error);
            
            // Show error message and fallback to all links
            container.innerHTML = `
                <div class="error-message">
                    <i class="fas fa-exclamation-triangle"></i>
                    <span>Không thể tải cấu hình. Hiển thị tất cả link.</span>
                </div>
            `;
            
            setTimeout(() => {
                this.renderDownloadButtons(container, downloadLinks);
            }, 2000);
        }
    }
}

// Create global instance
window.downloadConfigManager = new DownloadConfigManager();

// Auto-initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    // Check if this is an epub page with download configuration
    const downloadContainer = document.getElementById('downloadButtons');
    if (downloadContainer && typeof window.epubDownloadConfig !== 'undefined') {
        window.downloadConfigManager.initializePage(window.epubDownloadConfig);
    }
});
