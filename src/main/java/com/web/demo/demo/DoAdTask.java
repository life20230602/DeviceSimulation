package com.web.demo.demo;

import com.ruiyun.jvppeteer.api.core.Browser;
import com.ruiyun.jvppeteer.api.core.BrowserContext;
import com.ruiyun.jvppeteer.api.core.Page;
import com.ruiyun.jvppeteer.api.core.Target;
import com.ruiyun.jvppeteer.api.events.BrowserEvents;
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
    private DoAdTaskPojo taskPojo;
    public DoAdTask(DoAdTaskPojo taskPojo) {
        this.taskPojo = taskPojo;
    }
    public Object call() throws Exception {
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
        Page page = browserContext.newPage();
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
                        GoToOptions goToOptions = new GoToOptions();
                        goToOptions.setReferer(target.page().url());
                        target.page().goTo(taskPojo.getUrl(),goToOptions);
                    } catch (Exception e) {
                        System.out.println("跳转其他链接失败: "+e);
                    }
                }
            }
        });
        page._timeoutSettings.setDefaultNavigationTimeout(5000);
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

            goToOptions.setTimeout(5000);
            page.goTo(taskPojo.getUrl(), goToOptions);
            System.out.println("页面导航完成");
//            injectLog(page);
        } catch (Exception e) {
            System.err.println("页面导航失败: " + e.getMessage());
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
                System.out.println("=== 第 " + (i + 1) + " 次操作 ===");
                System.out.println("当前URL: " + page.url());
                if (!page.url().contains(taskPojo.getUrl())) {
                    GoToOptions goToOptions = new GoToOptions();
                    goToOptions.setReferer(page.url());
                    page.goTo(taskPojo.getUrl(),goToOptions);
                    System.out.println("当前URL2: " + page.url());
                }
                final int delay = new Random().nextInt(2000) + 500; // 随机等待
                Thread.sleep(delay);
                //随机滑动次数
                final int scrollCount = new Random().nextInt(1) + 3; // 随机1-3次
                for (int j = 0; j < scrollCount; j++) {
                    // 执行滑动
                    JvppeteerSwipe.jvppeteerSwipeUp(page);
                    Thread.sleep(300);
                }

                // 执行点击并记录位置
                JvppeteerSwipe.performClickOperationsWithRecording(page, clickConfig, recorder);
                Thread.sleep(delay);
            }
        } finally {
            browser.close();
            page.close();
        }
        return null;
    }

}
