package com.web.demo.demo;

import java.io.*;
import java.util.*;

/**
 * 简单的IP解析器
 * 解析ip.txt文件中的IP地址和端口信息
 */
public class IpParser {
    
    private List<String> ipList;
    
    public IpParser() {
        this.ipList = new ArrayList<>();
    }
    
    /**
     * 解析IP文件
     */
    public void parseIpFile(String filePath) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            
            System.out.println("开始解析IP文件: " + filePath);
            
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (!line.isEmpty() && line.contains(":")) {
                    ipList.add(line);
                }
            }
            
            System.out.println("IP文件解析完成，共解析 " + ipList.size() + " 个IP地址");
            
        } catch (IOException e) {
            System.err.println("读取IP文件失败: " + e.getMessage());
        }
    }
    
    /**
     * 获取所有IP
     */
    public List<String> getAllIps() {
        return new ArrayList<>(ipList);
    }
    
    /**
     * 提取一个IP（提取后丢弃）
     */
    public String extractIp() {
        if (ipList.isEmpty()) {
            return null;
        }
        return ipList.remove(0); // 提取第一个并删除
    }
    
    /**
     * 获取剩余IP数量
     */
    public int getRemainingCount() {
        return ipList.size();
    }
    
    /**
     * 打印前10个IP
     */
    public void printFirst10() {
        System.out.println("\n前10个IP地址:");
        for (int i = 0; i < Math.min(10, ipList.size()); i++) {
            System.out.println((i + 1) + ". " + ipList.get(i));
        }
    }
    
    /**
     * 测试方法
     */
    public static void main(String[] args) {
        IpParser parser = new IpParser();
        parser.parseIpFile("ip.txt");
        parser.printFirst10();
        
        // 测试提取模式
        System.out.println("\n=== 测试提取模式 ===");
        System.out.println("初始IP数量: " + parser.getRemainingCount());
        
        for (int i = 0; i < 5; i++) {
            String ip = parser.extractIp();
            if (ip != null) {
                System.out.println("提取第" + (i + 1) + "个IP: " + ip);
                System.out.println("剩余IP数量: " + parser.getRemainingCount());
            } else {
                System.out.println("没有更多IP可提取");
                break;
            }
        }
    }
}
