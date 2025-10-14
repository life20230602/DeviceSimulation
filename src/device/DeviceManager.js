const fs = require('fs').promises;
const path = require('path');

/**
 * 设备信息管理类
 * 整合设备型号、屏幕尺寸和UserAgent信息
 */
class DeviceManager {
    constructor() {
        this.devices = [];
        this.userAgentsByBrand = new Map();
        this.userAgentsByOS = new Map();
        this.extractedDevices = [];
        this.initialized = false;
    }

    /**
     * 初始化设备信息
     */
    async initialize() {
        if (this.initialized) {
            return;
        }

        try {
            // 加载UserAgent数据
            await this.loadUserAgentsFromFile();
            
            // 从UserAgent提取设备信息
            this.extractDevicesFromUserAgents();
            
            this.initialized = true;
            console.log(`设备管理器初始化完成，共加载 ${this.extractedDevices.length} 个设备`);
        } catch (error) {
            console.error('设备管理器初始化失败:', error);
            // 即使文件加载失败，也使用默认设备
            this.initializeDefaultDevices();
            this.initialized = true;
        }
    }

    /**
     * 从文件加载UserAgent数据
     */
    async loadUserAgentsFromFile() {
        const fileName = path.join(__dirname, '../../mobile_useragents_deduplicated.txt');
        
        try {
            const data = await fs.readFile(fileName, 'utf8');
            const lines = data.split('\n');
            let totalCount = 0;

            console.log('开始从文件加载UserAgent数据...');

            for (const line of lines) {
                const trimmedLine = line.trim();
                if (trimmedLine) {
                    totalCount++;
                    this.categorizeUserAgent(trimmedLine);

                    if (totalCount % 5000 === 0) {
                        console.log(`已处理 ${totalCount} 个UserAgent...`);
                    }
                }
            }

            console.log(`总共加载 ${totalCount} 个UserAgent`);
            this.printUserAgentStats();
        } catch (error) {
            console.warn('UserAgent文件不存在，使用默认设备:', error.message);
        }
    }

    /**
     * 分类UserAgent
     */
    categorizeUserAgent(userAgent) {
        if (!userAgent || !userAgent.trim()) {
            return;
        }

        const lowerUA = userAgent.toLowerCase();

        // 按品牌分类
        if (lowerUA.includes('huawei') || lowerUA.includes('honor')) {
            this.addToMap(this.userAgentsByBrand, '华为', userAgent);
        } else if (lowerUA.includes('xiaomi') || lowerUA.includes('redmi')) {
            this.addToMap(this.userAgentsByBrand, '小米', userAgent);
        } else if (lowerUA.includes('vivo')) {
            this.addToMap(this.userAgentsByBrand, 'Vivo', userAgent);
        } else if (lowerUA.includes('oppo') || lowerUA.includes('oneplus')) {
            this.addToMap(this.userAgentsByBrand, 'OPPO', userAgent);
        } else if (lowerUA.includes('samsung')) {
            this.addToMap(this.userAgentsByBrand, 'Samsung', userAgent);
        } else if (lowerUA.includes('meizu')) {
            this.addToMap(this.userAgentsByBrand, 'Meizu', userAgent);
        } else if (lowerUA.includes('lenovo')) {
            this.addToMap(this.userAgentsByBrand, 'Lenovo', userAgent);
        } else if (lowerUA.includes('google') || lowerUA.includes('pixel')) {
            this.addToMap(this.userAgentsByBrand, 'Google', userAgent);
        }

        // 按操作系统分类
        if (lowerUA.includes('android')) {
            this.addToMap(this.userAgentsByOS, 'Android', userAgent);
        } else if (lowerUA.includes('iphone') || lowerUA.includes('ipad') || lowerUA.includes('ipod')) {
            this.addToMap(this.userAgentsByOS, 'iOS', userAgent);
        }
    }

    addToMap(map, key, value) {
        if (!map.has(key)) {
            map.set(key, []);
        }
        map.get(key).push(value);
    }

    /**
     * 打印UserAgent统计信息
     */
    printUserAgentStats() {
        console.log('\n=== UserAgent 统计 ===');
        console.log('按品牌分类:');
        for (const [brand, uas] of this.userAgentsByBrand) {
            console.log(`  ${brand}: ${uas.length} 个`);
        }

        console.log('\n按操作系统分类:');
        for (const [os, uas] of this.userAgentsByOS) {
            console.log(`  ${os}: ${uas.length} 个`);
        }
    }

    /**
     * 从UserAgent提取设备信息
     */
    extractDevicesFromUserAgents() {
        console.log('\n开始从UserAgent提取设备信息...');

        // 从每个品牌的UserAgent中提取设备信息
        for (const [brand, userAgents] of this.userAgentsByBrand) {
            const processedDevices = new Set();
            let deviceCount = 0;

            for (const userAgent of userAgents) {
                if (deviceCount >= 20) break; // 每个品牌最多20个设备

                const deviceInfo = this.extractDeviceFromUserAgent(userAgent, brand);
                if (deviceInfo) {
                    const deviceKey = `${deviceInfo.brand}_${deviceInfo.model}_${deviceInfo.osVersion}`;
                    if (!processedDevices.has(deviceKey)) {
                        processedDevices.add(deviceKey);
                        this.extractedDevices.push(deviceInfo);
                        deviceCount++;
                    }
                }
            }

            console.log(`从 ${brand} 提取了 ${deviceCount} 个设备`);
        }

        console.log(`总共提取了 ${this.extractedDevices.length} 个设备`);
    }

    /**
     * 从单个UserAgent提取设备信息
     */
    extractDeviceFromUserAgent(userAgent, brand) {
        try {
            const lowerUA = userAgent.toLowerCase();

            // 提取操作系统和版本
            let os = 'Unknown';
            let osVersion = 'Unknown';
            let width = 375; // 默认宽度
            let height = 667; // 默认高度
            let deviceScaleFactor = 2.0; // 默认缩放

            if (lowerUA.includes('android')) {
                os = 'Android';
                // 提取Android版本
                if (lowerUA.includes('android 14')) {
                    osVersion = '14';
                } else if (lowerUA.includes('android 13')) {
                    osVersion = '13';
                } else if (lowerUA.includes('android 12')) {
                    osVersion = '12';
                } else if (lowerUA.includes('android 11')) {
                    osVersion = '11';
                } else if (lowerUA.includes('android 10')) {
                    osVersion = '10';
                } else if (lowerUA.includes('android 9')) {
                    osVersion = '9';
                } else if (lowerUA.includes('android 8')) {
                    osVersion = '8';
                } else {
                    osVersion = '11'; // 默认版本
                }

                // 根据品牌设置不同的屏幕尺寸
                if (brand === '华为' || brand === 'Honor') {
                    width = 360;
                    height = 780;
                    deviceScaleFactor = 3.0;
                } else if (brand === '小米') {
                    width = 393;
                    height = 851;
                    deviceScaleFactor = 2.75;
                } else if (brand === 'Vivo') {
                    width = 360;
                    height = 760;
                    deviceScaleFactor = 3.0;
                } else if (brand === 'OPPO') {
                    width = 375;
                    height = 812;
                    deviceScaleFactor = 3.0;
                } else if (brand === 'Samsung') {
                    width = 360;
                    height = 740;
                    deviceScaleFactor = 3.0;
                }

            } else if (lowerUA.includes('iphone') || lowerUA.includes('ipad')) {
                os = 'iOS';
                // 提取iOS版本
                if (lowerUA.includes('ios 18')) {
                    osVersion = '18';
                } else if (lowerUA.includes('ios 17')) {
                    osVersion = '17';
                } else if (lowerUA.includes('ios 16')) {
                    osVersion = '16';
                } else if (lowerUA.includes('ios 15')) {
                    osVersion = '15';
                } else if (lowerUA.includes('ios 14')) {
                    osVersion = '14';
                } else if (lowerUA.includes('ios 13')) {
                    osVersion = '13';
                } else if (lowerUA.includes('ios 12')) {
                    osVersion = '12';
                } else {
                    osVersion = '15'; // 默认版本
                }

                // iOS设备屏幕尺寸
                if (lowerUA.includes('ipad')) {
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
            const model = this.extractModelFromUserAgent(userAgent, brand);

            // 创建设备信息
            const device = {
                deviceName: `${brand} ${model}`,
                brand: brand,
                model: model,
                os: os,
                osVersion: osVersion,
                width: width,
                height: height,
                deviceScaleFactor: deviceScaleFactor,
                isMobile: true,
                hasTouch: true,
                userAgents: new Map()
            };

            // 添加这个UserAgent到设备
            const browserType = this.detectBrowserType(userAgent);
            device.userAgents.set(browserType, userAgent);

            return device;

        } catch (error) {
            console.error('提取设备信息失败:', error);
            return null;
        }
    }

    /**
     * 从UserAgent提取设备型号
     */
    extractModelFromUserAgent(userAgent, brand) {
        const lowerUA = userAgent.toLowerCase();

        // 华为设备型号提取
        if (brand === '华为' || brand === 'Honor') {
            if (lowerUA.includes('p40')) return 'P40';
            if (lowerUA.includes('p50')) return 'P50';
            if (lowerUA.includes('mate40')) return 'Mate40';
            if (lowerUA.includes('nova8')) return 'Nova8';
            if (lowerUA.includes('honor')) return 'Honor';
            return 'Unknown';
        }

        // 小米设备型号提取
        if (brand === '小米') {
            if (lowerUA.includes('mi 11')) return 'MI11';
            if (lowerUA.includes('mi 12')) return 'MI12';
            if (lowerUA.includes('mi 13')) return 'MI13';
            if (lowerUA.includes('redmi')) return 'Redmi';
            return 'Unknown';
        }

        // Vivo设备型号提取
        if (brand === 'Vivo') {
            if (lowerUA.includes('vivo')) return 'Vivo';
            return 'Unknown';
        }

        // OPPO设备型号提取
        if (brand === 'OPPO') {
            if (lowerUA.includes('oppo')) return 'OPPO';
            if (lowerUA.includes('oneplus')) return 'OnePlus';
            return 'Unknown';
        }

        // 三星设备型号提取
        if (brand === 'Samsung') {
            if (lowerUA.includes('galaxy')) return 'Galaxy';
            if (lowerUA.includes('samsung')) return 'Samsung';
            return 'Unknown';
        }

        // iOS设备型号提取
        if (lowerUA.includes('iphone')) {
            if (lowerUA.includes('iphone 15')) return 'iPhone 15';
            if (lowerUA.includes('iphone 14')) return 'iPhone 14';
            if (lowerUA.includes('iphone 13')) return 'iPhone 13';
            if (lowerUA.includes('iphone 12')) return 'iPhone 12';
            if (lowerUA.includes('iphone 11')) return 'iPhone 11';
            return 'iPhone';
        }

        if (lowerUA.includes('ipad')) {
            if (lowerUA.includes('ipad pro')) return 'iPad Pro';
            if (lowerUA.includes('ipad air')) return 'iPad Air';
            if (lowerUA.includes('ipad mini')) return 'iPad Mini';
            return 'iPad';
        }

        return 'Unknown';
    }

    /**
     * 检测浏览器类型
     */
    detectBrowserType(userAgent) {
        const lowerUA = userAgent.toLowerCase();

        if (lowerUA.includes('chrome')) {
            return 'chrome';
        } else if (lowerUA.includes('safari') && !lowerUA.includes('chrome')) {
            return 'safari';
        } else if (lowerUA.includes('ucbrowser') || lowerUA.includes('uc browser')) {
            return 'uc';
        } else if (lowerUA.includes('quark')) {
            return 'quark';
        } else if (lowerUA.includes('firefox')) {
            return 'firefox';
        } else if (lowerUA.includes('edge')) {
            return 'edge';
        } else if (lowerUA.includes('opera')) {
            return 'opera';
        } else if (lowerUA.includes('baiduboxapp')) {
            return 'baidu';
        } else if (lowerUA.includes('qq/')) {
            return 'qq';
        } else if (lowerUA.includes('micromessenger')) {
            return 'wechat';
        } else {
            return 'chrome'; // 默认返回chrome
        }
    }

    /**
     * 初始化默认设备
     */
    initializeDefaultDevices() {
        const defaultDevices = [
            {
                deviceName: 'iPhone 14 Pro',
                brand: 'Apple',
                model: 'iPhone 14 Pro',
                os: 'iOS',
                osVersion: '16',
                width: 393,
                height: 852,
                deviceScaleFactor: 3.0,
                isMobile: true,
                hasTouch: true,
                userAgents: new Map([['safari', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1']])
            },
            {
                deviceName: 'Samsung Galaxy S23',
                brand: 'Samsung',
                model: 'Galaxy S23',
                os: 'Android',
                osVersion: '13',
                width: 360,
                height: 740,
                deviceScaleFactor: 3.0,
                isMobile: true,
                hasTouch: true,
                userAgents: new Map([['chrome', 'Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36']])
            },
            {
                deviceName: 'Huawei P50',
                brand: '华为',
                model: 'P50',
                os: 'Android',
                osVersion: '11',
                width: 360,
                height: 780,
                deviceScaleFactor: 3.0,
                isMobile: true,
                hasTouch: true,
                userAgents: new Map([['chrome', 'Mozilla/5.0 (Linux; Android 11; ELS-AN00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36']])
            }
        ];

        this.extractedDevices = defaultDevices;
    }

    /**
     * 获取随机设备信息
     */
    getRandomDevice() {
        if (!this.initialized) {
            this.initializeDefaultDevices();
        }

        if (this.extractedDevices.length === 0) {
            this.initializeDefaultDevices();
        }

        const randomIndex = Math.floor(Math.random() * this.extractedDevices.length);
        const device = this.extractedDevices[randomIndex];
        
        // 添加随机UserAgent选择
        if (device.userAgents && device.userAgents.size > 0) {
            const userAgentArray = Array.from(device.userAgents.values());
            device.randomUserAgent = userAgentArray[Math.floor(Math.random() * userAgentArray.length)];
        } else {
            device.randomUserAgent = '';
        }

        return device;
    }

    /**
     * 获取所有设备
     */
    getAllDevices() {
        if (!this.initialized) {
            this.initializeDefaultDevices();
        }
        return this.extractedDevices;
    }

    /**
     * 根据品牌获取设备
     */
    getDevicesByBrand(brand) {
        if (!this.initialized) {
            this.initializeDefaultDevices();
        }
        return this.extractedDevices.filter(device => device.brand === brand);
    }

    /**
     * 根据操作系统获取设备
     */
    getDevicesByOS(os) {
        if (!this.initialized) {
            this.initializeDefaultDevices();
        }
        return this.extractedDevices.filter(device => device.os === os);
    }
}

module.exports = { DeviceManager };
