# 来路设置管理器使用说明

## 概述

来路设置管理器是一个独立的模块，用于管理浏览器访问的来路URL。它提供了完整的CRUD操作界面，支持URL的增删改查、分类管理、状态控制等功能。

## 功能特性

### 1. 来路设置管理
- **添加来路设置**: 支持添加新的来路URL，包含描述和分类信息
- **编辑来路设置**: 修改现有来路设置的URL、描述和分类
- **删除来路设置**: 安全删除不需要的来路设置
- **状态控制**: 支持激活/禁用来路设置

### 2. 数据组织
- **分类管理**: 支持按类别组织来路设置（如：search、social、video、shopping等）
- **描述信息**: 为每个来路设置添加描述，便于识别和管理
- **时间记录**: 自动记录创建和更新时间

### 3. 搜索和筛选
- **实时搜索**: 支持按URL、描述、分类进行模糊搜索
- **状态筛选**: 可以查看激活或禁用的来路设置

### 4. 统计信息
- **总数统计**: 显示所有来路设置的数量
- **状态统计**: 分别显示激活和禁用的数量

## 文件结构

```
referrer_manager.py          # 主要的来路设置管理器文件
├── ReferrerDatabaseManager  # 数据库管理类
├── ReferrerEditDialog      # 编辑对话框类
└── ReferrerManagerWidget   # 主界面管理类
```

## 数据库表结构

```sql
CREATE TABLE referrers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,           -- URL地址（唯一）
    description TEXT,                   -- 描述信息
    category TEXT DEFAULT 'general',    -- 分类
    is_active BOOLEAN DEFAULT 1,        -- 是否激活
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP   -- 更新时间
);
```

## 使用方法

### 1. 在主程序中使用

```python
from referrer_manager import ReferrerManagerWidget

# 在标签页中添加来路设置管理器
self.referrer_manager = ReferrerManagerWidget()
self.tab_widget.addTab(self.referrer_manager, "来路设置")
```

### 2. 获取激活的来路设置

```python
# 获取所有激活的来路设置
active_referrers = self.referrer_manager.get_active_referrers()

# 获取随机来路设置
random_referrer = self.referrer_manager.get_random_referrer()
```

### 3. 监听更新信号

```python
# 连接更新信号
self.referrer_manager.referrer_updated.connect(self.on_referrer_updated)

def on_referrer_updated(self):
    print("来路设置已更新")
```

## 界面操作

### 添加来路设置
1. 点击"添加来路设置"按钮
2. 在弹出的对话框中输入：
   - URL地址（必填）
   - 描述信息（可选）
   - 分类（可选，默认为general）
3. 点击"保存"按钮

### 编辑来路设置
1. 在表格中找到要编辑的行
2. 点击该行的"编辑"按钮
3. 在弹出的对话框中修改信息
4. 点击"保存"按钮

### 切换状态
1. 在表格中找到要操作的行
2. 点击"激活"或"禁用"按钮
3. 状态会立即更新

### 删除来路设置
1. 在表格中找到要删除的行
2. 点击"删除"按钮
3. 确认删除操作

### 搜索来路设置
1. 在搜索框中输入关键词
2. 系统会实时显示匹配的结果
3. 清空搜索框可恢复显示所有数据

## 默认数据

系统初始化时会自动创建以下分类的来路设置：

- **搜索引擎**: Google、百度、必应、搜狗、360
- **社交平台**: 知乎、微博、抖音、快手
- **视频平台**: B站、优酷、爱奇艺
- **购物平台**: 淘宝、京东、天猫
- **门户网站**: 腾讯、新浪、搜狐、网易

## 注意事项

1. **URL唯一性**: 每个URL地址在系统中只能存在一次
2. **数据安全**: 删除操作会要求用户确认
3. **状态管理**: 只有激活状态的来路设置才会被其他模块使用
4. **分类建议**: 建议使用有意义的分类名称，便于管理和查找

## 扩展功能

### 1. 批量操作
可以扩展支持批量导入、导出、删除等操作

### 2. 高级筛选
可以添加按时间范围、分类组合等高级筛选功能

### 3. 数据统计
可以添加访问统计、使用频率等数据分析功能

### 4. API接口
可以添加RESTful API接口，支持外部系统调用

## 技术实现

- **数据库**: SQLite3
- **UI框架**: PyQt5
- **架构模式**: MVC模式
- **信号机制**: PyQt信号槽机制
- **错误处理**: 完善的异常处理和用户提示

## 依赖要求

```
PyQt5 >= 5.15.0
sqlite3 (Python内置)
typing (Python内置)
```

## 测试

运行测试脚本验证功能：

```bash
python test_referrer.py
```

这将打开一个独立的来路设置管理器窗口，可以测试所有功能。
