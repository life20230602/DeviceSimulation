package com.web.demo.demo;

import com.ruiyun.jvppeteer.api.core.Page;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.Random;

public class InjectJs{
    // 根据设备
    public static void injectWithDevice(Page page, DeviceInfoManagerV2.DeviceInfo deviceInfo)  {
         try {
             // 语言修改
             page.evaluateOnNewDocument("() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN','en-US','en'] }); }");
             //z注入标记
             page.evaluateOnNewDocument("()=>{window.fix = {};}");
             // 修改型号
             if( deviceInfo.getBrand().equals("Apple")){
                 page.evaluateOnNewDocument("() =>{ Object.defineProperty(navigator, 'platform', { get: () => 'iPhone' }); }");
             }else{
                 page.evaluateOnNewDocument("() =>{ Object.defineProperty(navigator, 'platform', { get: () => 'Android' }); }");
             }

             // WebGL 注入 - 模拟真实的图形硬件信息
             injectWebGLInfo(page, deviceInfo);

             // 修改屏幕宽高
             int randSubHeight =  new Random().nextInt(139) + 20;
             int deviceHeight = deviceInfo.getHeight() - randSubHeight;
             page.evaluateOnNewDocument("() =>{ Object.defineProperty(window, 'innerHeight', { value: "+deviceHeight+",writable: true }); }");
             
         }catch (Exception e){
             e.printStackTrace();
         }
    }

    /**
     * 注入 WebGL 信息
     */
    private static void injectWebGLInfo(Page page, DeviceInfoManagerV2.DeviceInfo deviceInfo) {
        try {
            // 获取 WebGL 渲染器信息
            String webglRenderer = getWebGLRenderer(deviceInfo);
            String webglVendor = getWebGLVendor(deviceInfo);
            String webglVersion = getWebGLVersion(deviceInfo);
            
            System.out.println("注入 WebGL 信息 - 渲染器: " + webglRenderer + ", 供应商: " + webglVendor + ", 版本: " + webglVersion);
            
            // 使用 Proxy 方案注入 WebGL 信息
            String webglScript = 
                "() => { " +
                "  const utils = { " +
                "    cache: { " +
                "      Reflect: { " +
                "        apply: (target, ctx, args) => target.apply(ctx, args) " +
                "      } " +
                "    }, " +
                "    replaceWithProxy: (obj, propName, handler) => { " +
                "      const original = obj[propName]; " +
                "      obj[propName] = new Proxy(original, handler); " +
                "    } " +
                "  }; " +
                "  " +
                "  const opts = { " +
                "    vendor: '" + webglVendor + "', " +
                "    renderer: '" + webglRenderer + "', " +
                "    version: '" + webglVersion + "' " +
                "  }; " +
                "  " +
                "  const getParameterProxyHandler = { " +
                "    apply: function(target, ctx, args) { " +
                "      const param = (args || [])[0]; " +
                "      const result = utils.cache.Reflect.apply(target, ctx, args); " +
                "      " +
                "      if (param === 37445) { " +
                "        return opts.vendor || 'Intel Inc.'; " +
                "      } " +
                "      if (param === 37446) { " +
                "        return opts.renderer || 'Intel Iris OpenGL Engine'; " +
                "      } " +
                "      " +
                "      return result; " +
                "    } " +
                "  }; " +
                "  " +
                "  const addProxy = (obj, propName) => { " +
                "    utils.replaceWithProxy(obj, propName, getParameterProxyHandler); " +
                "  }; " +
                "  " +
                "  addProxy(WebGLRenderingContext.prototype, 'getParameter'); " +
                "  addProxy(WebGL2RenderingContext.prototype, 'getParameter'); " +
                "} ";
            
            page.evaluateOnNewDocument(webglScript);
            
        } catch (Exception e) {
            System.err.println("WebGL 注入失败: " + e.getMessage());
            e.printStackTrace();
        }
    }

    /**
     * 根据设备信息获取 WebGL 渲染器
     */
    private static String getWebGLRenderer(DeviceInfoManagerV2.DeviceInfo deviceInfo) {
        if (deviceInfo.getBrand().equals("Apple")) {
            // iOS 设备使用 Apple GPU
            return "Apple GPU";
        } else if (deviceInfo.getBrand().equals("Huawei") || deviceInfo.getBrand().equals("Honor")) {
            // 华为/荣耀设备
            return "Mali-G78 MP14";
        } else if (deviceInfo.getBrand().equals("Xiaomi")) {
            // 小米设备
            return "Adreno (TM) 650";
        } else if (deviceInfo.getBrand().equals("Vivo")) {
            // Vivo 设备
            return "Mali-G76 MP16";
        } else if (deviceInfo.getBrand().equals("Oppo")) {
            // OPPO 设备
            return "Adreno (TM) 640";
        } else if (deviceInfo.getBrand().equals("Samsung")) {
            // 三星设备
            return "Mali-G78 MP14";
        } else {
            // 其他 Android 设备
            return "Mali-G76 MP16";
        }
    }

    /**
     * 根据设备信息获取 WebGL 供应商
     */
    private static String getWebGLVendor(DeviceInfoManagerV2.DeviceInfo deviceInfo) {
        if (deviceInfo.getBrand().equals("Apple")) {
            return "Apple Inc.";
        } else {
            return "ARM";
        }
    }

    /**
     * 根据设备信息获取 WebGL 版本
     */
    private static String getWebGLVersion(DeviceInfoManagerV2.DeviceInfo deviceInfo) {
        if (deviceInfo.getBrand().equals("Apple")) {
            return "WebGL 1.0 (OpenGL ES 2.0 Metal - 86.104.1)";
        } else {
            return "WebGL 1.0 (OpenGL ES 2.0 Chromium)";
        }
    }

}
