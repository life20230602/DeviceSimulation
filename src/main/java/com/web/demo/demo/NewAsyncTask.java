package com.web.demo.demo;

import com.web.demo.demo.pojo.DoAdTaskPojo;
import com.web.demo.demo.pojo.IpData;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.*;

public class NewAsyncTask {
    // 神龙ip代理服务接口地址
    private static String url = "http://api.shenlongip.com/ip?key=lr7ju4bn&protocol=1&mr=1&pattern=json&need=1101&count=5&sign=8551d46e63a71a913a023227f0786b3a";
    private static String targetUrl = "https://toup-023.cfd";
    private static final ThreadPoolExecutor executor = new ThreadPoolExecutor(
            10,               // 核心线程数
            20,                         // 最大线程数
            10L, TimeUnit.MINUTES,      // 空闲线程存活时间
            new LinkedBlockingQueue<>(10000), // 工作队列
            Executors.defaultThreadFactory(), // 线程工厂
            new ThreadPoolExecutor.AbortPolicy() // 拒绝策略
    );
    public static void main(String[] args) {
        DeviceInfoManagerV2.DeviceInfo device = DeviceInfoManagerV2.getRandomDevice();
        int retryCount = 1;
        for (;true;) {
            List<IpData> ipDataList = ShenLongIPService.GetIps(url);
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
                System.out.println("已完成: "+ executor.getCompletedTaskCount()+"-,任务总数: "+ executor.getTaskCount());
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
