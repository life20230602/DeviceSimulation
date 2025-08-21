#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
创建SQLite数据库，插入默认的设备和URL数据
"""

import sqlite3
import os

def init_database():
    """初始化数据库"""
    # 数据库文件路径
    db_path = "webview_data.db"
    
    # 如果数据库文件已存在，先删除
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"已删除旧的数据库文件: {db_path}")
    
    # 创建数据库连接
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建设备表
    cursor.execute('''
        CREATE TABLE devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            width INTEGER NOT NULL,
            height INTEGER NOT NULL,
            user_agent TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建URL表
    cursor.execute('''
        CREATE TABLE urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    print("数据库表创建完成")
    
    # 插入默认设备数据
    devices = [
        # 桌面设备
        ("Desktop Windows", 1920, 1080, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
        ("Desktop macOS", 1440, 900, "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
        
        # Android 手机设备
        ("Samsung Galaxy S24 Ultra", 412, 915, "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"),
        ("Samsung Galaxy S23", 412, 915, "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"),
        ("Samsung Galaxy S22", 412, 915, "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"),
        ("Google Pixel 8 Pro", 412, 915, "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"),
        ("Google Pixel 8", 412, 915, "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"),
        ("Google Pixel 7", 412, 915, "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"),
        ("OnePlus 12", 412, 915, "Mozilla/5.0 (Linux; Android 14; CPH2581) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"),
        ("OnePlus 11", 412, 915, "Mozilla/5.0 (Linux; Android 13; CPH2449) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"),
        ("Xiaomi 14 Pro", 412, 915, "Mozilla/5.0 (Linux; Android 14; 2311DRK48C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"),
        ("Xiaomi 13 Ultra", 412, 915, "Mozilla/5.0 (Linux; Android 13; 2304FPN6DG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"),
        ("OPPO Find X7 Ultra", 412, 915, "Mozilla/5.0 (Linux; Android 14; PHJ110) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"),
        ("OPPO Find X6 Pro", 412, 915, "Mozilla/5.0 (Linux; Android 13; PGEM10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"),
        ("vivo X100 Pro+", 412, 915, "Mozilla/5.0 (Linux; Android 14; V2307A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"),
        ("vivo X90 Pro+", 412, 915, "Mozilla/5.0 (Linux; Android 13; V2246A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"),
        ("Huawei Mate 60 Pro+", 412, 915, "Mozilla/5.0 (Linux; Android 12; ALH-AN10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"),
        ("Huawei P60 Pro", 412, 915, "Mozilla/5.0 (Linux; Android 12; ALH-AN00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"),
        
        # iOS 手机设备
        ("iPhone 15 Pro Max", 430, 932, "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"),
        ("iPhone 15 Pro", 393, 852, "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"),
        ("iPhone 15 Plus", 430, 932, "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"),
        ("iPhone 15", 393, 852, "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"),
        ("iPhone 14 Pro Max", 430, 932, "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"),
        ("iPhone 14 Pro", 393, 852, "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"),
        ("iPhone 14 Plus", 430, 932, "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"),
        ("iPhone 14", 393, 852, "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"),
        ("iPhone 13 Pro Max", 428, 926, "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"),
        ("iPhone 13 Pro", 390, 844, "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"),
        ("iPhone 13", 390, 844, "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"),
        ("iPhone 12 Pro Max", 428, 926, "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"),
        ("iPhone 12 Pro", 390, 844, "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"),
        ("iPhone 12", 390, 844, "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"),
        ("iPhone SE (3rd gen)", 375, 667, "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"),
        ("iPhone SE (2nd gen)", 375, 667, "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1")
    ]
    
    cursor.executemany('''
        INSERT INTO devices (name, width, height, user_agent)
        VALUES (?, ?, ?, ?)
    ''', devices)
    
    print(f"已插入 {len(devices)} 个设备")
    
    # 插入默认URL数据
    urls = [
        ("https://www.baidu.com",)
    ]
    
    cursor.executemany('''
        INSERT INTO urls (url)
        VALUES (?)
    ''', urls)
    
    print(f"已插入 {len(urls)} 个URL")
    
    # 提交事务
    conn.commit()
    
    # 验证数据
    cursor.execute("SELECT COUNT(*) FROM devices")
    device_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM urls")
    url_count = cursor.fetchone()[0]
    
    print(f"\n数据库初始化完成:")
    print(f"- 设备数量: {device_count}")
    print(f"- URL数量: {url_count}")
    print(f"- 数据库文件: {db_path}")
    
    # 关闭连接
    conn.close()

if __name__ == "__main__":
    init_database()
