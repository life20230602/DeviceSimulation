/**
 * 预加载脚本 - 提供安全的IPC通信
 */

const { contextBridge, ipcRenderer } = require('electron');

// 暴露API到渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
    // IPC通信
    invoke: (channel, data) => ipcRenderer.invoke(channel, data),
    send: (channel, data) => ipcRenderer.send(channel, data),
    on: (channel, callback) => ipcRenderer.on(channel, callback)
});

console.log('预加载脚本已加载');
// 从命令行参数中提取设备信息
function getDeviceInfoFromArgs() {
    const deviceInfo = {};
    const args = process.argv;
    
    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg.startsWith('--device-')) {
            const key = arg.substring(9); // 移除 '--device-' 前缀
            const value = args[i + 1];
            
            if (key === 'platform') {
                deviceInfo.platform = value;
            } else if (key === 'screen-width') {
                deviceInfo.screenWidth = parseInt(value);
            } else if (key === 'screen-height') {
                deviceInfo.screenHeight = parseInt(value);
            } else if (key === 'inner-width') {
                deviceInfo.innerWidth = parseInt(value);
            } else if (key === 'inner-height') {
                deviceInfo.innerHeight = parseInt(value);
            } else if (key === 'color-depth') {
                deviceInfo.colorDepth = parseInt(value);
            } else if (key === 'pixel-depth') {
                deviceInfo.pixelDepth = parseInt(value);
            } else if (key === 'pixel-ratio') {
                deviceInfo.pixelRatio = parseFloat(value);
            } else if (key === 'cpu-cores') {
                deviceInfo.cpuCores = parseInt(value);
            } else if (key === 'webgl-supported') {
                deviceInfo.webglSupported = value === 'true';
            } else if (key === 'webgl-renderer') {
                deviceInfo.webglRenderer = value;
            } else if (key === 'webgl-vendor') {
                deviceInfo.webglVendor = value;
            } else if (key === 'brand') {
                deviceInfo.brand = value;
            } else if (key === 'model') {
                deviceInfo.model = value;
            }
        }
    }
    
    return deviceInfo;
}

// 获取设备信息
const deviceInfo = getDeviceInfoFromArgs();

// preload.js
// 这里的代码运行在"隔离世界"（preload），但我们会把要运行的 JS 注入到页面上下文。
// process.once('loaded') 是一个非常早的钩子 —— 在渲染器初始化后、页面脚本之前调用。
const injectionCode = `
  // 这是要在页面上下文最早执行的代码（示例：篡改 navigator）
  (function() {
    try {
      // 使用传递的设备信息
      const deviceInfo = ${JSON.stringify(deviceInfo)};
      
      // 篡改 navigator.platform
      Object.defineProperty(navigator, 'platform', { 
        get: () => deviceInfo.platform || 'Linux armv8l', 
        configurable: true 
      });
      
      // 隐藏 webdriver 属性
      Object.defineProperty(navigator, 'webdriver', { 
        get: () => false, 
        configurable: true 
      });
      
      // 篡改 screen 信息
      if (deviceInfo.screenWidth) {
        Object.defineProperty(screen, 'width', { 
          get: () => deviceInfo.screenWidth, 
          configurable: true 
        });
      }
      if (deviceInfo.screenHeight) {
        Object.defineProperty(screen, 'height', { 
          get: () => deviceInfo.screenHeight, 
          configurable: true 
        });
      }
      if (deviceInfo.colorDepth) {
        Object.defineProperty(screen, 'colorDepth', { 
          get: () => deviceInfo.colorDepth, 
          configurable: true 
        });
      }
      if (deviceInfo.pixelDepth) {
        Object.defineProperty(screen, 'pixelDepth', { 
          get: () => deviceInfo.pixelDepth, 
          configurable: true 
        });
      }
      
      // 篡改 window.innerWidth 和 innerHeight
      if (deviceInfo.innerWidth) {
        Object.defineProperty(window, 'innerWidth', { 
          get: () => deviceInfo.innerWidth, 
          configurable: true 
        });
      }
      if (deviceInfo.innerHeight) {
        Object.defineProperty(window, 'innerHeight', { 
          get: () => deviceInfo.innerHeight, 
          configurable: true 
        });
      }
      
      // 篡改 devicePixelRatio
      if (deviceInfo.pixelRatio) {
        Object.defineProperty(window, 'devicePixelRatio', { 
          get: () => deviceInfo.pixelRatio, 
          configurable: true 
        });
      }
      
      // 篡改 navigator.hardwareConcurrency (CPU核心数)
      if (deviceInfo.cpuCores) {
        Object.defineProperty(navigator, 'hardwareConcurrency', { 
          get: () => deviceInfo.cpuCores, 
          configurable: true 
        });
      }
      
      // 篡改 WebGL 信息
      if (deviceInfo.webglSupported !== undefined) {
        const originalGetContext = HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext = function(contextType, contextAttributes) {
          if (contextType === 'webgl' || contextType === 'experimental-webgl') {
            if (!deviceInfo.webglSupported) {
              return null;
            }
            const context = originalGetContext.call(this, contextType, contextAttributes);
            if (context && deviceInfo.webglRenderer) {
              const originalGetParameter = context.getParameter;
              context.getParameter = function(parameter) {
                if (parameter === context.RENDERER) {
                  return deviceInfo.webglRenderer;
                }
                if (parameter === context.VENDOR) {
                  return deviceInfo.webglVendor || 'WebKit';
                }
                return originalGetParameter.call(this, parameter);
              };
            }
            return context;
          }
          return originalGetContext.call(this, contextType, contextAttributes);
        };
      }
      
      // 随机模拟传感器信息
      const generateRandomSensorData = () => {
        return {
          acceleration: {
            x: (Math.random() - 0.5) * 0.2,
            y: (Math.random() - 0.5) * 0.2,
            z: (Math.random() - 0.5) * 0.2
          },
          accelerationIncludingGravity: {
            x: (Math.random() - 0.5) * 0.2 + 0.1,
            y: (Math.random() - 0.5) * 0.2 + 0.1,
            z: (Math.random() - 0.5) * 0.2 + 9.8
          },
          rotationRate: {
            alpha: (Math.random() - 0.5) * 0.1,
            beta: (Math.random() - 0.5) * 0.1,
            gamma: (Math.random() - 0.5) * 0.1
          },
          interval: 16
        };
      };
      
      // 随机模拟电池信息
      const generateRandomBatteryData = () => {
        const charging = Math.random() > 0.7; // 30%概率充电中
        const level = Math.random() * 0.8 + 0.2; // 0.2-1.0电量（20%-100%）
        return {
          charging: charging,
          chargingTime: charging ? Math.floor(Math.random() * 7200) : Infinity,
          dischargingTime: charging ? Infinity : Math.floor(Math.random() * 14400),
          level: level,
          timestamp: new Date().toISOString()
        };
      };
      
      // 随机模拟网络信息
      const generateRandomNetworkData = () => {
        const types = ['5g', '4g', 'slow-4g'];
        const type = types[Math.floor(Math.random() * types.length)];
        const downlink = type === '5g' ? Math.random() * 50 + 20 : 
                        type === '4g' ? Math.random() * 10 + 5 : 
                        Math.random() * 2 + 1;
        const rtt = type === '5g' ? Math.floor(Math.random() * 20 + 10) :
                   type === '4g' ? Math.floor(Math.random() * 50 + 20) :
                   Math.floor(Math.random() * 100 + 50);
        
        return {
          effectiveType: type,
          downlink: downlink,
          rtt: rtt,
          online: true
        };
      };
      
      // 模拟传感器API
      if ('DeviceMotionEvent' in window) {
        const originalAddEventListener = window.addEventListener;
        window.addEventListener = function(type, listener, options) {
          if (type === 'devicemotion') {
            const sensorData = generateRandomSensorData();
            // 立即触发一次事件
            setTimeout(() => {
              if (listener) {
                listener({
                  type: 'devicemotion',
                  acceleration: sensorData.acceleration,
                  accelerationIncludingGravity: sensorData.accelerationIncludingGravity,
                  rotationRate: sensorData.rotationRate,
                  interval: sensorData.interval
                });
              }
            }, 100);
            
            // 定期更新数据
            const interval = setInterval(() => {
              const newData = generateRandomSensorData();
              if (listener) {
                listener({
                  type: 'devicemotion',
                  acceleration: newData.acceleration,
                  accelerationIncludingGravity: newData.accelerationIncludingGravity,
                  rotationRate: newData.rotationRate,
                  interval: newData.interval
                });
              }
            }, 1000);
            
            // 返回清理函数
            return () => clearInterval(interval);
          } else if (type === 'deviceorientation') {
            // 模拟设备方向传感器
            const orientationData = {
              alpha: Math.random() * 360, // 0-360度
              beta: (Math.random() - 0.5) * 180, // -90到90度
              gamma: (Math.random() - 0.5) * 180, // -180到180度
              absolute: Math.random() > 0.5
            };
            
            // 立即触发一次事件
            setTimeout(() => {
              if (listener) {
                listener({
                  type: 'deviceorientation',
                  alpha: orientationData.alpha,
                  beta: orientationData.beta,
                  gamma: orientationData.gamma,
                  absolute: orientationData.absolute
                });
              }
            }, 100);
            
            // 定期更新数据
            const interval = setInterval(() => {
              const newData = {
                alpha: Math.random() * 360,
                beta: (Math.random() - 0.5) * 180,
                gamma: (Math.random() - 0.5) * 180,
                absolute: Math.random() > 0.5
              };
              if (listener) {
                listener({
                  type: 'deviceorientation',
                  alpha: newData.alpha,
                  beta: newData.beta,
                  gamma: newData.gamma,
                  absolute: newData.absolute
                });
              }
            }, 2000);
            
            // 返回清理函数
            return () => clearInterval(interval);
          }
          return originalAddEventListener.call(this, type, listener, options);
        };
      }
      
      // 模拟电池API
      if ('getBattery' in navigator) {
        const originalGetBattery = navigator.getBattery;
        navigator.getBattery = function() {
          const batteryData = generateRandomBatteryData();
          return Promise.resolve({
            charging: batteryData.charging,
            chargingTime: batteryData.chargingTime,
            dischargingTime: batteryData.dischargingTime,
            level: batteryData.level,
            addEventListener: function() {},
            removeEventListener: function() {},
            dispatchEvent: function() {}
          });
        };
      }
      
      // 模拟网络连接API
      if ('connection' in navigator) {
        const networkData = generateRandomNetworkData();
        Object.defineProperty(navigator, 'connection', {
          get: () => ({
            effectiveType: networkData.effectiveType,
            downlink: networkData.downlink,
            rtt: networkData.rtt,
            saveData: false,
            addEventListener: function() {},
            removeEventListener: function() {}
          }),
          configurable: true
        });
      }
      
      // 模拟在线状态
      Object.defineProperty(navigator, 'onLine', {
        get: () => true,
        configurable: true
      });
      
      // 定义全局标志
      window.__ELECTRON_INJECTED__ = true;
      window.__DEVICE_INFO__ = deviceInfo;
      
    } catch (e) {
      console.error('设备信息注入失败:', e);
    }
  })();
`;

// 最早时机：process.once('loaded')
process.once('loaded', () => {
  try {
    // 如果 document 已存在（大多数情况下在 loaded 时 documentElement 已存在），直接插入。
    const script = document.createElement('script');
    script.textContent = injectionCode;
    // 插入到 <head> 或 documentElement 的最前面，确保尽早执行
    (document.head || document.documentElement).appendChild(script);
    script.parentNode && script.parentNode.removeChild(script);
  } catch (e) {
    // fallback：在 DOMContentLoaded 也注入（确保不会丢）
    window.addEventListener('DOMContentLoaded', () => {
      try {
        const script = document.createElement('script');
        script.textContent = injectionCode;
        (document.head || document.documentElement).appendChild(script);
        script.parentNode && script.parentNode.removeChild(script);
      } catch (e2) {}
    }, { once: true });
  }
});
