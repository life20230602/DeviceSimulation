/**
 * 网络请求拦截器
 * 用于减少网络流量，阻止不必要的资源加载
 */
class NetworkInterceptor {
    constructor() {
        // 拦截配置
        this.blockImages = true;
        this.blockMedia = true;
        this.blockFonts = true;
        this.blockStylesheets = false;
        this.blockAnalytics = true;
        this.blockAds = true;
        this.blockTracking = true;
        
        // 允许的域名白名单
        this.allowedDomains = new Set();
        
        // 阻止的域名黑名单
        this.blockedDomains = new Set();
        
        // 阻止的文件扩展名
        this.blockedExtensions = new Set([
            'apk', 'jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'ico', 'bmp', 'tiff',
            'mp4', 'mp3', 'wav', 'avi', 'mov', 'wmv', 'flv', 'webm', 'ogg',
            'woff', 'woff2', 'ttf', 'eot', 'otf', 'm3u8'
        ]);
        
        // 阻止的URL模式
        this.blockedUrlPatterns = [
            /.*analytics.*/i,
            /.*tracking.*/i,
            /.*metrics.*/i,
            /.*ads.*/i,
            /.*advertisement.*/i,
            /.*doubleclick.*/i,
            /.*googlesyndication.*/i,
            /.*facebook\.com\/tr.*/i,
            /.*google-analytics.*/i,
            /.*googletagmanager.*/i,
            /.*hotjar.*/i,
            /.*mixpanel.*/i,
            /.*segment.*/i,
            /.*amplitude.*/i
        ];
        
        // 统计信息
        this.totalRequests = 0;
        this.blockedRequests = 0;
        this.totalBytesSaved = 0;
    }

    /**
     * 设置网络拦截
     */
    async setupInterception(page) {
        try {
            // 启用请求拦截
            await page.setRequestInterception(true);
            
            page.on('request', (request) => {
                this.totalRequests++;
                const url = request.url();
                const resourceType = request.resourceType();
                
                // 判断是否应该阻止请求
                if (this.shouldBlockRequest(url, resourceType)) {
                    this.blockedRequests++;
                    request.abort();
                } else {
                    // 允许请求继续
                    request.continue();
                }
            });
            
            console.log('网络请求拦截器已设置');
            
        } catch (error) {
            console.error('设置网络拦截失败:', error);
        }
    }

    /**
     * 判断是否应该阻止请求
     */
    shouldBlockRequest(url, resourceType) {
        // 检查域名白名单
        if (this.allowedDomains.size > 0) {
            const domain = this.extractDomain(url);
            if (this.allowedDomains.has(domain)) {
                return false; // 白名单中的域名允许通过
            }
        }
        
        // 检查域名黑名单
        if (this.blockedDomains.size > 0) {
            const domain = this.extractDomain(url);
            if (this.blockedDomains.has(domain)) {
                return true; // 黑名单中的域名直接阻止
            }
        }
        
        // 检查资源类型
        if (this.blockImages && resourceType === 'image') {
            return true;
        }
        
        if (this.blockMedia && resourceType === 'media') {
            return true;
        }
        
        if (this.blockFonts && resourceType === 'font') {
            return true;
        }
        
        if (this.blockStylesheets && resourceType === 'stylesheet') {
            return true;
        }
        
        // 检查URL模式
        for (const pattern of this.blockedUrlPatterns) {
            if (pattern.test(url)) {
                return true;
            }
        }
        
        // 检查文件扩展名
        if (this.hasBlockedExtension(url)) {
            return true;
        }
        
        return false;
    }

    /**
     * 检查URL是否包含被阻止的文件扩展名
     */
    hasBlockedExtension(url) {
        for (const ext of this.blockedExtensions) {
            const regex = new RegExp(`.*\\.${ext}(\\?.*)?$`, 'i');
            if (regex.test(url)) {
                return true;
            }
        }
        return false;
    }

    /**
     * 从URL中提取域名
     */
    extractDomain(url) {
        try {
            if (url.startsWith('http://') || url.startsWith('https://')) {
                let domain = url.substring(url.indexOf('://') + 3);
                const slashIndex = domain.indexOf('/');
                if (slashIndex !== -1) {
                    domain = domain.substring(0, slashIndex);
                }
                return domain;
            }
        } catch (error) {
            // 忽略解析错误
        }
        return '';
    }

    /**
     * 打印统计信息
     */
    printStatistics() {
        console.log('\n=== 网络拦截统计 ===');
        console.log(`总请求数: ${this.totalRequests}`);
        console.log(`阻止请求数: ${this.blockedRequests}`);
        console.log(`允许请求数: ${this.totalRequests - this.blockedRequests}`);
        console.log(`阻止率: ${((this.blockedRequests / this.totalRequests) * 100).toFixed(2)}%`);
        console.log('===================');
    }

    // 配置方法
    setBlockImages(blockImages) {
        this.blockImages = blockImages;
        return this;
    }

    setBlockMedia(blockMedia) {
        this.blockMedia = blockMedia;
        return this;
    }

    setBlockFonts(blockFonts) {
        this.blockFonts = blockFonts;
        return this;
    }

    setBlockStylesheets(blockStylesheets) {
        this.blockStylesheets = blockStylesheets;
        return this;
    }

    setBlockAnalytics(blockAnalytics) {
        this.blockAnalytics = blockAnalytics;
        return this;
    }

    setBlockAds(blockAds) {
        this.blockAds = blockAds;
        return this;
    }

    setBlockTracking(blockTracking) {
        this.blockTracking = blockTracking;
        return this;
    }

    addAllowedDomain(domain) {
        this.allowedDomains.add(domain);
        return this;
    }

    addBlockedDomain(domain) {
        this.blockedDomains.add(domain);
        return this;
    }

    addBlockedExtension(extension) {
        this.blockedExtensions.add(extension);
        return this;
    }

    addBlockedUrlPattern(pattern) {
        this.blockedUrlPatterns.push(pattern);
        return this;
    }
}

module.exports = { NetworkInterceptor };
