package com.web.demo.demo;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.ruiyun.jvppeteer.api.core.Browser;
import com.ruiyun.jvppeteer.api.core.BrowserContext;
import com.ruiyun.jvppeteer.api.core.Page;
import com.ruiyun.jvppeteer.api.core.Target;
import com.ruiyun.jvppeteer.api.events.BrowserEvents;
import com.ruiyun.jvppeteer.api.events.PageEvents;
import com.ruiyun.jvppeteer.cdp.core.Puppeteer;
import com.ruiyun.jvppeteer.cdp.entities.*;
import com.web.demo.demo.pojo.DoAdTaskPojo;
import com.web.demo.demo.pojo.IpData;

import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.concurrent.Callable;
import java.util.function.Consumer;

public class DoAdTask implements Callable {
    private static int TIMEOUT = 10000;
    private DoAdTaskPojo taskPojo;
    private String name;
    public DoAdTask(DoAdTaskPojo taskPojo) {
        this.taskPojo = taskPojo;
        this.name = "task-"+taskPojo.getIp();
    }
    public Object call() throws Exception {
        // 获取开始时间
        long startTime = System.currentTimeMillis();

        // 启动jvppeteer浏览器 - 模拟手机设备
        LaunchOptions.Builder options = LaunchOptions.builder();
        options.headless(true);
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
        browserContextOptions.setProxyServer(taskPojo.getIp()+":"+taskPojo.getPort());
        BrowserContext browserContext = browser.createBrowserContext(
                browserContextOptions
        );
        List<Page> pages = browser.pages();
        Page page = null;
        if(taskPojo.getIp() == null){
            page = browser.newPage();
        }else{
            page = browserContext.newPage();
        }
        page.authenticate(new Credentials(taskPojo.getProxyUserName(),taskPojo.getProxyPassword()));
        // 直接关掉新开的窗口
        browser.on(BrowserEvents.TargetCreated, (Consumer<Target>) target -> {
            if (target != null && target.page() != null) {
                target.page().close();
            }
        });
        browser.on(BrowserEvents.TargetChanged, (Consumer<Target>) target -> {
            if (target != null && target.page() != null) {
                if (!target.page().url().startsWith(taskPojo.getUrl())) {
                    try {
                        System.out.println("===target.page().url()===="+target.page().url());
                        target.page().goBack();
                    } catch (Exception e) {
                        try {
                            target.page().goTo(taskPojo.getUrl());
                        }catch (Exception ex){
                            System.out.println("跳转其他链接失败: ex "+ex);
                        }
                        System.out.println("跳转其他链接失败: "+e);
                    }
                }
            }
        });
        page._timeoutSettings.setDefaultNavigationTimeout(TIMEOUT);
        DeviceInfoManagerV2.DeviceInfo device = DeviceInfoManagerV2.getRandomDevice();
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
            if (!pages.isEmpty()) {
                pages.get(0).close();
            }
            System.out.println("开始导航到页面...");

            GoToOptions goToOptions = new GoToOptions();
            int percent = new Random().nextInt(100);
            if (percent < 20) {
                goToOptions.setReferer("https://yandex.cn/");
            } else if (percent < 30) {
                goToOptions.setReferer("https://www.google.com/");
            }
            goToOptions.setTimeout(TIMEOUT);
            page.goTo(taskPojo.getUrl(), goToOptions);
            long endTime = System.currentTimeMillis();
            System.out.println("页面导航完成,"+ (endTime-startTime)+" 毫秒");
//            injectLog(page);
        } catch (Exception e) {
            long endTime = System.currentTimeMillis();
            System.err.println( (endTime-startTime)+" 毫秒 , "+"页面导航失败: " + e.getMessage());
            browser.close();
            return null;
        }
        try {
            ClickConfigManager.ClickConfig clickConfig = new ClickConfigManager.ClickConfig(
                    device.getWidth(), device.getHeight()
            );
            // 创建点击位置记录器
            ClickPositionRecorder recorder = new ClickPositionRecorder(device.getWidth(), device.getHeight());

            final int count = new Random().nextInt(7) + 2; // 随机5-15次
            System.out.println("开始执行 " + count + " 次操作...");

            for (int i = 0; i < count; i++) {
                // 无法加载网页 关闭
                if(page.url().contains("chrome-error")){
                    break;
                }
                System.out.println("=== 第 " + (i + 1) + " 次操作 === url: "+page.url());
                final int delay = new Random().nextInt(2000) + 500; // 随机等待
                Thread.sleep(delay);
                //随机滑动次数
                final int scrollCount = new Random().nextInt(3) ; // 随机0-3次次
                for (int j = 0; j < scrollCount; j++) {
                    // 执行滑动
                    try {
                        jvppeteerSwipeUp(page);
                    }catch (Exception e) {
                        // 执行滑动异常,
                        continue;
                    }
                    int swipeUpDelay = new Random().nextInt(300) + 100;
                    Thread.sleep(swipeUpDelay);
                }
                // 执行点击并记录位置
               try {
                   performClickOperationsWithRecording(page, clickConfig, recorder);
                   Thread.sleep(delay);
               }catch (Exception e) {
                   // 执行点击异常
                   break;
               }
            }
        } finally {
            long endTime = System.currentTimeMillis();
            System.err.println( "完成耗时: "+(endTime-startTime)+" 毫秒");
            page.close();
            browser.close();
        }
        return null;
    }


    /**
     * jvppeteer 上滑操作
     */
    public static void jvppeteerSwipeUp(Page page) throws JsonProcessingException, InterruptedException {
        try {
            int width = (int) page.evaluate("window.innerWidth");
            int height = (int) page.evaluate("window.innerHeight");

            int startX = width / 2;
            int startY = (int) (height * 0.8); // 从页面80%位置开始
            int endX = width / 2;
            int endY = (int) (height * 0.2);   // 滑动到页面20%位置

//            System.out.println("jvppeteer滑动: 从(" + startX + "," + startY + ") 到(" + endX + "," + endY + ")");

            // 使用jvppeteer的触摸滑动 - touchStart/touchMove/touchEnd
//            System.out.println("开始触摸滑动: 从(" + startX + "," + startY + ") 到(" + endX + "," + endY + ")");

            // 触摸开始
            ObjectMapper mapper = new ObjectMapper();
            ObjectNode touchConfig = mapper.createObjectNode();
//            System.out.println("执行 touchStart 在位置: (" + startX + ", " + startY + ")");
            page.touchscreen().touchStart((double) startX, (double) startY, touchConfig);
            Thread.sleep(new Random().nextInt(40) + 30);

            // 模拟触摸移动过程
            int steps = new Random().nextInt(10)+5;
            for (int i = 1; i <= steps; i++) {
                int currentX = startX + (endX - startX) * i / steps;
                int currentY = startY + (endY - startY) * i / steps;
//                System.out.println("执行 touchMove 步骤 " + i + "/" + steps + " 到位置: (" + currentX + ", " + currentY + ")");
                page.touchscreen().touchMove((double) currentX, (double) currentY);
                Thread.sleep(new Random().nextInt(30)+20);
            }

            // 触摸结束
//            System.out.println("执行 touchEnd 在位置: (" + endX + ", " + endY + ")");
            page.touchscreen().touchEnd();
            Thread.sleep(100);

        } catch (Exception e) {
            System.err.println("jvppeteer上滑失败: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }
    /**
     * 执行点击操作并记录位置
     */
    public static void performClickOperationsWithRecording(Page page, ClickConfigManager.ClickConfig clickConfig, ClickPositionRecorder recorder) throws InterruptedException {
        try {
//            System.out.println("开始执行点击操作...");

            // 执行多次随机概率点击
            int count = new Random().nextInt(5);
            for (int i = 0; i < count; i++) {
                ClickConfigManager.ClickPosition randomClick = clickConfig.getRandomClickPosition();
//                System.out.println("随机点击" + (i + 1) + ": " + randomClick);

                // 记录点击位置
//                recorder.recordClick(randomClick, "click_" + (i + 1));

                // 执行点击
                boolean succ = performTouchClick(page, randomClick.x, randomClick.y);
                if (!succ) {
                    break;
                }
                Thread.sleep(200);
            }

            System.out.println("随机点击"+count+"次,操作完成！");

        } catch (Exception e) {
            System.err.println("点击操作失败: " + e.getMessage());
            throw new RuntimeException(e);
        }
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
            Thread.sleep(new Random().nextInt(40)+20); // 短暂延迟
            page.touchscreen().touchEnd();

            System.out.println("  执行点击: (" + x + ", " + y + ")");

        } catch (Exception e) {
            System.err.println("触摸点击失败: " + e.getMessage());
            return false;
        }
        return true;
    }

}
