#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
点击配置管理器
处理点击配置的百分比分配，提供12行6列的表格输入界面
"""

import sqlite3
from typing import List, Dict, Optional
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QDialog, QFormLayout, QSpinBox, 
                             QFrame, QTextEdit, QCheckBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QBrush

class ClickConfigDatabaseManager:
    """点击配置数据库管理器"""
    
    def __init__(self, db_path: str = "webview_data.db"):
        self.db_path = db_path
        self.init_click_config_table()
        
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)
        
    def init_click_config_table(self):
        """初始化点击配置表"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 检查表是否存在，如果不存在则创建
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS click_configs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    row_index INTEGER NOT NULL,
                    col_index INTEGER NOT NULL,
                    percentage INTEGER DEFAULT 0,
                    description TEXT,
                    is_enabled BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(row_index, col_index)
                )
            ''')
            
            conn.commit()
            conn.close()
            print("点击配置表初始化完成")
        except Exception as e:
            print(f"初始化点击配置表失败: {e}")
            
    def get_all_click_configs(self) -> List[Dict]:
        """获取所有点击配置"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, row_index, col_index, percentage, description, 
                   is_enabled, created_at, updated_at
            FROM click_configs
            ORDER BY row_index, col_index
        ''')
        
        configs = []
        for row in cursor.fetchall():
            configs.append({
                "id": row[0],
                "row_index": row[1],
                "col_index": row[2],
                "percentage": row[3] or 0,
                "description": row[4] or "",
                "is_enabled": bool(row[5]),
                "created_at": row[6],
                "updated_at": row[7]
            })
            
        conn.close()
        return configs
        
    def get_click_config_by_position(self, row_index: int, col_index: int) -> Optional[Dict]:
        """根据位置获取点击配置"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, row_index, col_index, percentage, description, 
                   is_enabled, created_at, updated_at
            FROM click_configs
            WHERE row_index = ? AND col_index = ?
        ''', (row_index, col_index))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "row_index": row[1],
                "col_index": row[2],
                "percentage": row[3] or 0,
                "description": row[4] or "",
                "is_enabled": bool(row[5]),
                "created_at": row[6],
                "updated_at": row[7]
            }
        return None
        
    def save_click_config(self, row_index: int, col_index: int, percentage: int,
                         description: str = "", is_enabled: bool = True) -> bool:
        """保存点击配置"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 检查是否已存在
            existing = self.get_click_config_by_position(row_index, col_index)
            
            if existing:
                # 更新现有配置
                cursor.execute('''
                    UPDATE click_configs
                    SET percentage = ?, description = ?, is_enabled = ?, 
                        updated_at = CURRENT_TIMESTAMP
                    WHERE row_index = ? AND col_index = ?
                ''', (percentage, description, is_enabled, row_index, col_index))
            else:
                # 插入新配置
                cursor.execute('''
                    INSERT INTO click_configs (row_index, col_index, percentage, 
                                             description, is_enabled)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row_index, col_index, percentage, description, is_enabled))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"保存点击配置失败: {e}")
            return False
            
    def delete_click_config(self, row_index: int, col_index: int) -> bool:
        """删除点击配置"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM click_configs 
                WHERE row_index = ? AND col_index = ?
            ''', (row_index, col_index))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"删除点击配置失败: {e}")
            return False
            
    def toggle_click_config_status(self, row_index: int, col_index: int) -> bool:
        """切换点击配置状态"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE click_configs
                SET is_enabled = CASE WHEN is_enabled = 1 THEN 0 ELSE 1 END,
                    updated_at = CURRENT_TIMESTAMP
                WHERE row_index = ? AND col_index = ?
            ''', (row_index, col_index))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"切换点击配置状态失败: {e}")
            return False
            
    def get_enabled_click_configs(self) -> List[Dict]:
        """获取所有启用的点击配置"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, row_index, col_index, percentage, description
            FROM click_configs
            WHERE is_enabled = 1
            ORDER BY row_index, col_index
        ''')
        
        configs = []
        for row in cursor.fetchall():
            configs.append({
                "id": row[0],
                "row_index": row[1],
                "col_index": row[2],
                "percentage": row[3] or 0,
                "description": row[4] or ""
            })
            
        conn.close()
        return configs
        
    def clear_all_configs(self) -> bool:
        """清空所有点击配置"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM click_configs')
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"清空点击配置失败: {e}")
            return False
            
    def get_config_count(self) -> int:
        """获取配置数量"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM click_configs')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
        
    def set_default_percentages(self, default_percentage: float = 0.02) -> bool:
        """设置所有位置的默认百分比值"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 为所有72个位置设置默认值
            for row in range(12):
                for col in range(6):
                    # 检查是否已存在配置
                    existing = self.get_click_config_by_position(row, col)
                    
                    if existing:
                        # 更新现有配置的百分比
                        cursor.execute('''
                            UPDATE click_configs
                            SET percentage = ?, updated_at = CURRENT_TIMESTAMP
                            WHERE row_index = ? AND col_index = ?
                        ''', (default_percentage, row, col))
                    else:
                        # 插入新配置
                        cursor.execute('''
                            INSERT INTO click_configs (row_index, col_index, percentage, 
                                                     description, is_enabled)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (row, col, default_percentage, f"位置({row+1},{col+1})", True))
            
            conn.commit()
            conn.close()
            print(f"已为所有位置设置默认概率: {default_percentage}%")
            return True
        except Exception as e:
            print(f"设置默认概率失败: {e}")
            return False

class ClickConfigEditDialog(QDialog):
    """点击配置编辑对话框"""
    
    def __init__(self, parent=None, config_data: Dict = None, row: int = 0, col: int = 0):
        super().__init__(parent)
        self.config_data = config_data
        self.row = row
        self.col = col
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle(f"编辑点击配置 - 位置({self.row+1}, {self.col+1})")
        self.setFixedSize(350, 250)
        
        layout = QVBoxLayout(self)
        
        # 位置信息
        position_label = QLabel(f"位置: 第{self.row+1}行，第{self.col+1}列")
        position_label.setFont(QFont("Arial", 12, QFont.Bold))
        position_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(position_label)
        
        # 表单布局
        form_layout = QFormLayout()
        
        # 百分比输入
        self.percentage_spin = QDoubleSpinBox()
        self.percentage_spin.setRange(0.0, 100.0)
        self.percentage_spin.setSuffix(" %")
        self.percentage_spin.setDecimals(2)  # 支持两位小数
        self.percentage_spin.setSingleStep(0.01)  # 步长0.01
        if self.config_data:
            self.percentage_spin.setValue(self.config_data.get("percentage", 0.02))
        else:
            self.percentage_spin.setValue(0.02)  # 默认值0.02
        form_layout.addRow("点击概率:", self.percentage_spin)
        
        # 描述输入
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        if self.config_data:
            self.description_edit.setText(self.config_data.get("description", ""))
        form_layout.addRow("描述:", self.description_edit)
        
        # 启用状态
        self.enabled_check = QCheckBox("启用此配置")
        if self.config_data:
            self.enabled_check.setChecked(self.config_data.get("is_enabled", True))
        else:
            self.enabled_check.setChecked(True)
        form_layout.addRow("", self.enabled_check)
        
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
            "percentage": self.percentage_spin.value(),
            "description": self.description_edit.toPlainText().strip(),
            "is_enabled": self.enabled_check.isChecked()
        }

class ClickConfigManagerWidget(QWidget):
    """点击配置管理界面"""
    
    click_config_updated = pyqtSignal()  # 点击配置更新信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_manager = ClickConfigDatabaseManager()
        self.rows = 12
        self.cols = 6
        self.init_ui()
        self.load_click_configs()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("点击配置管理")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 说明信息
        info_label = QLabel("点击表格中的单元格来配置点击概率，支持12行6列的配置矩阵")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(info_label)
        
        # 控制按钮区域
        control_frame = QFrame()
        control_frame.setFrameStyle(QFrame.Box)
        control_layout = QHBoxLayout(control_frame)
        
        # 保存所有按钮
        self.save_all_button = QPushButton("保存所有配置")
        self.save_all_button.clicked.connect(self.save_all_configs)
        self.save_all_button.setStyleSheet("""
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
        
        # 清空所有按钮
        self.clear_all_button = QPushButton("清空所有配置")
        self.clear_all_button.clicked.connect(self.clear_all_configs)
        self.clear_all_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        
        # 刷新按钮
        self.refresh_button = QPushButton("刷新")
        self.refresh_button.clicked.connect(self.load_click_configs)
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        
        # 设置默认值按钮
        self.set_default_button = QPushButton("设置默认值(0.02%)")
        self.set_default_button.clicked.connect(self.set_default_percentages)
        self.set_default_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        
        control_layout.addWidget(self.save_all_button)
        control_layout.addWidget(self.clear_all_button)
        control_layout.addWidget(self.refresh_button)
        control_layout.addWidget(self.set_default_button)
        control_layout.addStretch()
        
        layout.addWidget(control_frame)
        
        # 创建点击配置表格
        self.create_click_config_table()
        layout.addWidget(self.table)
        
        # 统计信息
        self.create_stats_frame()
        layout.addWidget(self.stats_frame)
        
    def create_click_config_table(self):
        """创建点击配置表格"""
        self.table = QTableWidget()
        self.table.setRowCount(self.rows)
        self.table.setColumnCount(self.cols)
        
        # 设置表头
        headers = []
        for i in range(self.cols):
            headers.append(f"列{i+1}")
        self.table.setHorizontalHeaderLabels(headers)
        
        # 设置行标签
        row_labels = []
        for i in range(self.rows):
            row_labels.append(f"行{i+1}")
        self.table.setVerticalHeaderLabels(row_labels)
        
        # 设置列宽和行高
        header = self.table.horizontalHeader()
        for i in range(self.cols):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
            
        # 设置表格样式
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectItems)
        
        # 增强表格分割线显示
        self.table.setShowGrid(True)
        self.table.setGridStyle(Qt.SolidLine)
        
        # 设置表格样式表，增强分割线
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #666666;
                border: 2px solid #333333;
                background-color: white;
            }
            QTableWidget::item {
                border: 1px solid #cccccc;
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                border: 2px solid #666666;
                padding: 8px;
                font-weight: bold;
                color: #333333;
            }
            QHeaderView::section:hover {
                background-color: #e0e0e0;
            }
        """)
        
        # 连接单元格点击信号
        self.table.cellClicked.connect(self.on_cell_clicked)
        
        # 初始化表格内容
        self.init_table_cells()
        
    def init_table_cells(self):
        """初始化表格单元格"""
        for row in range(self.rows):
            for col in range(self.cols):
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.table.setItem(row, col, item)
                
                # 设置默认背景色
                self.update_cell_appearance(row, col, None)
                
    def update_cell_appearance(self, row: int, col: int, config: Optional[Dict]):
        """更新单元格外观"""
        item = self.table.item(row, col)
        if not item:
            return
            
        # 设置单元格边框样式，增强分割线效果
        item.setData(Qt.UserRole, "border_style")
        
        if config and config.get("is_enabled", False):
            # 有配置且启用
            percentage = config.get("percentage", 0)
            if percentage > 0:
                item.setBackground(QBrush(QColor(144, 238, 144)))  # 浅绿色
                item.setText(f"{percentage}%")
                # 设置深色边框
                item.setData(Qt.UserRole, f"border: 2px solid #2E7D32; background: {QColor(144, 238, 144).name()}")
            else:
                item.setBackground(QBrush(QColor(255, 193, 7)))  # 黄色
                item.setText("0%")
                # 设置深色边框
                item.setData(Qt.UserRole, f"border: 2px solid #F57C00; background: {QColor(255, 193, 7).name()}")
            item.setToolTip(f"点击概率: {percentage}%\n描述: {config.get('description', '')}")
        elif config:
            # 有配置但禁用
            item.setBackground(QBrush(QColor(169, 169, 169)))  # 灰色
            item.setText(f"{config.get('percentage', 0)}%")
            # 设置深色边框
            item.setData(Qt.UserRole, f"border: 2px solid #424242; background: {QColor(169, 169, 169).name()}")
            item.setToolTip(f"已禁用\n点击概率: {config.get('percentage', 0)}%\n描述: {config.get('description', '')}")
        else:
            # 无配置
            item.setBackground(QBrush(QColor(240, 240, 240)))  # 浅灰色
            item.setText("")
            # 设置浅色边框
            item.setData(Qt.UserRole, f"border: 2px solid #BDBDBD; background: {QColor(240, 240, 240).name()}")
            item.setToolTip("点击配置")
            
    def create_stats_frame(self):
        """创建统计信息框架"""
        self.stats_frame = QFrame()
        self.stats_frame.setFrameStyle(QFrame.Box)
        stats_layout = QHBoxLayout(self.stats_frame)
        
        self.total_label = QLabel("总配置数: 0")
        self.enabled_label = QLabel("启用: 0")
        self.disabled_label = QLabel("禁用: 0")
        self.empty_label = QLabel("未配置: 0")
        self.total_percentage_label = QLabel("总概率: 0%")
        
        stats_layout.addWidget(self.total_label)
        stats_layout.addWidget(self.enabled_label)
        stats_layout.addWidget(self.disabled_label)
        stats_layout.addWidget(self.empty_label)
        stats_layout.addWidget(self.total_percentage_label)
        stats_layout.addStretch()
        
    def load_click_configs(self):
        """加载点击配置数据"""
        configs = self.db_manager.get_all_click_configs()
        self.update_table_display(configs)
        self.update_stats(configs)
        
    def update_table_display(self, configs: List[Dict]):
        """更新表格显示"""
        # 创建配置字典，键为(row, col)
        config_dict = {}
        for config in configs:
            key = (config["row_index"], config["col_index"])
            config_dict[key] = config
            
        # 更新每个单元格
        for row in range(self.rows):
            for col in range(self.cols):
                config = config_dict.get((row, col))
                self.update_cell_appearance(row, col, config)
                
    def update_stats(self, configs: List[Dict]):
        """更新统计信息"""
        total = len(configs)
        enabled = sum(1 for c in configs if c.get("is_enabled", False))
        disabled = total - enabled
        empty = self.rows * self.cols - total
        total_percentage = sum(c.get("percentage", 0) for c in configs if c.get("is_enabled", False))
        
        self.total_label.setText(f"总配置数: {total}")
        self.enabled_label.setText(f"启用: {enabled}")
        self.disabled_label.setText(f"禁用: {disabled}")
        self.empty_label.setText(f"未配置: {empty}")
        self.total_percentage_label.setText(f"总概率: {total_percentage}%")
        
    def on_cell_clicked(self, row: int, col: int):
        """单元格点击事件"""
        # 获取当前位置的配置
        config = self.db_manager.get_click_config_by_position(row, col)
        
        # 打开编辑对话框
        dialog = ClickConfigEditDialog(self, config, row, col)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            
            # 保存配置
            if self.db_manager.save_click_config(
                row, col, data["percentage"], data["description"], data["is_enabled"]
            ):
                QMessageBox.information(self, "成功", "点击配置保存成功")
                self.load_click_configs()
                self.click_config_updated.emit()
            else:
                QMessageBox.warning(self, "错误", "保存失败")
                
    def save_all_configs(self):
        """保存所有配置"""
        QMessageBox.information(self, "提示", "所有配置已自动保存到数据库")
        
    def clear_all_configs(self):
        """清空所有配置"""
        reply = QMessageBox.question(
            self, "确认清空", 
            "确定要清空所有点击配置吗？此操作不可恢复！",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.db_manager.clear_all_configs():
                QMessageBox.information(self, "成功", "所有点击配置已清空")
                self.load_click_configs()
                self.click_config_updated.emit()
            else:
                QMessageBox.warning(self, "错误", "清空失败")
                
    def set_default_percentages(self):
        """设置所有位置为默认概率值"""
        reply = QMessageBox.question(
            self, "确认设置默认值", 
            "确定要为所有位置设置默认概率0.02%吗？\n这将覆盖现有的概率设置。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.db_manager.set_default_percentages(0.02):
                QMessageBox.information(self, "成功", "已为所有位置设置默认概率0.02%")
                self.load_click_configs()
                self.click_config_updated.emit()
            else:
                QMessageBox.warning(self, "错误", "设置默认值失败")
                
    def get_enabled_click_configs(self) -> List[Dict]:
        """获取所有启用的点击配置"""
        return self.db_manager.get_enabled_click_configs()
        
    def get_click_config_at_position(self, row: int, col: int) -> Optional[Dict]:
        """获取指定位置的点击配置"""
        return self.db_manager.get_click_config_by_position(row, col)
        
    def export_configs_to_dict(self) -> Dict:
        """导出配置为字典格式"""
        configs = self.db_manager.get_all_click_configs()
        result = {}
        for config in configs:
            key = f"{config['row_index']}_{config['col_index']}"
            result[key] = {
                "percentage": config["percentage"],
                "description": config["description"],
                "enabled": config["is_enabled"]
            }
        return result
