# ngx_status
通过lua语言实现的基于共享字典的服务应用。用于实时监控Nginx域名连接状态、流量信息、请求时间、状态码、request_uri信息、nginx启动时间、版本、pid等信息.
通过python请求lua接口，解析json信息入库.
通过flask＋bootstrap 前端展示.

###Version
2016-12-19 发布 ngx_status version 1.0（v1.0）

###Description
* openresty lua python flask

###Note
* handcraft	web前端（50%）
* nginx_config	nginx配置
* scripts       脚本
* nginx restart 将清空共享字典

###Install
1. 安装openresty 或 nginx ＋ lua，配置文件nginx_conf目录
2. 创建handcraft数据库，执行handcraft.sql
3. 创建ngx_status数据库，执行ngx_status
4. 安装flask及相关支持库，查看handcraft目录：requirements.txt

###Data
    {
        global: {
            start_time: "2016-12-19 11:48:53",
            connections: {
                waiting: 1,
                active: 0,
                reading: 0,
                writing: 0
            },
            requests: {
                total: 5781,
                current: "2"
            },
            conn_time: "2016-12-19 11:52:32",
            PID: "11566",
            Version: "1.9.15"
        },
        www.yoyohandcraft.info: {
            upstream_requests_total: 5781,
                status code: {
                4xx: 5781
            },
            traffic: {
                received: 95669481,
                sent: 2260386
            },
            upstream_resp_time_sum: 13968.037,
            /: {
                cache: {
                    miss: 5781
                },
                status code: {
                    4xx: 5781
                },
                request_times: {
                    1000-inf: 4893,
                    500-1000: 501,
                    100-500: 260,
                    0-100: 127
                },
                requests_total: 5781
            },
            request_times: {
                1000-inf: 4893,
                500-1000: 501,
                100-500: 260,
                0-100: 127
            },
            requests_total: 5781
        }
    } 
