package com.web.demo.demo;


import org.proxyseller.Api;
import org.proxyseller.Config;

import java.util.Map;

public class Demo {

    public static void main(String[] args) throws Exception {

        Api api = new Api(new Config("5ab5458105490b996f4abd20a0ae2869"));
    }
}
