#!/bin/bash

echo "🚀 启动 Electron 自动化演示应用..."

# 检查 Node.js 是否安装
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js，请先安装 Node.js"
    exit 1
fi

# 检查 npm 是否安装
if ! command -v npm &> /dev/null; then
    echo "❌ 错误: 未找到 npm，请先安装 npm"
    exit 1
fi

# 检查依赖是否安装
if [ ! -d "node_modules" ]; then
    echo "📦 安装依赖..."
    npm install
fi

# 创建必要的目录
mkdir -p screenshots
mkdir -p logs

echo "✅ 环境检查完成"
echo "🎯 启动应用..."

# 启动应用
npm start