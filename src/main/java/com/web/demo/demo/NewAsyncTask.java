package com.web.demo.demo;

import com.web.demo.demo.pojo.DoAdTaskPojo;
import com.web.demo.demo.pojo.IpData;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

public class NewAsyncTask {
    // 神龙ip代理服务接口地址
    private static String url = "http://api.shenlongip.com/ip?key=lr7ju4bn&protocol=1&mr=1&pattern=json&need=1101&count=10&sign=8551d46e63a71a913a023227f0786b3a";
    private static String targetUrl = "https://toup-023.cfd";
    private static final ThreadPoolExecutor executor = new ThreadPoolExecutor(
            10,               // 核心线程数
            30,                         // 最大线程数
            60L, TimeUnit.SECONDS,      // 空闲线程存活时间
            new LinkedBlockingQueue<>(1000), // 工作队列
            Executors.defaultThreadFactory(), // 线程工厂
            new ThreadPoolExecutor.AbortPolicy() // 拒绝策略
    );
    public static void main(String[] args) {
        int retryCount = 1;
        for (;true;) {
            List<IpData> ipDataList = ShenLongIPService.GetIps(url);
            if (ipDataList == null || ipDataList.size() == 0) {
                retryCount++;
                continue;
            }
            if (retryCount >= 3) {
                System.out.println("获取IP失败, 重试次数超过3次");
            }
            try {
                List<Callable<DoAdTask>> taskList = new ArrayList<>();
                for (IpData ipData : ipDataList) {
                    DoAdTaskPojo obj = new DoAdTaskPojo(ipData.getIp(),ipData.getPort(),targetUrl,"b6fn4y","g36qk8x3");
                    taskList.add(new DoAdTask(obj));
                }
                executor.invokeAll(taskList);
                System.out.println("处理Ip条数, "+ipDataList.size()+"条");
            }catch (Exception e){
               System.out.println("执行任务异常, "+e);
            }
        }
    }
}
