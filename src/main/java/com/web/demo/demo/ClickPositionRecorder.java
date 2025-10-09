package com.web.demo.demo;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * 点击位置记录类
 * 记录点击位置并绘制到图片上
 */
public class ClickPositionRecorder {
    
    private List<ClickRecord> clickRecords;
    private int deviceWidth;
    private int deviceHeight;
    
    public ClickPositionRecorder(int deviceWidth, int deviceHeight) {
        this.deviceWidth = deviceWidth;
        this.deviceHeight = deviceHeight;
        this.clickRecords = new ArrayList<>();
    }
    
    /**
     * 记录一次点击
     */
    public void recordClick(int x, int y, String action, long timestamp) {
        ClickRecord record = new ClickRecord(x, y, action, timestamp);
        clickRecords.add(record);
        System.out.println("记录点击: " + record);
    }
    
    /**
     * 记录一次点击（使用ClickPosition）
     */
    public void recordClick(ClickConfigManager.ClickPosition clickPosition, String action) {
        recordClick(clickPosition.x, clickPosition.y, action, System.currentTimeMillis());
    }
    
    /**
     * 获取点击记录数量
     */
    public int getClickCount() {
        return clickRecords.size();
    }
    
    /**
     * 清空记录
     */
    public void clearRecords() {
        clickRecords.clear();
    }
    
    /**
     * 绘制点击位置到图片
     */
    public void drawClickPositions(String outputPath) {
        try {
            // 创建图片
            BufferedImage image = new BufferedImage(deviceWidth, deviceHeight, BufferedImage.TYPE_INT_RGB);
            Graphics2D g2d = image.createGraphics();
            
            // 设置抗锯齿
            g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            g2d.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
            
            // 绘制背景
            g2d.setColor(Color.WHITE);
            g2d.fillRect(0, 0, deviceWidth, deviceHeight);
            
            // 绘制网格（12x6）
            drawGrid(g2d);
            
            // 绘制点击位置
            drawClickPoints(g2d);
            
            // 绘制统计信息
            drawStatistics(g2d);
            
            g2d.dispose();
            
            // 保存图片
            ImageIO.write(image, "PNG", new File(outputPath));
            System.out.println("点击位置图片已保存: " + outputPath);
            
        } catch (IOException e) {
            System.err.println("保存点击位置图片失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * 绘制网格
     */
    private void drawGrid(Graphics2D g2d) {
        g2d.setColor(Color.LIGHT_GRAY);
        g2d.setStroke(new BasicStroke(1));
        
        int gridCols = 6;
        int gridRows = 12;
        int cellWidth = deviceWidth / gridCols;
        int cellHeight = deviceHeight / gridRows;
        
        // 绘制垂直线
        for (int i = 0; i <= gridCols; i++) {
            int x = i * cellWidth;
            g2d.drawLine(x, 0, x, deviceHeight);
        }
        
        // 绘制水平线
        for (int i = 0; i <= gridRows; i++) {
            int y = i * cellHeight;
            g2d.drawLine(0, y, deviceWidth, y);
        }
        
        // 绘制网格标签
        g2d.setColor(Color.BLACK);
        g2d.setFont(new Font("Arial", Font.PLAIN, 12));
        for (int row = 0; row < gridRows; row++) {
            for (int col = 0; col < gridCols; col++) {
                String label = "[" + row + "," + col + "]";
                int x = col * cellWidth + 5;
                int y = (row + 1) * cellHeight - 5;
                g2d.drawString(label, x, y);
            }
        }
    }
    
    /**
     * 绘制点击点
     */
    private void drawClickPoints(Graphics2D g2d) {
        if (clickRecords.isEmpty()) {
            return;
        }
        
        // 按时间顺序绘制，越晚的点击点越大
        for (int i = 0; i < clickRecords.size(); i++) {
            ClickRecord record = clickRecords.get(i);
            
            // 计算点的大小（越晚越大）
            int pointSize = 2;
            int halfSize = pointSize / 2;
            
            // 设置颜色（按顺序变化）
            Color color = getColorByIndex(i);
            g2d.setColor(color);
            
            // 绘制点击点
            g2d.fillOval(record.x - halfSize, record.y - halfSize, pointSize, pointSize);
            
            // 绘制边框
            g2d.setColor(Color.BLACK);
            g2d.setStroke(new BasicStroke(2));
            g2d.drawOval(record.x - halfSize, record.y - halfSize, pointSize, pointSize);
            
            // 绘制序号
            g2d.setColor(Color.WHITE);
            g2d.setFont(new Font("Arial", Font.BOLD, 10));
            String number = String.valueOf(i + 1);
            FontMetrics fm = g2d.getFontMetrics();
            int textWidth = fm.stringWidth(number);
            int textHeight = fm.getHeight();
            g2d.drawString(number, 
                record.x - textWidth/2, 
                record.y + textHeight/4);
        }
    }
    
    /**
     * 绘制统计信息
     */
    private void drawStatistics(Graphics2D g2d) {
        g2d.setColor(Color.BLACK);
        g2d.setFont(new Font("Arial", Font.BOLD, 16));
        
        // 绘制标题
        String title = "点击位置记录 - " + deviceWidth + "x" + deviceHeight;
        g2d.drawString(title, 10, 25);
        
        // 绘制统计信息
        g2d.setFont(new Font("Arial", Font.PLAIN, 14));
        g2d.drawString("总点击次数: " + clickRecords.size(), 10, 45);
        g2d.drawString("设备尺寸: " + deviceWidth + " x " + deviceHeight, 10, 65);
        g2d.drawString("网格: 12行 x 6列", 10, 85);
        
        // 绘制时间范围
        if (!clickRecords.isEmpty()) {
            long startTime = clickRecords.get(0).timestamp;
            long endTime = clickRecords.get(clickRecords.size() - 1).timestamp;
            long duration = endTime - startTime;
            g2d.drawString("执行时长: " + (duration / 1000.0) + "秒", 10, 105);
        }
    }
    
    /**
     * 根据索引获取颜色
     */
    private Color getColorByIndex(int index) {
        Color[] colors = {
            Color.RED, Color.BLUE, Color.GREEN, Color.ORANGE, 
            Color.MAGENTA, Color.CYAN, Color.PINK, Color.YELLOW,
            Color.GRAY, Color.DARK_GRAY
        };
        return colors[index % colors.length];
    }
    
    /**
     * 点击记录内部类
     */
    public static class ClickRecord {
        public final int x;
        public final int y;
        public final String action;
        public final long timestamp;
        
        public ClickRecord(int x, int y, String action, long timestamp) {
            this.x = x;
            this.y = y;
            this.action = action;
            this.timestamp = timestamp;
        }
        
        @Override
        public String toString() {
            return String.format("ClickRecord(x=%d, y=%d, action=%s, time=%d)", 
                x, y, action, timestamp);
        }
    }
    
    /**
     * 打印点击统计信息
     */
    public void printStatistics() {
        System.out.println("=== 点击位置统计 ===");
        System.out.println("总点击次数: " + clickRecords.size());
        System.out.println("设备尺寸: " + deviceWidth + " x " + deviceHeight);
        
        if (!clickRecords.isEmpty()) {
            long startTime = clickRecords.get(0).timestamp;
            long endTime = clickRecords.get(clickRecords.size() - 1).timestamp;
            long duration = endTime - startTime;
            System.out.println("执行时长: " + (duration / 1000.0) + "秒");
            
            // 按网格统计
            int[][] gridCount = new int[12][6];
            int cellWidth = deviceWidth / 6;
            int cellHeight = deviceHeight / 12;
            
            for (ClickRecord record : clickRecords) {
                int gridRow = record.y / cellHeight;
                int gridCol = record.x / cellWidth;
                if (gridRow >= 0 && gridRow < 12 && gridCol >= 0 && gridCol < 6) {
                    gridCount[gridRow][gridCol]++;
                }
            }
            
            System.out.println("网格点击分布:");
            for (int row = 0; row < 12; row++) {
                for (int col = 0; col < 6; col++) {
                    if (gridCount[row][col] > 0) {
                        System.out.printf("  [%d,%d]: %d次\n", row, col, gridCount[row][col]);
                    }
                }
            }
        }
        System.out.println("==================");
    }
}

