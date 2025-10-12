package com.web.demo.demo;

import com.web.demo.demo.pojo.DoAdTaskPojo;
import com.web.demo.demo.pojo.IpData;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import java.util.Random;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class NewAsyncTask {
    private static final AtomicInteger atomicInteger = new AtomicInteger(0);
    public static void incrementSuccessCount(){
        atomicInteger.incrementAndGet();
    }
    private static final ThreadPoolExecutor executor = new ThreadPoolExecutor(
            10,               // 核心线程数
            20,                         // 最大线程数
            10L, TimeUnit.MINUTES,      // 空闲线程存活时间
            new LinkedBlockingQueue<>(10000), // 工作队列
            Executors.defaultThreadFactory(), // 线程工厂
            new ThreadPoolExecutor.AbortPolicy() // 拒绝策略
    );
    public static void main(String[] args) {
        Properties prop = new Properties();
        String ipApiUrl = "";
        String targetUrl = "";
        try {
            // 加载properties文件，这里使用ClassLoader来获取资源流
            InputStream input = NewAsyncTask.class.getClassLoader().getResourceAsStream("application.properties");
            if (input == null) {
                System.out.println("Sorry, unable to find application.properties");
                return;
            }

            // 加载属性值
            prop.load(input);
            // 获取属性值
             ipApiUrl = prop.getProperty("ipApiUrl");
             targetUrl = prop.getProperty("targetUrl");
        } catch (IOException e) {
            e.printStackTrace();
        }
        DeviceInfoManagerV2.DeviceInfo device = DeviceInfoManagerV2.getRandomDevice();
        int retryCount = 1;
        for (;true;) {
            List<IpData> ipDataList = ShenLongIPService.GetIps(ipApiUrl);
            if (ipDataList == null || ipDataList.size() == 0) {
                retryCount++;
                continue;
            }
            if (retryCount >= 3) {
                System.out.println("获取IP失败, 重试次数超过3次");
                break;
            }
            try {
                for (IpData ipData : ipDataList) {
                    DoAdTaskPojo obj = new DoAdTaskPojo(ipData.getIp(),ipData.getPort(),targetUrl,"b6fn4y","g36qk8x3");
                    executor.submit(new DoAdTask(obj));
                }
                int delay =  new Random().nextInt(20) + 10;
                Thread.sleep(delay*1000); // 随机加5个
                System.out.println("实际已完成: "+atomicInteger.get()+",任务完成: "+ executor.getCompletedTaskCount()+"-,任务总数: "+ executor.getTaskCount());
            }catch (Exception e){
               System.out.println("执行任务异常, "+e);
            }
        }
        try {
            executor.shutdown();
        }catch (Exception e){

        }
    }
}
