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