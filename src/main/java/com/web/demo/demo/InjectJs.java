package com.web.demo.demo;

import com.ruiyun.jvppeteer.api.core.Page;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class InjectJs{
    // 根据设备
    public static void injectWithDevice(Page page,DeviceInfoManagerV2.DeviceInfo deviceInfo)  {
         try {
             // 语言修改
             page.evaluateOnNewDocument("() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN','en-US','en'] }); }");

             // 修改型号
             if( deviceInfo.getBrand().equals("Apple")){
                 page.evaluateOnNewDocument("() =>{ Object.defineProperty(navigator, 'platform', { get: () => 'iPhone' }); }");
             }else{
                 page.evaluateOnNewDocument("() =>{ Object.defineProperty(navigator, 'platform', { get: () => 'Android' }); }");
             }
         }catch (Exception e){
             e.printStackTrace();
         }
    }
}
