package com.web.demo.demo;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.ruiyun.jvppeteer.api.core.*;
import com.ruiyun.jvppeteer.api.events.BrowserEvents;
import com.ruiyun.jvppeteer.cdp.core.Puppeteer;
import com.ruiyun.jvppeteer.cdp.entities.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.function.Consumer;

/**
 * jvppeteer 滑动实现
 * 独立的jvppeteer滑动功能
 */
public class JvppeteerSwipe {

    public static void main(String[] args) {
        try {
            // 启动jvppeteer浏览器 - 模拟手机设备
            LaunchOptions.Builder options = LaunchOptions.builder();
            options.headless(false);
            options.args(Arrays.asList( // --incognito 无痕模式
                    "--no-sandbox",
                    "--disable-images",
                    "--disable-background-images",
                    "--disable-setuid-sandbox",
                    "--disable-web-security",
                    "--disable-features=VizDisplayCompositor",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--disable-extensions",
                    "--disable-plugins",
                    "--disable-default-apps",
                    "--disable-sync",
                    "--disable-translate",
                    "--hide-scrollbars",
                    "--mute-audio",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--disable-background-timer-throttling",
                    "--disable-backgrounding-occluded-windows",
                    "--disable-renderer-backgrounding",
                    "--disable-features=TranslateUI",
                    "--disable-ipc-flooding-protection",
                    // 禁用性能监控的Java参数
                    "--disable-background-networking",
                    "--disable-client-side-phishing-detection",
                    "--disable-component-extensions-with-background-pages",
                    "--disable-features=TranslateUI,BlinkGenPropertyTrees",
                    "--disable-hang-monitor",
                    "--disable-popup-blocking",
                    "--disable-prompt-on-repost",
                    "--disable-web-resources",
                    "--disable-features=PerformanceMetrics",
                    "--disable-features=PerformanceHints",
                    "--disable-features=PerformanceManager"
            ));
            Browser browser = Puppeteer.launch(options.build());
            BrowserContextOptions browserContextOptions = new BrowserContextOptions();
            browserContextOptions.setProxyServer("res.proxy-seller.com:10001");
            BrowserContext browserContext = browser.createBrowserContext(
                    browserContextOptions
            );
            List<Page> pages = browser.pages();
//            Page page = browserContext.newPage();
            Page page = browser.newPage();
            // 直接关掉新开的窗口
            browser.on(BrowserEvents.TargetCreated, (Consumer<Target>) target -> {
                if(target != null && target.page() != null) {
                    target.page().close();
                }
            });
            browser.on(BrowserEvents.TargetChanged, (Consumer<Target>) target -> {
                if(target != null && target.page() != null) {
                    if(!target.page().url().startsWith("https://toup-020.cfd")){
                        try {
                            int randSec = new Random().nextInt(3000)+ 3000;
                            Thread.sleep(randSec);
                            target.page().goBack();
                        } catch (Exception e) {
                            e.printStackTrace();
                            if(e.getMessage().contains("Session with given id not found")){
                                target.page().reload();
                            }else if(e.getMessage().contains("Index -1")){
                                target.page().close();
                            }
                        }
                    }
                }
            });
            page.authenticate(new Credentials("7f6157fcdadd1d9c","tTWX3juE"));
            page._timeoutSettings.setDefaultNavigationTimeout(3000);
            DeviceInfoManagerV2.DeviceInfo device = DeviceInfoManagerV2.getRandomDevice();
            System.out.println(new ObjectMapper().writeValueAsString(device));
            // 设置网络请求拦截
            NetworkInterceptor interceptor = new NetworkInterceptor()
                    .setBlockImages(true)
                    .setBlockMedia(true)
                    .setBlockFonts(true)
                    .setBlockAnalytics(true)
                    .setBlockAds(true)
                    .setBlockTracking(true);

            interceptor.setupInterception(page);

            //注入js
            InjectJs.injectWithDevice(page, device);

            Thread.sleep(3000);
            // 设置手机视口大小和移动端配置
            Viewport viewport = new Viewport();
            viewport.setWidth(device.getWidth());
            viewport.setHeight(device.getHeight());
            viewport.setDeviceScaleFactor(device.getDeviceScaleFactor());
            viewport.setIsMobile(true);
            viewport.setHasTouch(true);
            page.setViewport(viewport);
            // 设置移动端用户代理
            page.setUserAgent(device.getRandomUserAgent());
            // 导航到页面
            try {
                //关闭默认页
                if(!pages.isEmpty()){
                    pages.get(0).close();
                }
                System.out.println("开始导航到页面...");

                GoToOptions goToOptions = new GoToOptions();
                int perfercent = new Random().nextInt(100);
                if (perfercent < 20){
                    goToOptions.setReferer("https://www.baidu.com/");
                }else if (perfercent < 30){
                    goToOptions.setReferer("https://www.google.com/");
                }

                goToOptions.setTimeout(5000);
//                page.goTo("https://test.apiffdsfsafd25.cfd/test_device.html", goToOptions);
//                page.goTo("https://test.apiffdsfsafd25.cfd", goToOptions);
//                page.goTo("https://www.whatismybrowser.com/", goToOptions);
//                page.goTo("https://bot.sannysoft.com", goToOptions);
                page.goTo("https://toup-020.cfd", goToOptions);
                System.out.println("页面导航完成");
                injectLog(page);
            } catch (Exception e) {
                System.err.println("页面导航失败: " + e.getMessage());
            }

            ClickConfigManager.ClickConfig clickConfig = new ClickConfigManager.ClickConfig(
                    device.getWidth(), device.getHeight()
            );

            // 创建点击位置记录器
            ClickPositionRecorder recorder = new ClickPositionRecorder(device.getWidth(), device.getHeight());

//            final int count = new Random().nextInt(11) + 5; // 随机5-15次
            final int count = 2;
            System.out.println("开始执行 " + count + " 次操作...");
            for (int i = 0; i < count; i++) {
                // 无法加载网页 关闭
                if(page.url().contains("chrome-")){
                    System.out.println("####### 无法加载网页: " + page.url());
                    break;
                }
                System.out.println("=== 第 " + (i + 1) + " 次操作 ===");
                System.out.println("当前URL: " + page.url());

                //随机滑动次数
                final int scrollCount = new Random().nextInt(1) + 3; // 随机1-3次
                for (int j = 0; j < scrollCount; j++) {
                    // 执行滑动
                    boolean succ = jvppeteerSwipeUp(page);
                    if(!succ){ //失败, 不在进行随机滑动
                        break;
                    }
                    Thread.sleep(300);
                }

                // 执行点击并记录位置
                boolean succ = performClickOperationsWithRecording(page, clickConfig, recorder);
                if(!succ){
                    break;
                }
                final int delay = new Random().nextInt(1200) + 2000; // 随机等待
                Thread.sleep(delay);
            }
            // 打印统计信息
//            recorder.printStatistics();

            // 打印网络拦截统计
//            interceptor.printStatistics();

            //
            // 绘制点击位置图片
//            recorder.drawClickPositions("click_positions_" + System.currentTimeMillis() + ".png");

            // 截图
//            page.screenshot("jvppeteer_example.png");
            System.out.println("截图已保存: jvppeteer_example.png");
            browser.close();
        } catch (Exception e) {
            System.err.println("jvppeteer滑动失败: " + e.getMessage());
            e.printStackTrace();
        }
    }


    /**
     * jvppeteer 上滑操作
     */
    public static boolean jvppeteerSwipeUp(Page page)  {
        try {
            int width = (int) page.evaluate("window.innerWidth");
            int height = (int) page.evaluate("window.innerHeight");

            int startX = width / 2;
            int startY = (int) (height * 0.8); // 从页面80%位置开始
            int endX = width / 2;
            int endY = (int) (height * 0.2);   // 滑动到页面20%位置

            System.out.println("jvppeteer滑动: 从(" + startX + "," + startY + ") 到(" + endX + "," + endY + ")");

            // 使用jvppeteer的触摸滑动 - touchStart/touchMove/touchEnd
            System.out.println("开始触摸滑动: 从(" + startX + "," + startY + ") 到(" + endX + "," + endY + ")");

            // 触摸开始
            ObjectMapper mapper = new ObjectMapper();
            ObjectNode touchConfig = mapper.createObjectNode();
            System.out.println("执行 touchStart 在位置: (" + startX + ", " + startY + ")");
            page.touchscreen().touchStart((double) startX, (double) startY, touchConfig);
            Thread.sleep(50);

            // 模拟触摸移动过程
            int steps = 15;
            for (int i = 1; i <= steps; i++) {
                int currentX = startX + (endX - startX) * i / steps;
                int currentY = startY + (endY - startY) * i / steps;
                System.out.println("执行 touchMove 步骤 " + i + "/" + steps + " 到位置: (" + currentX + ", " + currentY + ")");
                page.touchscreen().touchMove((double) currentX, (double) currentY);
                Thread.sleep(30);
            }

            // 触摸结束
            System.out.println("执行 touchEnd 在位置: (" + endX + ", " + endY + ")");
            page.touchscreen().touchEnd();
            Thread.sleep(100);

        } catch (Exception e) {
            System.err.println("jvppeteer上滑失败: " + e.getMessage());
            return false;
        }
        return true;
    }

    /**
     * 执行点击操作（保留原方法，用于一次性点击）
     */
    private static void performClickOperations(Page page, ClickConfigManager.ClickConfig clickConfig) {
        try {
            System.out.println("开始执行点击操作...");

            // 执行多次随机概率点击
            for (int i = 0; i < 10; i++) {
                ClickConfigManager.ClickPosition randomClick = clickConfig.getRandomClickPosition();
                System.out.println("随机点击" + (i + 1) + ": " + randomClick);
                performTouchClick(page, randomClick.x, randomClick.y);
                Thread.sleep(500);
            }

            System.out.println("点击操作完成！");

        } catch (Exception e) {
            System.err.println("点击操作失败: " + e.getMessage());
            e.printStackTrace();
        }
    }

    /**
     * 执行点击操作并记录位置
     */
    public static boolean performClickOperationsWithRecording(Page page, ClickConfigManager.ClickConfig clickConfig, ClickPositionRecorder recorder) {
        try {
            System.out.println("开始执行点击操作...");

            // 执行多次随机概率点击
            for (int i = 0; i < 5; i++) { // 每次操作执行5次点击
                ClickConfigManager.ClickPosition randomClick = clickConfig.getRandomClickPosition();
                System.out.println("随机点击" + (i + 1) + ": " + randomClick);

                // 记录点击位置
//                recorder.recordClick(randomClick, "click_" + (i + 1));

                // 执行点击
                boolean succ = performTouchClick(page, randomClick.x, randomClick.y);
                if(!succ){ break;}
                Thread.sleep(200);
            }

            System.out.println("点击操作完成！");

        } catch (Exception e) {
            System.err.println("点击操作失败: " + e.getMessage());
            return false;
        }
        return true;
    }

    /**
     * 执行触摸点击
     */
    private static boolean performTouchClick(Page page, int x, int y) {
        try {
            ObjectMapper mapper = new ObjectMapper();
            ObjectNode touchConfig = mapper.createObjectNode();
            touchConfig.put("x", x);
            touchConfig.put("y", y);

            // 使用touchscreen进行点击
            page.touchscreen().touchStart((double) x, (double) y, touchConfig);
            Thread.sleep(50); // 短暂延迟
            page.touchscreen().touchEnd();

            System.out.println("  执行点击: (" + x + ", " + y + ")");

        } catch (Exception e) {
            System.err.println("触摸点击失败: " + e.getMessage());
            return false;
        }
        return true;
    }

    static void injectLog(Page page) throws JsonProcessingException {

        // 添加控制台日志监听 - 使用jvppeteer的方式
        page.evaluate("function() { " +
                "window.consoleLogs = []; " +
                "var originalLog = console.log; " +
                "var originalError = console.error; " +
                "var originalWarn = console.warn; " +
                "console.log = function() { " +
                "var args = Array.prototype.slice.call(arguments); " +
                "originalLog.apply(console, args); " +
                "window.consoleLogs.push({ type: 'log', message: args.join(' '), time: Date.now() }); " +
                "}; " +
                "console.error = function() { " +
                "var args = Array.prototype.slice.call(arguments); " +
                "originalError.apply(console, args); " +
                "window.consoleLogs.push({ type: 'error', message: args.join(' '), time: Date.now() }); " +
                "}; " +
                "console.warn = function() { " +
                "var args = Array.prototype.slice.call(arguments); " +
                "originalWarn.apply(console, args); " +
                "window.consoleLogs.push({ type: 'warn', message: args.join(' '), time: Date.now() }); " +
                "}; " +
                "}");

        // 添加移动端触摸事件监听和调试信息
        page.evaluate("function() { " +
                "console.log('=== 页面调试信息 ==='); " +
                "console.log('页面URL:', window.location.href); " +
                "console.log('页面标题:', document.title); " +
                "console.log('视口大小:', window.innerWidth, 'x', window.innerHeight); " +
                "console.log('用户代理:', navigator.userAgent); " +
                "console.log('触摸支持:', 'ontouchstart' in window); " +
                "console.log('页面加载完成，开始监听触摸事件'); " +
                "document.addEventListener('touchstart', function(e) { " +
                "console.log('Touch Start - 触摸点数量:', e.touches.length, '位置:', e.touches[0].clientX, e.touches[0].clientY); " +
                "console.log('Touch Start - 时间戳:', e.timeStamp); " +
                "}); " +
                "document.addEventListener('touchmove', function(e) { " +
                "console.log('Touch Move - 触摸点数量:', e.touches.length, '位置:', e.touches[0].clientX, e.touches[0].clientY); " +
                "console.log('Touch Move - 时间戳:', e.timeStamp); " +
                "}); " +
                "document.addEventListener('touchend', function(e) { " +
                "console.log('Touch End - 触摸点数量:', e.changedTouches.length); " +
                "console.log('Touch End - 时间戳:', e.timeStamp); " +
                "}); " +
                "console.log('触摸事件监听器已添加'); " +
                "console.log('=== 调试信息结束 ==='); " +
                "}");
    }

}
