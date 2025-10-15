const { BrowserWindow } = require('electron');
const path = require('path');
const { DeviceManager } = require('../device/DeviceManager');
const { ClickConfigManager } = require('../click/ClickConfigManager');

/**
 * 自动化管理器 - 多线程BrowserWindow模式
 * 每个线程启动一个独立的BrowserWindow，支持独立代理配置
 */
class AutomationManager {
    constructor() {
        this.mainWindow = null;
        this.deviceManager = new DeviceManager();
        this.clickConfigManager = new ClickConfigManager();
        this.isRunning = false;
        this.activeWindows = new Map(); // 存储活跃的BrowserWindow
        this.taskQueue = [];
        this.maxConcurrentTasks = 1;
        this.threadCount = 1;
        this.touchSessions = new Map(); // 管理每个webContents的触摸会话状态
        this.clickTimers = new Map(); // 管理每个webContents的定时点击器
    }

    /**
     * 发送日志到主窗口
     */
    logToMainWindow(message, type = 'info') {
        if (this.mainWindow && !this.mainWindow.isDestroyed()) {
            this.mainWindow.webContents.send('automation-log', {
                message,
                type,
                timestamp: new Date().toLocaleTimeString()
            });
        }
        // 同时输出到控制台
        console.log(`[AutomationManager] ${message}`);
    }

    /**
     * 初始化设备管理器
     */
    async initialize() {
        await this.deviceManager.initialize();
    }

    /**
     * 设置主窗口（用于UI控制）
     */
    setMainWindow(mainWindow) {
        this.mainWindow = mainWindow;
    }

    /**
     * 设置线程数
     */
    setThreadCount(count) {
        this.threadCount = Math.max(1, count);
        this.maxConcurrentTasks = this.threadCount;
    }

    /**
     * 创建并配置BrowserWindow
     */
    async createBrowserWindow(deviceInfo, proxyAppKey = null, threadId) {
        // 使用设备信息中的屏幕尺寸，强制手机模式
        const screenWidth = deviceInfo.screen.width;
        const screenHeight = deviceInfo.screen.height;
        
        const windowOptions = {
            width: screenWidth,
            height: screenHeight,
            webPreferences: {
                // sandbox:true,
                // images:true,
                nodeIntegration: false,
                contextIsolation: true,
                preload: path.join(__dirname, '../preload/device-injector.js'),
                additionalArguments: [
                    '--device-platform=' + deviceInfo.platform,
                    '--device-screen-width=' + deviceInfo.screen.width,
                    '--device-screen-height=' + deviceInfo.screen.height,
                    '--device-inner-width=' + deviceInfo.screen.innerWidth,
                    '--device-inner-height=' + deviceInfo.screen.innerHeight,
                    '--device-color-depth=' + deviceInfo.screen.colorDepth,
                    '--device-pixel-depth=' + deviceInfo.screen.pixelDepth,
                    '--device-pixel-ratio=' + deviceInfo.screen.devicePixelRatio,
                    '--device-cpu-cores=' + deviceInfo.hardware.cpuCores,
                    '--device-webgl-supported=' + (deviceInfo.hardware.webgl?.supported || false),
                    '--device-webgl-renderer=' + (deviceInfo.hardware.webgl?.renderer || ''),
                    '--device-webgl-vendor=' + (deviceInfo.hardware.webgl?.vendor || ''),
                    '--device-brand=' + deviceInfo.brand,
                    '--device-model=' + deviceInfo.model
                ]
            },
            show: true
        };

        // 如果配置了代理AppKey，添加到webPreferences
        if (proxyAppKey && proxyAppKey.trim() !== '') {
            windowOptions.webPreferences.proxy = this.buildProxyConfig(proxyAppKey);
        }

        const window = new BrowserWindow(windowOptions);

        // 附加调试器到 mainWindow 的网页内容(webContents),调试器版本为1.3
        await window.webContents.debugger.attach('1.3');
        
        // 等待窗口准备就绪后再配置设备模拟
        window.once('ready-to-show', async () => {
            try {
                // 启用设备模拟 - 使用更安全的参数
                window.webContents.enableDeviceEmulation({
                    screenPosition: 'mobile',
                    screenSize: {
                        width: screenWidth,
                        height: screenHeight
                    },
                    deviceScaleFactor: deviceInfo.screen.devicePixelRatio
                });
                
                // 启用触摸模拟,并配置为移动设备模式
                await window.webContents.debugger.sendCommand('Emulation.setTouchEmulationEnabled', {
                    enabled: true,
                    configuration: 'mobile',
                });
                
                // 启用"为鼠标事件生成触摸事件"的功能
                await window.webContents.debugger.sendCommand('Emulation.setEmitTouchEventsForMouse', { 
                    enabled: true 
                });
                
                this.logToMainWindow(`设备模拟配置完成 - 屏幕: ${screenWidth}x${screenHeight}`, 'info');
            } catch (error) {
                this.logToMainWindow(`设备模拟配置失败: ${error.message}`, 'error');
            }
        });

        // 记录设备信息
        const deviceName = `${deviceInfo.brand} ${deviceInfo.model}`;
        this.logToMainWindow(`创建BrowserWindow - 设备: ${deviceName}, 屏幕: ${screenWidth}x${screenHeight}`, 'info');
    

        // 监听窗口关闭事件
        window.on('closed', () => {
            this.activeWindows.delete(threadId);
            this.logToMainWindow(`线程 ${threadId} 的BrowserWindow已关闭`);
        });

        // 添加标志防止重复执行
        let hasExecutedAutomation = false;
        
        // 监听页面导航事件
        window.webContents.on('did-navigate', async (event, navigationUrl) => {
            
            // 在页面加载完成后执行自动化操作（只执行一次）
            if (!hasExecutedAutomation) {
                hasExecutedAutomation = true;
                try {
                    // 等待一段时间让页面稳定
                    await new Promise(resolve => setTimeout(resolve, 3000));
                    
                    // 执行自动化操作
                    this.logToMainWindow(`线程 ${threadId} 开始执行自动化操作...`, 'info');
                    await this.performAutomationActions(window.webContents);
                    this.logToMainWindow(`线程 ${threadId} 自动化操作完成`, 'success');
                } catch (error) {
                    this.logToMainWindow(`线程 ${threadId} 自动化操作失败: ${error.message}`, 'error');
                }
            }
        });
        
        
        // 设置用户代理
        await window.webContents.setUserAgent(deviceInfo.randomUserAgent);

        return window;
    }

    /**
     * 构建代理配置 - 使用AppKey方式
     */
    buildProxyConfig(proxyAppKey) {
        if (!proxyAppKey || proxyAppKey.trim() === '') {
            return null;
        }

        // 这里可以根据实际的代理服务API来构建代理配置
        // 假设AppKey对应一个代理服务，返回相应的代理规则
        return {
            proxyRules: `http://proxy-service.com:8080`, // 示例代理地址
            proxyBypassRules: 'localhost,127.0.0.1',
            // 可以添加认证信息等
            proxyAuth: {
                username: proxyAppKey,
                password: '' // 根据实际API要求设置
            }
        };
    }

    /**
     * 执行触摸点击
     */
    async performTouchClick(webContents, x, y) {
        if (!webContents) {
            throw new Error('webContents未初始化');
        }

        try {
            // 等待调试器准备就绪
            let retries = 0;
            while (retries < 5) {
                if (webContents.debugger.isAttached()) {
                    break;
                }
                await new Promise(resolve => setTimeout(resolve, 200));
                retries++;
            }

            if (!webContents.debugger.isAttached()) {
                this.logToMainWindow(`调试器未连接，跳过触摸点击: (${x}, ${y})`, 'warning');
                return;
            }

            // 发送触摸开始事件
            await webContents.debugger.sendCommand('Input.dispatchTouchEvent', {
                type: 'touchStart',
                touchPoints: [{
                    id: 1,
                    x: x,
                    y: y
                }]
            });

            // 短暂延迟
            await new Promise(resolve => setTimeout(resolve, 50));

            // 发送触摸结束事件
            await webContents.debugger.sendCommand('Input.dispatchTouchEvent', {
                type: 'touchEnd',
                touchPoints: [{
                    id: 1,
                    x: x,
                    y: y
                }]
            });

            this.logToMainWindow(`触摸点击执行完成: (${x}, ${y})`);
        } catch (error) {
            this.logToMainWindow(`执行触摸点击失败: ${error.message}`, 'error');
            throw error;
        }
    }

    /**
     * 执行滑动操作
     */
    async performSwipe(webContents, startX, startY, endX, endY) {
        if (!webContents) {
            throw new Error('webContents未初始化');
        }

        const webContentsId = webContents.id;
        
        try {
            // 等待调试器准备就绪
            let retries = 0;
            while (retries < 5) {
                if (webContents.debugger.isAttached()) {
                    break;
                }
                await new Promise(resolve => setTimeout(resolve, 200));
                retries++;
            }

            if (!webContents.debugger.isAttached()) {
                this.logToMainWindow(`调试器未连接，跳过滑动操作: (${startX}, ${startY}) -> (${endX}, ${endY})`, 'warning');
                return;
            }

            // 等待当前webContents的触摸会话结束
            while (this.touchSessions.get(webContentsId)) {
                await new Promise(resolve => setTimeout(resolve, 100));
            }

            // 标记触摸会话开始
            this.touchSessions.set(webContentsId, true);

            // 生成唯一的触摸ID，避免冲突
            const touchId = Date.now() % 10000; // 使用时间戳确保唯一性
            
            // 计算滑动距离和时间
            const distance = Math.sqrt((endX - startX) ** 2 + (endY - startY) ** 2);
            const duration = Math.max(200, Math.min(800, distance * 2)); // 200-800ms，根据距离调整
            const steps = Math.max(5, Math.floor(distance / 20)); // 每20像素一个点，最少5个点
            const stepDelay = duration / steps;

            // 确保触摸会话干净，先发送取消事件清理之前的触摸
            try {
                await webContents.debugger.sendCommand('Input.dispatchTouchEvent', {
                    type: 'touchCancel',
                    touchPoints: []
                });
                await new Promise(resolve => setTimeout(resolve, 100));
            } catch (e) {
                // 忽略取消事件的错误，可能没有活跃的触摸会话
            }

            // 额外等待确保触摸会话完全清理
            await new Promise(resolve => setTimeout(resolve, 200));

            // 发送触摸开始事件
            await webContents.debugger.sendCommand('Input.dispatchTouchEvent', {
                type: 'touchStart',
                touchPoints: [{
                    id: touchId,
                    x: startX,
                    y: startY
                }]
            });

            // 短暂等待确保touchStart生效
            await new Promise(resolve => setTimeout(resolve, 50));

            // 生成连续的触摸移动轨迹
            for (let i = 1; i <= steps; i++) {
                const progress = i / steps;
                
                // 使用贝塞尔曲线或线性插值生成平滑轨迹
                const currentX = startX + (endX - startX) * progress;
                const currentY = startY + (endY - startY) * progress;
                
                // 添加轻微的随机偏移，模拟手指的自然抖动
                const jitterX = (Math.random() - 0.5) * 2;
                const jitterY = (Math.random() - 0.5) * 2;
                
                await webContents.debugger.sendCommand('Input.dispatchTouchEvent', {
                    type: 'touchMove',
                    touchPoints: [{
                        id: touchId,
                        x: currentX + jitterX,
                        y: currentY + jitterY
                    }]
                });

                // 动态延迟，开始快，结束慢，模拟真实滑动
                const dynamicDelay = stepDelay * (1 + Math.sin(progress * Math.PI) * 0.3);
                await new Promise(resolve => setTimeout(resolve, dynamicDelay));
            }

            // 发送触摸结束事件
            await webContents.debugger.sendCommand('Input.dispatchTouchEvent', {
                type: 'touchEnd',
                touchPoints: [{
                    id: touchId,
                    x: endX,
                    y: endY
                }]
            });

            // 等待触摸会话完全结束
            await new Promise(resolve => setTimeout(resolve, 100));

            this.logToMainWindow(`滑动操作执行完成: (${startX}, ${startY}) -> (${endX}, ${endY})`);
        } catch (error) {
            this.logToMainWindow(`执行滑动操作失败: ${error.message}`, 'error');
            throw error;
        } finally {
            // 释放触摸会话
            this.touchSessions.set(webContentsId, false);
        }
    }

    /**
     * 开始定时点击
     */
    startPeriodicClick(webContents, intervalMs = 5000) {
        const webContentsId = webContents.id;
        
        // 如果已经有定时器在运行，先清除
        this.stopPeriodicClick(webContents);
        
        this.logToMainWindow(`开始定时点击，间隔: ${intervalMs}ms`, 'info');
        
        const timer = setInterval(async () => {
            try {
                // 获取当前窗口的屏幕尺寸
                const window = webContents.getOwnerBrowserWindow();
                const [width, height] = window.getSize();
                
                // 使用ClickConfigManager生成点击配置
                const clickConfig = this.clickConfigManager.createClickConfig(width, height);
                const pos = clickConfig.getRandomClickPosition();
                
                this.logToMainWindow(`定时点击位置: (${pos.x}, ${pos.y})`, 'info');
                
                // 执行点击操作
                await this.performTouchClick(webContents, pos.x, pos.y);
                
            } catch (error) {
                this.logToMainWindow(`定时点击失败: ${error.message}`, 'error');
            }
        }, intervalMs);
        
        // 存储定时器引用
        this.clickTimers.set(webContentsId, timer);
    }

    /**
     * 停止定时点击
     */
    stopPeriodicClick(webContents) {
        const webContentsId = webContents.id;
        const timer = this.clickTimers.get(webContentsId);
        
        if (timer) {
            clearInterval(timer);
            this.clickTimers.delete(webContentsId);
            this.logToMainWindow(`停止定时点击`, 'info');
        }
    }

    /**
     * 截图
     */
    async takeScreenshot(webContents, filename) {
        if (!webContents) {
            throw new Error('webContents未初始化');
        }

        try {
            const image = await webContents.capturePage();
            const fs = require('fs');
            const screenshotPath = path.join(__dirname, '../../screenshots', filename);
            
            // 确保截图目录存在
            const screenshotDir = path.dirname(screenshotPath);
            if (!fs.existsSync(screenshotDir)) {
                fs.mkdirSync(screenshotDir, { recursive: true });
            }

            fs.writeFileSync(screenshotPath, image.toPNG());
            this.logToMainWindow(`截图已保存: ${screenshotPath}`);
            return screenshotPath;
        } catch (error) {
            this.logToMainWindow(`截图失败: ${error.message}`, 'error');
            throw error;
        }
    }

    /**
     * 启动自动化任务
     */
    async startAutomation(config) {
        if (this.isRunning) {
            throw new Error('自动化任务已在运行中');
        }

        try {
            this.isRunning = true;
            const { url, taskCount, threadCount, proxyAppKey } = config;

            // 设置线程数
            this.setThreadCount(threadCount);

            // 确保设备管理器已初始化
            await this.deviceManager.initialize();

            this.logToMainWindow(`启动自动化任务: ${taskCount}个任务, ${threadCount}个并发线程`, 'success');

            // 创建任务队列
            const tasks = [];
            for (let i = 0; i < taskCount; i++) {
                tasks.push({
                    id: i + 1,
                    url,
                    device: this.deviceManager.getRandomDevice(), // 每个任务使用随机设备
                    proxyAppKey: proxyAppKey || null
                });
            }

            // 执行任务
            const results = await this.executeTasks(tasks);

            return {
                success: true,
                data: {
                    taskId: Date.now(),
                    results,
                    totalTasks: taskCount,
                    completedTasks: results.length
                }
            };

        } catch (error) {
            this.isRunning = false;
            this.logToMainWindow(`启动自动化任务失败: ${error.message}`, 'error');
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * 执行任务队列
     */
    async executeTasks(tasks) {
        const results = [];
        const executing = [];

        for (const task of tasks) {
            // 如果达到最大并发数，等待一个任务完成
            if (executing.length >= this.maxConcurrentTasks) {
                await Promise.race(executing);
            }

            // 启动新任务
            const taskPromise = this.executeTask(task).then(result => {
                executing.splice(executing.indexOf(taskPromise), 1);
                return result;
            });

            executing.push(taskPromise);
            results.push(taskPromise);
        }

        // 等待所有任务完成
        this.logToMainWindow(`等待 ${results.length} 个任务完成...`, 'info');
        const completedResults = await Promise.all(results);
        this.logToMainWindow(`所有任务执行完成，共 ${completedResults.length} 个结果`, 'success');
        return completedResults;
    }

    /**
     * 执行单个任务
     */
    async executeTask(task) {
        const { id, url, device, proxyAppKey } = task;
        let window = null;

        try {
            this.logToMainWindow(`开始执行任务 ${id}`, 'info');

            // 检查设备信息
            if (!device) {
                throw new Error('设备信息为空，请确保设备管理器已正确初始化');
            }

            // 创建BrowserWindow
            window = await this.createBrowserWindow(device, proxyAppKey, id);
            this.activeWindows.set(id, window);


            // 加载URL
            this.logToMainWindow(`任务 ${id} 开始加载URL: ${url}`, 'info');
            try {
                await window.webContents.loadURL(url, {
                    httpReferrer: 'https://www.google.com/'
                });
                this.logToMainWindow(`任务 ${id} URL加载请求已发送`, 'info');
            } catch (error) {
                this.logToMainWindow(`任务 ${id} URL加载失败: ${error.message}`, 'warning');
                // 不抛出错误，继续执行，因为可能是重定向问题
            }

            // 等待页面加载完成（宽松处理）
            await new Promise((resolve) => {
                const timeout = setTimeout(() => {
                    this.logToMainWindow(`任务 ${id} 页面加载超时，但继续执行`, 'warning');
                    resolve();
                }, 8000); // 8秒超时

                // 监听页面完全加载完成
                window.webContents.once('did-finish-load', () => {
                    this.logToMainWindow(`任务 ${id} 页面完全加载完成`, 'success');
                    clearTimeout(timeout);
                    resolve();
                });

                // 监听页面停止加载
                window.webContents.once('did-stop-loading', () => {
                    this.logToMainWindow(`任务 ${id} 页面停止加载`, 'info');
                    clearTimeout(timeout);
                    resolve();
                });

                // 即使加载失败也继续执行
                window.webContents.once('did-fail-load', (event, errorCode, errorDescription) => {
                    this.logToMainWindow(`任务 ${id} 页面加载失败但继续执行: ${errorCode} - ${errorDescription}`, 'warning');
                    clearTimeout(timeout);
                    resolve();
                });
            });

            // 启动定时点击（每5秒一次）
            this.startPeriodicClick(window.webContents, 5000);

            // 执行自动化操作
            try {
                this.logToMainWindow(`任务 ${id} 开始执行自动化操作...`, 'info');
                await this.performAutomationActions(window.webContents);
                this.logToMainWindow(`任务 ${id} 自动化操作完成`, 'success');
            } catch (error) {
                this.logToMainWindow(`任务 ${id} 自动化操作失败: ${error.message}`, 'error');
            }

            this.logToMainWindow(`任务 ${id} 执行完成`, 'success');

            return {
                taskId: id,
                success: true,
                screenshot: "",
                url: window.webContents.getURL()
            };

        } catch (error) {
            this.logToMainWindow(`任务 ${id} 执行失败: ${error.message}`, 'error');
            return {
                taskId: id,
                success: false,
                error: error.message
            };
        } finally {
            // 停止定时点击
            if (window && window.webContents) {
                this.stopPeriodicClick(window.webContents);
            }
        }
    }

    /**
     * 执行自动化操作
     */
    async performAutomationActions(webContents) {
        try {
            // 获取当前窗口的屏幕尺寸
            const window = webContents.getOwnerBrowserWindow();
            const [width, height] = window.getSize();
            
            // 模拟一些随机操作
            const actions = [
                async () => {
                    // 随机向上滑动1-3次
                    const swipeCount = Math.floor(Math.random() * 3) + 1; // 1-3次
                    this.logToMainWindow(`执行向上滑动 ${swipeCount} 次`, 'info');
                    
                    // 顺序执行滑动，避免触摸ID冲突
                    for (let i = 0; i < swipeCount; i++) {
                        // 生成符合人为习惯的滑动位置（偏向屏幕右侧）
                        const rightBias = 0.7; // 70%概率在右侧，30%概率在左侧
                        const isRightSide = Math.random() < rightBias;
                        
                        let startX, startY;
                        if (isRightSide) {
                            // 右侧区域：屏幕宽度的60%-90%
                            startX = width * 0.6 + Math.random() * width * 0.3;
                            startY = Math.random() * (height - 200) + 200; // 避免顶部和底部
                        } else {
                            // 左侧区域：屏幕宽度的10%-40%
                            startX = width * 0.1 + Math.random() * width * 0.3;
                            startY = Math.random() * (height - 200) + 200; // 避免顶部和底部
                        }
                        
                        // 向上滑动：结束位置Y坐标比开始位置小
                        const endX = startX + (Math.random() - 0.5) * 80; // X轴稍微偏移±40像素
                        const endY = startY - (Math.random() * 200 + 100); // Y轴向上100-300像素
                        
                        this.logToMainWindow(`执行第 ${i + 1}/${swipeCount} 次滑动: (${Math.round(startX)}, ${Math.round(startY)}) -> (${Math.round(endX)}, ${Math.round(endY)})`, 'info');
                        
                        await this.performSwipe(webContents, startX, startY, endX, endY);
                        
                        // 每次滑动间隔，确保触摸会话完全结束
                        if (i < swipeCount - 1) {
                            await new Promise(resolve => setTimeout(resolve, 1000));
                        }
                    }
                },
            ];

            // 随机执行1-3个操作
            const actionCount = Math.floor(Math.random() * 3) + 1;
            this.logToMainWindow(`开始执行 ${actionCount} 个自动化操作`, 'info');
            
            for (let i = 0; i < actionCount; i++) {
                const action = actions[Math.floor(Math.random() * actions.length)];
                
                await action();
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
            
            this.logToMainWindow(`完成 ${actionCount} 个自动化操作`, 'success');

        } catch (error) {
            this.logToMainWindow(`执行自动化操作失败: ${error.message}`, 'error');
        }
    }

    /**
     * 停止自动化任务
     */
    async stopAutomation() {
        try {
            this.isRunning = false;

            // 停止所有定时点击
            for (const [webContentsId, timer] of this.clickTimers) {
                clearInterval(timer);
            }
            this.clickTimers.clear();

            // 关闭所有活跃的窗口
            for (const [taskId, window] of this.activeWindows) {
                if (window && !window.isDestroyed()) {
                    // 停止该窗口的定时点击
                    this.stopPeriodicClick(window.webContents);
                    window.close();
                }
            }

            this.activeWindows.clear();
            this.logToMainWindow('自动化任务已停止', 'warning');

            return {
                success: true,
                message: '自动化任务已停止'
            };

        } catch (error) {
            this.logToMainWindow(`停止自动化任务失败: ${error.message}`, 'error');
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * 获取任务状态
     */
    getTaskStatus() {
        return {
            isRunning: this.isRunning,
            activeTasks: this.activeWindows.size,
            maxConcurrentTasks: this.maxConcurrentTasks,
            threadCount: this.threadCount
        };
    }
}

module.exports = { AutomationManager };