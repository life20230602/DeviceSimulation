package com.web.demo.demo;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

/**
 * 设备信息管理类 V2
 * 整合设备型号、屏幕尺寸和UserAgent信息
 * 每个设备包含多个UserAgent选项
 */
public class DeviceInfoManagerV2 {
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
        public String getDeviceName() {
            return deviceName;
        }

        public String getBrand() {
            return brand;
        }

        public String getModel() {
            return model;
        }

        public String getOs() {
            return os;
        }

        public String getOsVersion() {
            return osVersion;
        }

        public int getWidth() {
            return width;
        }

        public int getHeight() {
            return height;
        }

        public double getDeviceScaleFactor() {
            return deviceScaleFactor;
        }

        public String getRandomUserAgent() {
            List<String> uas = new ArrayList<>(userAgents.values());
            return uas.isEmpty() ? "" : uas.get(new Random().nextInt(uas.size()));
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
        // 从文件读取UserAgent数据
        loadUserAgentsFromFile();
    }


    // ========== 公共方法 ==========

    /**
     * 获取随机设备信息
     */
    public static DeviceInfo getRandomDevice() {
        if(USER_AGENTS_BY_BRAND.isEmpty()){
            initDeviceInfo();;
        }
        return getRandomExtractedDevice();
    }

    // UserAgent 存储
    private static final Map<String, List<String>> USER_AGENTS_BY_BRAND = new HashMap<>();
    private static final Map<String, List<String>> USER_AGENTS_BY_OS = new HashMap<>();

    // 从UserAgent提取的设备信息存储
    private static final List<DeviceInfo> EXTRACTED_DEVICES = new ArrayList<>();

    // 静态初始化标志
    private static boolean userAgentsLoaded = false;

    /**
     * 从文件加载UserAgent数据
     */
    private static void loadUserAgentsFromFile() {
        if (userAgentsLoaded) {
            return; // 已经加载过了
        }

        String fileName = "mobile_useragents_deduplicated.txt";
        try (BufferedReader reader = new BufferedReader(new FileReader(fileName))) {
            String line;
            int totalCount = 0;

            System.out.println("开始从文件加载UserAgent数据...");

            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (!line.isEmpty()) {
                    totalCount++;
                    categorizeUserAgent(line);

                    if (totalCount % 5000 == 0) {
                        System.out.println("已处理 " + totalCount + " 个UserAgent...");
                    }
                }
            }

            System.out.println("总共加载 " + totalCount + " 个UserAgent");
            printUserAgentStats();

            // 从UserAgent提取设备信息
            extractDevicesFromUserAgents();

            userAgentsLoaded = true;

        } catch (IOException e) {
            System.err.println("加载UserAgent文件失败: " + e.getMessage());
            e.printStackTrace();
            // 即使文件加载失败，也标记为已加载，避免重复尝试
            userAgentsLoaded = true;
        }
    }

    /**
     * 分类UserAgent
     */
    private static void categorizeUserAgent(String userAgent) {
        if (userAgent == null || userAgent.trim().isEmpty()) {
            return;
        }

        String lowerUA = userAgent.toLowerCase();

        // 按品牌分类
        if (lowerUA.contains("huawei") || lowerUA.contains("honor")) {
            USER_AGENTS_BY_BRAND.computeIfAbsent("华为", k -> new ArrayList<>()).add(userAgent);
        } else if (lowerUA.contains("xiaomi") || lowerUA.contains("redmi")) {
            USER_AGENTS_BY_BRAND.computeIfAbsent("小米", k -> new ArrayList<>()).add(userAgent);
        } else if (lowerUA.contains("vivo")) {
            USER_AGENTS_BY_BRAND.computeIfAbsent("Vivo", k -> new ArrayList<>()).add(userAgent);
        } else if (lowerUA.contains("oppo") || lowerUA.contains("oneplus")) {
            USER_AGENTS_BY_BRAND.computeIfAbsent("OPPO", k -> new ArrayList<>()).add(userAgent);
        } else if (lowerUA.contains("samsung")) {
            USER_AGENTS_BY_BRAND.computeIfAbsent("Samsung", k -> new ArrayList<>()).add(userAgent);
        } else if (lowerUA.contains("meizu")) {
            USER_AGENTS_BY_BRAND.computeIfAbsent("Meizu", k -> new ArrayList<>()).add(userAgent);
        } else if (lowerUA.contains("lenovo")) {
            USER_AGENTS_BY_BRAND.computeIfAbsent("Lenovo", k -> new ArrayList<>()).add(userAgent);
        } else if (lowerUA.contains("google") || lowerUA.contains("pixel")) {
            USER_AGENTS_BY_BRAND.computeIfAbsent("Google", k -> new ArrayList<>()).add(userAgent);
        }

        // 按操作系统分类
        if (lowerUA.contains("android")) {
            USER_AGENTS_BY_OS.computeIfAbsent("Android", k -> new ArrayList<>()).add(userAgent);
        } else if (lowerUA.contains("iphone") || lowerUA.contains("ipad") || lowerUA.contains("ipod")) {
            USER_AGENTS_BY_OS.computeIfAbsent("iOS", k -> new ArrayList<>()).add(userAgent);
        }
    }

    /**
     * 打印UserAgent统计信息
     */
    private static void printUserAgentStats() {
        System.out.println("\n=== UserAgent 统计 ===");
        System.out.println("按品牌分类:");
        USER_AGENTS_BY_BRAND.forEach((brand, uas) ->
                System.out.println("  " + brand + ": " + uas.size() + " 个"));

        System.out.println("\n按操作系统分类:");
        USER_AGENTS_BY_OS.forEach((os, uas) ->
                System.out.println("  " + os + ": " + uas.size() + " 个"));
    }

    /**
     * 检测浏览器类型
     */
    private static String detectBrowserType(String userAgent) {
        String lowerUA = userAgent.toLowerCase();

        if (lowerUA.contains("chrome")) {
            return "chrome";
        } else if (lowerUA.contains("safari") && !lowerUA.contains("chrome")) {
            return "safari";
        } else if (lowerUA.contains("ucbrowser") || lowerUA.contains("uc browser")) {
            return "uc";
        } else if (lowerUA.contains("quark")) {
            return "quark";
        } else if (lowerUA.contains("firefox")) {
            return "firefox";
        } else if (lowerUA.contains("edge")) {
            return "edge";
        } else if (lowerUA.contains("opera")) {
            return "opera";
        } else if (lowerUA.contains("baiduboxapp")) {
            return "baidu";
        } else if (lowerUA.contains("qq/")) {
            return "qq";
        } else if (lowerUA.contains("micromessenger")) {
            return "wechat";
        } else {
            return "chrome"; // 默认返回chrome
        }
    }

    /**
     * 从UserAgent提取设备信息
     */
    private static void extractDevicesFromUserAgents() {
        System.out.println("\n开始从UserAgent提取设备信息...");

        // 从每个品牌的UserAgent中提取设备信息
        for (Map.Entry<String, List<String>> entry : USER_AGENTS_BY_BRAND.entrySet()) {
            String brand = entry.getKey();
            List<String> userAgents = entry.getValue();

            // 为每个品牌提取最多20个不同的设备
            Set<String> processedDevices = new HashSet<>();
            int deviceCount = 0;

            for (String userAgent : userAgents) {
                if (deviceCount >= 20) break; // 每个品牌最多20个设备

                DeviceInfo deviceInfo = extractDeviceFromUserAgent(userAgent, brand);
                if (deviceInfo != null) {
                    String deviceKey = deviceInfo.getBrand() + "_" + deviceInfo.getModel() + "_" + deviceInfo.getOsVersion();
                    if (!processedDevices.contains(deviceKey)) {
                        processedDevices.add(deviceKey);
                        EXTRACTED_DEVICES.add(deviceInfo);
                        deviceCount++;
                    }
                }
            }

            System.out.println("从 " + brand + " 提取了 " + deviceCount + " 个设备");
        }

        System.out.println("总共提取了 " + EXTRACTED_DEVICES.size() + " 个设备");
    }

    /**
     * 从单个UserAgent提取设备信息
     */
    private static DeviceInfo extractDeviceFromUserAgent(String userAgent, String brand) {
        try {
            String lowerUA = userAgent.toLowerCase();

            // 提取操作系统和版本
            String os = "Unknown";
            String osVersion = "Unknown";
            int width = 375; // 默认宽度
            int height = 667; // 默认高度
            double deviceScaleFactor = 2.0; // 默认缩放

            if (lowerUA.contains("android")) {
                os = "Android";
                // 提取Android版本
                if (lowerUA.contains("android 14")) {
                    osVersion = "14";
                } else if (lowerUA.contains("android 13")) {
                    osVersion = "13";
                } else if (lowerUA.contains("android 12")) {
                    osVersion = "12";
                } else if (lowerUA.contains("android 11")) {
                    osVersion = "11";
                } else if (lowerUA.contains("android 10")) {
                    osVersion = "10";
                } else if (lowerUA.contains("android 9")) {
                    osVersion = "9";
                } else if (lowerUA.contains("android 8")) {
                    osVersion = "8";
                } else {
                    osVersion = "11"; // 默认版本
                }

                // 根据品牌设置不同的屏幕尺寸
                if (brand.equals("华为") || brand.equals("Honor")) {
                    width = 360;
                    height = 780;
                    deviceScaleFactor = 3.0;
                } else if (brand.equals("小米")) {
                    width = 393;
                    height = 851;
                    deviceScaleFactor = 2.75;
                } else if (brand.equals("Vivo")) {
                    width = 360;
                    height = 760;
                    deviceScaleFactor = 3.0;
                } else if (brand.equals("OPPO")) {
                    width = 375;
                    height = 812;
                    deviceScaleFactor = 3.0;
                } else if (brand.equals("Samsung")) {
                    width = 360;
                    height = 740;
                    deviceScaleFactor = 3.0;
                }

            } else if (lowerUA.contains("iphone") || lowerUA.contains("ipad")) {
                os = "iOS";
                // 提取iOS版本
                if (lowerUA.contains("ios 18")) {
                    osVersion = "18";
                } else if (lowerUA.contains("ios 17")) {
                    osVersion = "17";
                } else if (lowerUA.contains("ios 16")) {
                    osVersion = "16";
                } else if (lowerUA.contains("ios 15")) {
                    osVersion = "15";
                } else if (lowerUA.contains("ios 14")) {
                    osVersion = "14";
                } else if (lowerUA.contains("ios 13")) {
                    osVersion = "13";
                } else if (lowerUA.contains("ios 12")) {
                    osVersion = "12";
                } else {
                    osVersion = "15"; // 默认版本
                }

                // iOS设备屏幕尺寸
                if (lowerUA.contains("ipad")) {
                    width = 768;
                    height = 1024;
                    deviceScaleFactor = 2.0;
                } else {
                    width = 375;
                    height = 812;
                    deviceScaleFactor = 3.0;
                }
            }

            // 提取设备型号
            String model = extractModelFromUserAgent(userAgent, brand);

            // 创建设备信息
            DeviceInfo device = new DeviceInfo(
                    brand + " " + model,
                    brand,
                    model,
                    os,
                    osVersion,
                    width,
                    height,
                    deviceScaleFactor,
                    true, // isMobile
                    true  // hasTouch
            );

            // 添加这个UserAgent到设备
            String browserType = detectBrowserType(userAgent);
            device.userAgents.put(browserType, userAgent);

            return device;

        } catch (Exception e) {
            System.err.println("提取设备信息失败: " + e.getMessage());
            return null;
        }
    }

    /**
     * 从UserAgent提取设备型号
     */
    private static String extractModelFromUserAgent(String userAgent, String brand) {
        String lowerUA = userAgent.toLowerCase();

        // 华为设备型号提取
        if (brand.equals("华为") || brand.equals("Honor")) {
            if (lowerUA.contains("p40")) return "P40";
            if (lowerUA.contains("p50")) return "P50";
            if (lowerUA.contains("mate40")) return "Mate40";
            if (lowerUA.contains("nova8")) return "Nova8";
            if (lowerUA.contains("honor")) return "Honor";
            return "Unknown";
        }

        // 小米设备型号提取
        if (brand.equals("小米")) {
            if (lowerUA.contains("mi 11")) return "MI11";
            if (lowerUA.contains("mi 12")) return "MI12";
            if (lowerUA.contains("mi 13")) return "MI13";
            if (lowerUA.contains("redmi")) return "Redmi";
            return "Unknown";
        }

        // Vivo设备型号提取
        if (brand.equals("Vivo")) {
            if (lowerUA.contains("vivo")) return "Vivo";
            return "Unknown";
        }

        // OPPO设备型号提取
        if (brand.equals("OPPO")) {
            if (lowerUA.contains("oppo")) return "OPPO";
            if (lowerUA.contains("oneplus")) return "OnePlus";
            return "Unknown";
        }

        // 三星设备型号提取
        if (brand.equals("Samsung")) {
            if (lowerUA.contains("galaxy")) return "Galaxy";
            if (lowerUA.contains("samsung")) return "Samsung";
            return "Unknown";
        }

        // iOS设备型号提取
        if (lowerUA.contains("iphone")) {
            if (lowerUA.contains("iphone 15")) return "iPhone 15";
            if (lowerUA.contains("iphone 14")) return "iPhone 14";
            if (lowerUA.contains("iphone 13")) return "iPhone 13";
            if (lowerUA.contains("iphone 12")) return "iPhone 12";
            if (lowerUA.contains("iphone 11")) return "iPhone 11";
            return "iPhone";
        }

        if (lowerUA.contains("ipad")) {
            if (lowerUA.contains("ipad pro")) return "iPad Pro";
            if (lowerUA.contains("ipad air")) return "iPad Air";
            if (lowerUA.contains("ipad mini")) return "iPad Mini";
            return "iPad";
        }

        return "Unknown";
    }

    /**
     * 获取从UserAgent提取的随机设备
     */
    public static DeviceInfo getRandomExtractedDevice() {
        if (EXTRACTED_DEVICES.isEmpty()) {
            return getRandomDevice(); // 回退到硬编码设备
        }
        return EXTRACTED_DEVICES.get(new Random().nextInt(EXTRACTED_DEVICES.size()));
    }
}
