#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
来路设置管理器
处理来路URL的增删改查操作，并提供UI界面
"""

import sqlite3
from typing import List, Dict, Optional
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QDialog, QFormLayout,
                             QGroupBox, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class ReferrerDatabaseManager:
    """来路设置数据库管理器"""
    
    def __init__(self, db_path: str = "webview_data.db"):
        self.db_path = db_path
        self.init_referrer_table()
        
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)
        
    def init_referrer_table(self):
        """初始化来路设置表"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 检查表是否存在，如果不存在则创建
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS referrers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL UNIQUE,
                    description TEXT,
                    category TEXT DEFAULT 'general',
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            print("来路设置表初始化完成")
        except Exception as e:
            print(f"初始化来路设置表失败: {e}")
            
    def get_all_referrers(self) -> List[Dict]:
        """获取所有来路设置"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, url, description, category, is_active, created_at, updated_at
            FROM referrers
            ORDER BY created_at DESC
        ''')
        
        referrers = []
        for row in cursor.fetchall():
            referrers.append({
                "id": row[0],
                "url": row[1],
                "description": row[2] or "",
                "category": row[3] or "general",
                "is_active": bool(row[4]),
                "created_at": row[5],
                "updated_at": row[6]
            })
            
        conn.close()
        return referrers
        
    def get_referrer_by_id(self, referrer_id: int) -> Optional[Dict]:
        """根据ID获取来路设置"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, url, description, category, is_active, created_at, updated_at
            FROM referrers
            WHERE id = ?
        ''', (referrer_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "url": row[1],
                "description": row[2] or "",
                "category": row[3] or "general",
                "is_active": bool(row[4]),
                "created_at": row[5],
                "updated_at": row[6]
            }
        return None
        
    def add_referrer(self, url: str, description: str = "", category: str = "general") -> bool:
        """添加来路设置"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO referrers (url, description, category)
                VALUES (?, ?, ?)
            ''', (url, description, category))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # URL重复
            return False
        except Exception as e:
            print(f"添加来路设置失败: {e}")
            return False
            
    def update_referrer(self, referrer_id: int, url: str, description: str = "", 
                       category: str = "general", is_active: bool = True) -> bool:
        """更新来路设置"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE referrers
                SET url = ?, description = ?, category = ?, is_active = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (url, description, category, is_active, referrer_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"更新来路设置失败: {e}")
            return False
            
    def delete_referrer(self, referrer_id: int) -> bool:
        """删除来路设置"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM referrers WHERE id = ?', (referrer_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"删除来路设置失败: {e}")
            return False
            
    def toggle_referrer_status(self, referrer_id: int) -> bool:
        """切换来路设置状态"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE referrers
                SET is_active = CASE WHEN is_active = 1 THEN 0 ELSE 1 END,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (referrer_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"切换来路设置状态失败: {e}")
            return False
            
    def search_referrers(self, keyword: str) -> List[Dict]:
        """搜索来路设置"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, url, description, category, is_active, created_at, updated_at
            FROM referrers
            WHERE url LIKE ? OR description LIKE ? OR category LIKE ?
            ORDER BY created_at DESC
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        
        referrers = []
        for row in cursor.fetchall():
            referrers.append({
                "id": row[0],
                "url": row[1],
                "description": row[2] or "",
                "category": row[3] or "general",
                "is_active": bool(row[4]),
                "created_at": row[5],
                "updated_at": row[6]
            })
            
        conn.close()
        return referrers
        
    def get_referrer_count(self) -> int:
        """获取来路设置数量"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM referrers')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
        
    def get_active_referrers(self) -> List[Dict]:
        """获取所有激活的来路设置"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, url, description, category
            FROM referrers
            WHERE is_active = 1
            ORDER BY created_at DESC
        ''')
        
        referrers = []
        for row in cursor.fetchall():
            referrers.append({
                "id": row[0],
                "url": row[1],
                "description": row[2] or "",
                "category": row[3] or "general"
            })
            
        conn.close()
        return referrers

class ReferrerEditDialog(QDialog):
    """来路设置编辑对话框"""
    
    def __init__(self, parent=None, referrer_data: Dict = None):
        super().__init__(parent)
        self.referrer_data = referrer_data
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("编辑来路设置")
        self.setFixedSize(500, 300)
        
        layout = QVBoxLayout(self)
        
        # 表单布局
        form_layout = QFormLayout()
        
        # URL输入
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("请输入URL地址")
        if self.referrer_data:
            self.url_edit.setText(self.referrer_data.get("url", ""))
        form_layout.addRow("URL地址:", self.url_edit)
        
        # 描述输入
        self.description_edit = QLineEdit()
        self.description_edit.setPlaceholderText("请输入描述信息")
        if self.referrer_data:
            self.description_edit.setText(self.referrer_data.get("description", ""))
        form_layout.addRow("描述:", self.description_edit)
        
        # 分类输入
        self.category_edit = QLineEdit()
        self.category_edit.setPlaceholderText("请输入分类")
        if self.referrer_data:
            self.category_edit.setText(self.referrer_data.get("category", ""))
        form_layout.addRow("分类:", self.category_edit)
        
        layout.addLayout(form_layout)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.accept)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
    def get_data(self) -> Dict:
        """获取输入的数据"""
        return {
            "url": self.url_edit.text().strip(),
            "description": self.description_edit.text().strip(),
            "category": self.category_edit.text().strip()
        }

class ReferrerManagerWidget(QWidget):
    """来路设置管理界面"""
    
    referrer_updated = pyqtSignal()  # 来路设置更新信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_manager = ReferrerDatabaseManager()
        self.init_ui()
        self.load_referrers()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("来路设置管理")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 搜索和添加区域
        search_add_frame = QFrame()
        search_add_frame.setFrameStyle(QFrame.Box)
        search_add_layout = QHBoxLayout(search_add_frame)
        
        # 搜索框
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("搜索来路设置...")
        self.search_edit.textChanged.connect(self.search_referrers)
        search_add_layout.addWidget(QLabel("搜索:"))
        search_add_layout.addWidget(self.search_edit)
        
        # 添加按钮
        self.add_button = QPushButton("添加来路设置")
        self.add_button.clicked.connect(self.add_referrer)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        search_add_layout.addWidget(self.add_button)
        
        layout.addWidget(search_add_frame)
        
        # 来路设置表格
        self.create_referrer_table()
        layout.addWidget(self.table)
        
        # 统计信息
        self.create_stats_frame()
        layout.addWidget(self.stats_frame)
        
    def create_referrer_table(self):
        """创建来路设置表格"""
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "URL", "描述", "分类", "状态", "创建时间", "操作"
        ])
        
        # 设置列宽
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.Stretch)           # URL
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # 描述
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # 分类
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # 状态
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # 创建时间
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # 操作
        
        # 设置表格样式
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
    def create_stats_frame(self):
        """创建统计信息框架"""
        self.stats_frame = QFrame()
        self.stats_frame.setFrameStyle(QFrame.Box)
        stats_layout = QHBoxLayout(self.stats_frame)
        
        self.total_label = QLabel("总数: 0")
        self.active_label = QLabel("激活: 0")
        self.inactive_label = QLabel("禁用: 0")
        
        stats_layout.addWidget(self.total_label)
        stats_layout.addWidget(self.active_label)
        stats_layout.addWidget(self.inactive_label)
        stats_layout.addStretch()
        
    def load_referrers(self):
        """加载来路设置数据"""
        referrers = self.db_manager.get_all_referrers()
        self.update_table(referrers)
        self.update_stats(referrers)
        
    def update_table(self, referrers: List[Dict]):
        """更新表格数据"""
        self.table.setRowCount(len(referrers))
        
        for row, referrer in enumerate(referrers):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(referrer["id"])))
            
            # URL
            url_item = QTableWidgetItem(referrer["url"])
            url_item.setToolTip(referrer["url"])
            self.table.setItem(row, 1, url_item)
            
            # 描述
            desc_item = QTableWidgetItem(referrer["description"])
            self.table.setItem(row, 2, desc_item)
            
            # 分类
            self.table.setItem(row, 3, QTableWidgetItem(referrer["category"]))
            
            # 状态
            status_text = "激活" if referrer["is_active"] else "禁用"
            status_item = QTableWidgetItem(status_text)
            status_item.setForeground(Qt.green if referrer["is_active"] else Qt.red)
            self.table.setItem(row, 4, status_item)
            
            # 创建时间
            created_time = referrer["created_at"]
            if created_time:
                time_str = str(created_time)[:19]  # 截取到秒
            else:
                time_str = "未知"
            self.table.setItem(row, 5, QTableWidgetItem(time_str))
            
            # 操作按钮
            self.create_action_buttons(row, referrer)
            
    def create_action_buttons(self, row: int, referrer: Dict):
        """创建操作按钮"""
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(2, 2, 2, 2)
        
        # 编辑按钮
        edit_btn = QPushButton("编辑")
        edit_btn.setFixedSize(50, 25)
        edit_btn.clicked.connect(lambda: self.edit_referrer(referrer))
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        
        # 状态切换按钮
        status_text = "禁用" if referrer["is_active"] else "激活"
        status_btn = QPushButton(status_text)
        status_btn.setFixedSize(50, 25)
        status_btn.clicked.connect(lambda: self.toggle_referrer_status(referrer))
        status_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        
        # 删除按钮
        delete_btn = QPushButton("删除")
        delete_btn.setFixedSize(50, 25)
        delete_btn.clicked.connect(lambda: self.delete_referrer(referrer))
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(status_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addStretch()
        
        self.table.setCellWidget(row, 6, button_widget)
        
    def update_stats(self, referrers: List[Dict]):
        """更新统计信息"""
        total = len(referrers)
        active = sum(1 for r in referrers if r["is_active"])
        inactive = total - active
        
        self.total_label.setText(f"总数: {total}")
        self.active_label.setText(f"激活: {active}")
        self.inactive_label.setText(f"禁用: {inactive}")
        
    def search_referrers(self):
        """搜索来路设置"""
        keyword = self.search_edit.text().strip()
        if not keyword:
            self.load_referrers()
        else:
            referrers = self.db_manager.search_referrers(keyword)
            self.update_table(referrers)
            self.update_stats(referrers)
            
    def add_referrer(self):
        """添加来路设置"""
        dialog = ReferrerEditDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            
            if not data["url"]:
                QMessageBox.warning(self, "警告", "请输入URL地址")
                return
                
            if self.db_manager.add_referrer(data["url"], data["description"], data["category"]):
                QMessageBox.information(self, "成功", "来路设置添加成功")
                self.load_referrers()
                self.referrer_updated.emit()
            else:
                QMessageBox.warning(self, "警告", "URL地址已存在")
                
    def edit_referrer(self, referrer: Dict):
        """编辑来路设置"""
        dialog = ReferrerEditDialog(self, referrer)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            
            if not data["url"]:
                QMessageBox.warning(self, "警告", "请输入URL地址")
                return
                
            if self.db_manager.update_referrer(
                referrer["id"], data["url"], data["description"], 
                data["category"], referrer["is_active"]
            ):
                QMessageBox.information(self, "成功", "来路设置更新成功")
                self.load_referrers()
                self.referrer_updated.emit()
            else:
                QMessageBox.warning(self, "错误", "更新失败")
                
    def toggle_referrer_status(self, referrer: Dict):
        """切换来路设置状态"""
        if self.db_manager.toggle_referrer_status(referrer["id"]):
            self.load_referrers()
            self.referrer_updated.emit()
        else:
            QMessageBox.warning(self, "错误", "状态切换失败")
            
    def delete_referrer(self, referrer: Dict):
        """删除来路设置"""
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除来路设置 '{referrer['url']}' 吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.db_manager.delete_referrer(referrer["id"]):
                QMessageBox.information(self, "成功", "来路设置删除成功")
                self.load_referrers()
                self.referrer_updated.emit()
            else:
                QMessageBox.warning(self, "错误", "删除失败")
                
    def get_active_referrers(self) -> List[Dict]:
        """获取所有激活的来路设置"""
        return self.db_manager.get_active_referrers()
        
    def get_random_referrer(self) -> Optional[Dict]:
        """获取随机来路设置"""
        active_referrers = self.get_active_referrers()
        if not active_referrers:
            return None
        import random
        return random.choice(active_referrers)
