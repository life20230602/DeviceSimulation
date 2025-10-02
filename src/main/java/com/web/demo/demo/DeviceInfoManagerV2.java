package com.web.demo.demo;

import java.util.*;

/**
 * 设备信息管理类 V2
 * 整合设备型号、屏幕尺寸和UserAgent信息
 * 每个设备包含多个UserAgent选项
 */
public class DeviceInfoManagerV2 {
    
    // 设备信息存储
    private static final Map<String, DeviceInfo> DEVICE_INFO_MAP = new HashMap<>();
    
    static {
        initDeviceInfo();
    }
    
    /**
     * 设备信息类
     */
    public static class DeviceInfo {
        private final String deviceName;
        private final String brand;
        private final String model;
        private final String os;
        private final String osVersion;
        private final int width;
        private final int height;
        private final double deviceScaleFactor;
        private final boolean isMobile;
        private final boolean hasTouch;
        private final Map<String, String> userAgents; // 浏览器类型 -> UserAgent
        
        public DeviceInfo(String deviceName, String brand, String model, String os, String osVersion,
                         int width, int height, double deviceScaleFactor, boolean isMobile, boolean hasTouch) {
            this.deviceName = deviceName;
            this.brand = brand;
            this.model = model;
            this.os = os;
            this.osVersion = osVersion;
            this.width = width;
            this.height = height;
            this.deviceScaleFactor = deviceScaleFactor;
            this.isMobile = isMobile;
            this.hasTouch = hasTouch;
            this.userAgents = new HashMap<>();
        }
        
        // Getters
        public String getDeviceName() { return deviceName; }
        public String getBrand() { return brand; }
        public String getModel() { return model; }
        public String getOs() { return os; }
        public String getOsVersion() { return osVersion; }
        public int getWidth() { return width; }
        public int getHeight() { return height; }
        public double getDeviceScaleFactor() { return deviceScaleFactor; }
        public boolean isMobile() { return isMobile; }
        public boolean hasTouch() { return hasTouch; }
        public Map<String, String> getUserAgents() { return userAgents; }
        
        public void addUserAgent(String browser, String userAgent) {
            userAgents.put(browser, userAgent);
        }
        
        public String getUserAgent(String browser) {
            return userAgents.getOrDefault(browser, userAgents.values().iterator().next());
        }
        
        public String getRandomUserAgent() {
            List<String> uas = new ArrayList<>(userAgents.values());
            return uas.isEmpty() ? "" : uas.get(new Random().nextInt(uas.size()));
        }
        
        public List<String> getAllUserAgents() {
            return new ArrayList<>(userAgents.values());
        }
        
        public Set<String> getAvailableBrowsers() {
            return userAgents.keySet();
        }
        
        @Override
        public String toString() {
            return String.format("%s (%s %s) - %s %s - %dx%d - %d个UserAgent", 
                deviceName, brand, model, os, osVersion, width, height, userAgents.size());
        }
    }
    
    /**
     * 初始化设备信息
     */
    private static void initDeviceInfo() {
        // Android设备
        initAndroidDevices();
        // iOS设备
        initIOSDevices();
    }
    
    /**
     * 初始化Android设备
     */
    private static void initAndroidDevices() {
        // 华为设备
        addAndroidDevice("huawei_p40", "华为P40", "华为", "P40", "Android", "10", 360, 780, 3.0, "ELS-AN00");
        addAndroidDevice("huawei_mate40", "华为Mate40", "华为", "Mate40", "Android", "11", 375, 812, 3.0, "TET-AN00");
        addAndroidDevice("huawei_nova8", "华为Nova8", "华为", "Nova8", "Android", "10", 375, 812, 3.0, "JSC-AN00");
        addAndroidDevice("huawei_p50", "华为P50", "华为", "P50", "Android", "11", 375, 812, 3.0, "ABR-AL00");
        
        // 小米设备
        addAndroidDevice("xiaomi_mi11", "小米11", "小米", "MI11", "Android", "11", 393, 851, 2.75, "M2011K2C");
        addAndroidDevice("xiaomi_mi12", "小米12", "小米", "MI12", "Android", "12", 393, 851, 2.75, "2201123C");
        addAndroidDevice("xiaomi_mi13", "小米13", "小米", "MI13", "Android", "13", 393, 851, 2.75, "2211133C");
        addAndroidDevice("xiaomi_redmi_note11", "红米Note11", "小米", "Redmi Note11", "Android", "11", 393, 851, 2.75, "2109119DG");
        addAndroidDevice("xiaomi_redmi_note12", "红米Note12", "小米", "Redmi Note12", "Android", "12", 393, 851, 2.75, "22120RN86C");
        
        // 三星设备
        addAndroidDevice("samsung_s21", "三星S21", "三星", "S21", "Android", "11", 360, 800, 3.0, "SM-G991B");
        addAndroidDevice("samsung_s22", "三星S22", "三星", "S22", "Android", "12", 360, 800, 3.0, "SM-S906B");
        addAndroidDevice("samsung_s23", "三星S23", "三星", "S23", "Android", "13", 360, 800, 3.0, "SM-S911B");
        addAndroidDevice("samsung_note20", "三星Note20", "三星", "Note20", "Android", "11", 360, 800, 3.0, "SM-N981B");
        
        // OPPO设备
        addAndroidDevice("oppo_findx3", "OPPO FindX3", "OPPO", "FindX3", "Android", "11", 375, 812, 3.0, "PEDM00");
        addAndroidDevice("oppo_reno6", "OPPO Reno6", "OPPO", "Reno6", "Android", "11", 375, 812, 3.0, "PEXM00");
        addAndroidDevice("oppo_reno7", "OPPO Reno7", "OPPO", "Reno7", "Android", "12", 375, 812, 3.0, "PFJM00");
        addAndroidDevice("oppo_a95", "OPPO A95", "OPPO", "A95", "Android", "11", 375, 812, 3.0, "PCLM10");
        
        // Vivo设备
        addAndroidDevice("vivo_x70", "Vivo X70", "Vivo", "X70", "Android", "11", 375, 812, 3.0, "V2072A");
        addAndroidDevice("vivo_x80", "Vivo X80", "Vivo", "X80", "Android", "12", 375, 812, 3.0, "V2185A");
        addAndroidDevice("vivo_s12", "Vivo S12", "Vivo", "S12", "Android", "11", 375, 812, 3.0, "V2118A");
        addAndroidDevice("vivo_iqoo8", "Vivo iQOO8", "Vivo", "iQOO8", "Android", "11", 375, 812, 3.0, "V2145A");
        
        // 一加设备
        addAndroidDevice("oneplus_9", "一加9", "一加", "9", "Android", "11", 375, 812, 3.0, "LE2110");
        addAndroidDevice("oneplus_10", "一加10", "一加", "10", "Android", "12", 375, 812, 3.0, "NE2210");
        addAndroidDevice("oneplus_11", "一加11", "一加", "11", "Android", "13", 375, 812, 3.0, "PHB110");
        
        // Google Pixel设备
        addAndroidDevice("pixel_6", "Google Pixel 6", "Google", "Pixel 6", "Android", "12", 393, 851, 2.75, "Pixel 6");
        addAndroidDevice("pixel_7", "Google Pixel 7", "Google", "Pixel 7", "Android", "13", 393, 851, 2.75, "Pixel 7");
        addAndroidDevice("pixel_8", "Google Pixel 8", "Google", "Pixel 8", "Android", "14", 393, 851, 2.75, "Pixel 8");
        
        // 魅族设备
        addAndroidDevice("meizu_18", "魅族18", "魅族", "18", "Android", "11", 375, 812, 3.0, "M182Q");
        addAndroidDevice("meizu_18s", "魅族18s", "魅族", "18s", "Android", "11", 375, 812, 3.0, "M1872");
        
        // 联想设备
        addAndroidDevice("lenovo_z6", "联想Z6", "联想", "Z6", "Android", "11", 375, 812, 3.0, "L78051");
        addAndroidDevice("lenovo_z6_pro", "联想Z6 Pro", "联想", "Z6 Pro", "Android", "11", 375, 812, 3.0, "L78052");
        
        // 荣耀设备
        addAndroidDevice("honor_50", "荣耀50", "荣耀", "50", "Android", "11", 375, 812, 3.0, "NTH-AN00");
        addAndroidDevice("honor_magic3", "荣耀Magic3", "荣耀", "Magic3", "Android", "11", 375, 812, 3.0, "ELZ-AN00");
        addAndroidDevice("honor_v40", "荣耀V40", "荣耀", "V40", "Android", "10", 375, 812, 3.0, "YOK-AN10");
    }
    
    /**
     * 初始化iOS设备
     */
    private static void initIOSDevices() {
        // iPhone 15系列
        addIOSDevice("iphone_15", "iPhone 15", "Apple", "iPhone 15", "iOS", "17", 393, 852, 3.0, "17_0");
        addIOSDevice("iphone_15_pro", "iPhone 15 Pro", "Apple", "iPhone 15 Pro", "iOS", "17", 393, 852, 3.0, "17_0");
        addIOSDevice("iphone_15_plus", "iPhone 15 Plus", "Apple", "iPhone 15 Plus", "iOS", "17", 428, 926, 3.0, "17_0");
        addIOSDevice("iphone_15_pro_max", "iPhone 15 Pro Max", "Apple", "iPhone 15 Pro Max", "iOS", "17", 428, 926, 3.0, "17_0");
        
        // iPhone 14系列
        addIOSDevice("iphone_14", "iPhone 14", "Apple", "iPhone 14", "iOS", "16", 390, 844, 3.0, "16_0");
        addIOSDevice("iphone_14_pro", "iPhone 14 Pro", "Apple", "iPhone 14 Pro", "iOS", "16", 393, 852, 3.0, "16_0");
        addIOSDevice("iphone_14_plus", "iPhone 14 Plus", "Apple", "iPhone 14 Plus", "iOS", "16", 428, 926, 3.0, "16_0");
        addIOSDevice("iphone_14_pro_max", "iPhone 14 Pro Max", "Apple", "iPhone 14 Pro Max", "iOS", "16", 428, 926, 3.0, "16_0");
        
        // iPhone 13系列
        addIOSDevice("iphone_13", "iPhone 13", "Apple", "iPhone 13", "iOS", "15", 390, 844, 3.0, "15_0");
        addIOSDevice("iphone_13_pro", "iPhone 13 Pro", "Apple", "iPhone 13 Pro", "iOS", "15", 390, 844, 3.0, "15_0");
        addIOSDevice("iphone_13_mini", "iPhone 13 mini", "Apple", "iPhone 13 mini", "iOS", "15", 375, 812, 3.0, "15_0");
        addIOSDevice("iphone_13_pro_max", "iPhone 13 Pro Max", "Apple", "iPhone 13 Pro Max", "iOS", "15", 428, 926, 3.0, "15_0");
        
        // iPhone 12系列
        addIOSDevice("iphone_12", "iPhone 12", "Apple", "iPhone 12", "iOS", "14", 390, 844, 3.0, "14_7_1");
        addIOSDevice("iphone_12_pro", "iPhone 12 Pro", "Apple", "iPhone 12 Pro", "iOS", "14", 390, 844, 3.0, "14_7_1");
        addIOSDevice("iphone_12_mini", "iPhone 12 mini", "Apple", "iPhone 12 mini", "iOS", "14", 375, 812, 3.0, "14_7_1");
        addIOSDevice("iphone_12_pro_max", "iPhone 12 Pro Max", "Apple", "iPhone 12 Pro Max", "iOS", "14", 428, 926, 3.0, "14_7_1");
        
        // iPhone 11系列
        addIOSDevice("iphone_11", "iPhone 11", "Apple", "iPhone 11", "iOS", "13", 414, 896, 2.0, "13_7");
        addIOSDevice("iphone_11_pro", "iPhone 11 Pro", "Apple", "iPhone 11 Pro", "iOS", "13", 375, 812, 3.0, "13_7");
        addIOSDevice("iphone_11_pro_max", "iPhone 11 Pro Max", "Apple", "iPhone 11 Pro Max", "iOS", "13", 414, 896, 3.0, "13_7");
        
        // iPhone SE系列
        addIOSDevice("iphone_se2", "iPhone SE 2", "Apple", "iPhone SE 2", "iOS", "14", 375, 667, 2.0, "14_7_1");
        addIOSDevice("iphone_se3", "iPhone SE 3", "Apple", "iPhone SE 3", "iOS", "15", 375, 667, 2.0, "15_4_1");
        
        // iPhone XS系列
        addIOSDevice("iphone_xs", "iPhone XS", "Apple", "iPhone XS", "iOS", "12", 375, 812, 3.0, "12_5_5");
        addIOSDevice("iphone_xs_max", "iPhone XS Max", "Apple", "iPhone XS Max", "iOS", "12", 414, 896, 3.0, "12_5_5");
        addIOSDevice("iphone_xr", "iPhone XR", "Apple", "iPhone XR", "iOS", "12", 414, 896, 2.0, "12_5_5");
    }
    
    /**
     * 添加Android设备
     */
    private static void addAndroidDevice(String key, String deviceName, String brand, String model, 
                                       String os, String osVersion, int width, int height, 
                                       double deviceScaleFactor, String deviceCode) {
        DeviceInfo device = new DeviceInfo(deviceName, brand, model, os, osVersion, 
                                         width, height, deviceScaleFactor, true, true);
        
        // Chrome浏览器 - 多个版本
        device.addUserAgent("chrome", "Mozilla/5.0 (Linux; Android " + osVersion + "; " + deviceCode + ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.109 Mobile Safari/537.36");
        device.addUserAgent("chrome_old", "Mozilla/5.0 (Linux; Android " + osVersion + "; " + deviceCode + ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36");
        device.addUserAgent("chrome_new", "Mozilla/5.0 (Linux; Android " + osVersion + "; " + deviceCode + ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Mobile Safari/537.36");
        device.addUserAgent("chrome_beta", "Mozilla/5.0 (Linux; Android " + osVersion + "; " + deviceCode + ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36");
        
        // UC浏览器 - 多个版本
        device.addUserAgent("uc", "Mozilla/5.0 (Linux; Android " + osVersion + "; " + deviceCode + ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.109 Mobile Safari/537.36 UCBrowser/15.0.0.1306");
        device.addUserAgent("uc_old", "Mozilla/5.0 (Linux; Android " + osVersion + "; " + deviceCode + ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36 UCBrowser/13.4.0.1306");
        device.addUserAgent("uc_new", "Mozilla/5.0 (Linux; Android " + osVersion + "; " + deviceCode + ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Mobile Safari/537.36 UCBrowser/15.1.0.1306");
        
        // 夸克浏览器 - 多个版本
        device.addUserAgent("quark", "Mozilla/5.0 (Linux; Android " + osVersion + "; " + deviceCode + ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.109 Mobile Safari/537.36 Quark/4.0.0.130");
        device.addUserAgent("quark_old", "Mozilla/5.0 (Linux; Android " + osVersion + "; " + deviceCode + ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36 Quark/3.0.0.130");
        device.addUserAgent("quark_new", "Mozilla/5.0 (Linux; Android " + osVersion + "; " + deviceCode + ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Mobile Safari/537.36 Quark/4.1.0.130");

        // Edge浏览器
        device.addUserAgent("edge", "Mozilla/5.0 (Linux; Android " + osVersion + "; " + deviceCode + ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.109 Mobile Safari/537.36 Edg/120.0.0.0");
        device.addUserAgent("edge_old", "Mozilla/5.0 (Linux; Android " + osVersion + "; " + deviceCode + ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36 Edg/91.0.864.59");
        
        // Opera浏览器
        device.addUserAgent("opera", "Mozilla/5.0 (Linux; Android " + osVersion + "; " + deviceCode + ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.109 Mobile Safari/537.36 OPR/106.0.0.0");
        device.addUserAgent("opera_old", "Mozilla/5.0 (Linux; Android " + osVersion + "; " + deviceCode + ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36 OPR/77.0.4054.277");
        
        // 百度浏览器
        device.addUserAgent("baidu", "Mozilla/5.0 (Linux; Android " + osVersion + "; " + deviceCode + ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.109 Mobile Safari/537.36 baiduboxapp/12.0.0.10");

        DEVICE_INFO_MAP.put(key, device);
    }
    
    /**
     * 添加iOS设备
     */
    private static void addIOSDevice(String key, String deviceName, String brand, String model, 
                                   String os, String osVersion, int width, int height, 
                                   double deviceScaleFactor, String iosVersion) {
        DeviceInfo device = new DeviceInfo(deviceName, brand, model, os, osVersion, 
                                         width, height, deviceScaleFactor, true, true);
        
        // Safari浏览器 - 多个版本
        device.addUserAgent("safari", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/" + osVersion + ".0 Mobile/15E148 Safari/604.1");
        device.addUserAgent("safari_old", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/" + (Integer.parseInt(osVersion) - 1) + ".0 Mobile/15E148 Safari/604.1");
        device.addUserAgent("safari_new", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/" + (Integer.parseInt(osVersion) + 1) + ".0 Mobile/15E148 Safari/604.1");
        
        // Chrome浏览器 - 多个版本
        device.addUserAgent("chrome", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.109 Mobile/15E148 Safari/604.1");
        device.addUserAgent("chrome_old", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.120 Mobile/15E148 Safari/604.1");
        device.addUserAgent("chrome_new", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/121.0.6167.140 Mobile/15E148 Safari/604.1");
        
        // UC浏览器 - 多个版本
        device.addUserAgent("uc", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/" + osVersion + ".0 Mobile/15E148 Safari/604.1 UCBrowser/15.0.0.1306");
        device.addUserAgent("uc_old", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/" + (Integer.parseInt(osVersion) - 1) + ".0 Mobile/15E148 Safari/604.1 UCBrowser/13.4.0.1306");
        device.addUserAgent("uc_new", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/" + (Integer.parseInt(osVersion) + 1) + ".0 Mobile/15E148 Safari/604.1 UCBrowser/15.1.0.1306");
        
        // 夸克浏览器 - 多个版本
        device.addUserAgent("quark", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/" + osVersion + ".0 Mobile/15E148 Safari/604.1 Quark/4.0.0.130");
        device.addUserAgent("quark_old", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/" + (Integer.parseInt(osVersion) - 1) + ".0 Mobile/15E148 Safari/604.1 Quark/3.0.0.130");
        device.addUserAgent("quark_new", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/" + (Integer.parseInt(osVersion) + 1) + ".0 Mobile/15E148 Safari/604.1 Quark/4.1.0.130");
        
        // Firefox浏览器
        device.addUserAgent("firefox", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/120.0 Mobile/15E148 Safari/605.1.15");
        device.addUserAgent("firefox_old", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/91.0 Mobile/15E148 Safari/605.1.15");
        device.addUserAgent("firefox_new", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/121.0 Mobile/15E148 Safari/605.1.15");
        
        // Edge浏览器
        device.addUserAgent("edge", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/" + osVersion + ".0 Mobile/15E148 Safari/604.1 EdgiOS/120.0.0.0");
        device.addUserAgent("edge_old", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/" + (Integer.parseInt(osVersion) - 1) + ".0 Mobile/15E148 Safari/604.1 EdgiOS/91.0.864.59");
        
        // Opera浏览器
        device.addUserAgent("opera", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/" + osVersion + ".0 Mobile/15E148 Safari/604.1 OPiOS/106.0.0.0");
        device.addUserAgent("opera_old", "Mozilla/5.0 (iPhone; CPU iPhone OS " + iosVersion + " like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/" + (Integer.parseInt(osVersion) - 1) + ".0 Mobile/15E148 Safari/604.1 OPiOS/77.0.4054.277");

        DEVICE_INFO_MAP.put(key, device);
    }
    
    // ========== 公共方法 ==========
    
    /**
     * 根据设备键获取设备信息
     */
    public static DeviceInfo getDeviceInfo(String deviceKey) {
        return DEVICE_INFO_MAP.get(deviceKey);
    }
    
    /**
     * 获取所有设备信息
     */
    public static Map<String, DeviceInfo> getAllDevices() {
        return new HashMap<>(DEVICE_INFO_MAP);
    }
    
    /**
     * 根据品牌获取设备列表
     */
    public static List<DeviceInfo> getDevicesByBrand(String brand) {
        return DEVICE_INFO_MAP.values().stream()
                .filter(device -> device.getBrand().equalsIgnoreCase(brand))
                .collect(ArrayList::new, ArrayList::add, ArrayList::addAll);
    }
    
    /**
     * 根据操作系统获取设备列表
     */
    public static List<DeviceInfo> getDevicesByOS(String os) {
        return DEVICE_INFO_MAP.values().stream()
                .filter(device -> device.getOs().equalsIgnoreCase(os))
                .collect(ArrayList::new, ArrayList::add, ArrayList::addAll);
    }
    
    /**
     * 根据屏幕尺寸获取设备列表
     */
    public static List<DeviceInfo> getDevicesByScreenSize(int width, int height) {
        return DEVICE_INFO_MAP.values().stream()
                .filter(device -> device.getWidth() == width && device.getHeight() == height)
                .collect(ArrayList::new, ArrayList::add, ArrayList::addAll);
    }
    
    /**
     * 获取随机设备信息
     */
    public static DeviceInfo getRandomDevice() {
        List<DeviceInfo> devices = new ArrayList<>(DEVICE_INFO_MAP.values());
        return devices.get(new Random().nextInt(devices.size()));
    }
    
    /**
     * 根据操作系统获取随机设备
     */
    public static DeviceInfo getRandomDeviceByOS(String os) {
        List<DeviceInfo> devices = getDevicesByOS(os);
        return devices.isEmpty() ? null : devices.get(new Random().nextInt(devices.size()));
    }
    
    /**
     * 根据品牌获取随机设备
     */
    public static DeviceInfo getRandomDeviceByBrand(String brand) {
        List<DeviceInfo> devices = getDevicesByBrand(brand);
        return devices.isEmpty() ? null : devices.get(new Random().nextInt(devices.size()));
    }
    
    /**
     * 获取设备键列表
     */
    public static Set<String> getDeviceKeys() {
        return DEVICE_INFO_MAP.keySet();
    }
    
    /**
     * 打印所有设备信息
     */
    public static void printAllDevices() {
        System.out.println("=== 设备信息列表 ===");
        DEVICE_INFO_MAP.forEach((key, device) -> {
            System.out.println(key + ": " + device);
            System.out.println("  支持的浏览器: " + device.getAvailableBrowsers());
        });
    }
    
    /**
     * 打印设备统计信息
     */
    public static void printDeviceStats() {
        System.out.println("=== 设备统计信息 ===");
        System.out.println("总设备数量: " + DEVICE_INFO_MAP.size());
        
        Map<String, Long> brandCount = DEVICE_INFO_MAP.values().stream()
                .collect(java.util.stream.Collectors.groupingBy(DeviceInfo::getBrand, java.util.stream.Collectors.counting()));
        System.out.println("品牌分布: " + brandCount);
        
        Map<String, Long> osCount = DEVICE_INFO_MAP.values().stream()
                .collect(java.util.stream.Collectors.groupingBy(DeviceInfo::getOs, java.util.stream.Collectors.counting()));
        System.out.println("操作系统分布: " + osCount);
        
        int totalUserAgents = DEVICE_INFO_MAP.values().stream()
                .mapToInt(device -> device.getUserAgents().size())
                .sum();
        System.out.println("总UserAgent数量: " + totalUserAgents);
        System.out.println("平均每设备UserAgent数量: " + (totalUserAgents / DEVICE_INFO_MAP.size()));
    }
    
    /**
     * 测试方法
     */
    public static void main(String[] args) {
        System.out.println("=== 设备信息管理类 V2 测试 ===\n");
        
        // 打印统计信息
        printDeviceStats();
        
        System.out.println("\n=== 测试特定设备 ===");
        DeviceInfo huaweiP40 = getDeviceInfo("huawei_p40");
        if (huaweiP40 != null) {
            System.out.println("设备: " + huaweiP40);
            System.out.println("Chrome UserAgent: " + huaweiP40.getUserAgent("chrome"));
            System.out.println("随机UserAgent: " + huaweiP40.getRandomUserAgent());
            System.out.println("所有UserAgent数量: " + huaweiP40.getAllUserAgents().size());
            System.out.println("支持的浏览器: " + huaweiP40.getAvailableBrowsers());
        }
        
        System.out.println("\n=== 测试随机设备 ===");
        DeviceInfo randomDevice = getRandomDevice();
        System.out.println("随机设备: " + randomDevice);
        System.out.println("随机UserAgent: " + randomDevice.getRandomUserAgent());
        
        System.out.println("\n=== 测试品牌筛选 ===");
        List<DeviceInfo> huaweiDevices = getDevicesByBrand("华为");
        System.out.println("华为设备数量: " + huaweiDevices.size());
        huaweiDevices.forEach(device -> System.out.println("  " + device));
        
        System.out.println("\n=== 测试操作系统筛选 ===");
        List<DeviceInfo> androidDevices = getDevicesByOS("Android");
        System.out.println("Android设备数量: " + androidDevices.size());
        List<DeviceInfo> iosDevices = getDevicesByOS("iOS");
        System.out.println("iOS设备数量: " + iosDevices.size());
        
        System.out.println("\n=== 测试完成 ===");
    }
}
