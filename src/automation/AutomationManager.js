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
        const screenWidth = deviceInfo.width || 375;  // 默认iPhone宽度
        const screenHeight = deviceInfo.height || 667; // 默认iPhone高度
        
        const windowOptions = {
            width: screenWidth,
            height: screenHeight,
            webPreferences: {
                sandbox:true,
                images:true,
                nodeIntegration: true,
                contextIsolation: true,
                enableRemoteModule: true,
                webSecurity: false,
                devTools: true, // 启用开发者工具
                preload: path.join(__dirname, '../preload/device-injector.js')
            },
            show: true
        };

        // 如果配置了代理AppKey，添加到webPreferences
        if (proxyAppKey && proxyAppKey.trim() !== '') {
            windowOptions.webPreferences.proxy = this.buildProxyConfig(proxyAppKey);
        }

        const window = new BrowserWindow(windowOptions);

        // 附加调试器到 mainWindow 的网页内容(webContents),调试器版本为1.3
        // await window.webContents.debugger.attach('1.3');
        
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
                    deviceScaleFactor: deviceInfo.deviceScaleFactor || 2
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
        this.logToMainWindow(`创建BrowserWindow - 设备: ${deviceInfo.deviceName}, 屏幕: ${screenWidth}x${screenHeight}`, 'info');
    

        // 监听窗口关闭事件
        window.on('closed', () => {
            this.activeWindows.delete(threadId);
            this.logToMainWindow(`线程 ${threadId} 的BrowserWindow已关闭`);
        });

        // 添加标志防止重复执行
        let hasExecutedAutomation = false;
        
        window.webContents.on('did-navigate-in-page', async (event, navigationUrl) => {
            this.logToMainWindow(`线程 ${threadId} 页面内导航到: ${navigationUrl}`, 'info');
            
            // 在页面导航后执行自动化操作（只执行一次）
            if (!hasExecutedAutomation) {
                hasExecutedAutomation = true;
                try {
                    // 等待一段时间让页面稳定
                    await new Promise(resolve => setTimeout(resolve, 2000));
                    
                    // 执行自动化操作
                    this.logToMainWindow(`线程 ${threadId} 开始执行自动化操作...`, 'info');
                    await this.performAutomationActions(window.webContents);
                    this.logToMainWindow(`线程 ${threadId} 自动化操作完成`, 'success');
                } catch (error) {
                    this.logToMainWindow(`线程 ${threadId} 自动化操作失败: ${error.message}`, 'error');
                }
            }
        });

        // 监听页面加载状态
        window.webContents.on('did-start-loading', () => {
            this.logToMainWindow(`线程 ${threadId} 开始加载页面`, 'info');
        });

        window.webContents.on('did-stop-loading', () => {
            this.logToMainWindow(`线程 ${threadId} 页面加载完成`, 'info');
        });

        window.webContents.on('did-finish-load', () => {
            this.logToMainWindow(`线程 ${threadId} 页面完全加载完成`, 'success');
        });

        // 监听页面加载错误
        window.webContents.on('did-fail-load', (event, errorCode, errorDescription, validatedURL) => {
            this.logToMainWindow(`线程 ${threadId} 页面加载失败: ${errorCode} - ${errorDescription} (${validatedURL})`, 'error');
        });

        window.webContents.on('did-fail-provisional-load', (event, errorCode, errorDescription, validatedURL) => {
            this.logToMainWindow(`线程 ${threadId} 页面临时加载失败: ${errorCode} - ${errorDescription} (${validatedURL})`, 'error');
        });
        
        // 设置用户代理
        await window.webContents.setUserAgent(deviceInfo.randomUserAgent);

        // 注入设备信息
        await this.injectDeviceInfo(window.webContents, deviceInfo);

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
     * 注入设备信息 - 使用preload方式
     */
    async injectDeviceInfo(webContents, deviceInfo) {
        if (!webContents) {
            throw new Error('webContents未初始化');
        }

        try {
            // 通过IPC发送设备信息到preload脚本
            webContents.send('inject-device-info', deviceInfo);
            this.logToMainWindow('设备信息已发送到preload脚本');
        } catch (error) {
            this.logToMainWindow(`注入设备信息失败: ${error.message}`, 'error');
            throw error;
        }
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

            // 发送触摸开始事件
            await webContents.debugger.sendCommand('Input.dispatchTouchEvent', {
                type: 'touchStart',
                touchPoints: [{
                    id: 1,
                    x: startX,
                    y: startY
                }]
            });

            // 短暂延迟
            await new Promise(resolve => setTimeout(resolve, 100));

            // 发送触摸移动事件
            await webContents.debugger.sendCommand('Input.dispatchTouchEvent', {
                type: 'touchMove',
                touchPoints: [{
                    id: 1,
                    x: endX,
                    y: endY
                }]
            });

            // 短暂延迟
            await new Promise(resolve => setTimeout(resolve, 100));

            // 发送触摸结束事件
            await webContents.debugger.sendCommand('Input.dispatchTouchEvent', {
                type: 'touchEnd',
                touchPoints: [{
                    id: 1,
                    x: endX,
                    y: endY
                }]
            });

            this.logToMainWindow(`滑动操作执行完成: (${startX}, ${startY}) -> (${endX}, ${endY})`);
        } catch (error) {
            this.logToMainWindow(`执行滑动操作失败: ${error.message}`, 'error');
            throw error;
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
                screenshot: screenshotPath,
                url: window.webContents.getURL()
            };

        } catch (error) {
            this.logToMainWindow(`任务 ${id} 执行失败: ${error.message}`, 'error');
            return {
                taskId: id,
                success: false,
                error: error.message
            };
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
            
            // 使用ClickConfigManager生成点击配置
            const clickConfig = this.clickConfigManager.createClickConfig(width, height);
            this.logToMainWindow(`生成点击配置 - 屏幕尺寸: ${width}x${height}`, 'info');

            // 模拟一些随机操作
            const actions = [
                () => {
                    const pos1 = clickConfig.getRandomClickPosition();
                    return this.performTouchClick(webContents, pos1.x, pos1.y);
                },
                () => {
                    const pos2 = clickConfig.getRandomClickPosition();
                    return this.performTouchClick(webContents, pos2.x, pos2.y);
                },
                () => {
                    const startPos = clickConfig.getRandomClickPosition();
                    const endPos = clickConfig.getRandomClickPosition();
                    return this.performSwipe(webContents, startPos.x, startPos.y, endPos.x, endPos.y);
                },
                () => {
                    const pos3 = clickConfig.getRandomClickPosition();
                    return this.performTouchClick(webContents, pos3.x, pos3.y);
                }
            ];

            // 随机执行1-3个操作
            const actionCount = Math.floor(Math.random() * 3) + 1;
            this.logToMainWindow(`开始执行 ${actionCount} 个自动化操作`, 'info');
            
            for (let i = 0; i < actionCount; i++) {
                const action = actions[Math.floor(Math.random() * actions.length)];
                this.logToMainWindow(`执行第 ${i + 1}/${actionCount} 个操作`, 'info');
                
                // 如果是点击操作，显示点击位置
                if (i < 2 || (i === 2 && Math.random() > 0.5)) {
                    const pos = clickConfig.getRandomClickPosition();
                    this.logToMainWindow(`随机点击位置: (${pos.x}, ${pos.y})`, 'info');
                }
                
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

            // 关闭所有活跃的窗口
            for (const [taskId, window] of this.activeWindows) {
                if (window && !window.isDestroyed()) {
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