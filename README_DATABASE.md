# 数据库系统使用说明

## 🎯 概述

现在所有的设备和URL数据都存储在SQLite数据库中，不再硬编码在代码中。这样可以：
- 动态管理设备和URL
- 支持数据的增删改查
- 数据持久化存储
- 便于数据备份和恢复

## 🗄️ 数据库结构

### 设备表 (devices)
```sql
CREATE TABLE devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,           -- 设备名称（唯一）
    width INTEGER NOT NULL,              -- 屏幕宽度
    height INTEGER NOT NULL,             -- 屏幕高度
    user_agent TEXT NOT NULL,            -- User Agent字符串
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### URL表 (urls)
```sql
CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,            -- URL地址（唯一）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 使用方法

### 1. 初始化数据库
首次使用前，需要初始化数据库：
```bash
python3 init_database.py
```

这将创建数据库文件 `webview_data.db` 并插入默认数据：
- **34个设备**：包含桌面、Android、iOS设备
- **15个URL**：常用网站地址

### 2. 运行主程序
```bash
python3 main.py
```

### 3. 管理设备
- **查看设备**：切换到"设备管理"标签页
- **添加设备**：填写设备信息，点击"添加设备"
- **删除设备**：在设备列表中点击"删除"按钮
- **搜索设备**：支持按名称或User Agent搜索

### 4. 管理URL
- **查看URL**：切换到"URL列表"标签页
- **添加URL**：输入URL地址，点击"添加URL"
- **删除URL**：在URL列表中点击"删除"按钮
- **随机选择**：点击"随机选择URL"按钮

### 5. 运行测试
点击"运行"按钮，系统会：
1. 随机选择一个设备
2. 随机选择一个URL
3. 创建WebView弹窗
4. 应用设备的屏幕尺寸和User Agent

## 🔧 数据库管理器功能

### 设备管理
- `get_all_devices()` - 获取所有设备
- `get_device_by_id(id)` - 根据ID获取设备
- `add_device(name, width, height, user_agent)` - 添加设备
- `update_device(id, name, width, height, user_agent)` - 更新设备
- `delete_device(id)` - 删除设备
- `get_random_device()` - 获取随机设备
- `search_devices(keyword)` - 搜索设备

### URL管理
- `get_all_urls()` - 获取所有URL
- `get_url_by_id(id)` - 根据ID获取URL
- `add_url(url)` - 添加URL
- `update_url(id, url)` - 更新URL
- `delete_url(id)` - 删除URL
- `get_random_url()` - 获取随机URL
- `search_urls(keyword)` - 搜索URL

### 数据库维护
- `get_device_count()` - 获取设备数量
- `get_url_count()` - 获取URL数量
- `backup_database(path)` - 备份数据库
- `restore_database(path)` - 恢复数据库

## 📊 默认数据

### 设备类型
1. **桌面设备** (2个)
   - Windows Desktop
   - macOS Desktop

2. **Android设备** (16个)
   - Samsung Galaxy S24/S23/S22
   - Google Pixel 8/7系列
   - OnePlus 12/11
   - Xiaomi 14/13系列
   - OPPO Find X7/X6系列
   - vivo X100/X90系列
   - Huawei Mate 60/P60系列

3. **iOS设备** (16个)
   - iPhone 15/14/13/12系列
   - iPhone SE系列

### 默认URL
- 搜索引擎：百度、Google、Bing
- 开发平台：GitHub、Stack Overflow
- 社交媒体：知乎、微博、Twitter、Facebook、Instagram、LinkedIn
- 电商平台：淘宝、京东
- 娱乐平台：Netflix、YouTube

## 💡 高级功能

### 数据导入导出
```python
# 备份数据库
db_manager.backup_database("backup_20241201.db")

# 恢复数据库
db_manager.restore_database("backup_20241201.db")
```

### 搜索功能
```python
# 搜索包含"iPhone"的设备
devices = db_manager.search_devices("iPhone")

# 搜索包含"google"的URL
urls = db_manager.search_urls("google")
```

### 统计信息
```python
# 获取设备总数
device_count = db_manager.get_device_count()

# 获取URL总数
url_count = db_manager.get_url_count()
```

## 🐛 故障排除

### 数据库文件不存在
如果遇到数据库文件不存在的错误：
1. 运行 `python3 init_database.py` 初始化数据库
2. 确保程序有写入权限

### 数据重复错误
- 设备名称必须唯一
- URL地址必须唯一
- 检查是否已存在相同数据

### 性能优化
- 数据库文件会自动创建索引
- 大量数据时建议定期备份
- 可以添加更多索引优化查询性能

## 🔮 未来扩展

- 支持设备分类和标签
- 添加设备使用统计
- 支持URL访问历史记录
- 添加数据导入导出功能
- 支持多用户数据隔离
