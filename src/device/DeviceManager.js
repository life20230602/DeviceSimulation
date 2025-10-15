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

            // 提取平台信息
            let platform = 'Unknown';
            if (lowerUA.includes('android')) {
                if (lowerUA.includes('arm64') || lowerUA.includes('aarch64')) {
                    platform = 'Linux aarch64';
                } else if (lowerUA.includes('armv8')) {
                    platform = 'Linux armv8l';
                } else if (lowerUA.includes('armv7')) {
                    platform = 'Linux armv7l';
                } else {
                    platform = 'Linux armv8l';
                }
            } else if (lowerUA.includes('iphone') || lowerUA.includes('ipad')) {
                platform = 'Linux armv8l';
            }

            // 提取屏幕信息
            let width = 375;
            let height = 667;
            let innerWidth = 375;
            let innerHeight = 667;
            let colorDepth = 24;
            let pixelDepth = 24;
            let devicePixelRatio = 2.0;

            if (lowerUA.includes('android')) {
                // Android设备屏幕尺寸
                if (brand === '华为' || brand === 'Honor') {
                    width = 360;
                    height = 780;
                    innerWidth = 360;
                    innerHeight = 720;
                    devicePixelRatio = 3.0;
                } else if (brand === '小米') {
                    width = 393;
                    height = 851;
                    innerWidth = 393;
                    innerHeight = 800;
                    devicePixelRatio = 2.75;
                } else if (brand === 'Vivo') {
                    width = 360;
                    height = 760;
                    innerWidth = 360;
                    innerHeight = 720;
                    devicePixelRatio = 3.0;
                } else if (brand === 'OPPO') {
                    width = 375;
                    height = 812;
                    innerWidth = 375;
                    innerHeight = 780;
                    devicePixelRatio = 3.0;
                } else if (brand === 'Samsung') {
                    width = 360;
                    height = 740;
                    innerWidth = 360;
                    innerHeight = 700;
                    devicePixelRatio = 3.0;
                }
            } else if (lowerUA.includes('iphone') || lowerUA.includes('ipad')) {
                // iOS设备屏幕尺寸
                if (lowerUA.includes('ipad')) {
                    width = 768;
                    height = 1024;
                    innerWidth = 768;
                    innerHeight = 1000;
                    devicePixelRatio = 2.0;
                } else {
                    width = 375;
                    height = 812;
                    innerWidth = 375;
                    innerHeight = 780;
                    devicePixelRatio = 3.0;
                }
            }

            // 提取硬件信息
            const hardware = {
                cpuCores: 8
            };

            // 检查是否有WebGL信息
            if (lowerUA.includes('adreno') || lowerUA.includes('mali') || lowerUA.includes('powervr') || lowerUA.includes('sgx')) {
                hardware.webgl = {
                    supported: true,
                    renderer: this.extractWebGLRenderer(lowerUA),
                    vendor: this.extractWebGLVendor(lowerUA)
                };
            }

            // 提取设备型号
            const model = this.extractModelFromUserAgent(userAgent, brand);

            // 创建设备信息
            const device = {
                platform: platform,
                screen: {
                    width: width,
                    height: height,
                    innerWidth: innerWidth,
                    innerHeight: innerHeight,
                    colorDepth: colorDepth,
                    pixelDepth: pixelDepth,
                    devicePixelRatio: devicePixelRatio
                },
                hardware: hardware,
                brand: brand,
                model: model,
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
     * 提取WebGL渲染器
     */
    extractWebGLRenderer(lowerUA) {
        if (lowerUA.includes('adreno')) {
            return 'Adreno (TM) 618';
        } else if (lowerUA.includes('mali')) {
            return 'Mali-G78';
        } else if (lowerUA.includes('powervr')) {
            return 'PowerVR SGX';
        } else if (lowerUA.includes('sgx')) {
            return 'PowerVR SGX';
        }
        return 'Unknown';
    }

    /**
     * 提取WebGL厂商
     */
    extractWebGLVendor(lowerUA) {
        if (lowerUA.includes('adreno')) {
            return 'Qualcomm';
        } else if (lowerUA.includes('mali')) {
            return 'ARM';
        } else if (lowerUA.includes('powervr') || lowerUA.includes('sgx')) {
            return 'Imagination Technologies';
        }
        return 'Unknown';
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
     * 获取随机设备信息
     */
    getRandomDevice() {
        if (!this.initialized || this.extractedDevices.length === 0) {
            return null;
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
}

module.exports = { DeviceManager };
