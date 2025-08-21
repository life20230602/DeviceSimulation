#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库管理器
处理设备和URL的增删改查操作
"""

import sqlite3
import random
from typing import List, Dict, Optional

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str = "webview_data.db"):
        self.db_path = db_path
        
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)
        
    def get_all_devices(self) -> List[Dict]:
        """获取所有设备"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, width, height, user_agent, created_at
            FROM devices
            ORDER BY name
        ''')
        
        devices = []
        for row in cursor.fetchall():
            devices.append({
                "id": row[0],
                "name": row[1],
                "width": row[2],
                "height": row[3],
                "user_agent": row[4],
                "created_at": row[5]
            })
            
        conn.close()
        return devices
        
    def get_device_by_id(self, device_id: int) -> Optional[Dict]:
        """根据ID获取设备"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, width, height, user_agent, created_at
            FROM devices
            WHERE id = ?
        ''', (device_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "width": row[2],
                "height": row[3],
                "user_agent": row[4],
                "created_at": row[5]
            }
        return None
        
    def add_device(self, name: str, width: int, height: int, user_agent: str) -> bool:
        """添加设备"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO devices (name, width, height, user_agent)
                VALUES (?, ?, ?, ?)
            ''', (name, width, height, user_agent))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # 名称重复
            return False
        except Exception as e:
            print(f"添加设备失败: {e}")
            return False
            
    def update_device(self, device_id: int, name: str, width: int, height: int, user_agent: str) -> bool:
        """更新设备"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE devices
                SET name = ?, width = ?, height = ?, user_agent = ?
                WHERE id = ?
            ''', (name, width, height, user_agent, device_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"更新设备失败: {e}")
            return False
            
    def delete_device(self, device_id: int) -> bool:
        """删除设备"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM devices WHERE id = ?', (device_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"删除设备失败: {e}")
            return False
            
    def get_random_device(self) -> Optional[Dict]:
        """获取随机设备"""
        devices = self.get_all_devices()
        if not devices:
            return None
        return random.choice(devices)
        
    def get_all_urls(self) -> List[Dict]:
        """获取所有URL"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, url, created_at
            FROM urls
            ORDER BY url
        ''')
        
        urls = []
        for row in cursor.fetchall():
            urls.append({
                "id": row[0],
                "url": row[1],
                "created_at": row[2]
            })
            
        conn.close()
        return urls
        
    def get_url_by_id(self, url_id: int) -> Optional[Dict]:
        """根据ID获取URL"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, url, created_at
            FROM urls
            WHERE id = ?
        ''', (url_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "url": row[1],
                "created_at": row[2]
            }
        return None
        
    def add_url(self, url: str) -> bool:
        """添加URL"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('INSERT INTO urls (url) VALUES (?)', (url,))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # URL重复
            return False
        except Exception as e:
            print(f"添加URL失败: {e}")
            return False
            
    def update_url(self, url_id: int, url: str) -> bool:
        """更新URL"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('UPDATE urls SET url = ? WHERE id = ?', (url, url_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"更新URL失败: {e}")
            return False
            
    def delete_url(self, url_id: int) -> bool:
        """删除URL"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM urls WHERE id = ?', (url_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"删除URL失败: {e}")
            return False
            
    def get_random_url(self) -> Optional[Dict]:
        """获取随机URL"""
        urls = self.get_all_urls()
        if not urls:
            return None
        return random.choice(urls)
        
    def search_devices(self, keyword: str) -> List[Dict]:
        """搜索设备"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, width, height, user_agent, created_at
            FROM devices
            WHERE name LIKE ? OR user_agent LIKE ?
            ORDER BY name
        ''', (f'%{keyword}%', f'%{keyword}%'))
        
        devices = []
        for row in cursor.fetchall():
            devices.append({
                "id": row[0],
                "name": row[1],
                "width": row[2],
                "height": row[3],
                "user_agent": row[4],
                "created_at": row[5]
            })
            
        conn.close()
        return devices
        
    def search_urls(self, keyword: str) -> List[Dict]:
        """搜索URL"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, url, created_at
            FROM urls
            WHERE url LIKE ?
            ORDER BY url
        ''', (f'%{keyword}%',))
        
        urls = []
        for row in cursor.fetchall():
            urls.append({
                "id": row[0],
                "url": row[1],
                "created_at": row[2]
            })
            
        conn.close()
        return urls
        
    def get_device_count(self) -> int:
        """获取设备数量"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM devices')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
        
    def get_url_count(self) -> int:
        """获取URL数量"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM urls')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
        
    def backup_database(self, backup_path: str) -> bool:
        """备份数据库"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            return True
        except Exception as e:
            print(f"备份数据库失败: {e}")
            return False
            
    def restore_database(self, backup_path: str) -> bool:
        """恢复数据库"""
        try:
            import shutil
            shutil.copy2(backup_path, self.db_path)
            return True
        except Exception as e:
            print(f"恢复数据库失败: {e}")
            return False
