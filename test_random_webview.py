#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RandomWebViewDialog测试脚本
"""

import sys
from PyQt5.QtWidgets import QApplication
from random_webview_dialog import RandomWebViewDialog
from click_config_manager import ClickConfigManagerWidget
from PyQt5.QtCore import QUrl
def test_random_webview():
    """测试RandomWebViewDialog"""
    app = QApplication(sys.argv)
    
    # 创建点击配置管理器
    click_config_manager = ClickConfigManagerWidget()
    
    # 模拟设备数据
    device = {
        "name": "iPhone 15 Pro",
        "width": 393,
        "height": 852,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"
    }
    
    # 创建RandomWebViewDialog
    webview_dialog = RandomWebViewDialog(
        parent=None,
        device=device,
        # url="https://www.baidu.com",
        click_config_manager=click_config_manager
    )
    webview_dialog.setWindowTitle("RandomWebViewDialog测试")
    webview_dialog.resize(800, 600)
    webview_dialog.show()
    
    webview_dialog.webview.load(QUrl.fromLocalFile('/Users/track/Downloads/2.html'));

    print("RandomWebViewDialog测试窗口已打开")
    print(f"设备: {device['name']}")
    print(f"分辨率: {device['width']}x{device['height']}")
    print(f"网格: 12行 × 6列")
    print("功能:")
    print("- 页面加载完成后自动开始随机滑动和点击")
    print("- 每5秒根据点击配置概率执行一次点击")
    print("- 每3-8秒执行一次随机滑动")
    print("- 支持手动控制自动行为的开始/停止")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_random_webview()
