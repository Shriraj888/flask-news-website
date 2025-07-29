// Image Utilities for News Website
class ImageManager {
    constructor() {
        this.imageCache = new Map();
        this.lazyLoadObserver = null;
        this.initializeLazyLoading();
    }
    
    initializeLazyLoading() {
        // Create intersection observer for lazy loading
        this.lazyLoadObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    this.loadImage(img);
                    this.lazyLoadObserver.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px'
        });
        
        // Observe all images with lazy loading
        this.observeImages();
    }
    
    observeImages() {
        const images = document.querySelectorAll('.news-image[data-src]');
        images.forEach(img => {
            this.lazyLoadObserver.observe(img);
        });
    }
    
    async loadImage(img) {
        const src = img.dataset.src || img.src;
        
        if (this.imageCache.has(src)) {
            this.applyImage(img, this.imageCache.get(src));
            return;
        }
        
        try {
            // Show loading placeholder
            this.showImageLoading(img);
            
            // Load image with timeout
            const imageBlob = await this.loadImageWithTimeout(src, 10000);
            const imageUrl = URL.createObjectURL(imageBlob);
            
            // Cache the image
            this.imageCache.set(src, imageUrl);
            
            // Apply the image
            this.applyImage(img, imageUrl);
            
        } catch (error) {
            console.error('Failed to load image:', src, error);
            this.showImageError(img);
        }
    }
    
    loadImageWithTimeout(src, timeout) {
        return new Promise((resolve, reject) => {
            const timeoutId = setTimeout(() => {
                reject(new Error('Image load timeout'));
            }, timeout);
            
            fetch(src)
                .then(response => {
                    clearTimeout(timeoutId);
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}`);
                    }
                    return response.blob();
                })
                .then(resolve)
                .catch(reject);
        });
    }
    
    showImageLoading(img) {
        const container = img.parentElement;
        container.classList.add('loading');
        
        if (!container.querySelector('.image-loading')) {
            const loadingEl = document.createElement('div');
            loadingEl.className = 'image-loading';
            loadingEl.innerHTML = `
                <div class="image-loading-spinner">
                    <div class="spinner-dot"></div>
                    <div class="spinner-dot"></div>
                    <div class="spinner-dot"></div>
                </div>
            `;
            container.appendChild(loadingEl);
        }
    }
    
    applyImage(img, src) {
        const container = img.parentElement;
        
        img.src = src;
        img.onload = () => {
            container.classList.remove('loading');
            container.classList.add('loaded');
            
            // Remove loading element
            const loadingEl = container.querySelector('.image-loading');
            if (loadingEl) {
                loadingEl.remove();
            }
            
            // Add fade-in animation
            img.style.opacity = '0';
            requestAnimationFrame(() => {
                img.style.transition = 'opacity 0.5s ease';
                img.style.opacity = '1';
            });
        };
        
        img.onerror = () => {
            this.showImageError(img);
        };
    }
    
    showImageError(img) {
        const container = img.parentElement;
        container.classList.remove('loading');
        container.classList.add('error');
        
        // Remove loading element
        const loadingEl = container.querySelector('.image-loading');
        if (loadingEl) {
            loadingEl.remove();
        }
        
        // Hide the img element and show placeholder
        img.style.display = 'none';
        
        if (!container.querySelector('.image-error')) {
            const errorEl = document.createElement('div');
            errorEl.className = 'image-error';
            errorEl.innerHTML = `
                <div class="error-content">
                    <i class="fas fa-image-slash"></i>
                    <span>Image not available</span>
                </div>
            `;
            container.appendChild(errorEl);
        }
    }
    
    // Preload images for better performance
    preloadImages(imageUrls) {
        imageUrls.forEach(url => {
            if (!this.imageCache.has(url)) {
                const link = document.createElement('link');
                link.rel = 'prefetch';
                link.href = url;
                document.head.appendChild(link);
            }
        });
    }
    
    // Optimize image URL for different screen sizes
    getOptimizedImageUrl(originalUrl, width = 400, quality = 80) {
        if (!originalUrl) return null;
        
        // For demonstration, return original URL
        // In production, you might use a service like Cloudinary or similar
        return originalUrl;
    }
    
    // Clean up blob URLs to prevent memory leaks
    cleanup() {
        this.imageCache.forEach(url => {
            if (url.startsWith('blob:')) {
                URL.revokeObjectURL(url);
            }
        });
        this.imageCache.clear();
    }
}

// Performance monitoring
class ImagePerformanceMonitor {
    constructor() {
        this.metrics = {
            totalImages: 0,
            loadedImages: 0,
            failedImages: 0,
            averageLoadTime: 0,
            loadTimes: []
        };
    }
    
    trackImageLoad(startTime, success = true) {
        const loadTime = performance.now() - startTime;
        
        if (success) {
            this.metrics.loadedImages++;
            this.metrics.loadTimes.push(loadTime);
            this.metrics.averageLoadTime = this.metrics.loadTimes.reduce((a, b) => a + b, 0) / this.metrics.loadTimes.length;
        } else {
            this.metrics.failedImages++;
        }
        
        this.metrics.totalImages++;
    }
    
    getReport() {
        return {
            ...this.metrics,
            successRate: (this.metrics.loadedImages / this.metrics.totalImages * 100).toFixed(2) + '%'
        };
    }
}

// Initialize when DOM is loaded
let imageManager;
let performanceMonitor;

document.addEventListener('DOMContentLoaded', () => {
    imageManager = new ImageManager();
    performanceMonitor = new ImagePerformanceMonitor();
    
    // Clean up on page unload
    window.addEventListener('beforeunload', () => {
        if (imageManager) {
            imageManager.cleanup();
        }
    });
});

// Export for use in other scripts
window.ImageManager = ImageManager;
window.imageManager = imageManager;
