package com.web.demo.demo.pojo;

import java.util.List;

public  class IpDataReq {
    private String code;
    private List<IpData> data;

    public List<IpData> getData() {
        return data;
    }

    public void setData(List<IpData> data) {
        this.data = data;
    }

    @Override
    public String toString() {
        return "IpDataReq{" +
                "code='" + code + '\'' +
                ", data=" + data +
                '}';
    }
}
