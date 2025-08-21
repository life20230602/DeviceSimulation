import sys
import os
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTabWidget, QTextEdit, 
                             QLabel, QMessageBox, QDialog, QGridLayout,
                             QLineEdit, QScrollArea, QFrame, QTableWidget, QTableWidgetItem,
                             QHeaderView, QGroupBox, QFormLayout, QSpinBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl, QSize,pyqtSlot
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile, QWebEngineSettings,QWebEngineScript
from touch import HumanizedController
from PyQt5.QtCore import QTimer, QPoint, QRect, Qt, pyqtSlot
# 删除权重配置弹窗导入

# 导入数据库管理器
from database_manager import DatabaseManager
# 导入来路设置管理器
from referrer_manager import ReferrerManagerWidget
# 导入点击配置管理器
from click_config_manager import ClickConfigManagerWidget
# 导入随机WebView弹窗
from random_webview_dialog import RandomWebViewDialog

# 字体配置
def get_system_font():
    """根据操作系统获取合适的字体"""
    import platform
    system = platform.system()
    if system == "Windows":
        return "Microsoft YaHei"
    elif system == "Darwin":  # macOS
        return "Arial"
    elif system == "Linux":
        return "DejaVu Sans"
    else:
        return "Arial"

class MainWindow(QMainWindow):
    """主窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HS(火山) 浏览器管理工具")
        self.setGeometry(100, 100, 800, 600)
        self.auto_switch_ip_brower_timer = QTimer()
        self.auto_switch_ip_brower_timer.timeout.connect(self.auto_switch_ip_brower)
        # 删除模拟数据
        self.count = 1
        # 初始化数据库管理器
        self.db_manager = DatabaseManager()
        
        # 初始化UI
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建标签页
        self.create_tabs()
        
        # 删除控制区域创建
        
    def create_tabs(self):
        """创建标签页"""
        self.tab_widget = QTabWidget()
        
        # 本机浏览器标签
        local_browser_tab = QWidget()
        local_browser_layout = QVBoxLayout(local_browser_tab)
        local_browser_layout.addWidget(QLabel("本机浏览器配置"))
        
        # 控制按钮区域
        control_frame = QFrame()
        control_frame.setFrameStyle(QFrame.Box)
        control_frame.setMinimumHeight(150)
        
        control_layout = QHBoxLayout(control_frame)
        
        # 运行按钮
        self.run_button = QPushButton("运行")
        self.run_button.setMinimumSize(120, 80)
        self.run_button.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.run_button.clicked.connect(self.start_running)
        control_layout.addWidget(self.run_button)
        
        # 停止按钮
        self.stop_button = QPushButton("停止")
        self.stop_button.setMinimumSize(120, 80)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c62828;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.stop_button.clicked.connect(self.stop_running)
        control_layout.addWidget(self.stop_button)
        
        # 退出按钮
        self.exit_button = QPushButton("退出")
        self.exit_button.setMinimumSize(120, 80)
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
            QPushButton:pressed {
                background-color: #ef6c00;
            }
        """)
        self.exit_button.clicked.connect(self.close)
        control_layout.addWidget(self.exit_button)
        
        local_browser_layout.addWidget(control_frame)
        self.tab_widget.addTab(local_browser_tab, "本机浏览器")
        
        # API地址标签
        api_tab = QWidget()
        api_layout = QVBoxLayout(api_tab)
        api_layout.addWidget(QLabel("API地址配置"))
        self.tab_widget.addTab(api_tab, "API地址")
        
        # URL列表标签
        url_tab = QWidget()
        url_layout = QVBoxLayout(url_tab)
        self.create_url_management_tab(url_layout)
        self.tab_widget.addTab(url_tab, "URL列表")
        
        # 设备管理标签
        device_tab = QWidget()
        device_layout = QVBoxLayout(device_tab)
        self.create_device_management_tab(device_layout)
        self.tab_widget.addTab(device_tab, "设备管理")
        
        # 来路设置标签
        self.referrer_manager = ReferrerManagerWidget()
        self.tab_widget.addTab(self.referrer_manager, "来路设置")
        
        # 点击配置标签
        self.click_config_manager = ClickConfigManagerWidget()
        self.tab_widget.addTab(self.click_config_manager, "点击配置")
        
        # 流量曲线标签
        traffic_tab = QWidget()
        traffic_layout = QVBoxLayout(traffic_tab)
        traffic_layout.addWidget(QLabel("流量曲线"))
        self.tab_widget.addTab(traffic_tab, "流量曲线")
        
        # 高级设置标签
        advanced_tab = QWidget()
        advanced_layout = QVBoxLayout(advanced_tab)
        advanced_layout.addWidget(QLabel("高级设置"))
        self.tab_widget.addTab(advanced_tab, "高级设置")
        
        # 添加标签页到主布局
        main_layout = self.centralWidget().layout()
        main_layout.addWidget(self.tab_widget)
        
    # 删除create_control_area方法
        
    # 删除create_status_area方法
        
    # 删除show_weight_config方法
    def auto_switch_ip_brower(self):
        pass
        #  if self.webview_dialog is not None:
        #     self.webview_dialog.close()

        #  time.sleep(0.2)
        #  self.create_random_webview()
        #  self.count = self.count +1
        #  print(f"第{self.count}次切换")

    def start_running(self):
        """开始运行"""
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        # 删除状态日志记录
        
        # 随机获取设备信息并创建WebView弹窗
        self.create_random_webview()

        self.auto_switch_ip_brower_timer.start(1000*60)  # 转换为毫秒

        # 创建WebView弹窗后记录状态
        
    def stop_running(self):
        """停止运行"""
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        # 删除状态日志记录
            
    # 删除update_status方法
        
    def create_device_management_tab(self, layout):
        """创建设备管理标签页"""
        # 设备列表
        device_list_group = QGroupBox("设备列表")
        device_list_layout = QVBoxLayout(device_list_group)
        
        # 创建设备表格
        self.device_table = QTableWidget()
        self.device_table.setColumnCount(5)
        self.device_table.setHorizontalHeaderLabels(["设备名称", "屏幕宽度", "屏幕高度", "User Agent", "操作"])
        self.device_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.device_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.device_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.device_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.device_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        device_list_layout.addWidget(self.device_table)
        
        # 添加设备按钮
        add_device_btn = QPushButton("添加设备")
        add_device_btn.clicked.connect(self.add_device)
        device_list_layout.addWidget(add_device_btn)
        
        layout.addWidget(device_list_group)
        
        # 设备输入区域
        device_input_group = QGroupBox("添加/编辑设备")
        device_input_layout = QFormLayout(device_input_group)
        
        self.device_name_edit = QLineEdit()
        self.device_name_edit.setPlaceholderText("设备名称")
        device_input_layout.addRow("设备名称:", self.device_name_edit)
        
        self.screen_width_edit = QSpinBox()
        self.screen_width_edit.setRange(320, 3840)
        self.screen_width_edit.setValue(1920)
        device_input_layout.addRow("屏幕宽度:", self.screen_width_edit)
        
        self.screen_height_edit = QSpinBox()
        self.screen_height_edit.setRange(240, 2160)
        self.screen_height_edit.setValue(1080)
        device_input_layout.addRow("屏幕高度:", self.screen_height_edit)
        
        self.device_ua_edit = QLineEdit()
        self.device_ua_edit.setPlaceholderText("User Agent字符串")
        self.device_ua_edit.setText("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        device_input_layout.addRow("User Agent:", self.device_ua_edit)
        
        layout.addWidget(device_input_group)
        
        # 更新设备表格
        self.update_device_table()
        
    def create_url_management_tab(self, layout):
        """创建URL管理标签页"""
        # URL输入区域
        url_input_group = QGroupBox("添加URL")
        url_input_layout = QFormLayout(url_input_group)
        
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("输入URL地址")
        url_input_layout.addRow("URL:", self.url_edit)
        
        # URL控制按钮
        url_btn_layout = QHBoxLayout()
        
        add_url_btn = QPushButton("添加URL")
        add_url_btn.clicked.connect(self.add_url)
        url_btn_layout.addWidget(add_url_btn)
        
        random_url_btn = QPushButton("随机选择URL")
        random_url_btn.clicked.connect(self.random_url)
        url_btn_layout.addWidget(random_url_btn)
        
        url_input_layout.addRow(url_btn_layout)
        layout.addWidget(url_input_group)
        
        # URL列表
        url_list_group = QGroupBox("URL列表")
        url_list_layout = QVBoxLayout(url_list_group)
        
        self.url_table = QTableWidget()
        self.url_table.setColumnCount(2)
        self.url_table.setHorizontalHeaderLabels(["URL", "操作"])
        self.url_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.url_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        
        url_list_layout.addWidget(self.url_table)
        layout.addWidget(url_list_group)
        
        # 更新URL表格
        self.update_url_table()
        
    # 删除硬编码的load_default_devices方法
        
    # 删除硬编码的load_default_urls方法
        
    def update_device_table(self):
        """更新设备表格"""
        devices = self.db_manager.get_all_devices()
        self.device_table.setRowCount(len(devices))
        
        for row, device in enumerate(devices):
            # 设备名称
            name_item = QTableWidgetItem(device["name"])
            self.device_table.setItem(row, 0, name_item)
            
            # 屏幕宽度
            width_item = QTableWidgetItem(str(device["width"]))
            self.device_table.setItem(row, 1, width_item)
            
            # 屏幕高度
            height_item = QTableWidgetItem(str(device["height"]))
            self.device_table.setItem(row, 2, height_item)
            
            # User Agent
            ua_item = QTableWidgetItem(device["user_agent"])
            self.device_table.setItem(row, 3, ua_item)
            
            # 操作按钮
            delete_btn = QPushButton("删除")
            delete_btn.clicked.connect(lambda checked, d=device: self.delete_device(d["id"]))
            self.device_table.setCellWidget(row, 4, delete_btn)
            
    def update_url_table(self):
        """更新URL表格"""
        urls = self.db_manager.get_all_urls()
        self.url_table.setRowCount(len(urls))
        
        for row, url_data in enumerate(urls):
            # URL列 - 使用可编辑的表格项
            url_item = QTableWidgetItem(url_data["url"])
            url_item.setData(Qt.UserRole, url_data["id"])  # 存储URL ID
            self.url_table.setItem(row, 0, url_item)
            
            # 操作列
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.setContentsMargins(2, 2, 2, 2)
            
            # 编辑按钮
            edit_btn = QPushButton("编辑")
            edit_btn.setFixedSize(50, 25)
            edit_btn.clicked.connect(lambda checked, u=url_data: self.edit_url(u))
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
            
            # 删除按钮
            delete_btn = QPushButton("删除")
            delete_btn.setFixedSize(50, 25)
            delete_btn.clicked.connect(lambda checked, u=url_data: self.delete_url(u["id"]))
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
            button_layout.addWidget(delete_btn)
            button_layout.addStretch()
            
            self.url_table.setCellWidget(row, 1, button_widget)
            
    def add_device(self):
        """添加设备"""
        name = self.device_name_edit.text().strip()
        width = self.screen_width_edit.value()
        height = self.screen_height_edit.value()
        user_agent = self.device_ua_edit.text().strip()
        
        if not name or not user_agent:
            QMessageBox.warning(self, "警告", "请输入设备名称和User Agent")
            return
            
        # 添加到数据库
        if self.db_manager.add_device(name, width, height, user_agent):
            self.update_device_table()
            
            # 清空输入框
            self.device_name_edit.clear()
            self.screen_width_edit.setValue(1920)
            self.screen_height_edit.setValue(1080)
            self.device_ua_edit.setText("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            QMessageBox.information(self, "成功", "设备已添加")
        else:
            QMessageBox.warning(self, "错误", "添加设备失败，可能名称已存在")
        
    def delete_device(self, device_id):
        """删除设备"""
        device = self.db_manager.get_device_by_id(device_id)
        if device:
            if QMessageBox.question(self, "确认", f"确定要删除设备: {device['name']}") == QMessageBox.Yes:
                if self.db_manager.delete_device(device_id):
                    self.update_device_table()
                    QMessageBox.information(self, "成功", "设备已删除")
                else:
                    QMessageBox.warning(self, "错误", "删除设备失败")
        else:
            QMessageBox.warning(self, "错误", "设备不存在")
                
    def add_url(self):
        """添加URL"""
        url = self.url_edit.text().strip()
        if not url:
            QMessageBox.warning(self, "警告", "请输入URL")
            return
            
        # 添加到数据库
        if self.db_manager.add_url(url):
            self.update_url_table()
            self.url_edit.clear()
            QMessageBox.information(self, "成功", "URL已添加")
        else:
            QMessageBox.warning(self, "错误", "添加URL失败，可能URL已存在")
            
    def edit_url(self, url_data):
        """编辑URL"""
        from PyQt5.QtWidgets import QInputDialog
        
        # 弹出输入对话框
        new_url, ok = QInputDialog.getText(
            self, 
            "编辑URL", 
            f"请输入新的URL地址:\n当前URL: {url_data['url']}", 
            text=url_data['url']
        )
        
        if ok and new_url.strip():
            new_url = new_url.strip()
            
            # 检查URL是否已存在（排除当前URL）
            existing_urls = self.db_manager.get_all_urls()
            for url in existing_urls:
                if url["id"] != url_data["id"] and url["url"] == new_url:
                    QMessageBox.warning(self, "警告", "URL地址已存在")
                    return
            
            # 更新数据库
            if self.db_manager.update_url(url_data["id"], new_url):
                self.update_url_table()
                QMessageBox.information(self, "成功", "URL已更新")
            else:
                QMessageBox.warning(self, "错误", "更新URL失败")
                
    def delete_url(self, url_id):
        """删除URL"""
        url_data = self.db_manager.get_url_by_id(url_id)
        if url_data:
            if QMessageBox.question(self, "确认", f"确定要删除URL: {url_data['url']}") == QMessageBox.Yes:
                if self.db_manager.delete_url(url_id):
                    self.update_url_table()
                    QMessageBox.information(self, "成功", "URL已删除")
                else:
                    QMessageBox.warning(self, "错误", "删除URL失败")
        else:
            QMessageBox.warning(self, "错误", "URL不存在")
                
    def random_url(self):
        """随机选择URL"""
        random_url_data = self.db_manager.get_random_url()
        if random_url_data:
            QMessageBox.information(self, "随机URL", f"选中的URL: {random_url_data['url']}")
        else:
            QMessageBox.warning(self, "警告", "没有可用的URL")
        
    def get_random_device(self):
        """获取随机设备"""
        return self.db_manager.get_random_device()
        
    def create_random_webview(self):
        """创建随机设备的WebView弹窗"""
        # 随机获取设备
        device = self.get_random_device()
        if not device:
            QMessageBox.warning(self, "警告", "没有可用的设备")
            return
            
        # 随机获取URL
        random_url_data = self.db_manager.get_random_url()
        if not random_url_data:
            QMessageBox.warning(self, "警告", "没有可用的URL")
            return
            
        # 随机获取来路设置（用于设置HTTP Referer头）
        random_referrer = self.referrer_manager.get_random_referrer()
        referrer_url = random_referrer['url'] if random_referrer else None
            
        # 创建WebView弹窗 - 每次创建新的实例
        self.webview_dialog = RandomWebViewDialog(
            self, device, random_url_data['url'], self.click_config_manager, referrer_url
        )
        self.webview_dialog.show()
        
        # 连接弹窗关闭信号，清理引用
        self.webview_dialog.finished.connect(lambda: self.on_webview_closed(self.webview_dialog))
        
        # 删除状态日志记录
        
    def on_webview_closed(self, dialog):
        """WebView弹窗关闭时的处理"""
        try:
            # 清理弹窗引用
            if hasattr(self, 'webview_dialog') and self.webview_dialog == dialog:
                delattr(self, 'webview_dialog')
        except:
            pass



def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("HS(火山) 浏览器管理工具")
    app.setApplicationVersion("2.4.5")
    
    # 创建主窗口
    window = MainWindow()
    
    window.show()

    # 运行应用程序
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
