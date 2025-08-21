#!/bin/bash

echo "HS(火山) 浏览器管理工具 - macOS版本"
echo "========================================"
echo

# 设置macOS特定的环境变量
export QTWEBENGINE_CHROMIUM_FLAGS="--disable-web-security --disable-features=VizDisplayCompositor --no-sandbox"
export QT_MAC_WANTS_ICON=1
export QT_MAC_DISABLE_ICON=0
export QT_LOGGING_RULES="qt.webengine*=false"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.7+"
    echo "macOS: brew install python3"
    exit 1
fi

# 检查依赖
echo "检查依赖包..."
if ! python3 -c "import PyQt5, PyQtWebEngine" &> /dev/null; then
    echo "缺少依赖包，正在安装..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "依赖包安装失败，请手动运行: pip3 install -r requirements.txt"
        exit 1
    fi
fi

# 启动应用程序
echo "启动应用程序..."
echo "使用环境变量:"
echo "  QTWEBENGINE_CHROMIUM_FLAGS=$QTWEBENGINE_CHROMIUM_FLAGS"
echo "  QT_MAC_WANTS_ICON=$QT_MAC_WANTS_ICON"
echo "  QT_LOGGING_RULES=$QT_LOGGING_RULES"

# 使用python3启动
python3 main.py
