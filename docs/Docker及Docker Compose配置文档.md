# Docker及Docker Compose配置文档

本文档记录服务器端Docker以及Docker Compose安装以及配置的过程

## 1. Docker安装及配置

### 1.1 Docker安装

以Ubuntu为例

使用如下命令一键安装Docker

```
curl -sSL https://get.daocloud.io/docker | sh
```



### 1.2 Docker测试

在终端运行如下命令测试docker:

```
docker run ubuntu:20.04 /bin/echo "Hello World!"
```

预期在命令行打印出：

```
Hello World！
```



使用如下命令可以创建一个交互式的容器，即拥有终端的可对话的容器：

```
docker run -it ubuntu:20.04 /bin/bash
```

预期出现如下界面：

![docker_1](../src/docker_1.png)

使用exit命令可以退出容器终端：

![docker_2](../src/docker_2.png)



### 1.3 Docker相关配置

--Docker镜像加速

使用命令：

```
sudo vim /etc/docker/daemon.json
```

在打开的文件中加入如下内容：

```
{
  "registry-mirrors": [
    "https://reg-mirror.qiniu.com"
  ],
  "exec-opts": [ "native.cgroupdriver=systemd" ]
}
```

输入:wq保存并退出

之后使用如下命令重新启动Docker服务：

```
sudo systemctl daemon-reload
sudo systemctl restart docker
```



## 2. Docker Compose安装及配置

### 2.1 Docker Compose安装

使用如下命令安装Docker Compose：

```
curl -L https://get.daocloud.io/docker/compose/releases/download/v2.4.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
```

安装完成后，使用如下命令赋予相关文件可执行权限并创建软链接：

```
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

测试是否安装成功：

```
docker-compose --version
```

预期出现如下界面：

![docker_3](../src/docker_3.png)

代表安装成功



### 2.2 Docker Compose测试

#### 2.2.1 创建测试目录

```
mkdir composetest
cd composetest
```

#### 2.2.2 创建测试文件

在测试目录中创建名为app.py的python文件，将如下内容复制到该python文件中：

```
import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


**def** get_hit_count():
  retries = 5
  **while** True:
    **try**:
      **return** cache.incr('hits')
    **except** redis.exceptions.ConnectionError **as** exc:
      **if** retries == 0:
        **raise** exc
      retries -= 1
      time.sleep(0.5)



@app.route('/')
**def** hello():
  count = get_hit_count()
  **return** 'Hello World! I have been seen {} times.**\n**'.format(count)
```


