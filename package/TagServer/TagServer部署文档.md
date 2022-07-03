# TagServer部署文档

1、安装相关依赖，挂载juicefs，启动ray集群，并将tagging.py中路径设置为juicefs挂载的路径（详情参见docs目录下的DisGraFS部署文档）

2、解压prometheus.tar.gz，进入目录下

3、将prometheus.yml文件内容作如下替换：

```
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

rule_files:

  # - "first_rules.yml"

  # - "second_rules.yml"

scrape_configs:

  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "juicefs"
    static_configs:
      - targets: ["localhost:9567"]
```

4、使用如下命令启动prometheus：

```
./prometheus --config.file=prometheus.yml
```

5、使用如下命令安装Grafana：

```bash
sudo apt-get install -y wget
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
```

```bash
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
```

```bash
sudo apt-get update
sudo apt-get install grafana
```

6、启动Grafana：

```bash
sudo systemctl daemon-reload
sudo systemctl start grafana-server
sudo systemctl status grafana-server
```

之后即可在http://localhost:3000看到Grafana监控

在启动主服务器程序之后，使用:

```
python3 tag_server.py
```

即可