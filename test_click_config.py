#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
点击配置管理器测试脚本
"""

import sys
from PyQt5.QtWidgets import QApplication
from click_config_manager import ClickConfigManagerWidget

def test_click_config_manager():
    """测试点击配置管理器"""
    app = QApplication(sys.argv)
    
    # 创建点击配置管理器窗口
    click_config_widget = ClickConfigManagerWidget()
    click_config_widget.setWindowTitle("点击配置管理器测试")
    click_config_widget.resize(1200, 800)
    click_config_widget.show()
    
    # 连接信号
    click_config_widget.click_config_updated.connect(lambda: print("点击配置已更新"))
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_click_config_manager()
