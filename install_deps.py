#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖安装脚本 - 专门处理PyQt安装问题
"""

import sys
import subprocess
import platform
import os

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n{description}...")
    print(f"执行命令: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ 成功: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 失败: {e}")
        if e.stderr:
            print(f"错误信息: {e.stderr}")
        return False

def check_system():
    """检查系统信息"""
    print("系统信息:")
    print(f"操作系统: {platform.system()}")
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    print(f"pip版本: ", end="")
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        print(result.stdout.strip())
    except:
        print("未知")

def install_pyqt_conda():
    """使用conda安装PyQt"""
    print("\n尝试使用conda安装PyQt...")
    
    # 检查conda是否可用
    try:
        result = subprocess.run("conda --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 找到conda")
            
            # 创建环境
            env_name = "webview"
            if run_command(f"conda create -n {env_name} python=3.9 -y", "创建conda环境"):
                print(f"\n请运行以下命令激活环境并安装依赖:")
                print(f"conda activate {env_name}")
                print("conda install -c conda-forge pyqt=5.15.9 pyqtwebengine=5.15.6")
                return True
        else:
            print("❌ conda不可用")
    except:
        print("❌ conda不可用")
    
    return False

def install_pyqt_pip():
    """使用pip安装PyQt"""
    print("\n尝试使用pip安装PyQt...")
    
    # 先尝试安装预编译的wheel包
    packages = [
        "PyQt5==5.15.7",
        "PyQtWebEngine==5.15.5"
    ]
    
    for package in packages:
        if run_command(f"{sys.executable} -m pip install {package}", f"安装 {package}"):
            print(f"✅ {package} 安装成功")
        else:
            print(f"❌ {package} 安装失败")
            return False
    
    return True

def install_pyqt_system():
    """使用系统包管理器安装PyQt"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        print("\n尝试使用Homebrew安装PyQt...")
        if run_command("brew --version", "检查Homebrew"):
            if run_command("brew install pyqt5 pyqtwebengine", "安装PyQt"):
                return True
    elif system == "Linux":
        print("\n尝试使用apt安装PyQt...")
        if run_command("sudo apt update", "更新包列表"):
            if run_command("sudo apt install python3-pyqt5 python3-pyqt5.qtwebengine", "安装PyQt"):
                return True
    
    return False

def test_import():
    """测试PyQt导入"""
    print("\n测试PyQt导入...")
    
    try:
        import PyQt5
        print("✅ PyQt5 导入成功")
        
        import PyQt5.QtWebEngineWidgets
        print("✅ PyQtWebEngine 导入成功")
        
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def main():
    """主函数"""
    print("PyQt依赖安装脚本")
    print("=" * 50)
    
    # 检查系统信息
    check_system()
    
    # 尝试不同的安装方法
    methods = [
        ("conda安装", install_pyqt_conda),
        ("pip安装", install_pyqt_pip),
        ("系统包管理器安装", install_pyqt_system)
    ]
    
    for method_name, method_func in methods:
        print(f"\n{'='*20} {method_name} {'='*20}")
        if method_func():
            print(f"✅ {method_name} 成功!")
            break
        else:
            print(f"❌ {method_name} 失败")
    else:
        print("\n❌ 所有安装方法都失败了")
        print("\n建议:")
        print("1. 使用conda创建新环境")
        print("2. 手动下载wheel包安装")
        print("3. 使用系统包管理器")
        return False
    
    # 测试导入
    if test_import():
        print("\n🎉 所有依赖安装成功!")
        print("现在可以运行应用程序了:")
        print("python main.py")
        return True
    else:
        print("\n❌ 依赖安装可能有问题")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
