/**
 * 代理配置基类 - 多态设计模式
 */
class ProxyConfig {
    constructor() {
        this.type = 'base';
    }

    /**
     * 获取代理配置
     * @returns {Object|null} 代理配置对象
     */
    getConfig() {
        throw new Error('getConfig method must be implemented');
    }

    /**
     * 验证配置是否有效
     * @returns {boolean} 配置是否有效
     */
    isValid() {
        throw new Error('isValid method must be implemented');
    }

    /**
     * 渲染配置界面
     * @param {HTMLElement} container 容器元素
     */
    render(container) {
        throw new Error('render method must be implemented');
    }

    /**
     * 从界面获取配置值
     * @returns {Object|null} 配置对象
     */
    getValue() {
        throw new Error('getValue method must be implemented');
    }

    /**
     * 设置配置值
     * @param {Object} config 配置对象
     */
    setValue(config) {
        throw new Error('setValue method must be implemented');
    }
}

/**
 * 无代理配置
 */
class NoProxyConfig extends ProxyConfig {
    constructor() {
        super();
        this.type = 'none';
    }

    getConfig() {
        return null;
    }

    isValid() {
        return true;
    }

    render(container) {
        container.innerHTML = '<p class="proxy-info">当前使用无代理模式</p>';
    }

    getValue() {
        return null;
    }

    setValue(config) {
        // 无代理不需要设置值
    }
}

/**
 * HTTP代理配置
 */
class HttpProxyConfig extends ProxyConfig {
    constructor() {
        super();
        this.type = 'http';
        this.config = {
            host: '',
            port: '',
            username: '',
            password: ''
        };
    }

    getConfig() {
        if (!this.isValid()) return null;
        return {
            type: 'http',
            host: this.config.host,
            port: parseInt(this.config.port),
            username: this.config.username,
            password: this.config.password
        };
    }

    isValid() {
        return this.config.host && this.config.port;
    }

    render(container) {
        container.innerHTML = `
            <div class="proxy-form">
                <div class="form-row">
                    <div class="form-group">
                        <label for="proxyHost">主机地址:</label>
                        <input type="text" id="proxyHost" placeholder="127.0.0.1" value="${this.config.host}">
                    </div>
                    <div class="form-group">
                        <label for="proxyPort">端口:</label>
                        <input type="number" id="proxyPort" placeholder="8080" value="${this.config.port}">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="proxyUsername">用户名 (可选):</label>
                        <input type="text" id="proxyUsername" placeholder="username" value="${this.config.username}">
                    </div>
                    <div class="form-group">
                        <label for="proxyPassword">密码 (可选):</label>
                        <input type="password" id="proxyPassword" placeholder="password" value="${this.config.password}">
                    </div>
                </div>
            </div>
        `;
    }

    getValue() {
        const host = document.getElementById('proxyHost')?.value || '';
        const port = document.getElementById('proxyPort')?.value || '';
        const username = document.getElementById('proxyUsername')?.value || '';
        const password = document.getElementById('proxyPassword')?.value || '';
        
        this.config = { host, port, username, password };
        return this.getConfig();
    }

    setValue(config) {
        if (config) {
            this.config = {
                host: config.host || '',
                port: config.port || '',
                username: config.username || '',
                password: config.password || ''
            };
        }
    }
}

/**
 * SOCKS5代理配置
 */
class Socks5ProxyConfig extends ProxyConfig {
    constructor() {
        super();
        this.type = 'socks5';
        this.config = {
            host: '',
            port: '',
            username: '',
            password: ''
        };
    }

    getConfig() {
        if (!this.isValid()) return null;
        return {
            type: 'socks5',
            host: this.config.host,
            port: parseInt(this.config.port),
            username: this.config.username,
            password: this.config.password
        };
    }

    isValid() {
        return this.config.host && this.config.port;
    }

    render(container) {
        container.innerHTML = `
            <div class="proxy-form">
                <div class="form-row">
                    <div class="form-group">
                        <label for="proxyHost">主机地址:</label>
                        <input type="text" id="proxyHost" placeholder="127.0.0.1" value="${this.config.host}">
                    </div>
                    <div class="form-group">
                        <label for="proxyPort">端口:</label>
                        <input type="number" id="proxyPort" placeholder="1080" value="${this.config.port}">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="proxyUsername">用户名 (可选):</label>
                        <input type="text" id="proxyUsername" placeholder="username" value="${this.config.username}">
                    </div>
                    <div class="form-group">
                        <label for="proxyPassword">密码 (可选):</label>
                        <input type="password" id="proxyPassword" placeholder="password" value="${this.config.password}">
                    </div>
                </div>
            </div>
        `;
    }

    getValue() {
        const host = document.getElementById('proxyHost')?.value || '';
        const port = document.getElementById('proxyPort')?.value || '';
        const username = document.getElementById('proxyUsername')?.value || '';
        const password = document.getElementById('proxyPassword')?.value || '';
        
        this.config = { host, port, username, password };
        return this.getConfig();
    }

    setValue(config) {
        if (config) {
            this.config = {
                host: config.host || '',
                port: config.port || '',
                username: config.username || '',
                password: config.password || ''
            };
        }
    }
}

/**
 * 自定义代理配置
 */
class CustomProxyConfig extends ProxyConfig {
    constructor() {
        super();
        this.type = 'custom';
        this.config = {
            url: ''
        };
    }

    getConfig() {
        if (!this.isValid()) return null;
        return {
            type: 'custom',
            url: this.config.url
        };
    }

    isValid() {
        return this.config.url && this.config.url.trim() !== '';
    }

    render(container) {
        container.innerHTML = `
            <div class="proxy-form">
                <div class="form-group">
                    <label for="proxyUrl">代理URL:</label>
                    <input type="text" id="proxyUrl" placeholder="http://username:password@host:port" value="${this.config.url}">
                    <small class="form-help">支持格式: http://user:pass@host:port 或 socks5://user:pass@host:port</small>
                </div>
            </div>
        `;
    }

    getValue() {
        const url = document.getElementById('proxyUrl')?.value || '';
        this.config = { url };
        return this.getConfig();
    }

    setValue(config) {
        if (config) {
            this.config = {
                url: config.url || ''
            };
        }
    }
}

/**
 * 代理配置工厂
 */
class ProxyConfigFactory {
    static create(type) {
        switch (type) {
            case 'none':
                return new NoProxyConfig();
            case 'http':
                return new HttpProxyConfig();
            case 'socks5':
                return new Socks5ProxyConfig();
            case 'custom':
                return new CustomProxyConfig();
            default:
                throw new Error(`Unknown proxy type: ${type}`);
        }
    }

    static getSupportedTypes() {
        return ['none', 'http', 'socks5', 'custom'];
    }
}

module.exports = {
    ProxyConfig,
    NoProxyConfig,
    HttpProxyConfig,
    Socks5ProxyConfig,
    CustomProxyConfig,
    ProxyConfigFactory
};
