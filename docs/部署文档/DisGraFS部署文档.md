# DisGraFS部署文档

本文档记录USTC 2022 OSH课程x-WowKiddy组部署DisGraFS的过程以及遇到的一些问题。	——丁程



## 1. juicefs部署

juicefs需要在打标服务器和客户端中部署。其中客户端自带juicefs程序，因此只需在打标服务器上安装。

### 1.1 juicefs的安装

部署使用linux系统，在github上搜索juicefs，下载文件名包含linux-amd64的压缩包，在终端依次执行以下命令：

```
JFS_LATEST_TAG=$(curl -s https://api.github.com/repos/juicedata/juicefs/releases/latest | grep 'tag_name' | cut -d '"' -f 4 | tr -d 'v')
```

```
wget "https://github.com/juicedata/juicefs/releases/download/v${JFS_LATEST_TAG}/juicefs-${JFS_LATEST_TAG}-linux-amd64.tar.gz"
```

```
tar -zxf "juicefs-${JFS_LATEST_TAG}-linux-amd64.tar.gz"
```

```
sudo install juicefs /usr/local/bin
```

完成上述 4 个步骤，在终端执行 `juicefs` 命令，返回帮助信息，则说明客户端安装成功。

### 1.2 juicefs分布式模式的部署

首先，juicefs部署需要使用云数据库，这里部署使用阿里云服务器，购买了阿里云256M云数据库Redis版服务。数据库用户名为irisesd，密码为xxx. 数据库公网访问地址为disgrafs.redis.rds.aliyuncs.com。

在juicefs中，用于访问数据库的地址为redis://irisesd:xxx@disgrafs.redis.rds.aliyuncs.com:6379/1.

#### 1.2.1 创建文件系统

```
juicefs format \
    --storage oss \
    --bucket https://myjfs.oss-cn-shanghai.aliyuncs.com \
    --access-key ABCDEFGHIJKLMNopqXYZ \
    --secret-key ZYXwvutsrqpoNMLkJiHgfeDCBA \
    redis://tom:mypassword@myjfs-sh-abc.redis.rds.aliyuncs.com:6379/1 \
    myjfs
```

使用上述命令可以创建一个文件系统，其中access-key与secret-key可以在阿里云数据库的管理界面查看，这里因为已经预先创建好了文件系统，就不再给出具体密钥。



#### 1.2.2 挂载文件系统

```
juicefs mount redis://irisesd:xxx@disgrafs.redis.rds.aliyuncs.com:6379/1 ~/Desktop/jfs 
```

使用上述命令可以将创建好的文件系统挂载到本地的指定目录下。其中，~/Desktop/jfs为需要挂载的目录，可以根据需要自行更换。

若出现形如：

```
2022/04/16 21:07:30.070939 juicefs[22568] <FATAL>: load setting: ERR illegal address: 36.5.105.57:10395 [mount.go:172]
```

的信息，是因为在阿里云数据库的白名单中没有本机对应公网IP地址。

解决方法：打开阿里云数据库管理界面，将报错信息中的ip：36.5.105.57（根据信息自行更换）添加到白名单中即可。

若出现报错信息显示某个目录或文件不存在，可能为cache问题。

解决方法：在上述挂载命令中加入--cache-dir /mycache，即使用命令：

```
juicefs mount redis://irisesd:xxx@disgrafs.redis.rds.aliyuncs.com:6379/1 ~/Desktop/jfs --cache-dir /mycache
```

即可解决该问题。

#### 1.2.3 卸载文件系统

使用命令：

```
juicefs umount ~/Desktop/jfs
```

可以卸载文件系统。



## 2. Ray及tagging的部署

该节中的所有内容均部署在打标服务器上。

### 2.1 Ray的安装

Ubuntu20.04下的安装步骤

1.检查python版本：尽量安装python最新版本，同时确保header和worker的python版本相同。

2.如有pip，跳过此步，否则按如下安装pip：

```shell
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3 get-pip.py
```

3.更新

```shell
sudo apt update
```

4.安装ray最新发行版

```shell
pip install -U ray
pip install 'ray[default]' #美化cli界面
```

### 2.2 Ray Cluster搭建

使用命令：

```
ray start --head --port=6379
```

创建head节点。

输入header节点创立后，命令行提示中Next steps下面的第二行，

```shell
ray start --address='172.30.239.56:6379' --redis-password='5241590000000000' #视实际情况修改address
```

如果要退出集群，只需

```shell
ray stop
```

如果在启动ray头节点时出现问题，请先使用如下命令：

```
sudo service redis stop
```

之后再使用

```
ray start --head --port=6379
```

启动头节点即可。

### 2.3 tagging依赖的安装

```
pip install pdfplumber
pip install sphinx
pip install ffmpeg
pip install SpeechRecognition
pip install tinytag
pip install pydub
python3 -m nltk.downloader stopwords
python3 -m nltk.downloader universal_tagset
python3 -m spacy download en
pip install git+https://github.com.cnpmjs.org/boudinfl/pke.git #请确保以安装好git;从cnpmjs下载是为了防被墙，若可科学上网，可换为pip install git+https://github.com/boudinfl/pke.git	//upon download
```

其中，github.com.cnpmjs.org可能无法使用，可以考虑更换为其他的github镜像。

其中遇到的一些问题：

1）

```
python3 -m nltk.downloader stopwords
python3 -m nltk.downloader universal_tagset
```

这两个安装语句在安装时可能会遇到问题，报错信息如下：

![tagging_1](../../src/tagging_1.png)

解决方法如下：

打开将图中所示下载路径/root/nltk_data

![tagging_2](../../src/tagging_2.png)

将图中所示两个文件夹中所有的内容复制到以下路径：

```
/usr/local/lib/python3.8/dist-packages/nltk
```

该路径为nltk安装的路径，请根据本机情况自行调整

2）

```
python3 -m spacy download en
```

该语句在spacy版本大于等于3.0时会报错.

解决方法：将其改为以下命令

```
python3 -m spacy download en_core_web_sm
```

### 2.4 python文件中需要修改的部分

#### 2.4.1 tag_server.py

目前已知49行中：

```
wsClient = await websockets.connect('ws://47.119.121.73:9090')
```

对应的ip需要改成部署使用的服务器的对应地址。

#### 2.4.2 tagging.py

172行中：

```
filePath = "/root/jfs/" + filePath
```

对应的路径需要改为juicefs文件系统挂载在打标服务器上的路径，最后一定要加上/

建议在打标服务器上挂载时，挂载路径使用全小写。

## 3.neo4j图数据库的部署

neo4j最新版本需要使用jdk11且只能使用11，jdk的安装在此不再赘述。

在neo4j官网选择最新community版本的neo4j压缩包，在目录下解压，这里假设解压后的目录为/usr/local/neo4j

使用命令:

```
vim conf/neo4j.conf 
```

可以修改配置文件。

将其中71行的

```
# dbms.default_listen_address=0.0.0.0
```

前方的#去掉。

按下esc后输入:wq保存并退出。

修改完配置文件后，使用命令：

```
cd bin
./neo4j start
```

启动neo4j，预期看到如下消息：

![neo4j_1](../../src/neo4j_1.png)

代表neo4j启动成功。

此时用浏览器启动图上所示地址：

![neo4j_2](../../src/neo4j_2.png)

其中数据库名称不用填写，在username中填入neo4j，在password中填入需要设定的密码。点击connect后进入如下界面：

![neo4j_3](../../src/neo4j_3.png)

代表部署成功。

如想要退出neo4j服务器，只需在上述bin目录下使用：

```
./neo4j stop
```

即可



## 4. web&server部分文件修改

### 4.1 main_server目录下文件

#### 4.1.1 pytoneo.py

![neo4j_4](../../src/code_1.png)

如上所示的代码中，需要将url中的ip换为服务器对应ip，如为本机部署则可以使用localhost

然后将password换为上面进入neo4j界面时设定的密码

#### 4.1.2 serverWeb.py

![code_2](../../src/code_2.png)

将此处的url以及password作如上更改。



### 4.2 web目录下文件

#### 4.2.1 根目录下index.html

![code_3](../../src/code_3.png)

如图所示的ip换为服务器地址。

#### 4.2.2 GraphGui2目录下index.html

![code_4](../../src/code_4.png)

如图所示的地方，ip换为服务器地址。

btoa处第二个neo4j换为上面在neo4j界面设定的密码。

#### 4.2.3 GraphGui2目录下action.js

![code_5](../../src/code_5.png)

如上所示处，disgrafs://后面换为访问云数据库使用的url，ws://后面的额地址换为服务器对应ip。

#### 4.2.4 GraphGui2目录下login.js

![code_6](../../src/code_6.png)

如上所示处ip换为服务器对应ip



## 5.Client部分文件修改

这里文件应该只需修改release/DisGraFS-Client-Windows-x86_64/DisGraFS-Client.py

修改过的文件为：

[客户端程序](../code/DisGraFS-Client.py)

（见code文件夹）

细节如下：

1、Windows端juicefs挂载路径应当使用未占用盘，如X: 或Z:  这里与linux不同，linux版本juicefs挂载路径为当前已存在的目录下的一个文件夹。在上述文件中，将在X: 盘中挂载juicefs文件系统。如X：盘已占用，请自行替换代码中的相关内容。

2、Windows端python版本请使用3.8.10及以下，使用3.10版本的python会与现有asycnio库接口冲突，产生报错信息。

客户端的部分操作将在后文启动顺序进行讲解。

## 6.网页端部署

### 6.1 Apache2安装

在服务器端部署网页需要安装apache2.这里使用以下命令安装apache2:

```
sudo apt install apache2
```

安装完毕之后，在服务器端会自动创建/var/www/html 文件夹

###  6.2 端口配置

在服务器端使用如下命令关闭防火墙：

```
sudo ufw disable
```

之后，在服务器管理控制台，在安全组设置中加入连接需要的对应端口。即可正常连接。

服务器需要开放的端口有：9090、6379、7474、7687

### 6.3 网页端部署

将DisGraFS的web文件夹下的所有文件拷贝到/var/www/html/ 目录下即可。注意：访问的主页面需要命名为index.html

### 6.4 网页端访问

通过http://xxx.xxx.xxx.xxx或者http://xxx.xxx.xxx.xxx/index.html即可访问网页端。其中xxx部分换为服务器公网ip地址。

本项目部署访问地址为http://47.101.152.229/index.html

若打开网页显示无法连接到服务器，则是服务器端主程序未开启，请联系本人（

## 7.启动步骤

### 7.1 索引服务器启动

在索引服务器需要做两件事，其一为启动neo4j，其二为启动服务器端主程序。

#### 7.1.1 启动neo4j

进入neo4j的安装路径，这里以本项目服务器为例：

![启动_1](../../src/启动_1.png)

出现如上所示信息代表启动成功。

#### 7.1.2 服务器端主程序启动

进入DisGraFS项目中web&server/main_server 目录

启动serverWeb.py

![启动_2](../../src/启动_2.png)

出现如上信息代表启动成功



### 7.2 打标服务器启动

多台打标服务器需要位于同一局域网内，若使用阿里云服务器，则购置的多台服务器位于同一专用网络也可。

打标服务器需要做的有三件事：其一为挂载juicefs，其二为启动ray集群，其三为启动打标服务器程序

#### 7.2.1 挂载juicefs

在打标服务器安装并挂载juicefs，挂载的路径可以自己指定，但需要在tagging.py中将filePath修改为对应的挂载路径，具体在2.4.2节中已讲述

使用如下命令挂载juicefs：

```
juicefs mount redis://irisesd:DCchengding2003@disgrafs.redis.rds.aliyuncs.com:6379/1 /root/osh/mnt
```

![启动_3](../../src/启动_3.png)

出现如图所示信息代表挂载成功。

#### 7.2.2 ray集群启动

保持以上终端不动，重新打开一个终端。

使用如下命令启动ray集群：

```
ray start --head --port=6379
```

![启动_4](../../src/启动_4.png)

出现如上信息代表头节点启动成功，然后在位于同一局域网中的其他服务器（本台服务器也可）上使用命令：

```
ray start --address='172.23.36.108:6379'
```

启动work节点。

#### 7.2.3 打标服务器程序启动

在已经启动索引服务器端主程序的前提下，启动tag_server.py

```
python3 tag_server.py
```

在打标服务器端出现如下信息：

![启动_5](../../src/启动_5.png)

并且索引服务器端出现如下信息时：

![启动_6](../../src/启动_6.png)

打标服务器连接成功。



### 7.3 客户端配置

* 先使用DisGraFS的客户端文件夹中的setup.bat安装相关依赖，并允许添加注册表项。

* 这之后，使用文件夹中的winfsp安装程序安装winfsp，安装完毕后重启系统。

* 使用将客户端python文件修改为上述给出的python文件中的内容。

* 将浏览器设置成允许javascript脚本运行。

至此，服务器端配置成功，下面介绍启动顺序。

1）打开浏览器，输入http://47.101.152.229/index.html 看到如下界面：

![启动_7](../../src/启动_7.png)

并且索引服务器端出现如下信息：

![启动_8](../../src/启动_8.png)

代表连接成功。

之后输入挂载路径和用户名。

这里输入什么都可以，因为在客户端代码中已经将对应的挂载路径锁定为X：，防止因路径问题而崩溃。

输入之后点击BEGIN，进入如下界面：

![启动_9](../../src/启动_9.png)

注意，这里仅仅是对文件系统进行展示，如果需要在网页端对文件进行打开和删除操作，需要点击启动客户端。

点击启动客户端之后如果出现如下信息：

![启动_10](../../src/启动_10.png)

其原因为本机的ip地址未被加入云数据库的白名单中，请联系本人（

加入白名单后显示如下信息：

![启动_11](../../src/启动_11.png)

代表启动成功。这之后，请保持cmd开启，即可在网页端进行文件打开、文件删除、查看关系等操作。

一些效果预览如下：

![启动_12](../../src/启动_12.png)

点击文件旁边的tag可以查看相关tag

![启动_13](../../src/启动_13.png)

点击打开文件可以正常打开

![启动_14](../../src/启动_14.png)

搜索功能正常



## 8.issue

以上为总体服务器端部署流程以及客户端配置过程。

如配置过程中遇到问题，请在下方留言并联系本人（
