#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试referrer设置的脚本
"""

import sys
from PyQt5.QtWidgets import QApplication
from random_webview_dialog import RandomWebViewDialog

def test_referrer_webview():
    """测试referrer设置"""
    app = QApplication(sys.argv)
    
    # 模拟设备
    device = {
        "name": "iPhone 15 Pro",
        "width": 393,
        "height": 852,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    }
    
    # 测试URL
    test_url = "https://www.baidu.com"
    
    # 测试referrer
    test_referrer = "https://www.google.com"
    
    print(f"测试URL: {test_url}")
    print(f"测试Referrer: {test_referrer}")
    
    # 创建WebView弹窗
    dialog = RandomWebViewDialog(
        parent=None,
        device=device,
        url=test_url,
        click_config_manager=None,
        referrer_url=test_referrer
    )
    
    dialog.show()
    
    print("WebView弹窗已打开，请检查网络请求的Referer头")
    print("按Ctrl+C退出")
    
    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("\n测试结束")

if __name__ == "__main__":
    test_referrer_webview()
