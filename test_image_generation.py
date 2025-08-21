#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from random_webview_dialog import RandomWebViewDialog
from click_config_manager import ClickConfigManagerWidget

def test_image_generation():
    """测试点击位置图片生成功能"""
    app = QApplication(sys.argv)
    
    # 创建点击配置管理器
    click_config_manager = ClickConfigManagerWidget()
    
    # 模拟设备数据
    device = {
        "name": "iPhone 15 Pro",
        "width": 393,
        "height": 852,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    }
    
    # 创建RandomWebViewDialog
    dialog = RandomWebViewDialog(None, device, "https://example.com", click_config_manager)
    
    # 模拟一些点击位置
    dialog.click_positions = [
        {
            'timestamp': 1234567890,
            'grid_position': (1, 1),
            'percentage': 0.02,
            'coordinates': (50, 100),
            'device_size': (393, 852)
        },
        {
            'timestamp': 1234567891,
            'grid_position': (2, 3),
            'percentage': 0.02,
            'coordinates': (150, 200),
            'device_size': (393, 852)
        },
        {
            'timestamp': 1234567892,
            'grid_position': (5, 4),
            'percentage': 0.02,
            'coordinates': (250, 300),
            'device_size': (393, 852)
        }
    ]
    
    print(f"模拟了 {len(dialog.click_positions)} 个点击位置")
    
    # 测试图片生成
    print("测试生成点击位置图片...")
    dialog.generate_click_positions_image()
    
    print("测试完成！")
    
    # 不显示窗口，只测试功能
    dialog.close()

if __name__ == "__main__":
    test_image_generation()
