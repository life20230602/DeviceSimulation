#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
来路设置管理器测试脚本
"""

import sys
from PyQt5.QtWidgets import QApplication
from referrer_manager import ReferrerManagerWidget

def test_referrer_manager():
    """测试来路设置管理器"""
    app = QApplication(sys.argv)
    
    # 创建来路设置管理器窗口
    referrer_widget = ReferrerManagerWidget()
    referrer_widget.setWindowTitle("来路设置管理器测试")
    referrer_widget.resize(1000, 600)
    referrer_widget.show()
    
    # 连接信号
    referrer_widget.referrer_updated.connect(lambda: print("来路设置已更新"))
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_referrer_manager()
