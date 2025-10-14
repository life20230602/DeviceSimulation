const { app, BrowserWindow, ipcMain, webContents } = require('electron');
const path = require('path');
const { AutomationManager } = require('./src/automation/AutomationManager');
const { ClickConfigManager } = require('./src/click/ClickConfigManager');

class ElectronApp {
    constructor() {
        this.mainWindow = null;
        this.automationManager = new AutomationManager();
        this.clickConfigManager = new ClickConfigManager();
    }

    createWindow() {
        // 创建浏览器窗口
        this.mainWindow = new BrowserWindow({
            width: 800,
            height: 600,
            webPreferences: {
                nodeIntegration: false,
                contextIsolation: true,
                enableRemoteModule: false,
                webSecurity: false,
                preload: path.join(__dirname, 'src/preload/device-injector.js')
            },
            icon: path.join(__dirname, 'assets/icon.png'),
            show: false
        });

        // 设置AutomationManager的主窗口
        this.automationManager.setMainWindow(this.mainWindow);

        // 加载应用页面
        this.mainWindow.loadFile('src/renderer/index.html');

        // 窗口准备好后显示
        this.mainWindow.once('ready-to-show', () => {
            this.mainWindow.show();
        });

        // 开发模式下打开开发者工具
        if (process.argv.includes('--dev')) {
            this.mainWindow.webContents.openDevTools();
        }

        // 窗口关闭事件
        this.mainWindow.on('closed', () => {
            this.mainWindow = null;
        });
    }

    setupIpcHandlers() {


        // 启动自动化任务
        ipcMain.handle('start-automation', async (event, config) => {
            try {
                const result = await this.automationManager.startAutomation(config);
                return { success: true, data: result };
            } catch (error) {
                return { success: false, error: error.message };
            }
        });

        // 停止自动化任务
        ipcMain.handle('stop-automation', async () => {
            try {
                await this.automationManager.stopAutomation();
                return { success: true };
            } catch (error) {
                return { success: false, error: error.message };
            }
        });

        // 获取自动化任务状态
        ipcMain.handle('get-automation-status', async () => {
            try {
                const status = this.automationManager.getTaskStatus();
                return { success: true, data: status };
            } catch (error) {
                return { success: false, error: error.message };
            }
        });



        // 截图
        ipcMain.handle('take-screenshot', async (event, filename) => {
            try {
                const result = await this.automationManager.takeScreenshot(filename);
                return { success: true, data: result };
            } catch (error) {
                return { success: false, error: error.message };
            }
        });



    }

    async initialize() {
        // 设置IPC处理器
        this.setupIpcHandlers();
        
        console.log('Electron应用初始化完成');
    }
}

// 创建应用实例
const electronApp = new ElectronApp();

// 当 Electron 完成初始化并准备创建浏览器窗口时调用此方法
app.whenReady().then(async () => {
    await electronApp.initialize();
    electronApp.createWindow();
});

// 当所有窗口都关闭时退出应用
app.on('window-all-closed', () => {
    // 在 macOS 上，应用和菜单栏通常会保持活跃状态，直到用户使用 Cmd + Q 明确退出
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    // 在 macOS 上，当单击 dock 图标并且没有其他窗口打开时，通常在应用中重新创建窗口
    if (BrowserWindow.getAllWindows().length === 0) {
        electronApp.createWindow();
    }
});

// 安全设置：防止新窗口创建
app.on('web-contents-created', (event, contents) => {
    contents.on('new-window', (event, navigationUrl) => {
        event.preventDefault();
    });
});

module.exports = { ElectronApp };
