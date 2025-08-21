import webview
import platform
import random
import time
import json
from datetime import datetime
from threading import Thread

class DeviceSimulator:
    def __init__(self, window):
        self.window = window
        self.device_profiles = self.load_device_profiles()
        self.current_profile = self.get_default_profile()
        self.device_info = self.generate_device_info()
        self.screen_metrics = self.calculate_screen_metrics()
        self.injected_js = self.generate_injection_js()
        
    def load_device_profiles(self):
        """加载预定义的设备配置文件"""
        return {
            "iPhone 14 Pro": {
                "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
                "screen": {"width": 393, "height": 852, "pixel_ratio": 3},
                "device": {"type": "mobile", "os": "iOS", "os_version": "16.0"},
                "touch_support": True,
                "platform": "iPhone"
            },
            "Samsung Galaxy S22 Ultra": {
                "user_agent": "Mozilla/5.0 (Linux; Android 12; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
                "screen": {"width": 384, "height": 854, "pixel_ratio": 3.5},
                "device": {"type": "mobile", "os": "Android", "os_version": "12"},
                "touch_support": True,
                "platform": "Android"
            },
            "iPad Pro 12.9": {
                "user_agent": "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
                "screen": {"width": 1024, "height": 1366, "pixel_ratio": 2},
                "device": {"type": "tablet", "os": "iOS", "os_version": "16.0"},
                "touch_support": True,
                "platform": "iPad"
            },
            "Desktop Chrome": {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                "screen": {"width": 1920, "height": 1080, "pixel_ratio": 1},
                "device": {"type": "desktop", "os": "Windows", "os_version": "10"},
                "touch_support": False,
                "platform": "Win32"
            },
            "MacBook Pro": {
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
                "screen": {"width": 1440, "height": 900, "pixel_ratio": 2},
                "device": {"type": "desktop", "os": "macOS", "os_version": "13.5"},
                "touch_support": False,
                "platform": "MacIntel"
            }
        }
    
    def get_default_profile(self):
        """根据当前系统获取默认设备配置"""
        system = platform.system()
        if system == "Darwin":
            return "MacBook Pro"
        elif system == "Windows":
            return "Desktop Chrome"
        elif system == "Linux":
            return "Samsung Galaxy S22 Ultra"
        else:
            return "Desktop Chrome"
    
    def generate_device_info(self):
        """生成设备信息"""
        profile = self.device_profiles[self.current_profile]
        return {
            "profile": self.current_profile,
            "user_agent": profile["user_agent"],
            "screen": profile["screen"],
            "device": profile["device"],
            "device_id": f"device-{random.randint(100000, 999999)}-{int(time.time())}",
            "geolocation": self.generate_geolocation(),
            "network": self.generate_network_info(),
            "battery": self.generate_battery_status(),
            "hardware": self.get_hardware_info(),
            "platform": profile["platform"],
            "touch_support": profile["touch_support"],
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_geolocation(self):
        """生成地理位置信息"""
        cities = [
            {"city": "New York", "lat": 40.7128, "lon": -74.0060, "timezone": "America/New_York"},
            {"city": "London", "lat": 51.5074, "lon": -0.1278, "timezone": "Europe/London"},
            {"city": "Tokyo", "lat": 35.6895, "lon": 139.6917, "timezone": "Asia/Tokyo"},
            {"city": "Sydney", "lat": -33.8688, "lon": 151.2093, "timezone": "Australia/Sydney"},
            {"city": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729, "timezone": "America/Sao_Paulo"}
        ]
        return random.choice(cities)
    
    def generate_network_info(self):
        """生成网络信息"""
        connection_types = ["4g", "wifi", "5g", "3g", "2g", "ethernet"]
        return {
            "type": random.choice(connection_types),
            "effective_type": random.choice(["slow-2g", "2g", "3g", "4g"]),
            "downlink": random.uniform(0.5, 50),
            "rtt": random.randint(50, 500),
            "online": True
        }
    
    def generate_battery_status(self):
        """生成电池状态"""
        return {
            "level": random.uniform(0.1, 1.0),
            "charging": random.choice([True, False]),
            "charging_time": random.randint(0, 3600),
            "discharging_time": random.randint(300, 7200)
        }
    
    def get_hardware_info(self):
        """获取硬件信息"""
        profile = self.device_profiles[self.current_profile]["device"]
        return {
            "cpu_cores": self.get_cpu_core_count(),
            "device_memory": self.get_device_memory(),
            "max_touch_points": self.get_max_touch_points(),
            "concurrency": self.get_hardware_concurrency()
        }
    
    def get_cpu_core_count(self):
        """获取CPU核心数"""
        profile = self.device_profiles[self.current_profile]["device"]
        if profile["type"] == "mobile":
            return random.choice([4, 6, 8])
        elif profile["type"] == "tablet":
            return random.choice([4, 6])
        else:  # desktop
            return random.choice([4, 6, 8, 12, 16])
    
    def get_device_memory(self):
        """获取设备内存(GB)"""
        profile = self.device_profiles[self.current_profile]["device"]
        if profile["type"] == "mobile":
            return random.choice([4, 6, 8, 12])
        elif profile["type"] == "tablet":
            return random.choice([4, 6, 8])
        else:  # desktop
            return random.choice([8, 16, 32, 64])
    
    def get_max_touch_points(self):
        """获取最大触摸点数"""
        profile = self.device_profiles[self.current_profile]["device"]
        if profile["type"] in ["mobile", "tablet"]:
            return 10
        return 0
    
    def get_hardware_concurrency(self):
        """获取硬件并发数"""
        return self.get_cpu_core_count() * 2
    
    def calculate_screen_metrics(self):
        """计算屏幕指标"""
        profile = self.device_profiles[self.current_profile]
        screen = profile["screen"]
        return {
            "width": screen["width"],
            "height": screen["height"],
            "avail_width": screen["width"] - 20,
            "avail_height": screen["height"] - 100,
            "pixel_ratio": screen["pixel_ratio"],
            "color_depth": 24,
            "orientation": "portrait-primary" if screen["width"] < screen["height"] else "landscape-primary"
        }
    
    def generate_injection_js(self):
        
        """生成要注入的JavaScript代码"""
        return f"""
        // 覆盖navigator对象属性
        Object.defineProperty(navigator, 'userAgent', {{
            value: '{self.device_info["user_agent"]}',
            writable: false
        }});
        
        Object.defineProperty(navigator, 'platform', {{
            value: '{self.device_info["platform"]}',
            writable: false
        }});
        
        Object.defineProperty(navigator, 'maxTouchPoints', {{
            value: {self.device_info["hardware"]["max_touch_points"]},
            writable: false
        }});
        
        Object.defineProperty(navigator, 'hardwareConcurrency', {{
            value: {self.device_info["hardware"]["concurrency"]},
            writable: false
        }});
        
        Object.defineProperty(navigator, 'deviceMemory', {{
            value: {self.device_info["hardware"]["device_memory"]},
            writable: false
        }});
        
        // 覆盖screen对象属性
        Object.defineProperty(screen, 'width', {{
            value: {self.screen_metrics["width"]},
            writable: false
        }});
        
        Object.defineProperty(screen, 'height', {{
            value: {self.screen_metrics["height"]},
            writable: false
        }});
        
        Object.defineProperty(screen, 'availWidth', {{
            value: {self.screen_metrics["avail_width"]},
            writable: false
        }});
        
        Object.defineProperty(screen, 'availHeight', {{
            value: {self.screen_metrics["avail_height"]},
            writable: false
        }});
        
        Object.defineProperty(screen, 'pixelDepth', {{
            value: {self.screen_metrics["color_depth"]},
            writable: false
        }});
        
        Object.defineProperty(screen, 'colorDepth', {{
            value: {self.screen_metrics["color_depth"]},
            writable: false
        }});
        
        Object.defineProperty(screen, 'devicePixelRatio', {{
            value: {self.screen_metrics["pixel_ratio"]},
            writable: false
        }});
        
        // 覆盖电池API
        navigator.getBattery = () => Promise.resolve({{
            level: {self.device_info["battery"]["level"]},
            charging: {str(self.device_info["battery"]["charging"]).lower()},
            chargingTime: {self.device_info["battery"]["charging_time"]},
            dischargingTime: {self.device_info["battery"]["discharging_time"]}
        }});
        
        // 覆盖网络API
        Object.defineProperty(navigator, 'connection', {{
            value: {{
                type: '{self.device_info["network"]["type"]}',
                effectiveType: '{self.device_info["network"]["effective_type"]}',
                downlink: {self.device_info["network"]["downlink"]},
                rtt: {self.device_info["network"]["rtt"]},
                onchange: null,
                addEventListener: function() {{}},
                removeEventListener: function() {{}}
            }},
            writable: false
        }});
        
        // 覆盖地理位置API
        navigator.geolocation.getCurrentPosition = (success, error, options) => {{
            success({{
                coords: {{
                    latitude: {self.device_info["geolocation"]["lat"]},
                    longitude: {self.device_info["geolocation"]["lon"]},
                    accuracy: 50,
                    altitude: null,
                    altitudeAccuracy: null,
                    heading: null,
                    speed: null
                }},
                timestamp: {int(time.time() * 1000)}
            }});
        }};
        
        navigator.geolocation.watchPosition = navigator.geolocation.getCurrentPosition;
        
        // 覆盖时区
        Intl.DateTimeFormat().resolvedOptions().timeZone = '{self.device_info["geolocation"]["timezone"]}';
        
        // 添加设备ID到localStorage
        localStorage.setItem('device_id', '{self.device_info["device_id"]}');
        
        console.log('设备信息模拟已注入: {self.current_profile}');
        """
    
    def set_profile(self, profile_name):
        """设置设备配置文件"""
        if profile_name in self.device_profiles:
            self.current_profile = profile_name
            self.device_info = self.generate_device_info()
            self.screen_metrics = self.calculate_screen_metrics()
            self.injected_js = self.generate_injection_js()
            
            # 更新窗口大小
            self.window.resize(
                self.screen_metrics["width"], 
                self.screen_metrics["height"]
            )
            
            # 重新注入JS
            self.window.evaluate_js(self.injected_js)
            
            return True
        return False
    
    def get_device_info(self):
        """获取当前设备信息"""
        return self.device_info

def simulate_device(window, device_profile):
    """模拟设备的完整流程"""
    # 设置用户代理（必须在窗口加载前设置）
    # webview.settings['user_agent'] = device_profile["user_agent"]
    
    # 调整窗口大小
    window.resize(
        device_profile["screen"]["width"], 
        device_profile["screen"]["height"]
    )
    
    # 创建模拟器实例
    simulator = DeviceSimulator(window)
    
    # 延迟执行JS注入（等待页面加载）
    def delayed_injection():
        time.sleep(2)  # 等待页面加载
        window.evaluate_js(simulator.injected_js)
    
    Thread(target=delayed_injection).start()
    
    return simulator