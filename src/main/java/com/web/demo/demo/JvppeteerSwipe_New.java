package com.web.demo.demo;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.ruiyun.jvppeteer.api.core.Browser;
import com.ruiyun.jvppeteer.api.core.BrowserContext;
import com.ruiyun.jvppeteer.api.core.Page;
import com.ruiyun.jvppeteer.api.core.Target;
import com.ruiyun.jvppeteer.api.events.BrowserEvents;
import com.ruiyun.jvppeteer.cdp.core.Puppeteer;
import com.ruiyun.jvppeteer.cdp.entities.*;
import com.web.demo.demo.pojo.DoAdTaskPojo;
import com.web.demo.demo.pojo.IpData;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.function.Consumer;

/**
 * jvppeteer 滑动实现
 * 独立的jvppeteer滑动功能
 */
public class JvppeteerSwipe_New {

    public static void main(String[] args) {
        //初始化先
        DeviceInfoManagerV2.DeviceInfo device = DeviceInfoManagerV2.getRandomDevice();

        String targetUrl = "https://toup-023.cfd";
        DoAdTaskPojo obj = new DoAdTaskPojo(null,0,targetUrl,"b6fn4y","g36qk8x3");
        try {
            long start = System.currentTimeMillis();
            List<Callable<DoAdTask>> taskList = new ArrayList<>();
            for(int i=0;i<10;i++){
                taskList.add(new DoAdTask(obj));
            }
            ExecutorService executorService = Executors.newFixedThreadPool(10);
            executorService.invokeAll(taskList);
            long end = System.currentTimeMillis();
            System.out.println((end-start) +" 毫秒");
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
