# jvppeteer 集成说明

## 当前状态

✅ **已完成：**
- jvppeteer 3.4.1 依赖已添加到 pom.xml
- 项目结构已准备好集成 jvppeteer
- Playwright 功能完全正常

⚠️ **待完成：**
- jvppeteer API 使用方式需要进一步研究
- LaunchOptions.Builder 构造函数访问权限问题

## 依赖信息

```xml
<dependency>
    <groupId>io.github.fanyong920</groupId>
    <artifactId>jvppeteer</artifactId>
    <version>3.4.1</version>
</dependency>
```

## 正确的包结构

根据实际jar包内容，正确的导入应该是：

```java
import com.ruiyun.jvppeteer.api.core.Browser;
import com.ruiyun.jvppeteer.api.core.Page;
import com.ruiyun.jvppeteer.cdp.core.Puppeteer;
import com.ruiyun.jvppeteer.cdp.entities.LaunchOptions;
import com.ruiyun.jvppeteer.cdp.entities.Viewport;
```

## 当前问题

1. **LaunchOptions.Builder 构造函数是私有的**
   - 需要找到正确的创建方式
   - 可能需要使用静态工厂方法

2. **API 使用方式需要验证**
   - 需要查看官方文档或示例
   - 确认正确的API调用方式

## 下一步计划

1. 研究 jvppeteer 3.4.1 的官方文档
2. 找到正确的 LaunchOptions 创建方式
3. 实现完整的 jvppeteer 滑动功能
4. 集成到主应用中

## 当前可用功能

- ✅ Playwright 滑动（完全可用）
- ✅ 随机上拉滑动
- ✅ 视频录制
- ✅ 多种滑动方向
- ⚠️ jvppeteer 滑动（开发中）

## 使用方法

**使用 Playwright（推荐）：**
```bash
mvn exec:java -Dexec.mainClass="com.web.demo.demo.DemoApplication"
```

**尝试使用 jvppeteer：**
```bash
mvn exec:java -Dexec.mainClass="com.web.demo.demo.DemoApplication" -Dexec.args="jvppeteer"
```

## 技术细节

- jvppeteer 使用 CDP (Chrome DevTools Protocol)
- 与 Playwright 的 API 完全不同
- 需要正确的浏览器启动和页面操作方式
- 鼠标操作和截图功能需要适配

## 参考资源

- [jvppeteer GitHub](https://github.com/fanyong920/jvppeteer)
- [jvppeteer 文档](https://fanyong920.github.io/jvppeteer/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)




