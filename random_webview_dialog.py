#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
随机WebView弹窗
实现网格划分、随机滑动和基于配置的点击功能
"""

import random
import math
import time
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFrame)
from PyQt5.QtCore import Qt, QUrl, QRect, QPoint, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWebEngineWidgets import (QWebEngineView, QWebEnginePage, 
                                     QWebEngineProfile, QWebEngineSettings, 
                                     QWebEngineScript)
from touch import HumanizedController

class RandomWebViewDialog(QDialog):
    """随机WebView弹窗"""
    
    def __init__(self, parent=None, device=None, url=None, click_config_manager=None, referrer_url=None):
        super().__init__(parent)
        self.device = device
        self.url = url
        self.click_config_manager = click_config_manager
        self.referrer_url = referrer_url
        
        # 网格设置
        self.grid_rows = 12
        self.grid_cols = 6
        
        # 滑动和点击定时器
        self.scroll_timer = QTimer()
        self.click_timer = QTimer()
        self.scroll_timer.timeout.connect(self.perform_random_scroll)
        self.click_timer.timeout.connect(self.perform_random_click)
        
        # 域名检查定时器
        self.domain_check_timer = QTimer()
        self.domain_check_timer.timeout.connect(self.check_domain_and_redirect)
        
        # 页面加载状态
        self.page_loaded = False
        
        # 存储原始域名
        self.original_domain = None
        
        # 滑动控制变量
        self.scroll_count = 0
        self.max_scroll_count = 3
        
        self.setWindowTitle(f"WebView - {device['name'] if device else 'Unknown Device'}")
        self.setGeometry(100, 100, device['width'] if device else 1200, device['height'] if device else 800)
        self.setModal(False)  # 非模态，可以同时打开多个
        
        # 设置窗口属性，确保关闭时能正确清理
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        
        # 初始化UI
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout()
        
        # 设备信息显示
        if self.device:
            device_info = QLabel(f"设备: {self.device['name']} | "
                               f"分辨率: {self.device['width']}x{self.device['height']} | "
                               f"URL: {self.url}")
            device_info.setStyleSheet("""
                QLabel {
                    background-color: #e3f2fd;
                    padding: 10px;
                    border-radius: 5px;
                    border-left: 4px solid #2196f3;
                    font-weight: bold;
                }
            """)
            layout.addWidget(device_info)
        
        # 网格信息显示
        grid_info = QLabel(f"网格: {self.grid_rows}行 × {self.grid_cols}列 | "
                          f"每5秒随机点击 | 支持随机滑动")
        grid_info.setStyleSheet("""
            QLabel {
                background-color: #f3e5f5;
                padding: 8px;
                border-radius: 5px;
                border-left: 4px solid #9c27b0;
                font-weight: bold;
            }
        """)
        layout.addWidget(grid_info)
        
        # 创建WebView
        self.webview = QWebEngineView()
        
        # 设置WebView配置
        self.setup_webview()
        
        # 连接信号
        self.webview.loadStarted.connect(self.on_load_started)
        self.webview.loadProgress.connect(self.on_load_progress)
        self.webview.loadFinished.connect(self.on_load_finished)
        
        # 添加WebView到布局
        layout.addWidget(self.webview)
        
        # 底部控制按钮
        control_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("刷新")
        refresh_btn.clicked.connect(self.webview.reload)
        refresh_btn.setStyleSheet("""
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
        control_layout.addWidget(refresh_btn)
        
        # 开始/停止自动行为按钮
        self.auto_behavior_btn = QPushButton("开始自动行为")
        self.auto_behavior_btn.clicked.connect(self.toggle_auto_behavior)
        self.auto_behavior_btn.setStyleSheet("""
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
        control_layout.addWidget(self.auto_behavior_btn)
        
        # 生成点击位置图片按钮
        generate_image_btn = QPushButton("生成点击位置图")
        generate_image_btn.clicked.connect(self.generate_click_positions_image)
        generate_image_btn.setStyleSheet("""
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
        control_layout.addWidget(generate_image_btn)
        
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
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
        control_layout.addWidget(close_btn)
        
        layout.addLayout(control_layout)
        
        # 设置布局
        self.setLayout(layout)
        
        # 初始化触摸控制器
        self.humanized_touch = HumanizedController(self.webview)
        
        # 记录点击位置
        self.click_positions = []
        
        # 加载URL
        if self.url:
            self.webview.load(QUrl(self.url))

    def setup_webview(self):
        """设置WebView配置"""
        if not self.device:
            return
        
        # 创建自定义profile
        profile = QWebEngineProfile("random_webview_profile", self.webview)
        
        # 设置User Agent
        profile.setHttpUserAgent(self.device["user_agent"])
        
        # 设置Referrer策略（如果提供了referrer_url）
        if self.referrer_url:
            # 通过自定义请求拦截器设置referrer
            print(f"将通过请求拦截器设置HTTP Referer: {self.referrer_url}")
        
        # 创建自定义页面
        page = QWebEnginePage(profile, self.webview)
        
        # 如果提供了referrer_url，设置请求拦截器
        if self.referrer_url:
            # 重写acceptNavigationRequest方法来设置referrer
            original_accept_navigation = page.acceptNavigationRequest
            
            def custom_accept_navigation(url, _type, is_main_frame):
                # 在导航请求中添加referrer头
                if is_main_frame and _type == QWebEnginePage.NavigationTypeTyped:
                    # 对于主框架的输入导航，设置referrer
                    print(f"导航到 {url}，使用referrer: {self.referrer_url}")
                    
                    # 尝试通过页面设置referrer
                    try:
                        # 使用页面级别的referrer设置
                        page.setUrl(url)
                        print(f"已设置页面URL: {url}")
                    except Exception as e:
                        print(f"设置页面URL失败: {e}")
                        
                return original_accept_navigation(url, _type, is_main_frame)
            
            page.acceptNavigationRequest = custom_accept_navigation
            
            # 设置页面的referrer策略
            try:
                # 尝试设置referrer策略
                page.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
                print(f"已启用远程URL访问，referrer: {self.referrer_url}")
            except Exception as e:
                print(f"设置referrer策略失败: {e}")
        
        # 创建自定义页面
        page = QWebEnginePage(profile, self.webview)
        
        # 启用JavaScript
        settings = page.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
        
        # 注入脚本，覆盖 navigator/screen/devicePixelRatio 等
        js = """
        // 修改 navigator
        Object.defineProperty(navigator, 'platform', { get: () => 'iPhone' });
        Object.defineProperty(navigator, 'vendor', { get: () => 'Apple Computer, Inc.' });
        Object.defineProperty(navigator, 'maxTouchPoints', { get: () => 5 });
        Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 6 });
        Object.defineProperty(navigator, 'deviceMemory', { get: () => 4 });

        // 修改 screen 信息
        Object.defineProperty(screen, 'width', { get: () => 390 });
        Object.defineProperty(screen, 'height', { get: () => 844 });
        Object.defineProperty(window, 'devicePixelRatio', { get: () => 3 });

        // 添加触摸事件支持
        document.addEventListener("touchstart", function(){}, true);

        // ========= 伪造 WebGL GPU =========
        const getParameterProxy = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) { // UNMASKED_VENDOR_WEBGL
                return "Apple Inc.";
            }
            if (parameter === 37446) { // UNMASKED_RENDERER_WEBGL
                return "Apple A14 GPU";  // 模拟 iPhone 12/13 GPU
            }
            return getParameterProxy.apply(this, arguments);
        };

        // WebGL2 也要覆盖
        if (window.WebGL2RenderingContext) {
            const getParameterProxy2 = WebGL2RenderingContext.prototype.getParameter;
            WebGL2RenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) {
                    return "Apple Inc.";
                }
                if (parameter === 37446) {
                    return "Apple A14 GPU";
                }
                return getParameterProxy2.apply(this, arguments);
            };
        }
        """
        script = QWebEngineScript()
        script.setInjectionPoint(QWebEngineScript.DocumentCreation)
        script.setWorldId(QWebEngineScript.MainWorld)
        script.setRunsOnSubFrames(True)
        script.setSourceCode(js)

        profile.scripts().insert(script)

        # 设置视口大小
        self.webview.resize(self.device["width"], self.device["height"])
        self.webview.setPage(page)
        
    def on_load_started(self):
        """页面开始加载"""
        self.setWindowTitle(f"加载中... - {self.device['name'] if self.device else 'Unknown Device'}")
        self.page_loaded = False
        
        # 提取并存储原始域名
        if self.url and not self.original_domain:
            try:
                from urllib.parse import urlparse
                parsed_url = urlparse(self.url)
                self.original_domain = parsed_url.netloc
                print(f"原始域名: {self.original_domain}")
            except Exception as e:
                print(f"解析域名失败: {e}")
                self.original_domain = None
        
    def on_load_progress(self, progress):
        """页面加载进度变化"""
        self.setWindowTitle(f"加载中 {progress}% - {self.device['name'] if self.device else 'Unknown Device'}")
        
        # 当加载进度达到80%时开始模拟用户行为
        if progress >= 80 and not self.page_loaded:
            print(f"页面加载进度达到{progress}%，开始模拟用户行为")
            self.page_loaded = True
            # 启动定时器
            self.start_auto_behavior()
            
            # 启动域名检查定时器（3秒后检查）
            if self.original_domain:
                self.domain_check_timer.start(3000)
                print(f"域名检查定时器已启动，3秒后检查是否跳转到外部域名")
        
    def on_load_finished(self, success):
        """页面加载完成"""
        if success:
            self.setWindowTitle(f"WebView - {self.device['name'] if self.device else 'Unknown Device'}")
        else:
            self.setWindowTitle(f"加载失败 - {self.device['name'] if self.device else 'Unknown Device'}")
            
    def start_auto_behavior(self):
        """开始自动行为"""
        if not self.page_loaded:
            return
            
        # 重置滑动计数
        self.scroll_count = 0
        
        # 立即开始第一次滑动
        self.scroll_timer.start(100)  # 100ms后开始第一次滑动
        
        # 开始随机点击（每5秒一次）
        self.click_timer.start(5000)
        
        # 更新按钮状态
        self.auto_behavior_btn.setText("停止自动行为")
        self.auto_behavior_btn.setStyleSheet("""
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
        
    def stop_auto_behavior(self):
        """停止自动行为"""
        self.scroll_timer.stop()
        self.click_timer.stop()
        
        # 更新按钮状态
        self.auto_behavior_btn.setText("开始自动行为")
        self.auto_behavior_btn.setStyleSheet("""
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
        
    def toggle_auto_behavior(self):
        """切换自动行为状态"""
        if self.scroll_timer.isActive():
            self.stop_auto_behavior()
        else:
            self.start_auto_behavior()
            
    def perform_random_scroll(self):
        """执行随机滑动 - 只模拟Y方向向上滑动，执行3次"""
        if not self.page_loaded:
            return
            
        # 检查是否已达到最大滑动次数
        if self.scroll_count >= self.max_scroll_count:
            print(f"已完成{self.max_scroll_count}次滑动，停止滑动")
            self.scroll_timer.stop()
            return
            
        # 生成随机滑动参数 - 只向上滑动
        start_x = random.randint(100, self.device["width"] - 100)
        start_y = random.randint(200, self.device["height"] - 100)  # 从中间开始
        
        # 只模拟Y方向向上滑动，X坐标保持不变
        end_x = start_x
        end_y = start_y - random.randint(150, 300)  # 向上滑动150-300px
        
        # 确保滑动范围在页面内
        end_y = max(50, end_y)
        
        # 执行人性化的平滑滑动
        self.perform_smooth_swipe(start_x, start_y, end_x, end_y)
        
        self.scroll_count += 1
        print(f"执行第{self.scroll_count}次向上滑动: ({start_x}, {start_y}) -> ({end_x}, {end_y})")
        
        # 如果还有滑动次数，设置下次滑动时间为2秒
        if self.scroll_count < self.max_scroll_count:
            self.scroll_timer.start(2000)  # 2秒后执行下次滑动
        else:
            print(f"滑动完成，共执行{self.max_scroll_count}次")
    
    def perform_smooth_swipe(self, start_x, start_y, end_x, end_y):
        """执行平滑的人性化滑动 - 使用Qt事件实现"""
        try:
            from PyQt5.QtCore import QPoint, QTimer
            from PyQt5.QtGui import QMouseEvent
            from PyQt5.QtCore import Qt
            from PyQt5.QtWidgets import QApplication
            
            # 计算滑动距离
            scroll_distance = end_y - start_y
            
            print(f"Qt事件滑动: Y方向滚动距离={scroll_distance}px")
            
            # 使用Qt鼠标事件来模拟滑动
            if abs(scroll_distance) > 5:  # 只有足够大的滚动距离才执行
                # 计算滑动步数
                scroll_steps = max(8, abs(scroll_distance) // 20)  # 每20px一步，增加步数
                step_distance = scroll_distance / scroll_steps
                
                # 确保webview有焦点
                self.webview.setFocus()
                self.webview.activateWindow()
                
                # 开始执行滑动
                self.current_swipe_step = 0
                self.swipe_steps = scroll_steps
                self.swipe_start_x = start_x
                self.swipe_start_y = start_y
                self.swipe_step_distance = step_distance
                
                # 立即执行第一步
                self.execute_swipe_step()
                
                print(f"Qt事件滑动开始: {scroll_steps}步")
            else:
                print(f"滚动距离太小，跳过滑动")
            
        except Exception as e:
            print(f"Qt事件滑动失败: {e}")
            # 回退到简单滑动
            self.simple_swipe_fallback(start_x, start_y, end_x, end_y)
    
    def execute_swipe_step(self):
        """执行滑动步骤"""
        try:
            from PyQt5.QtCore import QPoint, QTimer
            from PyQt5.QtGui import QMouseEvent
            from PyQt5.QtCore import Qt
            from PyQt5.QtWidgets import QApplication
            
            if self.current_swipe_step < self.swipe_steps:
                # 计算当前位置
                progress = self.current_swipe_step / self.swipe_steps
                current_x = self.swipe_start_x
                current_y = self.swipe_start_y + (self.swipe_step_distance * self.current_swipe_step)
                
                # 获取全局坐标
                local_point = QPoint(int(current_x), int(current_y))
                global_point = self.webview.mapToGlobal(local_point)
                
                # 创建鼠标按下事件（如果是第一步）
                if self.current_swipe_step == 0:
                    press_event = QMouseEvent(
                        QMouseEvent.MouseButtonPress,
                        local_point,
                        global_point,
                        Qt.LeftButton,
                        Qt.LeftButton,
                        Qt.NoModifier
                    )
                    QApplication.sendEvent(self.webview, press_event)
                    QApplication.processEvents()
                    print(f"滑动开始: 按下鼠标")
                
                # 创建鼠标移动事件
                move_event = QMouseEvent(
                    QMouseEvent.MouseMove,
                    local_point,
                    global_point,
                    Qt.LeftButton,  # 保持按下状态
                    Qt.LeftButton,
                    Qt.NoModifier
                )
                QApplication.sendEvent(self.webview, move_event)
                QApplication.processEvents()
                
                self.current_swipe_step += 1
                print(f"滑动步骤: {self.current_swipe_step}/{self.swipe_steps}")
                
                # 延迟执行下一步
                QTimer.singleShot(50, self.execute_swipe_step)
                
            else:
                # 滑动完成，释放鼠标
                final_x = self.swipe_start_x
                final_y = self.swipe_start_y + (self.swipe_step_distance * self.swipe_steps)
                
                local_point = QPoint(int(final_x), int(final_y))
                global_point = self.webview.mapToGlobal(local_point)
                
                release_event = QMouseEvent(
                    QMouseEvent.MouseButtonRelease,
                    local_point,
                    global_point,
                    Qt.LeftButton,
                    Qt.NoButton,
                    Qt.NoModifier
                )
                QApplication.sendEvent(self.webview, release_event)
                QApplication.processEvents()
                print(f"Qt事件滑动完成: {self.swipe_steps}步")
                
        except Exception as e:
            print(f"执行滑动步骤失败: {e}")
    
    def ease_in_out_cubic(self, t):
        """三次缓动函数，模拟更自然的加速和减速"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2
    
    def simple_swipe_fallback(self, start_x, start_y, end_x, end_y):
        """简单滑动回退方案"""
        try:
            # 使用简单的Qt事件作为回退
            from PyQt5.QtCore import QPoint
            from PyQt5.QtGui import QMouseEvent
            from PyQt5.QtCore import Qt
            from PyQt5.QtWidgets import QApplication
            
            start_global = self.webview.mapToGlobal(QPoint(start_x, start_y))
            end_global = self.webview.mapToGlobal(QPoint(end_x, end_y))
            
            # 简化的滑动：移动→按下→移动→释放
            move_event = QMouseEvent(QMouseEvent.MouseMove, QPoint(start_x, start_y), start_global, Qt.NoButton, Qt.NoButton, Qt.NoModifier)
            QApplication.sendEvent(self.webview, move_event)
            
            press_event = QMouseEvent(QMouseEvent.MouseButtonPress, QPoint(start_x, start_y), start_global, Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
            QApplication.sendEvent(self.webview, press_event)
            
            time.sleep(0.1)
            
            release_event = QMouseEvent(QMouseEvent.MouseButtonRelease, QPoint(end_x, end_y), end_global, Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
            QApplication.sendEvent(self.webview, release_event)
            
            print(f"回退到简单Qt滑动完成")
        except Exception as e:
            print(f"回退滑动也失败: {e}")
    
    def perform_webview_click(self, x, y):
        """在webview内执行点击事件 - 完善的Qt事件方法"""
        try:
            print(f"执行点击: 坐标({x}, {y})")
            
            from PyQt5.QtCore import QPoint, QTimer
            from PyQt5.QtGui import QMouseEvent
            from PyQt5.QtCore import Qt
            from PyQt5.QtWidgets import QApplication
            
            # 确保webview有焦点并激活
            self.webview.setFocus()
            self.webview.activateWindow()
            self.webview.raise_()
            
            # 获取webview的本地和全局坐标
            local_point = QPoint(x, y)
            global_point = self.webview.mapToGlobal(local_point)
            
            # 先移动到目标位置
            move_event = QMouseEvent(
                QMouseEvent.MouseMove,
                local_point,
                global_point,
                Qt.NoButton,
                Qt.NoButton,
                Qt.NoModifier
            )
            
            # 创建鼠标按下事件
            press_event = QMouseEvent(
                QMouseEvent.MouseButtonPress,
                local_point,
                global_point,
                Qt.LeftButton,
                Qt.LeftButton,
                Qt.NoModifier
            )
            
            # 创建鼠标释放事件
            release_event = QMouseEvent(
                QMouseEvent.MouseButtonRelease,
                local_point,
                global_point,
                Qt.LeftButton,
                Qt.NoButton,
                Qt.NoModifier
            )
            
            # 按顺序发送事件，使用多种方法确保事件被处理
            # 方法1: 直接发送到webview
            QApplication.sendEvent(self.webview, move_event)
            QApplication.processEvents()
            time.sleep(0.05)
            
            QApplication.sendEvent(self.webview, press_event)
            QApplication.processEvents()
            time.sleep(0.1)
            
            QApplication.sendEvent(self.webview, release_event)
            QApplication.processEvents()
            
            # 方法2: 尝试发送到webview的page
            try:
                self.webview.page().event(press_event)
                time.sleep(0.05)
                self.webview.page().event(release_event)
                print(f"额外通过page发送事件: ({x}, {y})")
            except Exception as page_e:
                print(f"通过page发送事件失败: {page_e}")
            
            # 方法3: 尝试发送到webview的focusProxy
            try:
                if self.webview.focusProxy():
                    QApplication.sendEvent(self.webview.focusProxy(), press_event)
                    time.sleep(0.05)
                    QApplication.sendEvent(self.webview.focusProxy(), release_event)
                    print(f"额外通过focusProxy发送事件: ({x}, {y})")
            except Exception as proxy_e:
                print(f"通过focusProxy发送事件失败: {proxy_e}")
            
            print(f"Qt点击事件序列完成: ({x}, {y})")
            
        except Exception as e:
            print(f"Qt点击失败: {e}")
            # 回退到传统方法
            self.fallback_click(x, y)
    
    def fallback_click(self, x, y):
        """回退点击方法"""
        try:
            from PyQt5.QtCore import QPoint
            from PyQt5.QtGui import QMouseEvent
            from PyQt5.QtCore import Qt
            from PyQt5.QtWidgets import QApplication
            
            global_point = self.webview.mapToGlobal(QPoint(x, y))
            
            # 简化的点击事件
            press_event = QMouseEvent(
                QMouseEvent.MouseButtonPress,
                QPoint(x, y),
                global_point,
                Qt.LeftButton,
                Qt.LeftButton,
                Qt.NoModifier
            )
            
            release_event = QMouseEvent(
                QMouseEvent.MouseButtonRelease,
                QPoint(x, y),
                global_point,
                Qt.LeftButton,
                Qt.LeftButton,
                Qt.NoModifier
            )
            
            QApplication.sendEvent(self.webview, press_event)
            time.sleep(0.05)
            QApplication.sendEvent(self.webview, release_event)
            
            print(f"回退点击完成: ({x}, {y})")
            
        except Exception as e:
            print(f"回退点击也失败: {e}")
            # 最后的回退
            self.humanized_touch.humanized_click(x, y)
    
    def check_domain_and_redirect(self):
        """检查当前页面域名，如果跳转到外部域名则回到首页"""
        if not self.original_domain:
            print("没有原始域名信息，跳过域名检查")
            return
            
        # 获取当前页面URL
        self.webview.page().runJavaScript("window.location.href", self.on_current_url_checked)
    
    def on_current_url_checked(self, current_url):
        """处理当前URL检查结果"""
        if not current_url:
            print("无法获取当前URL")
            return
            
        try:
            from urllib.parse import urlparse
            parsed_url = urlparse(current_url)
            current_domain = parsed_url.netloc
            
            print(f"当前域名: {current_domain}, 原始域名: {self.original_domain}")
            
            # 检查是否跳转到外部域名
            if current_domain != self.original_domain:
                print(f"检测到跳转到外部域名: {current_domain} -> {self.original_domain}")
                print("正在重定向回原始域名首页...")
                
                # 构建原始域名首页URL
                original_home_url = f"https://{self.original_domain}/"
                self.webview.load(QUrl(original_home_url))
                
                # 停止域名检查定时器
                self.domain_check_timer.stop()
            else:
                print("域名未发生变化，继续监控...")
                # 继续监控，每10秒检查一次
                self.domain_check_timer.start(10000)
                
        except Exception as e:
            print(f"域名检查出错: {e}")
            # 出错时继续监控
            self.domain_check_timer.start(10000)
        
    def perform_random_click(self):
        """执行随机点击"""
        if not self.page_loaded or not self.click_config_manager:
            return
            
        # 获取启用的点击配置
        enabled_configs = self.click_config_manager.get_enabled_click_configs()
        if not enabled_configs:
            return
            
        # 根据概率选择点击位置
        selected_config = self.select_click_config_by_probability(enabled_configs)
        if not selected_config:
            return
            
        # 计算网格中的实际点击位置
        click_x, click_y = self.calculate_grid_click_position(selected_config)
        
        # 记录点击位置
        click_info = {
            'timestamp': time.time(),
            'grid_position': (selected_config['row_index']+1, selected_config['col_index']+1),
            'percentage': selected_config['percentage'],
            'coordinates': (click_x, click_y),
            'device_size': (self.device["width"], self.device["height"])
        }
        self.click_positions.append(click_info)
        
        # 执行物理点击 - 使用正确的鼠标事件确保在webview内生效
        self.perform_webview_click(click_x, click_y)
        
        print(f"在网格位置({selected_config['row_index']+1},{selected_config['col_index']+1}) "
              f"执行点击，概率:{selected_config['percentage']}%，"
              f"实际坐标:({click_x},{click_y})")
        print(f"已记录点击位置，总计: {len(self.click_positions)} 次")
        
    def select_click_config_by_probability(self, enabled_configs):
        """根据概率选择点击配置"""
        # 计算总概率
        total_probability = sum(config.get("percentage", 0) for config in enabled_configs)
        if total_probability <= 0:
            return None
            
        # 生成随机数
        random_value = random.uniform(0, total_probability)
        
        # 根据概率选择配置
        current_probability = 0
        for config in enabled_configs:
            current_probability += config.get("percentage", 0)
            if random_value <= current_probability:
                return config
                
        return None
        
    def calculate_grid_click_position(self, config):
        """计算网格中的实际点击位置"""
        row = config["row_index"]
        col = config["col_index"]
        
        # 计算网格大小
        grid_width = self.device["width"] / self.grid_cols
        grid_height = self.device["height"] / self.grid_rows
        
        # 计算网格中心点
        center_x = int(col * grid_width + grid_width / 2)
        center_y = int(row * grid_height + grid_height / 2)
        
        # 在网格内添加随机偏移（避免总是点击中心）
        offset_x = random.randint(-int(grid_width/4), int(grid_width/4))
        offset_y = random.randint(-int(grid_height/4), int(grid_height/4))
        
        final_x = max(10, min(center_x + offset_x, self.device["width"] - 10))
        final_y = max(10, min(center_y + offset_y, self.device["height"] - 10))
        
        return final_x, final_y
        
    def get_grid_info(self):
        """获取网格信息"""
        if not self.device:
            return {}
            
        grid_width = self.device["width"] / self.grid_cols
        grid_height = self.device["height"] / self.grid_rows
        
        return {
            "rows": self.grid_rows,
            "cols": self.grid_cols,
            "grid_width": grid_width,
            "grid_height": grid_height,
            "total_cells": self.grid_rows * self.grid_cols
        }
        
    def generate_click_positions_image(self):
        """生成点击位置图片"""
        if not self.click_positions:
            print("没有点击记录，无法生成图片")
            return
            
        try:
            from PIL import Image, ImageDraw, ImageFont
            import os
            
            # 获取设备尺寸
            device_width = self.device["width"]
            device_height = self.device["height"]
            
            # 创建图片
            img = Image.new('RGB', (device_width, device_height), color='white')
            draw = ImageDraw.Draw(img)
            
            # 绘制网格
            grid_width = device_width / self.grid_cols
            grid_height = device_height / self.grid_rows
            
            # 绘制网格线
            for i in range(self.grid_cols + 1):
                x = int(i * grid_width)
                draw.line([(x, 0), (x, device_height)], fill='lightgray', width=1)
                
            for i in range(self.grid_rows + 1):
                y = int(i * grid_height)
                draw.line([(0, y), (device_width, y)], fill='lightgray', width=1)
            
            # 绘制点击位置
            for i, click in enumerate(self.click_positions):
                x, y = click['coordinates']
                grid_row, grid_col = click['grid_position']
                
                # 绘制点击点
                draw.ellipse([x-5, y-5, x+5, y+5], fill='red', outline='darkred')
                
                # 绘制点击信息
                info_text = f"{grid_row},{grid_col}"
                try:
                    # 尝试使用默认字体
                    draw.text((x+8, y-8), info_text, fill='darkred')
                except:
                    # 如果默认字体不可用，使用简单绘制
                    draw.text((x+8, y-8), info_text, fill='darkred')
            
            # 添加标题和统计信息
            title = f"点击位置图 - {self.device['name']}"
            draw.text((10, 10), title, fill='black')
            
            stats_text = f"总点击次数: {len(self.click_positions)}"
            draw.text((10, 30), stats_text, fill='black')
            
            # 保存图片
            filename = f"click_positions_{int(time.time())}.png"
            img.save(filename)
            print(f"点击位置图片已保存: {filename}")
            
        except ImportError:
            print("需要安装PIL库来生成图片: pip install Pillow")
        except Exception as e:
            print(f"生成图片时出错: {e}")
    
    def closeEvent(self, event):
        """关闭事件"""
        # 停止所有定时器
        self.scroll_timer.stop()
        self.click_timer.stop()
        self.domain_check_timer.stop()
        event.accept()
