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
// preload.js
// 这里的代码运行在“隔离世界”（preload），但我们会把要运行的 JS 注入到页面上下文。
// process.once('loaded') 是一个非常早的钩子 —— 在渲染器初始化后、页面脚本之前调用。
const injectionCode = `
  // 这是要在页面上下文最早执行的代码（示例：篡改 navigator）
  (function() {
    try {
      Object.defineProperty(navigator, 'platform', { get: () => 'Android', configurable: true });
      Object.defineProperty(navigator, 'webdriver', { get: () => false, configurable: true });
      // 你可以在这里放任意想要的 JS（尽量不要引入 Node API）
      // 例如重写 canvas/getContext 以伪造指纹（复杂），或定义全局标志
      window.__ELECTRON_INJECTED__ = true;
    } catch (e) {
      // ignore
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
