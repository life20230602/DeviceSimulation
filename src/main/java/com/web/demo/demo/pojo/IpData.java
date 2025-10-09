package com.web.demo.demo.pojo;

public  class IpData {
        private String ip;
        private int port;
        private String prov;
        private String city;
        private String expire;

        // Getters and Setters
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

        public String getProv() {
            return prov;
        }

        public void setProv(String prov) {
            this.prov = prov;
        }

        public String getCity() {
            return city;
        }

        public void setCity(String city) {
            this.city = city;
        }

        public String getExpire() {
            return expire;
        }

        public void setExpire(String expire) {
            this.expire = expire;
        }

        @Override
        public String toString() {
            return "IpData{" +
                    "ip='" + ip + '\'' +
                    ", port=" + port +
                    ", prov='" + prov + '\'' +
                    ", city='" + city + '\'' +
                    ", expire='" + expire + '\'' +
                    '}';
        }
    }