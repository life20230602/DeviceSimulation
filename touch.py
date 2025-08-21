import sys
import random
import time
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
        
    def start_browsing(self, click_interval_min=1, click_interval_max=3, scroll_interval_min=10, scroll_interval_max=30):
        print('start_browsing')
        """开始模拟浏览行为"""
        self.browsing_mode = True
        
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
        
        # 执行点击
        self.humanized_click(x, y)
        
        # 重新设置随机间隔
        interval = random.uniform(5, 15)
        self.click_timer.setInterval(interval * 1000)
        
    def perform_scroll(self):
        """执行随机滚动"""
        scroll_amount = random.randint(100, 500)
        if random.choice([True, False]):
            # 向上滚动
            self.webview.page().runJavaScript(f"window.scrollBy(0, -{scroll_amount});")
        else:
            # 向下滚动
            self.webview.page().runJavaScript(f"window.scrollBy(0, {scroll_amount});")
            
        # 重新设置随机间隔
        interval = random.uniform(10, 30)
        self.scroll_timer.setInterval(interval * 1000)
        
    def humanized_click(self, x, y):
        """模拟人类点击行为（包括微小移动和随机延迟）"""
        # 添加微小随机偏移（人类点击不会完全精确）
        offset_x = random.randint(-3, 3)
        offset_y = random.randint(-3, 3)
        target_x = x + offset_x
        target_y = y + offset_y
        
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