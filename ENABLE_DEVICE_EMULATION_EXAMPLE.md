# enableDeviceEmulation 使用示例

## 概述

`enableDeviceEmulation` 是 Electron 中用于模拟移动设备的重要方法，可以让桌面应用模拟移动设备的显示和行为。

## 基本用法

### 1. 模拟 iPhone 设备

```javascript
const { BrowserWindow } = require('electron');

// 创建窗口
const window = new BrowserWindow({
    width: 375,
    height: 667,
    webPreferences: {
        nodeIntegration: true,
        contextIsolation: true
    }
});

// 启用设备模拟 - iPhone 6/7/8
window.webContents.enableDeviceEmulation({
    screenPosition: 'mobile',
    screenSize: {
        width: 375,
        height: 667
    },
    viewPosition: { x: 0, y: 0 },
    deviceScaleFactor: 2,
    viewSize: {
        width: 375,
        height: 667
    },
    scale: 1
});
```

### 2. 模拟 Android 设备

```javascript
// 模拟 Samsung Galaxy S8
window.webContents.enableDeviceEmulation({
    screenPosition: 'mobile',
    screenSize: {
        width: 360,
        height: 740
    },
    viewPosition: { x: 0, y: 0 },
    deviceScaleFactor: 3,
    viewSize: {
        width: 360,
        height: 740
    },
    scale: 1
});
```

### 3. 模拟 iPad 设备

```javascript
// 模拟 iPad Pro
window.webContents.enableDeviceEmulation({
    screenPosition: 'mobile',
    screenSize: {
        width: 1024,
        height: 1366
    },
    viewPosition: { x: 0, y: 0 },
    deviceScaleFactor: 2,
    viewSize: {
        width: 1024,
        height: 1366
    },
    scale: 1
});
```

## 参数详解

### screenPosition
- `'desktop'`: 桌面模式（默认）
- `'mobile'`: 移动设备模式

### screenSize
- 必需参数（当 screenPosition 为 'mobile' 时）
- 设置模拟设备的屏幕尺寸
- 格式：`{width: number, height: number}`

### viewPosition
- 可选参数
- 设置视图在屏幕上的位置
- 格式：`{x: number, y: number}`
- 默认值：`{x: 0, y: 0}`

### deviceScaleFactor
- 可选参数
- 设备像素比（DPR）
- 0 表示使用原始设备缩放因子
- 默认值：`0`

### viewSize
- 可选参数
- 设置模拟的视图尺寸
- 格式：`{width: number, height: number}`

### scale
- 可选参数
- 可用空间内模拟视图的缩放比例
- 默认值：`1`

## 常用设备配置

### iPhone 系列
```javascript
// iPhone 12 Pro
{
    screenPosition: 'mobile',
    screenSize: { width: 390, height: 844 },
    deviceScaleFactor: 3,
    viewSize: { width: 390, height: 844 }
}

// iPhone 12 Pro Max
{
    screenPosition: 'mobile',
    screenSize: { width: 428, height: 926 },
    deviceScaleFactor: 3,
    viewSize: { width: 428, height: 926 }
}
```

### Android 系列
```javascript
// Google Pixel 5
{
    screenPosition: 'mobile',
    screenSize: { width: 393, height: 851 },
    deviceScaleFactor: 2.75,
    viewSize: { width: 393, height: 851 }
}

// Samsung Galaxy S21
{
    screenPosition: 'mobile',
    screenSize: { width: 384, height: 854 },
    deviceScaleFactor: 3,
    viewSize: { width: 384, height: 854 }
}
```

## 完整示例

```javascript
const { BrowserWindow } = require('electron');

class DeviceEmulationExample {
    constructor() {
        this.window = null;
    }

    // 创建模拟设备窗口
    createDeviceWindow(deviceConfig) {
        this.window = new BrowserWindow({
            width: deviceConfig.screenSize.width,
            height: deviceConfig.screenSize.height,
            resizable: false,
            webPreferences: {
                nodeIntegration: true,
                contextIsolation: true,
                webSecurity: false
            }
        });

        // 启用设备模拟
        this.window.webContents.enableDeviceEmulation(deviceConfig);

        // 加载页面
        this.window.loadURL('https://example.com');

        return this.window;
    }

    // 模拟 iPhone
    createIPhone() {
        return this.createDeviceWindow({
            screenPosition: 'mobile',
            screenSize: { width: 375, height: 667 },
            viewPosition: { x: 0, y: 0 },
            deviceScaleFactor: 2,
            viewSize: { width: 375, height: 667 },
            scale: 1
        });
    }

    // 模拟 Android
    createAndroid() {
        return this.createDeviceWindow({
            screenPosition: 'mobile',
            screenSize: { width: 360, height: 640 },
            viewPosition: { x: 0, y: 0 },
            deviceScaleFactor: 3,
            viewSize: { width: 360, height: 640 },
            scale: 1
        });
    }

    // 禁用设备模拟
    disableEmulation() {
        if (this.window && !this.window.isDestroyed()) {
            this.window.webContents.disableDeviceEmulation();
        }
    }
}

// 使用示例
const example = new DeviceEmulationExample();
const iphoneWindow = example.createIPhone();
```

## 注意事项

1. **窗口尺寸匹配**: 确保 BrowserWindow 的尺寸与 screenSize 匹配
2. **设备缩放因子**: deviceScaleFactor 影响像素密度，通常移动设备为 2-3
3. **触摸事件**: 启用设备模拟后，建议同时配置触摸事件模拟
4. **用户代理**: 配合 setUserAgent 设置移动设备用户代理
5. **调试器**: 可以配合 Chrome DevTools Protocol 进行更精细的控制

## 相关方法

- `disableDeviceEmulation()`: 禁用设备模拟
- `setUserAgent()`: 设置用户代理
- `debugger.sendCommand()`: 发送调试命令
