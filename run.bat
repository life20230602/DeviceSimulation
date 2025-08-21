@echo off
chcp 65001 >nul
echo HS(火山) 浏览器管理工具
echo ================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖
echo 检查依赖包...
python -c "import PyQt5, PyQtWebEngine" >nul 2>&1
if errorlevel 1 (
    echo 缺少依赖包，正在安装...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 依赖包安装失败，请手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

REM 启动应用程序
echo 启动应用程序...
python main.py

pause
