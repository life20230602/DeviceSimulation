package com.web.demo.demo.pojo;

import com.ruiyun.jvppeteer.api.core.Browser;
import com.ruiyun.jvppeteer.api.core.BrowserContext;
import com.ruiyun.jvppeteer.api.core.Page;
import com.ruiyun.jvppeteer.api.core.Target;
import com.ruiyun.jvppeteer.api.events.BrowserEvents;
import com.ruiyun.jvppeteer.cdp.core.Puppeteer;
import com.ruiyun.jvppeteer.cdp.entities.*;
import com.web.demo.demo.*;

import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.function.Consumer;

public class DoAdTaskPojo {
   private String ip;
   private int port;
   private String url;
   private String proxyUserName;
   private String proxyPassword;

    public DoAdTaskPojo() {
    }

    public DoAdTaskPojo(String ip, int port, String url, String proxyUserName, String proxyPassword) {
        this.ip = ip;
        this.port = port;
        this.url = url;
        this.proxyUserName = proxyUserName;
        this.proxyPassword = proxyPassword;
    }

    public String getIp() {
        return ip;
    }

    public void setIp(String ip) {
        this.ip = ip;
    }

    public int getPort() {
        return port;
    }

    public void setPort(int port) {
        this.port = port;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getProxyUserName() {
        return proxyUserName;
    }

    public void setProxyUserName(String proxyUserName) {
        this.proxyUserName = proxyUserName;
    }

    public String getProxyPassword() {
        return proxyPassword;
    }

    public void setProxyPassword(String proxyPassword) {
        this.proxyPassword = proxyPassword;
    }
}
