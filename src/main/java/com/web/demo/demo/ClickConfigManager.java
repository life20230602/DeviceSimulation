package com.web.demo.demo;

import java.util.*;

/**
 * 点击配置管理类
 * 根据屏幕尺寸生成12行6列的网格，支持通过概率进行随机点击
 */
public class ClickConfigManager {
    
    // 网格配置
    private static final int GRID_ROWS = 12;
    private static final int GRID_COLS = 6;
    
    /**
     * 点击配置类
     */
    public static class ClickConfig {
        private final int screenWidth;
        private final int screenHeight;
        private final double[][] gridProbabilities; // 12x6的网格概率配置
        private final Random random;
        
        public ClickConfig(int screenWidth, int screenHeight) {
            this.screenWidth = screenWidth;
            this.screenHeight = screenHeight;
            this.gridProbabilities = new double[GRID_ROWS][GRID_COLS];
            this.random = new Random();
            
            // 初始化默认网格概率
            initDefaultGridProbabilities();
        }
        
        /**
         * 初始化默认网格概率
         */
        private void initDefaultGridProbabilities() {
            // 直接写死12行6列的概率值，方便单独修改
            // 上下高中间低，右边高左边低
            gridProbabilities[0] = new double[]{0.00, 0.00, 0.00, 0.00, 0.00, 0.00}; // 第0行 - 概率为0
            gridProbabilities[1] = new double[]{0.00, 0.00, 0.00, 0.00, 0.00, 0.00}; // 第1行 - 概率为0
            gridProbabilities[2] = new double[]{0.05, 0.08, 0.12, 0.15, 0.18, 0.22}; // 第2行 - 上高，右侧高
            gridProbabilities[3] = new double[]{0.08, 0.12, 0.15, 0.18, 0.22, 0.25}; // 第3行 - 上高，右侧高
            gridProbabilities[4] = new double[]{0.02, 0.03, 0.05, 0.08, 0.12, 0.15}; // 第4行 - 中间低，右侧高
            gridProbabilities[5] = new double[]{0.01, 0.02, 0.03, 0.05, 0.08, 0.10}; // 第5行 - 中间最低，右侧高
            gridProbabilities[6] = new double[]{0.01, 0.02, 0.03, 0.05, 0.08, 0.10}; // 第6行 - 中间最低，右侧高
            gridProbabilities[7] = new double[]{0.02, 0.03, 0.05, 0.08, 0.12, 0.15}; // 第7行 - 中间低，右侧高
            gridProbabilities[8] = new double[]{0.05, 0.08, 0.12, 0.15, 0.18, 0.22}; // 第8行 - 下高，右侧高
            gridProbabilities[9] = new double[]{0.08, 0.12, 0.15, 0.18, 0.22, 0.25}; // 第9行 - 下高，右侧高
            gridProbabilities[10] = new double[]{0.00, 0.00, 0.00, 0.00, 0.00, 0.00}; // 第10行 - 概率为0
            gridProbabilities[11] = new double[]{0.00, 0.00, 0.00, 0.00, 0.00, 0.00}; // 第11行 - 概率为0
        }
        
        /**
         * 根据概率随机选择网格并生成点击位置
         */
        public ClickPosition getRandomClickPosition() {
            // 根据概率选择网格
            int[] selectedGrid = selectGridByProbability();
            int row = selectedGrid[0];
            int col = selectedGrid[1];
            
            // 在选中的网格内随机生成点击位置
            return generateRandomPositionInGrid(row, col);
        }
        
        /**
         * 根据概率选择网格
         */
        private int[] selectGridByProbability() {
            // 计算总概率
            double totalProbability = 0;
            for (int row = 0; row < GRID_ROWS; row++) {
                for (int col = 0; col < GRID_COLS; col++) {
                    totalProbability += gridProbabilities[row][col];
                }
            }
            
            // 生成随机数
            double randomValue = random.nextDouble() * totalProbability;
            
            // 根据概率选择网格
            double currentProbability = 0;
            for (int row = 0; row < GRID_ROWS; row++) {
                for (int col = 0; col < GRID_COLS; col++) {
                    currentProbability += gridProbabilities[row][col];
                    if (randomValue <= currentProbability) {
                        return new int[]{row, col};
                    }
                }
            }
            
            // 如果没选中（理论上不会发生），返回中心网格
            return new int[]{GRID_ROWS / 2, GRID_COLS / 2};
        }
        
        /**
         * 在指定网格内生成随机点击位置
         */
        private ClickPosition generateRandomPositionInGrid(int row, int col) {
            // 计算网格单元大小
            double cellWidth = (double) screenWidth / GRID_COLS;
            double cellHeight = (double) screenHeight / GRID_ROWS;
            
            // 计算网格边界
            double left = col * cellWidth;
            double right = left + cellWidth;
            double top = row * cellHeight;
            double bottom = top + cellHeight;
            
            // 在网格内随机生成坐标
            int x = (int) (left + random.nextDouble() * (right - left));
            int y = (int) (top + random.nextDouble() * (bottom - top));
            
            // 确保坐标在屏幕范围内
            x = Math.max(0, Math.min(screenWidth - 1, x));
            y = Math.max(0, Math.min(screenHeight - 1, y));
            
            return new ClickPosition(x, y, row, col, gridProbabilities[row][col]);
        }
        
        /**
         * 设置网格概率
         */
        public void setGridProbability(int row, int col, double probability) {
            if (row < 0 || row >= GRID_ROWS || col < 0 || col >= GRID_COLS) {
                throw new IllegalArgumentException("网格坐标超出范围: (" + row + ", " + col + ")");
            }
            if (probability < 0 || probability > 1) {
                throw new IllegalArgumentException("概率必须在0-1之间: " + probability);
            }
            gridProbabilities[row][col] = probability;
        }
        
        /**
         * 获取网格概率
         */
        public double getGridProbability(int row, int col) {
            if (row < 0 || row >= GRID_ROWS || col < 0 || col >= GRID_COLS) {
                throw new IllegalArgumentException("网格坐标超出范围: (" + row + ", " + col + ")");
            }
            return gridProbabilities[row][col];
        }
        
        /**
         * 获取总概率
         */
        public double getTotalProbability() {
            double total = 0;
            for (int row = 0; row < GRID_ROWS; row++) {
                for (int col = 0; col < GRID_COLS; col++) {
                    total += gridProbabilities[row][col];
                }
            }
            return total;
        }
        
        /**
         * 打印网格配置
         */
        public void printGridConfig() {
            System.out.println("=== 点击网格配置 ===");
            System.out.println("屏幕尺寸: " + screenWidth + "x" + screenHeight);
            System.out.println("网格大小: " + GRID_ROWS + "x" + GRID_COLS);
            System.out.println("总概率: " + String.format("%.3f", getTotalProbability()));
            System.out.println("\n网格概率配置:");
            
            for (int row = 0; row < GRID_ROWS; row++) {
                System.out.printf("第%2d行: ", row);
                for (int col = 0; col < GRID_COLS; col++) {
                    System.out.printf("%.3f ", gridProbabilities[row][col]);
                }
                System.out.println();
            }
        }
        
        // Getters
        public int getScreenWidth() { return screenWidth; }
        public int getScreenHeight() { return screenHeight; }
        public double[][] getGridProbabilities() { return gridProbabilities; }
    }
    
    /**
     * 点击位置类
     */
    public static class ClickPosition {
        public final int x;
        public final int y;
        public final int gridRow;
        public final int gridCol;
        public final double probability;
        
        public ClickPosition(int x, int y, int gridRow, int gridCol, double probability) {
            this.x = x;
            this.y = y;
            this.gridRow = gridRow;
            this.gridCol = gridCol;
            this.probability = probability;
        }
        
        @Override
        public String toString() {
            return String.format("ClickPosition(x=%d, y=%d, grid=[%d,%d], prob=%.3f)", 
                x, y, gridRow, gridCol, probability);
        }
    }
    
    /**
     * 创建点击配置
     */
    public static ClickConfig createClickConfig(int screenWidth, int screenHeight) {
        return new ClickConfig(screenWidth, screenHeight);
    }
    
    /**
     * 创建常用屏幕尺寸的点击配置
     */
    public static ClickConfig createCommonClickConfig(String screenType) {
        switch (screenType.toLowerCase()) {
            case "iphone":
                return new ClickConfig(375, 812);
            case "android":
                return new ClickConfig(412, 839);
            case "tablet":
                return new ClickConfig(768, 1024);
            case "desktop":
                return new ClickConfig(1920, 1080);
            default:
                return new ClickConfig(412, 839); // 默认Android尺寸
        }
    }
    
    /**
     * 测试方法
     */
    public static void main(String[] args) {
        System.out.println("=== 点击配置管理类测试 ===\n");
        
        // 创建点击配置
        ClickConfig config = createClickConfig(412, 839);
        config.printGridConfig();
        
        System.out.println("\n=== 测试随机点击 ===");
        for (int i = 0; i < 10; i++) {
            ClickPosition pos = config.getRandomClickPosition();
            System.out.println("随机点击" + (i+1) + ": " + pos);
        }
        
        System.out.println("\n=== 测试概率调整 ===");
        // 调整中心区域概率
        config.setGridProbability(5, 2, 0.30); // 中心概率提高
        config.setGridProbability(5, 3, 0.30); // 中心概率提高
        config.setGridProbability(6, 2, 0.30); // 中心概率提高
        config.setGridProbability(6, 3, 0.30); // 中心概率提高
        
        System.out.println("调整后的配置:");
        config.printGridConfig();
        
        System.out.println("\n=== 调整后的随机点击 ===");
        for (int i = 0; i < 5; i++) {
            ClickPosition pos = config.getRandomClickPosition();
            System.out.println("随机点击" + (i+1) + ": " + pos);
        }
        
        System.out.println("\n=== 测试不同屏幕尺寸 ===");
        ClickConfig iphoneConfig = createCommonClickConfig("iphone");
        System.out.println("iPhone配置:");
        iphoneConfig.printGridConfig();
        
        ClickConfig androidConfig = createCommonClickConfig("android");
        System.out.println("\nAndroid配置:");
        androidConfig.printGridConfig();
        
        System.out.println("\n=== 测试完成 ===");
    }
}