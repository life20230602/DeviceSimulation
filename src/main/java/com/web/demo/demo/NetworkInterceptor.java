package com.web.demo.demo;

import com.ruiyun.jvppeteer.api.core.Page;
import com.ruiyun.jvppeteer.api.core.Request;
import com.ruiyun.jvppeteer.api.core.Response;
import com.ruiyun.jvppeteer.api.events.PageEvents;
import com.ruiyun.jvppeteer.cdp.entities.ResourceType;

import java.util.*;
import java.util.function.Consumer;
import java.util.regex.Pattern;

/**
 * 网络请求拦截器
 * 用于减少网络流量，阻止不必要的资源加载
 */
public class NetworkInterceptor {
    
    // 拦截配置
    private boolean blockImages = true;
    private boolean blockMedia = true;
    private boolean blockFonts = true;
    private boolean blockStylesheets = false;
    private boolean blockAnalytics = true;
    private boolean blockAds = true;
    private boolean blockTracking = true;
    
    // 允许的域名白名单
    private Set<String> allowedDomains = new HashSet<>();
    
    // 阻止的域名黑名单
    private Set<String> blockedDomains = new HashSet<>();
    
    // 阻止的文件扩展名
    private Set<String> blockedExtensions = new HashSet<>();
    
    // 阻止的URL模式
    private List<Pattern> blockedUrlPatterns = new ArrayList<>();
    
    // 统计信息
    private int totalRequests = 0;
    private int blockedRequests = 0;
    private long totalBytesSaved = 0;
    
    public NetworkInterceptor() {
        initDefaultConfig();
    }
    
    /**
     * 初始化默认配置
     */
    private void initDefaultConfig() {
        // 默认阻止的文件扩展名
        blockedExtensions.addAll(Arrays.asList(
            "apk","jpg", "jpeg", "png", "gif", "webp", "svg", "ico", "bmp", "tiff",
            "mp4", "mp3", "wav", "avi", "mov", "wmv", "flv", "webm", "ogg",
            "woff", "woff2", "ttf", "eot", "otf","m3u8"
        ));
        
        // 默认阻止的URL模式
        blockedUrlPatterns.addAll(Arrays.asList(
            Pattern.compile(".*analytics.*", Pattern.CASE_INSENSITIVE),
            Pattern.compile(".*tracking.*", Pattern.CASE_INSENSITIVE),
            Pattern.compile(".*metrics.*", Pattern.CASE_INSENSITIVE),
            Pattern.compile(".*ads.*", Pattern.CASE_INSENSITIVE),
            Pattern.compile(".*advertisement.*", Pattern.CASE_INSENSITIVE),
            Pattern.compile(".*doubleclick.*", Pattern.CASE_INSENSITIVE),
            Pattern.compile(".*googlesyndication.*", Pattern.CASE_INSENSITIVE),
            Pattern.compile(".*facebook\\.com/tr.*", Pattern.CASE_INSENSITIVE),
            Pattern.compile(".*google-analytics.*", Pattern.CASE_INSENSITIVE),
            Pattern.compile(".*googletagmanager.*", Pattern.CASE_INSENSITIVE),
            Pattern.compile(".*hotjar.*", Pattern.CASE_INSENSITIVE),
            Pattern.compile(".*mixpanel.*", Pattern.CASE_INSENSITIVE),
            Pattern.compile(".*segment.*", Pattern.CASE_INSENSITIVE),
            Pattern.compile(".*amplitude.*", Pattern.CASE_INSENSITIVE)
        ));
    }
    
    /**
     * 设置网络拦截
     */
    public void setupInterception(Page page) {
        try {
            // 启用请求拦截
            page.setRequestInterception(true);
            page.on(PageEvents.Request, new Consumer<Request>() {
                @Override
                public void accept(Request request) {
                    String url = request.url();
                    ResourceType resourceType = request.resourceType();
                    // 打印请求信息
                    if( url.contains("statistics")){
                        System.out.println("加载统计js: "+ url);
                    }
                    // 判断是否应该阻止请求
                    if (shouldBlockRequest(url, resourceType)) {
                        blockedRequests++;
                        request.abort();
                    } else {
                        // 允许请求继续
                        request.continueRequest();
                    }
                }
            });
            
            System.out.println("网络请求拦截器已设置");
            
        } catch (Exception e) {
            System.err.println("设置网络拦截失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * 判断是否应该阻止请求
     */
    private boolean shouldBlockRequest(String url, ResourceType resourceType) {
        // 检查域名白名单
        if (!allowedDomains.isEmpty()) {
            String domain = extractDomain(url);
            if (allowedDomains.contains(domain)) {
                return false; // 白名单中的域名允许通过
            }
        }
        
        // 检查域名黑名单
        if (!blockedDomains.isEmpty()) {
            String domain = extractDomain(url);
            if (blockedDomains.contains(domain)) {
                return true; // 黑名单中的域名直接阻止
            }
        }
        
        // 检查资源类型
        if (blockImages && "image".equals(resourceType.type())) {
            return true;
        }
        
        if (blockMedia && "media".equals(resourceType.type())) {
            return true;
        }
        
        if (blockStylesheets) {
            return true;
        }
        
        // 检查URL模式
        for (Pattern pattern : blockedUrlPatterns) {
            if (pattern.matcher(url).matches()) {
                return true;
            }
        }
        
        // 检查文件扩展名
        if (hasBlockedExtension(url)) {
            return true;
        }
        
        return false;
    }
    
    /**
     * 检查URL是否包含被阻止的文件扩展名
     */
    private boolean hasBlockedExtension(String url) {
        for (String ext : blockedExtensions) {
            if (url.toLowerCase().matches(".*\\." + ext + "(\\?.*)?$")) {
                return true;
            }
        }
        return false;
    }
    
    /**
     * 从URL中提取域名
     */
    private String extractDomain(String url) {
        try {
            if (url.startsWith("http://") || url.startsWith("https://")) {
                String domain = url.substring(url.indexOf("://") + 3);
                int slashIndex = domain.indexOf('/');
                if (slashIndex != -1) {
                    domain = domain.substring(0, slashIndex);
                }
                return domain;
            }
        } catch (Exception e) {
            // 忽略解析错误
        }
        return "";
    }
    
    /**
     * 打印统计信息
     */
    public void printStatistics() {
        System.out.println("\n=== 网络拦截统计 ===");
        System.out.println("总请求数: " + totalRequests);
        System.out.println("阻止请求数: " + blockedRequests);
        System.out.println("允许请求数: " + (totalRequests - blockedRequests));
        System.out.println("阻止率: " + String.format("%.2f%%", (double) blockedRequests / totalRequests * 100));
        System.out.println("===================");
    }
    
    // 配置方法
    public NetworkInterceptor setBlockImages(boolean blockImages) {
        this.blockImages = blockImages;
        return this;
    }
    
    public NetworkInterceptor setBlockMedia(boolean blockMedia) {
        this.blockMedia = blockMedia;
        return this;
    }
    
    public NetworkInterceptor setBlockFonts(boolean blockFonts) {
        this.blockFonts = blockFonts;
        return this;
    }
    
    public NetworkInterceptor setBlockStylesheets(boolean blockStylesheets) {
        this.blockStylesheets = blockStylesheets;
        return this;
    }
    
    public NetworkInterceptor setBlockAnalytics(boolean blockAnalytics) {
        this.blockAnalytics = blockAnalytics;
        return this;
    }
    
    public NetworkInterceptor setBlockAds(boolean blockAds) {
        this.blockAds = blockAds;
        return this;
    }
    
    public NetworkInterceptor setBlockTracking(boolean blockTracking) {
        this.blockTracking = blockTracking;
        return this;
    }
    
    public NetworkInterceptor addAllowedDomain(String domain) {
        this.allowedDomains.add(domain);
        return this;
    }
    
    public NetworkInterceptor addBlockedDomain(String domain) {
        this.blockedDomains.add(domain);
        return this;
    }
    
    public NetworkInterceptor addBlockedExtension(String extension) {
        this.blockedExtensions.add(extension);
        return this;
    }
    
    public NetworkInterceptor addBlockedUrlPattern(Pattern pattern) {
        this.blockedUrlPatterns.add(pattern);
        return this;
    }
}
