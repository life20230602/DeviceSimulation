package com.web.demo.demo;

import com.google.gson.Gson;
import com.web.demo.demo.pojo.IpData;
import com.web.demo.demo.pojo.IpDataReq;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;

public class ShenLongIPService {

    public static void main(String[] args) {
        IpData ipData = GetIp();
        System.out.println("ipData: " + ipData);
    }
    public static IpData GetIp() {
        try {
            String url = "http://api.shenlongip.com/ip?key=lr7ju4bn&protocol=1&mr=1&pattern=json&need=1101&count=1&sign=8551d46e63a71a913a023227f0786b3a";

            // 创建 URL 对象
            URL obj = new URL(url);
            HttpURLConnection con = (HttpURLConnection) obj.openConnection();

            // 设置请求方式为 GET
            con.setRequestMethod("GET");

            // 设置请求头部，模拟浏览器行为
            con.setRequestProperty("User-Agent", "Mozilla/5.0");

            // 获取响应码
            int responseCode = con.getResponseCode();
//            System.out.println("Response Code: " + responseCode);

            // 读取响应内容
            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            String inputLine;
            StringBuffer response = new StringBuffer();

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();

            // 输出响应结果
            System.out.println("Response JSON: " + response.toString());
            Gson gson = new Gson();
            IpDataReq req =  gson.fromJson(response.toString(), IpDataReq.class);
            if(req == null || req.getData().isEmpty()){
                return null;
            }
            return req.getData().get(0);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }


}