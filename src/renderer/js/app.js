// 使用预加载脚本暴露的API
let ipcRenderer = null;

// 等待预加载脚本完成
function waitForElectronAPI() {
    return new Promise((resolve) => {
        if (window.electronAPI) {
            ipcRenderer = window.electronAPI;
            resolve();
        } else {
            setTimeout(() => waitForElectronAPI().then(resolve), 100);
        }
    });
}

class AutomationApp {
    constructor() {
        this.isRunning = false;
        this.currentDevice = null;
        this.clickConfig = null;
        this.logs = [];
        this.currentProxyConfig = null;
        
        this.init();
    }

    async init() {
        // 等待Electron API加载完成
        await waitForElectronAPI();
        
        this.initializeElements();
        this.setupEventListeners();
        this.updateTaskStatus();
    }

    initializeElements() {
        // 配置相关元素
        this.targetUrlInput = document.getElementById('targetUrl');
        this.taskCountInput = document.getElementById('taskCount');
        this.threadCountInput = document.getElementById('threadCount');
        this.proxyAppKeyInput = document.getElementById('proxyAppKey');

        // 控制相关元素
        this.startAutomationBtn = document.getElementById('startAutomation');
        this.stopAutomationBtn = document.getElementById('stopAutomation');
        this.takeScreenshotBtn = document.getElementById('takeScreenshot');
        this.taskStatusDiv = document.getElementById('taskStatus');

        // 日志相关元素
        this.clearLogsBtn = document.getElementById('clearLogs');
        this.exportLogsBtn = document.getElementById('exportLogs');
        this.logContainer = document.getElementById('logContainer');
    }

    setupEventListeners() {

        // 控制相关事件
        this.startAutomationBtn.addEventListener('click', () => this.startAutomation());
        this.stopAutomationBtn.addEventListener('click', () => this.stopAutomation());
        this.takeScreenshotBtn.addEventListener('click', () => this.takeScreenshot());

        // 日志相关事件
        this.clearLogsBtn.addEventListener('click', () => this.clearLogs());
        this.exportLogsBtn.addEventListener('click', () => this.exportLogs());

        // 监听AutomationManager的日志
        ipcRenderer.on('automation-log', (event, logData) => {
            this.log(logData.message, logData.type);
        });


        // 屏幕尺寸变化事件

        // 定期更新任务状态
        setInterval(() => this.updateTaskStatus(), 1000);
    }





    async startAutomation() {
        if (this.isRunning) {
            this.log('自动化任务已在运行中', 'warning');
            return;
        }

        try {
            this.log('正在启动自动化任务...', 'info');
            this.isRunning = true;
            this.startAutomationBtn.disabled = true;
            this.stopAutomationBtn.disabled = false;

            const config = {
                url: this.targetUrlInput.value,
                // url: 'https://www.toyrevr.com:2096/1028.html', // 检测debug
                // url: 'https://test.apiffdsfsafd25.cfd/test_device.html',
                taskCount: parseInt(this.taskCountInput.value),
                threadCount: parseInt(this.threadCountInput.value),
                proxyAppKey: this.proxyAppKeyInput.value.trim()
            };

            const result = await ipcRenderer.invoke('start-automation', config);
            
            if (result.success) {
                this.log(`自动化任务启动成功，任务ID: ${result.data.taskId}`, 'success');
            } else {
                this.log(`自动化任务启动失败: ${result.error}`, 'error');
                this.isRunning = false;
                this.startAutomationBtn.disabled = false;
                this.stopAutomationBtn.disabled = true;
            }
        } catch (error) {
            this.log(`自动化任务启动异常: ${error.message}`, 'error');
            this.isRunning = false;
            this.startAutomationBtn.disabled = false;
            this.stopAutomationBtn.disabled = true;
        }
    }

    async stopAutomation() {
        try {
            this.log('正在停止自动化任务...', 'info');
            const result = await ipcRenderer.invoke('stop-automation');
            
            if (result.success) {
                this.log('自动化任务已停止', 'success');
                this.isRunning = false;
                this.startAutomationBtn.disabled = false;
                this.stopAutomationBtn.disabled = true;
            } else {
                this.log(`停止自动化任务失败: ${result.error}`, 'error');
            }
        } catch (error) {
            this.log(`停止自动化任务异常: ${error.message}`, 'error');
        }
    }

    async takeScreenshot() {
        try {
            this.log('正在截图...', 'info');
            const filename = `screenshot_${Date.now()}.png`;
            const result = await ipcRenderer.invoke('take-screenshot', filename);
            
            if (result.success) {
                this.log(`截图成功: ${result.data}`, 'success');
            } else {
                this.log(`截图失败: ${result.error}`, 'error');
            }
        } catch (error) {
            this.log(`截图异常: ${error.message}`, 'error');
        }
    }

    async updateTaskStatus() {
        try {
            const result = await ipcRenderer.invoke('get-automation-status');
            
            if (result.success) {
                const status = result.data;
                this.isRunning = status.isRunning;
                
                let statusHtml = `
                    <p>状态: <strong>${status.isRunning ? '运行中' : '空闲'}</strong></p>
                    <p>活跃任务数: <strong>${status.activeTasksCount}</strong></p>
                `;
                
                if (status.currentTask) {
                    statusHtml += `
                        <p>当前任务: <strong>${status.currentTask.id}</strong></p>
                        <p>任务状态: <strong>${status.currentTask.status}</strong></p>
                    `;
                    
                    if (status.currentTask.duration) {
                        statusHtml += `<p>执行时长: <strong>${(status.currentTask.duration / 1000).toFixed(2)}秒</strong></p>`;
                    }
                } else {
                    statusHtml += '<p>当前任务: <strong>无</strong></p>';
                }
                
                this.taskStatusDiv.innerHTML = statusHtml;
                
                // 更新按钮状态
                this.startAutomationBtn.disabled = status.isRunning;
                this.stopAutomationBtn.disabled = !status.isRunning;
            }
        } catch (error) {
            console.error('更新任务状态失败:', error);
        }
    }

    parseProxyConfig(proxyString) {
        if (!proxyString || !proxyString.trim()) {
            return null;
        }

        const parts = proxyString.split(':');
        if (parts.length >= 2) {
            return {
                ip: parts[0],
                port: parseInt(parts[1]),
                username: parts[2] || '',
                password: parts[3] || ''
            };
        }
        return null;
    }






    log(message, type = 'info') {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = {
            timestamp,
            message,
            type
        };
        
        this.logs.push(logEntry);
        
        const logElement = document.createElement('p');
        logElement.className = `log-entry ${type}`;
        logElement.textContent = `[${timestamp}] ${message}`;
        
        this.logContainer.appendChild(logElement);
        this.logContainer.scrollTop = this.logContainer.scrollHeight;
        
        // 限制日志数量
        if (this.logs.length > 1000) {
            this.logs = this.logs.slice(-500);
            const logElements = this.logContainer.querySelectorAll('.log-entry');
            for (let i = 0; i < logElements.length - 500; i++) {
                logElements[i].remove();
            }
        }
    }

    clearLogs() {
        this.logs = [];
        this.logContainer.innerHTML = '<p class="log-entry">日志已清空</p>';
    }

    exportLogs() {
        const logText = this.logs.map(log => 
            `[${log.timestamp}] [${log.type.toUpperCase()}] ${log.message}`
        ).join('\n');
        
        const blob = new Blob([logText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `automation_logs_${Date.now()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.log('日志已导出', 'success');
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new AutomationApp();
});
