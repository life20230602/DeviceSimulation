# RandomWebViewDialog 使用说明

## 概述

`RandomWebViewDialog` 是一个独立的随机WebView弹窗模块，实现了智能的用户行为模拟功能。它将WebView页面平分为12行6列的网格，支持随机滑动和基于配置概率的点击操作。

## 主要功能

### 1. 网格划分
- **网格结构**: 12行 × 6列，共72个网格单元
- **自动计算**: 根据设备分辨率自动计算每个网格的大小
- **精确定位**: 支持在指定网格内进行随机偏移点击

### 2. 随机滑动
- **自动触发**: 页面加载完成后自动开始
- **随机间隔**: 每3-8秒执行一次随机滑动
- **智能范围**: 滑动范围在页面边界内，避免无效操作
- **自然模拟**: 模拟真实用户的滑动行为

### 3. 智能点击
- **概率控制**: 根据点击配置管理器的概率设置执行点击
- **定时触发**: 每5秒执行一次点击操作
- **网格定位**: 在选中的网格内随机选择点击位置
- **状态监控**: 实时显示点击位置和概率信息

### 4. 行为控制
- **自动开始**: 页面加载完成后自动开始所有行为
- **手动控制**: 支持手动开始/停止自动行为
- **实时状态**: 按钮状态实时反映当前行为状态

## 文件结构

```
random_webview_dialog.py          # 主要的RandomWebViewDialog文件
├── RandomWebViewDialog          # 主对话框类
├── 网格管理                      # 12×6网格划分和计算
├── 随机滑动                      # 智能滑动模拟
├── 概率点击                      # 基于配置的点击执行
└── 行为控制                      # 自动行为管理
```

## 使用方法

### 1. 基本使用

```python
from random_webview_dialog import RandomWebViewDialog
from click_config_manager import ClickConfigManagerWidget

# 创建点击配置管理器
click_config_manager = ClickConfigManagerWidget()

# 创建设备数据
device = {
    "name": "iPhone 15 Pro",
    "width": 393,
    "height": 852,
    "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X)..."
}

# 创建RandomWebViewDialog
webview_dialog = RandomWebViewDialog(
    parent=None,
    device=device,
    url="https://www.example.com",
    click_config_manager=click_config_manager
)

webview_dialog.show()
```

### 2. 在主程序中使用

```python
# 在MainWindow中
def start_running(self):
    # 获取随机设备和URL
    device = self.db_manager.get_random_device()
    random_url_data = self.db_manager.get_random_url()
    
    # 创建WebView弹窗，传递点击配置管理器
    self.webview_dialog = RandomWebViewDialog(
        self, device, random_url_data['url'], self.click_config_manager
    )
    self.webview_dialog.show()
```

## 核心算法

### 1. 网格划分算法

```python
def calculate_grid_click_position(self, config):
    """计算网格中的实际点击位置"""
    row = config["row_index"]
    col = config["col_index"]
    
    # 计算网格大小
    grid_width = self.device["width"] / self.grid_cols
    grid_height = self.device["height"] / self.grid_rows
    
    # 计算网格中心点
    center_x = int(col * grid_width + grid_width / 2)
    center_y = int(row * grid_height + grid_height / 2)
    
    # 在网格内添加随机偏移
    offset_x = random.randint(-int(grid_width/4), int(grid_width/4))
    offset_y = random.randint(-int(grid_height/4), int(grid_height/4))
    
    # 确保坐标在有效范围内
    final_x = max(10, min(center_x + offset_x, self.device["width"] - 10))
    final_y = max(10, min(center_y + offset_y, self.device["height"] - 10))
    
    return final_x, final_y
```

### 2. 概率选择算法

```python
def select_click_config_by_probability(self, enabled_configs):
    """根据概率选择点击配置"""
    # 计算总概率
    total_probability = sum(config.get("percentage", 0) for config in enabled_configs)
    if total_probability <= 0:
        return None
        
    # 生成随机数
    random_value = random.uniform(0, total_probability)
    
    # 根据概率选择配置
    current_probability = 0
    for config in enabled_configs:
        current_probability += config.get("percentage", 0)
        if random_value <= current_probability:
            return config
            
    return None
```

### 3. 随机滑动算法

```python
def perform_random_scroll(self):
    """执行随机滑动"""
    # 生成随机滑动参数
    start_x = random.randint(100, self.device["width"] - 100)
    start_y = random.randint(100, self.device["height"] - 100)
    end_x = start_x + random.randint(-200, 200)
    end_y = start_y + random.randint(-200, 200)
    
    # 确保滑动范围在页面内
    end_x = max(50, min(end_x, self.device["width"] - 50))
    end_y = max(50, min(end_y, self.device["height"] - 50))
    
    # 执行滑动
    self.humanized_touch.perform_swipe(
        QPoint(start_x, start_y),
        QPoint(end_x, end_y),
        duration=random.randint(500, 1500)
    )
```

## 配置要求

### 1. 点击配置管理器
- 必须提供有效的点击配置管理器实例
- 配置管理器应包含启用的点击配置
- 每个配置应包含行索引、列索引和概率值

### 2. 设备信息
- 设备名称（name）
- 屏幕宽度（width）
- 屏幕高度（height）
- User Agent字符串

### 3. 依赖模块
- PyQt5
- PyQtWebEngine
- touch模块（HumanizedController）

## 界面特性

### 1. 信息显示
- **设备信息**: 显示设备名称、分辨率和URL
- **网格信息**: 显示网格结构和行为说明
- **状态指示**: 实时显示当前行为状态

### 2. 控制按钮
- **刷新**: 重新加载当前页面
- **开始/停止自动行为**: 控制自动行为的开关
- **关闭**: 关闭对话框

### 3. 样式设计
- **现代化UI**: 使用Material Design风格的按钮
- **颜色编码**: 不同功能使用不同颜色区分
- **响应式布局**: 自适应不同设备分辨率

## 工作流程

### 1. 初始化阶段
1. 创建对话框和WebView
2. 设置设备配置和User Agent
3. 注入JavaScript脚本
4. 初始化触摸控制器

### 2. 页面加载阶段
1. 监听页面加载开始事件
2. 更新窗口标题显示加载状态
3. 监听页面加载完成事件

### 3. 自动行为阶段
1. 页面加载完成后自动开始
2. 启动随机滑动定时器（3-8秒间隔）
3. 启动随机点击定时器（5秒间隔）
4. 根据概率选择点击位置

### 4. 行为执行阶段
1. **滑动执行**: 在页面范围内随机生成滑动路径
2. **点击执行**: 根据配置概率选择网格位置
3. **位置计算**: 将网格坐标转换为实际像素坐标
4. **操作执行**: 通过触摸控制器执行具体操作

## 测试方法

### 1. 独立测试
```bash
python3 test_random_webview.py
```

### 2. 集成测试
在主程序中运行，测试与点击配置管理器的集成

### 3. 功能验证
- 验证网格划分是否正确
- 验证随机滑动是否自然
- 验证概率点击是否按配置执行
- 验证自动行为控制是否有效

## 注意事项

### 1. 性能考虑
- 定时器间隔不宜过短，避免过度消耗资源
- 随机数生成使用高效的算法
- 及时清理定时器，避免内存泄漏

### 2. 错误处理
- 检查设备信息的有效性
- 验证点击配置管理器的可用性
- 处理页面加载失败的情况

### 3. 用户体验
- 提供清晰的状态反馈
- 支持手动控制自动行为
- 显示详细的操作日志

## 扩展功能

### 1. 自定义网格
- 支持自定义行数和列数
- 支持不规则网格形状
- 支持动态网格调整

### 2. 行为模式
- 支持多种滑动模式
- 支持多种点击模式
- 支持行为序列配置

### 3. 数据分析
- 记录行为执行日志
- 统计点击分布情况
- 分析用户行为模式

## 故障排除

### 1. 常见问题
- **页面不加载**: 检查网络连接和URL有效性
- **点击不执行**: 检查点击配置管理器是否正确传递
- **滑动异常**: 检查触摸控制器是否正确初始化

### 2. 调试方法
- 查看控制台输出信息
- 检查定时器状态
- 验证配置数据完整性

### 3. 性能优化
- 调整定时器间隔
- 优化随机数生成
- 减少不必要的计算操作
