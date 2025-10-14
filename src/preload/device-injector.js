/**
 * 预加载脚本 - 提供安全的IPC通信、传感器数据模拟和设备信息注入
 */

const { contextBridge, ipcRenderer } = require('electron');

// 传感器数据模拟器
class SensorSimulator {
    constructor() {
        this.motionData = {
            x: 0,
            y: 0,
            z: 0
        };
        this.orientationData = {
            alpha: 0,
            beta: 0,
            gamma: 0
        };
        this.isSimulating = false;
        this.simulationInterval = null;
        this.deviceType = 'mobile'; // mobile, tablet, desktop
    }

    /**
     * 设置设备类型
     */
    setDeviceType(type) {
        this.deviceType = type;
    }

    /**
     * 生成模拟的加速度数据
     */
    generateMotionData() {
        // 模拟轻微的随机震动
        const baseX = this.deviceType === 'mobile' ? 0.1 : 0.05;
        const baseY = this.deviceType === 'mobile' ? 0.2 : 0.1;
        const baseZ = this.deviceType === 'mobile' ? 9.8 : 0.05;

        this.motionData = {
            x: baseX + (Math.random() - 0.5) * 0.2,
            y: baseY + (Math.random() - 0.5) * 0.2,
            z: baseZ + (Math.random() - 0.5) * 0.1
        };

        return this.motionData;
    }

    /**
     * 生成模拟的设备方向数据
     */
    generateOrientationData() {
        // 模拟设备旋转
        this.orientationData = {
            alpha: Math.random() * 360, // 0-360度
            beta: (Math.random() - 0.5) * 180, // -90到90度
            gamma: (Math.random() - 0.5) * 180  // -90到90度
        };

        return this.orientationData;
    }

    /**
     * 开始传感器数据模拟
     */
    startSimulation() {
        if (this.isSimulating) return;

        this.isSimulating = true;
        
        // 模拟设备运动事件
        this.simulationInterval = setInterval(() => {
            const motionData = this.generateMotionData();
            const orientationData = this.generateOrientationData();

            // 触发 DeviceMotionEvent
            if (window.DeviceMotionEvent) {
                const motionEvent = new DeviceMotionEvent('devicemotion', {
                    acceleration: {
                        x: motionData.x,
                        y: motionData.y,
                        z: motionData.z
                    },
                    accelerationIncludingGravity: {
                        x: motionData.x,
                        y: motionData.y,
                        z: motionData.z
                    },
                    rotationRate: {
                        alpha: orientationData.alpha,
                        beta: orientationData.beta,
                        gamma: orientationData.gamma
                    }
                });

                window.dispatchEvent(motionEvent);
            }

            // 触发 DeviceOrientationEvent
            if (window.DeviceOrientationEvent) {
                const orientationEvent = new DeviceOrientationEvent('deviceorientation', {
                    alpha: orientationData.alpha,
                    beta: orientationData.beta,
                    gamma: orientationData.gamma
                });

                window.dispatchEvent(orientationEvent);
            }
        }, 100); // 每100ms更新一次
    }

    /**
     * 停止传感器数据模拟
     */
    stopSimulation() {
        if (this.simulationInterval) {
            clearInterval(this.simulationInterval);
            this.simulationInterval = null;
        }
        this.isSimulating = false;
    }

    /**
     * 获取当前传感器数据
     */
    getCurrentData() {
        return {
            motion: this.motionData,
            orientation: this.orientationData,
            isSimulating: this.isSimulating
        };
    }
}

// 设备信息注入器
class DeviceInjector {
    constructor() {
        this.currentDevice = null;
    }

    /**
     * 根据设备信息注入相关属性
     */
    injectWithDevice(deviceInfo) {
        try {
            this.currentDevice = deviceInfo;
            
            // 语言修改
            this.injectLanguages();
            
            // 注入标记
            this.injectFixFlag();
            
            // 修改平台信息
            this.injectPlatform(deviceInfo);
            
            // WebGL 注入 - 模拟真实的图形硬件信息
            this.injectWebGLInfo(deviceInfo);
            
            // 设备屏幕比例
            this.injectDevicePixelRatio(deviceInfo);
            
            // 内存返回null
            this.injectDeviceMemory();
            
            // userAgentData 返回null
            this.injectUserAgentData();
            
            // 电池信息 返回null
            this.injectBatteryInfo();
            
            // webdriver 设置为false
            this.injectWebdriver();
            
            console.log('设备信息注入完成:', deviceInfo);
            
        } catch (error) {
            console.error('设备信息注入失败:', error);
        }
    }

    /**
     * 注入语言设置
     */
    injectLanguages() {
        Object.defineProperty(navigator, 'languages', {
            get: () => ['zh-CN', 'en-US', 'en'],
            configurable: true
        });
    }

    /**
     * 注入修复标记
     */
    injectFixFlag() {
        window.fix = {};
    }

    /**
     * 注入平台信息
     */
    injectPlatform(deviceInfo) {
        const platform = deviceInfo.brand === 'Apple' ? 'iPhone' : 'Android';
        Object.defineProperty(navigator, 'platform', {
            get: () => platform,
            configurable: true
        });
    }

    /**
     * 注入设备像素比
     */
    injectDevicePixelRatio(deviceInfo) {
        Object.defineProperty(window, 'devicePixelRatio', {
            get: () => deviceInfo.deviceScaleFactor || 2.0,
            configurable: true
        });
    }

    /**
     * 注入设备内存信息（返回null）
     */
    injectDeviceMemory() {
        Object.defineProperty(navigator, 'deviceMemory', {
            get: () => null,
            configurable: true
        });
    }

    /**
     * 注入用户代理数据（返回null）
     */
    injectUserAgentData() {
        Object.defineProperty(navigator, 'userAgentData', {
            get: () => null,
            configurable: true
        });
    }

    /**
     * 注入电池信息（返回null）
     */
    injectBatteryInfo() {
        Object.defineProperty(navigator, 'getBattery', {
            get: () => null,
            configurable: true
        });
    }

    /**
     * 注入webdriver信息（设置为false）
     */
    injectWebdriver() {
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false,
            configurable: true
        });
    }

    /**
     * 注入 WebGL 信息
     */
    injectWebGLInfo(deviceInfo) {
        try {
            const webglRenderer = this.getWebGLRenderer(deviceInfo);
            const webglVendor = this.getWebGLVendor(deviceInfo);
            const webglVersion = this.getWebGLVersion(deviceInfo);
            
            console.log(`注入 WebGL 信息 - 渲染器: ${webglRenderer}, 供应商: ${webglVendor}, 版本: ${webglVersion}`);
            
            // 使用 Proxy 方案注入 WebGL 信息
            const utils = {
                cache: {
                    Reflect: {
                        apply: (target, ctx, args) => target.apply(ctx, args)
                    }
                },
                replaceWithProxy: (obj, propName, handler) => {
                    const original = obj[propName];
                    obj[propName] = new Proxy(original, handler);
                }
            };
            
            const opts = {
                vendor: webglVendor,
                renderer: webglRenderer,
                version: webglVersion
            };
            
            const getParameterProxyHandler = {
                apply: function(target, ctx, args) {
                    const param = (args || [])[0];
                    const result = utils.cache.Reflect.apply(target, ctx, args);
                    
                    if (param === 37445) {
                        return opts.vendor || 'Intel Inc.';
                    }
                    if (param === 37446) {
                        return opts.renderer || 'Intel Iris OpenGL Engine';
                    }
                    
                    return result;
                }
            };
            
            const addProxy = (obj, propName) => {
                utils.replaceWithProxy(obj, propName, getParameterProxyHandler);
            };
            
            addProxy(WebGLRenderingContext.prototype, 'getParameter');
            addProxy(WebGL2RenderingContext.prototype, 'getParameter');
            
        } catch (error) {
            console.error('WebGL 注入失败:', error);
        }
    }

    /**
     * 根据设备信息获取 WebGL 渲染器
     */
    getWebGLRenderer(deviceInfo) {
        const brand = deviceInfo.brand.toLowerCase();
        
        if (brand === 'apple') {
            return 'Apple GPU';
        } else if (brand === 'huawei' || brand === 'honor') {
            return 'Mali-G78 MP14';
        } else if (brand === 'xiaomi') {
            return 'Adreno (TM) 650';
        } else if (brand === 'vivo') {
            return 'Mali-G76 MP16';
        } else if (brand === 'oppo') {
            return 'Adreno (TM) 640';
        } else if (brand === 'samsung') {
            return 'Mali-G78 MP14';
        } else {
            return 'Mali-G76 MP16';
        }
    }

    /**
     * 根据设备信息获取 WebGL 供应商
     */
    getWebGLVendor(deviceInfo) {
        return deviceInfo.brand === 'Apple' ? 'Apple Inc.' : 'ARM';
    }

    /**
     * 根据设备信息获取 WebGL 版本
     */
    getWebGLVersion(deviceInfo) {
        if (deviceInfo.brand === 'Apple') {
            return 'WebGL 1.0 (OpenGL ES 2.0 Metal - 86.104.1)';
        } else {
            return 'WebGL 1.0 (OpenGL ES 2.0 Chromium)';
        }
    }

    /**
     * 获取当前设备信息
     */
    getCurrentDevice() {
        return this.currentDevice;
    }
}

// 创建传感器模拟器实例
const sensorSimulator = new SensorSimulator();

// 创建设备注入器实例
const deviceInjector = new DeviceInjector();

// 暴露API到渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
    // IPC通信
    invoke: (channel, data) => ipcRenderer.invoke(channel, data),
    send: (channel, data) => ipcRenderer.send(channel, data),
    on: (channel, callback) => ipcRenderer.on(channel, callback),
    
    // 传感器模拟API
    sensorSimulator: {
        startSimulation: () => sensorSimulator.startSimulation(),
        stopSimulation: () => sensorSimulator.stopSimulation(),
        setDeviceType: (type) => sensorSimulator.setDeviceType(type),
        getCurrentData: () => sensorSimulator.getCurrentData(),
        generateMotionData: () => sensorSimulator.generateMotionData(),
        generateOrientationData: () => sensorSimulator.generateOrientationData()
    },
    
    // 设备注入API
    deviceInjector: {
        injectWithDevice: (deviceInfo) => deviceInjector.injectWithDevice(deviceInfo),
        getCurrentDevice: () => deviceInjector.getCurrentDevice(),
        injectLanguages: () => deviceInjector.injectLanguages(),
        injectPlatform: (deviceInfo) => deviceInjector.injectPlatform(deviceInfo),
        injectWebGLInfo: (deviceInfo) => deviceInjector.injectWebGLInfo(deviceInfo),
        injectDevicePixelRatio: (deviceInfo) => deviceInjector.injectDevicePixelRatio(deviceInfo),
        injectDeviceMemory: () => deviceInjector.injectDeviceMemory(),
        injectUserAgentData: () => deviceInjector.injectUserAgentData(),
        injectBatteryInfo: () => deviceInjector.injectBatteryInfo(),
        injectWebdriver: () => deviceInjector.injectWebdriver()
    }
});

// 自动开始传感器模拟（仅在移动设备模拟模式下）
if (window.navigator && window.navigator.userAgent) {
    const userAgent = window.navigator.userAgent.toLowerCase();
    const isMobileDevice = /android|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(userAgent);
    
    if (isMobileDevice) {
        sensorSimulator.setDeviceType('mobile');
        sensorSimulator.startSimulation();
        console.log('移动设备传感器模拟已启动');
    } else {
        sensorSimulator.setDeviceType('desktop');
        console.log('桌面设备传感器模拟已准备就绪');
    }
}

console.log('预加载脚本已加载 - 包含传感器数据模拟和设备信息注入功能');