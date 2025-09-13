import sys
import random
import time
import json
from PyQt5.QtCore import QTimer, QPoint, QRect, Qt, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QMouseEvent, QKeyEvent
import numpy as np

class HumanizedController():
    def __init__(self, webview: QWebEngineView):
        self.webview = webview
        self.click_areas = []  # 存储点击区域和权重: (rect, weight)
        self.browsing_mode = False
        self.click_timer = QTimer()
        self.click_timer.timeout.connect(self.perform_random_click)
        self.scroll_timer = QTimer()
        self.scroll_timer.timeout.connect(self.perform_scroll)
        # self.webview.loadFinished.connect(self.on_load_finished)
        
    def add_click_area(self, rect, weight=1):
        """添加点击区域和权重"""
        self.click_areas.append((rect, weight))
        
    def start_browsing(self, click_interval_min=1, click_interval_max=3, scroll_interval_min=10, scroll_interval_max=30, use_touch=False):
        print('start_browsing')
        """开始模拟浏览行为"""
        self.browsing_mode = True
        self.use_touch = use_touch  # 存储触摸模式设置
        
        # 设置随机点击定时器
        click_interval = random.uniform(click_interval_min, click_interval_max)
        self.click_timer.start(click_interval * 1000)  # 转换为毫秒
        
        # 设置随机滚动定时器
        scroll_interval = random.uniform(scroll_interval_min, scroll_interval_max)
        self.scroll_timer.start(scroll_interval * 1000)  # 转换为毫秒
        
    def stop_browsing(self):
        """停止模拟浏览行为"""
        self.browsing_mode = False
        self.click_timer.stop()
        self.scroll_timer.stop()
        
    def perform_random_click(self):
        """根据权重随机选择区域并执行点击"""
        if not self.click_areas:
            return
            
        # 根据权重选择点击区域
        weights = [weight for _, weight in self.click_areas]
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]
        
        # 随机选择区域
        selected_index = np.random.choice(len(self.click_areas), p=normalized_weights)
        selected_rect, _ = self.click_areas[selected_index]
        
        # 在选定区域内随机选择点击位置
        x = random.randint(selected_rect.left(), selected_rect.right())
        y = random.randint(selected_rect.top(), selected_rect.bottom())
        
        # 执行点击，使用触摸模式（如果启用）
        use_touch = getattr(self, 'use_touch', False)
        self.humanized_click(x, y, use_touch=use_touch)
        
        # 重新设置随机间隔
        interval = random.uniform(5, 15)
        self.click_timer.setInterval(interval * 1000)
        
    def perform_scroll(self, use_touch=None):
        """执行随机滚动"""
        scroll_amount = random.randint(100, 500)
        
        # 如果没有指定use_touch，使用实例设置
        if use_touch is None:
            use_touch = getattr(self, 'use_touch', False)
        
        if use_touch:
            # 使用触摸滑动
            # 获取当前滚动位置
            self.webview.page().runJavaScript("""
                (function() {
                    const currentScrollY = window.pageYOffset || document.documentElement.scrollTop;
                    const currentScrollX = window.pageXOffset || document.documentElement.scrollLeft;
                    
                    // 计算滑动方向
                    const scrollUp = Math.random() < 0.5;
                    const scrollAmount = Math.floor(Math.random() * 400) + 100;
                    
                    let startY, endY;
                    if (scrollUp) {
                        startY = currentScrollY + 200;
                        endY = startY - scrollAmount;
                    } else {
                        startY = currentScrollY + 200;
                        endY = startY + scrollAmount;
                    }
                    
                    // 触发触摸滑动
                    window.touchScrollStartY = startY;
                    window.touchScrollEndY = endY;
                    window.touchScrollAmount = scrollAmount;
                    window.touchScrollUp = scrollUp;
                })();
            """)
            
            # 执行触摸滑动
            self.webview.page().runJavaScript("""
                (function() {
                    if (window.touchScrollStartY !== undefined) {
                        const touchId = Math.floor(Math.random() * 9000) + 1000;
                        const startX = window.innerWidth / 2;
                        const startY = window.touchScrollStartY;
                        const endX = window.innerWidth / 2;
                        const endY = window.touchScrollEndY;
                        
                        // 触摸开始
                        const touchStart = new TouchEvent('touchstart', {
                            bubbles: true,
                            cancelable: true,
                            touches: [{
                                identifier: touchId,
                                target: document.elementFromPoint(startX, startY),
                                clientX: startX,
                                clientY: startY,
                                pageX: startX,
                                pageY: startY,
                                screenX: startX,
                                screenY: startY,
                                radiusX: 10,
                                radiusY: 10,
                                rotationAngle: 0,
                                force: 1.0
                            }],
                            targetTouches: [{
                                identifier: touchId,
                                target: document.elementFromPoint(startX, startY),
                                clientX: startX,
                                clientY: startY,
                                pageX: startX,
                                pageY: startY,
                                screenX: startX,
                                screenY: startY,
                                radiusX: 10,
                                radiusY: 10,
                                rotationAngle: 0,
                                force: 1.0
                            }],
                            changedTouches: [{
                                identifier: touchId,
                                target: document.elementFromPoint(startX, startY),
                                clientX: startX,
                                clientY: startY,
                                pageX: startX,
                                pageY: startY,
                                screenX: startX,
                                screenY: startY,
                                radiusX: 10,
                                radiusY: 10,
                                rotationAngle: 0,
                                force: 1.0
                            }]
                        });
                        
                setTrusted(touchStart);
                document.elementFromPoint(startX, startY).dispatchEvent(touchStart);
                        
                        // 触摸移动
                        const steps = 20;
                        const stepY = (endY - startY) / steps;
                        let currentStep = 0;
                        
                        const moveInterval = setInterval(() => {
                            currentStep++;
                            const currentY = startY + (stepY * currentStep);
                            
                            const touchMove = new TouchEvent('touchmove', {
                                bubbles: true,
                                cancelable: true,
                                touches: [{
                                    identifier: touchId,
                                    target: document.elementFromPoint(endX, currentY),
                                    clientX: endX,
                                    clientY: currentY,
                                    pageX: endX,
                                    pageY: currentY,
                                    screenX: endX,
                                    screenY: currentY,
                                    radiusX: 10,
                                    radiusY: 10,
                                    rotationAngle: 0,
                                    force: 1.0
                                }],
                                targetTouches: [{
                                    identifier: touchId,
                                    target: document.elementFromPoint(endX, currentY),
                                    clientX: endX,
                                    clientY: currentY,
                                    pageX: endX,
                                    pageY: currentY,
                                    screenX: endX,
                                    screenY: currentY,
                                    radiusX: 10,
                                    radiusY: 10,
                                    rotationAngle: 0,
                                    force: 1.0
                                }],
                                changedTouches: [{
                                    identifier: touchId,
                                    target: document.elementFromPoint(endX, currentY),
                                    clientX: endX,
                                    clientY: currentY,
                                    pageX: endX,
                                    pageY: currentY,
                                    screenX: endX,
                                    screenY: currentY,
                                    radiusX: 10,
                                    radiusY: 10,
                                    rotationAngle: 0,
                                    force: 1.0
                                }]
                            });
                            
                            setTrusted(touchMove);
                            document.elementFromPoint(endX, currentY).dispatchEvent(touchMove);
                            
                            if (currentStep >= steps) {
                                clearInterval(moveInterval);
                                
                                // 触摸结束
                                const touchEnd = new TouchEvent('touchend', {
                                    bubbles: true,
                                    cancelable: true,
                                    touches: [],
                                    targetTouches: [],
                                    changedTouches: [{
                                        identifier: touchId,
                                        target: document.elementFromPoint(endX, endY),
                                        clientX: endX,
                                        clientY: endY,
                                        pageX: endX,
                                        pageY: endY,
                                        screenX: endX,
                                        screenY: endY,
                                        radiusX: 10,
                                        radiusY: 10,
                                        rotationAngle: 0,
                                        force: 1.0
                                    }]
                                });
                                
                                setTrusted(touchEnd);
                                document.elementFromPoint(endX, endY).dispatchEvent(touchEnd);
                            }
                        }, 50);
                    }
                })();
            """)
        else:
            # 使用传统的JavaScript滚动
            if random.choice([True, False]):
                # 向上滚动
                self.webview.page().runJavaScript(f"window.scrollBy(0, -{scroll_amount});")
            else:
                # 向下滚动
                self.webview.page().runJavaScript(f"window.scrollBy(0, {scroll_amount});")
            
        # 重新设置随机间隔
        interval = random.uniform(10, 30)
        self.scroll_timer.setInterval(interval * 1000)
        
    def humanized_click(self, x, y, use_touch=False):
        """模拟人类点击行为（包括微小移动和随机延迟）"""
        # 添加微小随机偏移（人类点击不会完全精确）
        offset_x = random.randint(-3, 3)
        offset_y = random.randint(-3, 3)
        target_x = x + offset_x
        target_y = y + offset_y
        
        if use_touch:
            # 使用触摸事件
            self.simulate_touch_click(target_x, target_y)
        else:
            # 使用鼠标事件
            # 模拟鼠标移动和点击
            self.simulate_mouse_move(target_x, target_y)
            
            # 添加随机延迟（人类点击前会有短暂停顿）
            delay = random.uniform(0.1, 0.3)
            time.sleep(delay)
            
            # 执行点击
            self.simulate_mouse_click(target_x, target_y)
            
            # 添加点击后随机微小移动
            time.sleep(0.1)
            self.simulate_mouse_move(target_x + random.randint(-5, 5), target_y + random.randint(-5, 5))
        
    def simulate_mouse_move(self, x, y):
        """模拟鼠标移动"""
        event = QMouseEvent(
            QMouseEvent.MouseMove,
            QPoint(x, y),
            Qt.LeftButton,
            Qt.LeftButton,
            Qt.NoModifier
        )
        print("移动",x,y)
        QApplication.sendEvent(self.webview, event)
        
    def simulate_mouse_click(self, x, y):
        """模拟鼠标点击"""
        # 鼠标按下
        press_event = QMouseEvent(
            QMouseEvent.MouseButtonPress,
            QPoint(x, y),
            Qt.LeftButton,
            Qt.LeftButton,
            Qt.NoModifier
        )
        QApplication.sendEvent(self.webview, press_event)
        
        # 短暂延迟
        time.sleep(random.uniform(0.05, 0.1))
        
        # 鼠标释放
        release_event = QMouseEvent(
            QMouseEvent.MouseButtonRelease,
            QPoint(x, y),
            Qt.LeftButton,
            Qt.LeftButton,
            Qt.NoModifier
        )
        print("点击",x,y)
        QApplication.sendEvent(self.webview, release_event)
    
    def simulate_touch_click(self, x, y):
        """使用JavaScript模拟触摸点击事件 - 使用兼容性更好的方法并代理isTrusted属性"""
        # 生成触摸事件ID
        touch_id = random.randint(1000, 9999)
        
        # 创建触摸开始事件 - 使用更兼容的方法并代理isTrusted属性
        touch_start_js = f"""
        (function() {{
            const touchId = {touch_id};
            const targetX = {x};
            const targetY = {y};
            
            // 获取目标元素
            const targetElement = document.elementFromPoint(targetX, targetY);
            if (!targetElement) {{
                console.log('无法找到目标元素');
                return;
            }}
            
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
            
            // 直接修改isTrusted属性的函数
            const setTrusted = (event) => {{
                try {{
                    // 方法1: 尝试使用Object.defineProperty
                    Object.defineProperty(event, 'isTrusted', {{
                        value: true,
                        writable: false,
                        enumerable: true,
                        configurable: false
                    }});
                }} catch (e) {{
                    console.log('defineProperty失败，尝试其他方法:', e.message);
                    try {{
                        // 方法2: 尝试直接赋值
                        event.isTrusted = true;
                    }} catch (e2) {{
                        console.log('直接赋值失败:', e2.message);
                        try {{
                            // 方法3: 尝试使用Object.defineProperty with different config
                            Object.defineProperty(event, 'isTrusted', {{
                                value: true,
                                writable: true,
                                enumerable: true,
                                configurable: true
                            }});
                        }} catch (e3) {{
                            console.log('所有方法都失败了:', e3.message);
                        }}
                    }}
                }}
                return event;
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
                
                // 代理isTrusted属性
                setTrusted(touchStart);
                
                targetElement.dispatchEvent(touchStart);
                console.log('TouchEvent触摸开始事件已触发 (isTrusted:', touchStart.isTrusted, '):', targetX, targetY);
                
                // 短暂延迟后触发触摸结束事件
                setTimeout(() => {{
                    const touchEnd = new TouchEvent('touchend', {{
                        bubbles: true,
                        cancelable: true,
                        touches: [],
                        targetTouches: [],
                        changedTouches: [touchProps]
                    }});
                    
                    // 代理isTrusted属性
                    setTrusted(touchEnd);
                    
                    targetElement.dispatchEvent(touchEnd);
                    console.log('TouchEvent触摸结束事件已触发 (isTrusted:', touchEnd.isTrusted, '):', targetX, targetY);
                    
                    // 同时触发click事件以确保兼容性
                    const clickEvent = new MouseEvent('click', {{
                        bubbles: true,
                        cancelable: true,
                        clientX: targetX,
                        clientY: targetY,
                        button: 0,
                        buttons: 1
                    }});
                    
                    // 代理click事件的isTrusted属性
                    setTrusted(clickEvent);
                    
                    targetElement.dispatchEvent(clickEvent);
                    console.log('点击事件已触发 (isTrusted:', clickEvent.isTrusted, '):', targetX, targetY);
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
                    
                    // 代理isTrusted属性
                    setTrusted(event);
                    
                    return event;
                }};
                
                // 触发自定义触摸开始事件
                const customTouchStart = createCustomTouchEvent('touchstart', [touchProps], [touchProps]);
                targetElement.dispatchEvent(customTouchStart);
                console.log('自定义触摸开始事件已触发 (isTrusted:', customTouchStart.isTrusted, '):', targetX, targetY);
                
                // 短暂延迟后触发自定义触摸结束事件
                setTimeout(() => {{
                    const customTouchEnd = createCustomTouchEvent('touchend', [], [touchProps]);
                    targetElement.dispatchEvent(customTouchEnd);
                    console.log('自定义触摸结束事件已触发 (isTrusted:', customTouchEnd.isTrusted, '):', targetX, targetY);
                    
                    // 同时触发click事件以确保兼容性
                    const clickEvent = new MouseEvent('click', {{
                        bubbles: true,
                        cancelable: true,
                        clientX: targetX,
                        clientY: targetY,
                        button: 0,
                        buttons: 1
                    }});
                    
                    // 代理click事件的isTrusted属性
                    setTrusted(clickEvent);
                    
                    targetElement.dispatchEvent(clickEvent);
                    console.log('点击事件已触发 (isTrusted:', clickEvent.isTrusted, '):', targetX, targetY);
                }}, {random.randint(50, 150)});
            }}
        }})();
        """
        
        print(f"触摸点击: ({x}, {y})")
        self.webview.page().runJavaScript(touch_start_js)
    
    def simulate_touch_swipe(self, start_x, start_y, end_x, end_y, duration=500):
        """使用JavaScript模拟触摸滑动事件 - 使用兼容性更好的方法并代理isTrusted属性"""
        touch_id = random.randint(1000, 9999)
        
        # 计算滑动步骤
        steps = max(10, int(duration / 50))  # 每50ms一步
        step_x = (end_x - start_x) / steps
        step_y = (end_y - start_y) / steps
        
        swipe_js = f"""
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
            
            let currentStep = 0;
            
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
            
            // 直接修改isTrusted属性的函数
            const setTrusted = (event) => {{
                try {{
                    // 方法1: 尝试使用Object.defineProperty
                    Object.defineProperty(event, 'isTrusted', {{
                        value: true,
                        writable: false,
                        enumerable: true,
                        configurable: false
                    }});
                }} catch (e) {{
                    console.log('defineProperty失败，尝试其他方法:', e.message);
                    try {{
                        // 方法2: 尝试直接赋值
                        event.isTrusted = true;
                    }} catch (e2) {{
                        console.log('直接赋值失败:', e2.message);
                        try {{
                            // 方法3: 尝试使用Object.defineProperty with different config
                            Object.defineProperty(event, 'isTrusted', {{
                                value: true,
                                writable: true,
                                enumerable: true,
                                configurable: true
                            }});
                        }} catch (e3) {{
                            console.log('所有方法都失败了:', e3.message);
                        }}
                    }}
                }}
                return event;
            }};
            
            // 创建自定义触摸事件
            const createCustomTouchEvent = (type, touches, changedTouches) => {{
                const event = new CustomEvent(type, {{
                    bubbles: true,
                    cancelable: true
                }});
                
                // 添加触摸属性
                event.touches = touches || [];
                event.targetTouches = touches || [];
                event.changedTouches = changedTouches || [];
                
                // 代理isTrusted属性
                const proxiedEvent = setTrusted(event);
                
                return event;
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
                    
                    // 代理isTrusted属性
                    setTrusted(event);
                    
                    return event;
                }} catch (e) {{
                    console.log('TouchEvent不支持，使用自定义事件:', e.message);
                    return createCustomTouchEvent(type, touches, changedTouches);
                }}
            }};
            
            // 触摸开始
            const touchStart = tryTouchEvent('touchstart', 
                [createTouchProps(startElement, startX, startY, touchId)], 
                [createTouchProps(startElement, startX, startY, touchId)]
            );
            
            startElement.dispatchEvent(touchStart);
            console.log('触摸滑动开始 (isTrusted:', touchStart.isTrusted, '):', startX, startY);
            
            // 触摸移动
            const moveInterval = setInterval(() => {{
                currentStep++;
                const currentX = startX + (stepX * currentStep);
                const currentY = startY + (stepY * currentStep);
                
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
                        console.log('触摸滑动结束 (isTrusted:', touchEnd.isTrusted, '):', endX, endY);
                    }}
                }}
            }}, duration / steps);
        }})();
        """
        
        print(f"触摸滑动: ({start_x}, {start_y}) -> ({end_x}, {end_y})")
        self.webview.page().runJavaScript(swipe_js)
    
    # @pyqtSlot(bool)
    def on_load_finished(self, success:bool):
        """页面加载完成后的回调"""
        print(success)
        if success and self.browsing_mode:
            # 页面重新加载后重新开始浏览行为
            self.start_browsing()

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Humanized Web Browser")
#         self.setGeometry(100, 100, 1200, 800)
        
#         # 创建中央部件和布局
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout(central_widget)
        
#         # 创建人机交互Web视图
#         self.web_view = HumanizedWebView()
#         layout.addWidget(self.web_view)
        
#         # 加载网页
#         self.web_view.load("https://example.com")
        
#         # 添加点击区域（示例）
#         # 假设我们想模拟点击页面上的三个区域，权重分别为3, 2, 1
#         self.web_view.add_click_area(QRect(100, 200, 150, 50), 3)  # 高权重区域
#         self.web_view.add_click_area(QRect(300, 400, 100, 80), 2)  # 中等权重区域
#         self.web_view.add_click_area(QRect(500, 600, 120, 60), 1)  # 低权重区域
        
#         # 延迟启动浏览行为，等待页面加载
#         QTimer.singleShot(3000, self.start_browsing)
        
#     def start_browsing(self):
#         """启动浏览行为"""
#         self.web_view.start_browsing()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())