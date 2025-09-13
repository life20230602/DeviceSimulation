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
        self.click_timer.timeout.connect(self.perform_random_click)
        
        # 域名检查定时器
        self.domain_check_timer = QTimer()
        self.domain_check_timer.timeout.connect(self.check_domain_and_redirect)
        
        # URL变化检查定时器
        self.url_change_timer = QTimer()
        self.url_change_timer.timeout.connect(self.check_url_change)
        self.url_change_timer.setSingleShot(True)
        
        # 页面加载状态
        self.page_loaded = False
        
        # 存储原始URL用于对比
        self.original_url = url
        # 存储当前加载的URL用于变化检查
        self.current_loaded_url = None
        
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
            if self.referrer_url:
                self.load_with_referrer_header()
            else:
                self.webview.load(QUrl(self.url))

    def setup_webview(self):
        """设置WebView配置"""
        if not self.device:
            return
        
        # 创建自定义profile
        profile = QWebEngineProfile("random_webview_profile", self.webview)
        
        # 设置User Agent
        profile.setHttpUserAgent(self.device["user_agent"])
        
        # 如果有referrer_url，设置请求拦截器
        if self.referrer_url:
            print(f"将设置Referer: {self.referrer_url}")
            self.setup_referrer_interceptor(profile)
        
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
    
    def setup_referrer_interceptor(self, profile):
        """设置Referer请求拦截器"""
        from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
        
        class ReferrerInterceptor(QWebEngineUrlRequestInterceptor):
            def __init__(self, referrer_url):
                super().__init__()
                self.referrer_url = referrer_url
                
            def interceptRequest(self, info):
                """拦截请求并添加Referer头"""
                url = info.requestUrl().toString()
                print(f"拦截请求: {url}")
                print(f"添加Referer头: {self.referrer_url}")
                
                # 添加Referer头
                info.setHttpHeader(b"Referer", self.referrer_url.encode())
                
                # 也可以添加其他头
                if self.device and 'user_agent' in self.device:
                    info.setHttpHeader(b"User-Agent", self.device['user_agent'].encode())
        
        # 创建拦截器实例
        interceptor = ReferrerInterceptor(self.referrer_url)
        
        # 设置到profile
        profile.setUrlRequestInterceptor(interceptor)
        print("Referer请求拦截器已设置")
    
    def check_referrer_effectiveness(self):
        """检查referrer是否生效"""
        if not self.referrer_url:
            return
            
        js_code = f"""
        console.error('=== Referrer检查 ===');
        console.error('设置的Referer URL: {self.referrer_url}');
        console.error('document.referrer:', document.referrer);
        console.error('document.referrer长度:', document.referrer.length);
        console.error('是否为空:', document.referrer === '');
        console.error('是否匹配:', document.referrer === '{self.referrer_url}');
        """
        
        self.webview.page().runJavaScript(js_code)
    
    def trigger_random_swipes(self):
        """触发随机滑动3-5次，每次间隔500毫秒"""
        if not self.page_loaded or not self.device:
            return
            
        # 随机生成滑动次数（3-5次）
        swipe_count = random.randint(3, 5)
        print(f"将执行{swipe_count}次随机滑动，每次间隔500毫秒")
        
        # 为每次滑动设置延迟，避免同时执行
        for i in range(swipe_count):
            delay = i * 500  # 每次滑动间隔500毫秒
            QTimer.singleShot(delay, lambda idx=i: self.execute_single_swipe(idx + 1, swipe_count))
    
    def execute_single_swipe(self, swipe_index, total_swipes):
        """执行单次滑动"""
        if not self.page_loaded or not self.device:
            print("页面未加载完成或设备信息缺失，跳过滑动")
            return
            
        # 生成随机滑动参数 - 只向上滑动
        start_x = random.randint(100, self.device["width"] - 100)
        start_y = random.randint(200, self.device["height"] - 100)
        
        # 只模拟Y方向向上滑动，X坐标保持不变
        end_x = start_x
        end_y = start_y - random.randint(150, 300)  # 向上滑动150-300px
        
        # 确保滑动范围在页面内
        end_y = max(50, end_y)
        
        print(f"执行第{swipe_index}/{total_swipes}次滑动: ({start_x}, {start_y}) -> ({end_x}, {end_y})")
        
        # 执行滑动
        self.perform_touch_swipe_js(start_x, start_y, end_x, end_y)
    
    def load_with_referrer_header(self):
        """使用自定义HTTP请求加载URL并设置Referer头"""
        if not self.url or not self.referrer_url:
            return
            
        try:
            from PyQt5.QtWebEngineCore import QWebEngineHttpRequest
            
            # 创建自定义HTTP请求
            request = QWebEngineHttpRequest(QUrl(self.url))
            
            # 设置Referer头
            request.setHeader(b"Referer", self.referrer_url.encode())
            
            # 设置User-Agent头
            if self.device and 'user_agent' in self.device:
                request.setHeader(b"User-Agent", self.device['user_agent'].encode())
            
            # 设置其他常用头
            request.setHeader(b"Accept", b"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
            request.setHeader(b"Accept-Language", b"zh-CN,zh;q=0.9,en;q=0.8")
            request.setHeader(b"Accept-Encoding", b"gzip, deflate, br")
            request.setHeader(b"Connection", b"keep-alive")
            request.setHeader(b"Upgrade-Insecure-Requests", b"1")
            
            print(f"使用自定义请求加载: {self.url}")
            print(f"Referer头: {self.referrer_url}")
            
            # 加载请求
            self.webview.page().load(request)
            
        except Exception as e:
            print(f"自定义请求加载失败: {e}")
            # 回退到普通加载
            self.webview.load(QUrl(self.url))
    
    def on_load_started(self):
        """页面开始加载"""
        self.setWindowTitle(f"加载中... - {self.device['name'] if self.device else 'Unknown Device'}")
        self.page_loaded = False
        
        # 记录当前加载的URL
        current_url = self.webview.url().toString()
        self.current_loaded_url = current_url
        print(f"开始加载URL: {current_url}")
        
    def on_load_progress(self, progress):
        """页面加载进度变化"""
        self.setWindowTitle(f"加载中 {progress}% - {self.device['name'] if self.device else 'Unknown Device'}")
        
        # 当加载进度达到80%时开始模拟用户行为
        if progress >= 80 and not self.page_loaded:
            print(f"页面加载进度达到{progress}%，开始模拟用户行为")
            self.page_loaded = True
            # 启动定时器
            self.start_auto_behavior()
            
            # 触发随机滑动
            self.trigger_random_swipes()
            
            # 启动URL检查定时器（3秒后检查）
            if self.original_url:
                self.domain_check_timer.start(3000)
                print(f"URL检查定时器已启动，3秒后检查是否跳转到外部URL")
            
            # 启动URL变化检查定时器（20秒后检查）
            self.url_change_timer.start(20000)
            print(f"URL变化检查定时器已启动，20秒后检查URL是否变化")
        
    def on_load_finished(self, success):
        """页面加载完成"""
        if success:
            self.setWindowTitle(f"WebView - {self.device['name'] if self.device else 'Unknown Device'}")
            
            # 检查referrer是否生效
            if self.referrer_url:
                self.check_referrer_effectiveness()
        else:
            self.setWindowTitle(f"加载失败 - {self.device['name'] if self.device else 'Unknown Device'}")
            
    def start_auto_behavior(self):
        """开始自动行为"""
        if not self.page_loaded:
            return
            
        # 重置滑动计数
        self.scroll_count = 0
        
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
        if self.click_timer.isActive():
            self.stop_auto_behavior()
        else:
            self.start_auto_behavior()
            
    
    
    def perform_touch_swipe_js(self, start_x, start_y, end_x, end_y):
        """通过JavaScript直接滑动页面，同时模拟触摸事件"""
        import random
        
        # 检查页面是否已加载
        if not self.page_loaded:
            print("页面未加载完成，跳过滑动")
            return
        
        # 生成触摸事件ID
        touch_id = random.randint(1000, 9999)
        
        # 计算滑动参数
        duration = 800  # 滑动持续时间(ms)
        steps = max(20, int(duration / 40))  # 每40ms一步
        step_x = (end_x - start_x) / steps
        step_y = (end_y - start_y) / steps
        
        # 通过JavaScript直接滑动页面并模拟触摸事件
        touch_swipe_js = f"""
        (function() {{
            const touchId = {touch_id};
            const startX = {start_x};
            const startY = {start_y};
            const endX = {end_x};
            const endY = {end_y};
            const steps = {steps};
            const stepX = {step_x};
            const stepY = {step_y};
            const duration = {duration};
            
            // 获取起始目标元素
            const startElement = document.elementFromPoint(startX, startY);
            if (!startElement) {{
                console.log('无法找到起始目标元素');
                return;
            }}
            
            // 创建触摸对象属性
            const createTouchProps = (element, x, y, id) => {{
                return {{
                    identifier: id,
                    target: element,
                    clientX: x,
                    clientY: y,
                    pageX: x,
                    pageY: y,
                    screenX: x,
                    screenY: y,
                    radiusX: 10,
                    radiusY: 10,
                    rotationAngle: 0,
                    force: 1.0
                }};
            }};
            
            // 尝试使用TouchEvent，如果失败则使用自定义事件
            const tryTouchEvent = (type, touches, changedTouches) => {{
                try {{
                    const event = new TouchEvent(type, {{
                        bubbles: true,
                        cancelable: true,
                        touches: touches,
                        targetTouches: touches,
                        changedTouches: changedTouches
                    }});
                    return event;
                }} catch (e) {{
                    console.log('TouchEvent不支持，使用自定义事件:', e.message);
                    const event = new CustomEvent(type, {{
                        bubbles: true,
                        cancelable: true
                    }});
                    event.touches = touches || [];
                    event.targetTouches = touches || [];
                    event.changedTouches = changedTouches || [];
                    return event;
                }}
            }};
            
            // 计算滑动距离
            const scrollDeltaX = endX - startX;
            const scrollDeltaY = endY - startY;
            
            // 触摸开始
            const touchStart = tryTouchEvent('touchstart', 
                [createTouchProps(startElement, startX, startY, touchId)], 
                [createTouchProps(startElement, startX, startY, touchId)]
            );
            
            startElement.dispatchEvent(touchStart);
            console.log('触摸滑动开始:', startX, startY);
            
            // 触摸移动和页面滑动
            let currentStep = 0;
            let lastScrollX = 0;
            let lastScrollY = 0;
            
            const moveInterval = setInterval(() => {{
                currentStep++;
                const currentX = startX + (stepX * currentStep);
                const currentY = startY + (stepY * currentStep);
                
                // 计算当前滑动进度
                const progress = currentStep / steps;
                const currentScrollX = -(scrollDeltaX * progress);
                const currentScrollY = -(scrollDeltaY * progress);
                
                // 计算这一步的滑动增量
                const deltaX = currentScrollX - lastScrollX;
                const deltaY = currentScrollY - lastScrollY;
                
                // 执行页面滑动
                if (Math.abs(deltaX) > 0 || Math.abs(deltaY) > 0) {{
                    window.scrollBy(deltaX, deltaY);
                    lastScrollX = currentScrollX;
                    lastScrollY = currentScrollY;
                }}
                
                // 获取当前元素
                const currentElement = document.elementFromPoint(currentX, currentY);
                if (currentElement) {{
                    const touchMove = tryTouchEvent('touchmove',
                        [createTouchProps(currentElement, currentX, currentY, touchId)],
                        [createTouchProps(currentElement, currentX, currentY, touchId)]
                    );
                    
                    currentElement.dispatchEvent(touchMove);
                }}
                
                if (currentStep >= steps) {{
                    clearInterval(moveInterval);
                    
                    // 触摸结束
                    const endElement = document.elementFromPoint(endX, endY);
                    if (endElement) {{
                        const touchEnd = tryTouchEvent('touchend',
                            [],
                            [createTouchProps(endElement, endX, endY, touchId)]
                        );
                        
                        endElement.dispatchEvent(touchEnd);
                        console.log('触摸滑动结束:', endX, endY);
                    }}
                    
                    console.log('页面滑动完成，总滑动距离:', scrollDeltaX, scrollDeltaY);
                }}
            }}, duration / steps);
        }})();
        """
        
        # 执行JavaScript滑动和触摸事件
        self.webview.page().runJavaScript(touch_swipe_js)
        print(f"JavaScript滑动和触摸事件已发送: ({start_x}, {start_y}) -> ({end_x}, {end_y})")
    

    
    def perform_webview_click(self, x, y):
        """在webview内执行点击事件 - 使用JavaScript触摸事件"""
        try:
            print(f"执行触摸点击: 坐标({x}, {y})")
            
            # 确保webview有焦点并激活
            self.webview.setFocus()
            self.webview.activateWindow()
            self.webview.raise_()
            
            # 使用JavaScript触摸事件替代Qt鼠标事件
            self.perform_touch_click_js(x, y)
            
        except Exception as e:
            print(f"触摸点击失败: {e}")
    
    def perform_touch_click_js(self, x, y):
        """使用JavaScript执行触摸点击事件"""
        import random
        
        # 生成触摸事件ID
        touch_id = random.randint(1000, 9999)
        
        # 直接执行触摸点击事件
        touch_click_js = f"""
        (function() {{
            const touchId = {touch_id};
            
            // 直接执行触摸点击事件
            const targetX = {x};
            const targetY = {y};
            
            // 获取目标元素
            const targetElement = document.elementFromPoint(targetX, targetY);
            if (!targetElement) {{
                console.log('无法找到目标元素');
                return;
            }}
            
            console.log('目标元素:', targetElement);
            
            // 创建触摸对象属性
            const touchProps = {{
                identifier: touchId,
                target: targetElement,
                clientX: targetX,
                clientY: targetY,
                pageX: targetX,
                pageY: targetY,
                screenX: targetX,
                screenY: targetY,
                radiusX: 10,
                radiusY: 10,
                rotationAngle: 0,
                force: 1.0
            }};
            
            // 方法1: 尝试使用TouchEvent（如果支持）
            try {{
                // 创建触摸开始事件
                const touchStart = new TouchEvent('touchstart', {{
                    bubbles: true,
                    cancelable: true,
                    touches: [touchProps],
                    targetTouches: [touchProps],
                    changedTouches: [touchProps]
                }});
                
                targetElement.dispatchEvent(touchStart);
                console.log('TouchEvent触摸开始事件已触发:', targetX, targetY);
                
                // 短暂延迟后触发触摸结束事件
                setTimeout(() => {{
                    const touchEnd = new TouchEvent('touchend', {{
                        bubbles: true,
                        cancelable: true,
                        touches: [],
                        targetTouches: [],
                        changedTouches: [touchProps]
                    }});
                    
                    targetElement.dispatchEvent(touchEnd);
                    console.log('TouchEvent触摸结束事件已触发:', targetX, targetY);
                    
                    // 同时触发click事件以确保兼容性
                    const clickEvent = new MouseEvent('click', {{
                        bubbles: true,
                        cancelable: true,
                        clientX: targetX,
                        clientY: targetY,
                        button: 0,
                        buttons: 1
                    }});
                    
                    targetElement.dispatchEvent(clickEvent);
                    console.log('点击事件已触发:', targetX, targetY);
                }}, {random.randint(50, 150)});
                
            }} catch (e) {{
                console.log('TouchEvent不支持，使用自定义事件:', e.message);
                
                // 方法2: 使用自定义事件模拟触摸
                const createCustomTouchEvent = (type, touches, changedTouches) => {{
                    const event = new CustomEvent(type, {{
                        bubbles: true,
                        cancelable: true
                    }});
                    
                    // 添加触摸属性
                    event.touches = touches || [];
                    event.targetTouches = touches || [];
                    event.changedTouches = changedTouches || [];
                    
                    return event;
                }};
                
                // 触发自定义触摸开始事件
                const customTouchStart = createCustomTouchEvent('touchstart', [touchProps], [touchProps]);
                targetElement.dispatchEvent(customTouchStart);
                console.log('自定义触摸开始事件已触发:', targetX, targetY);
                
                // 短暂延迟后触发自定义触摸结束事件
                setTimeout(() => {{
                    const customTouchEnd = createCustomTouchEvent('touchend', [], [touchProps]);
                    targetElement.dispatchEvent(customTouchEnd);
                    console.log('自定义触摸结束事件已触发:', targetX, targetY);
                    
                    // 同时触发click事件以确保兼容性
                    const clickEvent = new MouseEvent('click', {{
                        bubbles: true,
                        cancelable: true,
                        clientX: targetX,
                        clientY: targetY,
                        button: 0,
                        buttons: 1
                    }});
                    
                    targetElement.dispatchEvent(clickEvent);
                    console.log('点击事件已触发:', targetX, targetY);
                }}, {random.randint(50, 150)});
            }}
        }})();
        """
        
        # 执行JavaScript触摸事件
        self.webview.page().runJavaScript(touch_click_js)
        print(f"JavaScript触摸点击事件已发送: ({x}, {y})")
    
    def check_domain_and_redirect(self):
        """检查当前页面URL，如果跳转到外部URL则回到原始URL"""
        if not self.original_url:
            print("没有原始URL信息，跳过URL检查")
            return
            
        # 获取当前页面URL
        self.webview.page().runJavaScript("window.location.href", self.on_current_url_checked)
    
    def on_current_url_checked(self, current_url):
        """处理当前URL检查结果"""
        if not current_url:
            print("无法获取当前URL")
            return
            
        try:
            print(f"当前URL: {current_url}")
            print(f"原始URL: {self.original_url}")
            
            # 标准化URL进行比较（移除协议、www、末尾斜杠等）
            current_normalized = self.normalize_url(current_url)
            original_normalized = self.normalize_url(self.original_url)
            
            print(f"标准化后 - 当前: {current_normalized}")
            print(f"标准化后 - 原始: {original_normalized}")
            
            # 检查是否跳转到外部URL
            if current_normalized != original_normalized:
                print(f"检测到跳转到外部URL，正在重定向回原始URL...")
                print(f"重定向到: {self.original_url}")
                self.webview.load(QUrl(self.original_url))
                
                # 停止URL检查定时器
                self.domain_check_timer.stop()
            else:
                print("URL未发生变化，继续监控...")
                # 继续监控，每10秒检查一次
                self.domain_check_timer.start(10000)
                
        except Exception as e:
            print(f"URL检查出错: {e}")
            # 出错时继续监控
            self.domain_check_timer.start(10000)
    
    def normalize_url(self, url):
        """标准化URL用于比较"""
        if not url:
            return ""
        
        # 移除协议前缀
        if url.startswith('https://'):
            url = url[8:]
        elif url.startswith('http://'):
            url = url[7:]
        
        # 移除www前缀
        if url.startswith('www.'):
            url = url[4:]
        
        # 移除末尾的斜杠
        if url.endswith('/'):
            url = url[:-1]
        
        return url.lower()
    
    def check_url_change(self):
        """检查URL是否在20秒后发生变化，如果未变化则重新加载原始URL"""
        if not self.original_url or not self.current_loaded_url:
            print("没有URL信息，跳过URL变化检查")
            return
            
        # 获取当前页面URL
        self.webview.page().runJavaScript("window.location.href", self.on_url_change_checked)
    
    def on_url_change_checked(self, current_url):
        """处理URL变化检查结果"""
        if not current_url:
            print("无法获取当前URL，重新加载原始URL")
            self.webview.load(QUrl(self.original_url))
            return
            
        try:
            print(f"URL变化检查 - 当前URL: {current_url}")
            print(f"URL变化检查 - 加载时URL: {self.current_loaded_url}")
            
            # 标准化URL进行比较
            current_normalized = self.normalize_url(current_url)
            loaded_normalized = self.normalize_url(self.current_loaded_url)
            
            print(f"标准化后 - 当前: {current_normalized}")
            print(f"标准化后 - 加载时: {loaded_normalized}")
            
            # 检查URL是否发生变化
            if current_normalized == loaded_normalized:
                print("URL在20秒内未发生变化，重新加载原始URL")
                print(f"重新加载: {self.original_url}")
                self.webview.load(QUrl(self.original_url))
            else:
                print("URL已发生变化，继续监控")
                
        except Exception as e:
            print(f"URL变化检查出错: {e}")
            # 出错时重新加载原始URL
            self.webview.load(QUrl(self.original_url))
        
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
        self.click_timer.stop()
        self.domain_check_timer.stop()
        self.url_change_timer.stop()
        event.accept()
