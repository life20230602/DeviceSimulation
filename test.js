const { DeviceManager } = require('./src/device/DeviceManager');
const { ClickConfigManager } = require('./src/click/ClickConfigManager');
const { NetworkInterceptor } = require('./src/network/NetworkInterceptor');

async function testModules() {
    console.log('🧪 开始测试模块...\n');

    try {
        // 测试设备管理器
        console.log('📱 测试设备管理器...');
        const deviceManager = new DeviceManager();
        await deviceManager.initialize();
        
        const device = deviceManager.getRandomDevice();
        console.log('✅ 随机设备:', device.deviceName);
        console.log('   分辨率:', `${device.width}x${device.height}`);
        console.log('   系统:', `${device.os} ${device.osVersion}`);
        console.log('   UserAgent:', device.randomUserAgent.substring(0, 50) + '...\n');

        // 测试点击配置管理器
        console.log('🎯 测试点击配置管理器...');
        const clickConfigManager = new ClickConfigManager();
        const clickConfig = clickConfigManager.createClickConfig(375, 812);
        
        console.log('✅ 点击配置创建成功');
        console.log('   屏幕尺寸:', `${clickConfig.getScreenWidth()}x${clickConfig.getScreenHeight()}`);
        console.log('   总概率:', clickConfig.getTotalProbability().toFixed(3));
        
        // 测试随机点击位置
        for (let i = 0; i < 3; i++) {
            const clickPos = clickConfig.getRandomClickPosition();
            console.log(`   随机点击${i+1}: (${clickPos.x}, ${clickPos.y})`);
        }
        console.log('');

        // 测试网络拦截器
        console.log('🌐 测试网络拦截器...');
        const networkInterceptor = new NetworkInterceptor()
            .setBlockImages(true)
            .setBlockMedia(true)
            .setBlockAnalytics(true);
        
        console.log('✅ 网络拦截器配置成功');
        console.log('   阻止图片:', networkInterceptor.blockImages);
        console.log('   阻止媒体:', networkInterceptor.blockMedia);
        console.log('   阻止分析:', networkInterceptor.blockAnalytics);
        console.log('');

        console.log('🎉 所有模块测试通过！');
        console.log('\n📋 测试摘要:');
        console.log('   ✅ 设备管理器 - 正常');
        console.log('   ✅ 点击配置管理器 - 正常');
        console.log('   ✅ 网络拦截器 - 正常');
        console.log('\n🚀 应用已准备就绪，可以运行 npm start 启动！');

    } catch (error) {
        console.error('❌ 测试失败:', error.message);
        console.error(error.stack);
        process.exit(1);
    }
}

// 运行测试
testModules();