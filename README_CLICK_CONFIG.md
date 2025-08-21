# 点击配置管理器使用说明

## 概述

点击配置管理器是一个独立的模块，用于管理浏览器自动化点击的概率配置。它提供了12行6列的表格输入界面，支持为每个位置分配点击概率百分比，并将所有配置保存到SQLite数据库中。

## 功能特性

### 1. 点击配置管理
- **矩阵式配置**: 12行6列的配置矩阵，共72个可配置位置
- **概率设置**: 支持设置每个位置的点击概率（0-100%）
- **状态控制**: 支持启用/禁用单个配置
- **描述信息**: 为每个配置添加描述，便于识别和管理

### 2. 数据组织
- **位置标识**: 每个配置都有明确的行列位置标识
- **概率分配**: 每个位置可以设置0-100%的点击概率
- **时间记录**: 自动记录创建和更新时间

### 3. 界面交互
- **可视化表格**: 直观的表格界面，不同状态用不同颜色表示
- **点击配置**: 点击表格单元格即可打开配置对话框
- **实时反馈**: 配置状态实时显示在界面上
- **工具提示**: 鼠标悬停显示详细配置信息

### 4. 数据管理
- **自动保存**: 配置修改后自动保存到数据库
- **批量操作**: 支持清空所有配置
- **数据导出**: 支持导出配置为字典格式
- **统计信息**: 显示配置总数、启用数量、总概率等统计信息

## 文件结构

```
click_config_manager.py          # 主要的点击配置管理器文件
├── ClickConfigDatabaseManager  # 数据库管理类
├── ClickConfigEditDialog      # 编辑对话框类
└── ClickConfigManagerWidget   # 主界面管理类
```

## 数据库表结构

```sql
CREATE TABLE click_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    row_index INTEGER NOT NULL,           -- 行索引（0-11）
    col_index INTEGER NOT NULL,           -- 列索引（0-5）
    percentage INTEGER DEFAULT 0,         -- 点击概率（0-100%）
    description TEXT,                     -- 描述信息
    is_enabled BOOLEAN DEFAULT 1,         -- 是否启用
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 更新时间
    UNIQUE(row_index, col_index)         -- 位置唯一约束
);
```

## 使用方法

### 1. 在主程序中使用

```python
from click_config_manager import ClickConfigManagerWidget

# 在标签页中添加点击配置管理器
self.click_config_manager = ClickConfigManagerWidget()
self.tab_widget.addTab(self.click_config_manager, "点击配置")
```

### 2. 获取启用的点击配置

```python
# 获取所有启用的点击配置
enabled_configs = self.click_config_manager.get_enabled_click_configs()

# 获取指定位置的配置
config = self.click_config_manager.get_click_config_at_position(row, col)
```

### 3. 监听更新信号

```python
# 连接更新信号
self.click_config_manager.click_config_updated.connect(self.on_click_config_updated)

def on_click_config_updated(self):
    print("点击配置已更新")
```

### 4. 导出配置数据

```python
# 导出所有配置为字典格式
configs_dict = self.click_config_manager.export_configs_to_dict()
```

## 界面操作

### 配置点击概率
1. 点击表格中的任意单元格
2. 在弹出的对话框中设置：
   - **点击概率**: 设置该位置的点击概率（0-100%）
   - **描述**: 添加配置说明
   - **启用状态**: 是否启用此配置
3. 点击"保存"按钮

### 查看配置状态
- **浅绿色**: 已配置且启用的位置（概率>0%）
- **黄色**: 已配置且启用的位置（概率=0%）
- **灰色**: 已配置但禁用的位置
- **浅灰色**: 未配置的位置

### 批量操作
- **保存所有配置**: 确认所有配置已保存
- **清空所有配置**: 删除所有配置（需确认）
- **刷新**: 重新加载数据库中的配置

### 统计信息
- **总配置数**: 已配置的位置总数
- **启用**: 启用的配置数量
- **禁用**: 禁用的配置数量
- **未配置**: 未配置的位置数量
- **总概率**: 所有启用配置的概率总和

## 配置示例

### 基本点击配置
```python
{
    "row_index": 0,
    "col_index": 0,
    "percentage": 25,
    "description": "首页登录按钮",
    "is_enabled": True
}
```

### 批量配置示例
```python
# 配置第一行的所有列，概率递增
for col in range(6):
    config = {
        "row_index": 0,
        "col_index": col,
        "percentage": (col + 1) * 10,  # 10%, 20%, 30%, 40%, 50%, 60%
        "description": f"第{col+1}列按钮",
        "is_enabled": True
    }
    # 保存配置...
```

## 注意事项

1. **位置唯一性**: 每个行列位置只能有一个配置
2. **概率范围**: 点击概率范围为0-100%
3. **状态管理**: 只有启用状态的配置才会被其他模块使用
4. **数据安全**: 清空操作会要求用户确认
5. **概率总和**: 建议所有启用配置的概率总和不超过100%

## 扩展功能

### 1. 批量导入导出
可以扩展支持CSV、JSON等格式的批量导入导出

### 2. 配置模板
可以添加常用配置模板，快速应用到多个位置

### 3. 概率验证
可以添加概率验证功能，检查概率总和是否合理

### 4. 配置历史
可以添加配置修改历史记录，支持撤销操作

## 技术实现

- **数据库**: SQLite3
- **UI框架**: PyQt5
- **表格控件**: QTableWidget
- **对话框**: QDialog
- **信号机制**: PyQt信号槽机制
- **数据验证**: 完善的输入验证和错误处理

## 依赖要求

```
PyQt5 >= 5.15.0
sqlite3 (Python内置)
typing (Python内置)
```

## 测试

运行测试脚本验证功能：

```bash
python3 test_click_config.py
```

这将打开一个独立的点击配置管理器窗口，可以测试所有功能。

## 集成建议

### 1. 与自动化模块集成
```python
# 根据概率执行点击
enabled_configs = self.click_config_manager.get_enabled_click_configs()
for config in enabled_configs:
    if config["is_enabled"]:
        # 根据概率决定是否点击
        if random.randint(1, 100) <= config["percentage"]:
            # 执行点击操作
            self.perform_click(config["row_index"], config["col_index"])
```

### 2. 与设备管理集成
```python
# 根据设备尺寸调整点击位置
device = self.get_current_device()
config = self.click_config_manager.get_click_config_at_position(row, col)
if config and config["is_enabled"]:
    # 计算实际点击位置
    actual_x = int((row / 12) * device["width"])
    actual_y = int((col / 6) * device["height"])
    # 执行点击...
```

### 3. 与来路设置集成
```python
# 结合来路设置和点击配置
referrer = self.referrer_manager.get_random_referrer()
if referrer:
    # 先访问来路页面
    self.navigate_to(referrer["url"])
    
    # 然后根据概率执行点击配置
    click_configs = self.click_config_manager.get_enabled_click_configs()
    for config in click_configs:
        # 根据概率执行点击...
```

## 性能优化

1. **延迟加载**: 配置数据按需加载，避免一次性加载所有数据
2. **缓存机制**: 对频繁访问的配置进行缓存
3. **批量操作**: 支持批量保存和更新操作

## 故障排除

### 常见问题
1. **配置不保存**: 检查数据库权限和连接状态
2. **界面不显示**: 确认PyQt5安装正确
3. **概率无效**: 检查概率值是否在0-100范围内

### 调试方法
1. 查看控制台输出信息
2. 检查数据库文件完整性
3. 验证配置文件权限
4. 测试独立运行模式
