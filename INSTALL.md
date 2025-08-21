# 安装指南 - 解决PyQt安装问题

## 🚨 常见问题：Preparing metadata (pyproject.toml) 卡住

这是因为PyQt5和PyQtWebEngine需要编译，过程很慢且容易失败。

## 🔧 推荐解决方案

### 方案1：使用conda（最稳定）

```bash
# 1. 安装Miniconda
# 下载：https://docs.conda.io/en/latest/miniconda.html

# 2. 创建新环境
conda create -n webview python=3.9

# 3. 激活环境
conda activate webview

# 4. 安装PyQt
conda install -c conda-forge pyqt=5.15.9 pyqtwebengine=5.15.6

# 5. 安装其他依赖
pip install requests

# 6. 运行应用
python main.py
```

### 方案2：使用预编译wheel包

```bash
# 1. 卸载可能存在的包
pip uninstall PyQt5 PyQtWebEngine -y

# 2. 安装预编译包
pip install PyQt5==5.15.7
pip install PyQtWebEngine==5.15.5

# 3. 安装其他依赖
pip install requests
```

### 方案3：使用系统包管理器

**macOS:**
```bash
brew install pyqt5 pyqtwebengine
pip install requests
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3-pyqt5 python3-pyqt5.qtwebengine
pip install requests
```

## 🚀 快速安装脚本

运行我们提供的安装脚本：

```bash
python install_deps.py
```

这个脚本会自动尝试多种安装方法。

## 📋 系统要求

- **Python**: 3.7 - 3.11（推荐3.9）
- **操作系统**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **内存**: 至少4GB RAM
- **磁盘空间**: 至少2GB可用空间

## ❌ 不兼容的版本

避免使用以下版本组合：
- Python 3.12+ (PyQt5不支持)
- PyQt5 5.16+ (可能有兼容性问题)
- PyQtWebEngine 5.16+ (可能有兼容性问题)

## 🔍 故障排除

### 问题1：pip安装卡住
**解决方案**: 使用conda或系统包管理器

### 问题2：导入错误
**解决方案**: 检查Python版本，确保使用3.7-3.11

### 问题3：WebEngine不工作
**解决方案**: 确保安装了正确的PyQtWebEngine版本

### 问题4：权限错误
**解决方案**: 使用虚拟环境或conda环境

## 📱 验证安装

运行测试脚本：

```bash
python test_basic.py
```

如果看到成功消息，说明安装正确。

## 🌟 最佳实践

1. **使用虚拟环境**: 避免污染系统Python
2. **优先使用conda**: 预编译包，安装更快
3. **版本锁定**: 使用固定版本号避免兼容性问题
4. **系统更新**: 确保系统是最新版本

## 📞 获取帮助

如果仍然遇到问题：

1. 检查Python版本：`python --version`
2. 检查pip版本：`pip --version`
3. 查看错误日志
4. 尝试不同的Python版本
5. 使用conda环境

## 🎯 下一步

安装成功后，查看：
- `QUICKSTART.md` - 快速启动指南
- `README.md` - 完整功能说明
- `main.py` - 运行主程序
