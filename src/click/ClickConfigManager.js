/**
 * 点击配置管理类
 * 根据屏幕尺寸生成12行6列的网格，支持通过概率进行随机点击
 */
class ClickConfigManager {
    constructor() {
        this.GRID_ROWS = 12;
        this.GRID_COLS = 6;
    }

    /**
     * 创建点击配置
     */
    createClickConfig(screenWidth, screenHeight) {
        return new ClickConfig(screenWidth, screenHeight);
    }

    /**
     * 创建常用屏幕尺寸的点击配置
     */
    createCommonClickConfig(screenType) {
        const configs = {
            'iphone': { width: 375, height: 812 },
            'android': { width: 412, height: 839 },
            'tablet': { width: 768, height: 1024 },
            'desktop': { width: 1920, height: 1080 }
        };

        const config = configs[screenType.toLowerCase()] || configs['android'];
        return new ClickConfig(config.width, config.height);
    }
}

/**
 * 点击配置类
 */
class ClickConfig {
    constructor(screenWidth, screenHeight) {
        this.screenWidth = screenWidth;
        this.screenHeight = screenHeight;
        this.gridProbabilities = [];
        this.GRID_ROWS = 12;
        this.GRID_COLS = 6;
        
        // 初始化默认网格概率
        this.initDefaultGridProbabilities();
    }

    /**
     * 初始化默认网格概率
     */
    initDefaultGridProbabilities() {
        // 直接写死12行6列的概率值，方便单独修改
        // 上下高中间低，右边高左边低
        this.gridProbabilities = [
            [0.00, 0.00, 0.00, 0.00, 0.00, 0.00], // 第0行 - 概率为0
            [0.00, 0.00, 0.00, 0.00, 0.00, 0.00], // 第1行 - 概率为0
            [0.05, 0.08, 0.12, 0.15, 0.18, 0.22], // 第2行 - 上高，右侧高
            [0.08, 0.12, 0.15, 0.18, 0.22, 0.25], // 第3行 - 上高，右侧高
            [0.02, 0.03, 0.05, 0.08, 0.12, 0.15], // 第4行 - 中间低，右侧高
            [0.01, 0.02, 0.03, 0.05, 0.08, 0.10], // 第5行 - 中间最低，右侧高
            [0.01, 0.02, 0.03, 0.05, 0.08, 0.10], // 第6行 - 中间最低，右侧高
            [0.02, 0.03, 0.05, 0.08, 0.12, 0.15], // 第7行 - 中间低，右侧高
            [0.05, 0.08, 0.12, 0.15, 0.18, 0.22], // 第8行 - 下高，右侧高
            [0.08, 0.12, 0.15, 0.18, 0.22, 0.25], // 第9行 - 下高，右侧高
            [0.00, 0.00, 0.00, 0.00, 0.00, 0.00], // 第10行 - 概率为0
            [0.00, 0.00, 0.00, 0.00, 0.00, 0.00]  // 第11行 - 概率为0
        ];
    }

    /**
     * 根据概率随机选择网格并生成点击位置
     */
    getRandomClickPosition() {
        // 根据概率选择网格
        const selectedGrid = this.selectGridByProbability();
        const row = selectedGrid[0];
        const col = selectedGrid[1];
        
        // 在选中的网格内随机生成点击位置
        return this.generateRandomPositionInGrid(row, col);
    }

    /**
     * 根据概率选择网格
     */
    selectGridByProbability() {
        // 计算总概率
        let totalProbability = 0;
        for (let row = 0; row < this.GRID_ROWS; row++) {
            for (let col = 0; col < this.GRID_COLS; col++) {
                totalProbability += this.gridProbabilities[row][col];
            }
        }
        
        // 生成随机数
        const randomValue = Math.random() * totalProbability;
        
        // 根据概率选择网格
        let currentProbability = 0;
        for (let row = 0; row < this.GRID_ROWS; row++) {
            for (let col = 0; col < this.GRID_COLS; col++) {
                currentProbability += this.gridProbabilities[row][col];
                if (randomValue <= currentProbability) {
                    return [row, col];
                }
            }
        }
        
        // 如果没选中（理论上不会发生），返回中心网格
        return [Math.floor(this.GRID_ROWS / 2), Math.floor(this.GRID_COLS / 2)];
    }

    /**
     * 在指定网格内生成随机点击位置
     */
    generateRandomPositionInGrid(row, col) {
        // 计算网格单元大小
        const cellWidth = this.screenWidth / this.GRID_COLS;
        const cellHeight = this.screenHeight / this.GRID_ROWS;
        
        // 计算网格边界
        const left = col * cellWidth;
        const right = left + cellWidth;
        const top = row * cellHeight;
        const bottom = top + cellHeight;
        
        // 在网格内随机生成坐标
        const x = Math.floor(left + Math.random() * (right - left));
        const y = Math.floor(top + Math.random() * (bottom - top));
        
        // 确保坐标在屏幕范围内
        const finalX = Math.max(0, Math.min(this.screenWidth - 1, x));
        const finalY = Math.max(0, Math.min(this.screenHeight - 1, y));
        
        return new ClickPosition(
            finalX, 
            finalY, 
            row, 
            col, 
            this.gridProbabilities[row][col]
        );
    }

    /**
     * 设置网格概率
     */
    setGridProbability(row, col, probability) {
        if (row < 0 || row >= this.GRID_ROWS || col < 0 || col >= this.GRID_COLS) {
            throw new Error(`网格坐标超出范围: (${row}, ${col})`);
        }
        if (probability < 0 || probability > 1) {
            throw new Error(`概率必须在0-1之间: ${probability}`);
        }
        this.gridProbabilities[row][col] = probability;
    }

    /**
     * 获取网格概率
     */
    getGridProbability(row, col) {
        if (row < 0 || row >= this.GRID_ROWS || col < 0 || col >= this.GRID_COLS) {
            throw new Error(`网格坐标超出范围: (${row}, ${col})`);
        }
        return this.gridProbabilities[row][col];
    }

    /**
     * 获取总概率
     */
    getTotalProbability() {
        let total = 0;
        for (let row = 0; row < this.GRID_ROWS; row++) {
            for (let col = 0; col < this.GRID_COLS; col++) {
                total += this.gridProbabilities[row][col];
            }
        }
        return total;
    }

    /**
     * 打印网格配置
     */
    printGridConfig() {
        console.log('=== 点击网格配置 ===');
        console.log(`屏幕尺寸: ${this.screenWidth}x${this.screenHeight}`);
        console.log(`网格大小: ${this.GRID_ROWS}x${this.GRID_COLS}`);
        console.log(`总概率: ${this.getTotalProbability().toFixed(3)}`);
        console.log('\n网格概率配置:');
        
        for (let row = 0; row < this.GRID_ROWS; row++) {
            let rowStr = `第${row.toString().padStart(2, ' ')}行: `;
            for (let col = 0; col < this.GRID_COLS; col++) {
                rowStr += `${this.gridProbabilities[row][col].toFixed(3)} `;
            }
            console.log(rowStr);
        }
    }

    // Getters
    getScreenWidth() { return this.screenWidth; }
    getScreenHeight() { return this.screenHeight; }
    getGridProbabilities() { return this.gridProbabilities; }
}

/**
 * 点击位置类
 */
class ClickPosition {
    constructor(x, y, gridRow, gridCol, probability) {
        this.x = x;
        this.y = y;
        this.gridRow = gridRow;
        this.gridCol = gridCol;
        this.probability = probability;
    }

    toString() {
        return `ClickPosition(x=${this.x}, y=${this.y}, grid=[${this.gridRow},${this.gridCol}], prob=${this.probability.toFixed(3)})`;
    }
}

module.exports = { ClickConfigManager, ClickConfig, ClickPosition };
