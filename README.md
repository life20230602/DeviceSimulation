# Electron 自动化演示

基于 Electron + Puppeteer 的移动端自动化测试工具，从 Java jvppeteer 项目移植而来。

## 功能特性

### 🎯 核心功能
- **设备模拟**: 支持多种移动设备模拟（iPhone、Android等）
- **智能点击**: 12x6网格概率点击系统
- **网络拦截**: 自动阻止图片、媒体、分析脚本等
- **触摸操作**: 模拟真实的触摸点击和滑动
- **批量任务**: 支持多任务并发执行
- **代理支持**: 支持HTTP代理配置

### 📱 设备管理
- 自动从UserAgent提取设备信息
- 支持华为、小米、Vivo、OPPO、Samsung等品牌
- 动态设备配置（分辨率、缩放、UserAgent等）
- WebGL信息注入，模拟真实设备

### 🎮 操作模拟
- 基于概率的智能点击算法
- 模拟真实用户行为（随机延迟、滑动等）
- 触摸事件模拟（touchstart、touchmove、touchend）
- 支持自定义点击概率网格

### 🌐 网络优化
- 智能资源拦截，减少网络流量
- 阻止不必要的资源加载
- 支持域名白名单/黑名单
- 实时网络统计

## 技术栈

- **Electron**: 跨平台桌面应用框架
- **Puppeteer**: Chrome DevTools Protocol 自动化
- **Node.js**: 后端运行时
- **HTML/CSS/JavaScript**: 前端界面

## 安装和运行

### 环境要求
- Node.js 16.0+
- npm 或 yarn

### 安装依赖
```bash
cd /Users/mac/Downloads/nodejsDemo
npm install
```

### 开发模式运行
```bash
npm run dev
```

### 生产模式运行
```bash
npm start
```

### 构建应用
```bash
npm run build
```

## 项目结构

```
nodejsDemo/
├── main.js                          # 主进程入口
├── package.json                     # 项目配置
├── src/
│   ├── automation/
│   │   ├── AutomationManager.js     # 自动化管理器
│   │   └── TaskManager.js          # 任务管理器
│   ├── device/
│   │   └── DeviceManager.js        # 设备信息管理
│   ├── network/
│   │   └── NetworkInterceptor.js   # 网络拦截器
│   ├── click/
│   │   └── ClickConfigManager.js   # 点击配置管理
│   └── renderer/                   # 渲染进程
│       ├── index.html              # 主页面
│       ├── css/
│       │   └── style.css           # 样式文件
│       └── js/
│           └── app.js              # 前端逻辑
└── assets/                         # 资源文件
```

## 使用说明

### 1. 设备配置
- 点击"获取随机设备"选择测试设备
- 系统会自动加载设备信息并显示详细信息
- 支持自定义屏幕分辨率

### 2. 任务配置
- 设置目标URL（默认：https://toup-023.cfd）
- 配置任务数量和并发数
- 可选配置代理服务器

### 3. 点击配置
- 12x6网格概率配置
- 可视化概率调整
- 支持自定义点击区域

### 4. 执行任务
- 点击"开始自动化"启动任务
- 实时查看任务状态和日志
- 支持截图和日志导出

## 配置说明

### 代理配置格式
```
ip:port:username:password
```
例如：`127.0.0.1:8080:user:pass`

### 点击概率网格
- 12行6列的网格系统
- 每个网格可设置0-1的概率值
- 颜色编码：
  - 绿色：高概率 (≥0.15)
  - 橙色：中概率 (0.05-0.15)
  - 红色：低概率 (<0.05)
  - 灰色：零概率 (0)

## API 接口

### 主进程 IPC 接口
- `get-random-device`: 获取随机设备
- `create-click-config`: 创建点击配置
- `perform-touch-click`: 执行触摸点击
- `perform-swipe`: 执行滑动操作
- `start-automation`: 启动自动化任务
- `stop-automation`: 停止自动化任务
- `start-batch-tasks`: 启动批量任务
- `get-task-status`: 获取任务状态
- `take-screenshot`: 截图

## 开发说明

### 添加新设备
在 `DeviceManager.js` 中的 `initializeDefaultDevices()` 方法中添加新设备配置。

### 自定义点击概率
在 `ClickConfigManager.js` 中的 `initDefaultGridProbabilities()` 方法中修改默认概率。

### 扩展网络拦截
在 `NetworkInterceptor.js` 中添加新的拦截规则。

## 注意事项

1. **性能优化**: 建议并发任务数不超过10个
2. **内存管理**: 长时间运行后建议重启应用
3. **网络稳定**: 确保网络连接稳定，避免任务失败
4. **代理配置**: 使用代理时确保代理服务器可用

## 故障排除

### 常见问题
1. **设备加载失败**: 检查UserAgent文件是否存在
2. **任务执行失败**: 检查网络连接和目标URL
3. **触摸操作无效**: 确保页面支持触摸事件
4. **代理连接失败**: 验证代理配置和服务器状态

### 日志查看
- 应用内日志面板显示实时日志
- 支持日志导出功能
- 日志级别：info、success、warning、error

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request 来改进项目。

---

**注意**: 本项目仅用于学习和研究目的，请遵守相关法律法规和网站使用条款。