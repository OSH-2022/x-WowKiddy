# **2022 OSH team**

本文档供参考，腾讯在线文档：

​	https://docs.qq.com/doc/p/25644b07b14d29b577be03d50a7502959091d81f?dver=3.0.27601543



///**多人编辑分享项目进展的案例（要梯子）:**

/// https://docs.google.com/document/d/1qiNeVgPlleg6Mjq9WI3iS--IA5o1FbpywAcq1Do_9xI/edit?usp=sharing

///**开会、任务安排模板：**

/// https://github.com/OSH-2019/x-monthly-subscription/blob/master/discussion/2.md

///**我们需要一定的文档编辑规范以方便我们的交流：**

///（？...）代表你对某些描述的疑问或不解，后跟->(...)代表回答

///TODO:   代表待做

/// ——{...} 代表补充

///-*欢迎添加规范条例*-

# **#留言板#**

余丰：我写了下关于GPU选题的一些东西，大家再提出些其它的选题，我去看看虚拟化和GPU虚拟之类的资料。

丁程：ok

柯景瀚：富坚老贼什么时候更新啊。。。都三年多了QAQ                 ![img](https://docimg2.docs.qq.com/image/gW3sfMxKESeo3uGNrDmMcg.png?w=978&h=557)                         ![img](https://docimg2.docs.qq.com/image/W4Asrhpo67vzkYReq_ylvg.png?w=976&h=113)        



# **#任务发布区#**

| **任务名** | **备注**           | **急迫？重要？** | **猎人及自定ddl** | **进展** |
| ---------- | ------------------ | ---------------- | ----------------- | -------- |
| 好好吃饭   | 这是个例子到点就吃 | 0，1             |                   |          |

#  **#项目讨论区#**

## **；Amazing Work——实时协作系统**

### **&不成熟的想法：**

核心功能：

1. 纯文本实时编辑——代码
2. 聊天框
3. 权限
4. 文件系统——库的创立
5. 修改历史溯源
6. 先web再插件
7. 再连接时，实时更新
8. 知识图谱、NLP...把DisGraph的图搜索效果加入
9. 可视频对话

案例：

https://floobits.com/

https://aws.amazon.com/cn/cloud9/

### **&项目目标（暂定）：**

1. 实现实时协作系统的基本功能——每个节点数据通过多次访问拉取更新后的数据，服务端实现协调更新数据分布到整个系统。（应用即可为一个实时的代码编辑器）
2. 对于实时编辑器这一块的话国外的一些大厂的应用做的比较完善，如果我们往这方面走的话可能得多作出一些创新，不过我觉得更应该重视的是实时协作系统这块，并不一定要局限于做一个实时编辑器，我们实现的根本基础应该是多个客户端的数据及时交互与统一，DisGraph做到的是新增、获取、搜索、删除文件，我们应该在相关方面作出更进一步的创新，否则该项目意义不大。

### **&项目需要：**





# **#关于实时协作操作系统的可行性调研#**

## **；进展**

## **；背景与目的（what why）**

### **&目前存在的市场有关产品：**

（吴）国内有如燕麦云腾讯文档石墨文档等产品已经比较完善的实现了实时编辑等功能（如多人协同、指定权限、回溯历史版本并记录更改历史等），和我们一开始的web应用的想法较为一致，或许我们需要更进一步的创新。

（吴）Notion中的在线实时markdown编辑器功能十分完善，支持版本的记录和实时更新。（这种面向程序猿的应用国内貌似很少）

（吴）Visual Studio Live Share 的核心功能包括：

- 实时共享代码编辑
- 跟随团队其他成员的光标
- 协作调试代码
- 共享本地服务器
- 共享终端

该产品或许和我们的构想很像？

## **；【实时协作文档编辑】项目的技术路线（how）**

### **&可用轮子：**

（吴）PouchDB可以实现数据在浏览器端和服务器端的双向同步。

（吴）实现实时通信的常用方法是使用websocket，我了解的目前python有着非常完善的库，例如websocket和websockets，二者的区别在于后者对于异步通信有着更完善的支持。而如果设计web方面java的spring框架也是非常强大的工具。

Operational Transformation，即OT技术。（关注分布式OT技术）



### **&难点：**

（吴）由于是多人编辑，那么每一个客户端都可以被看作是一个发送同步数据的服务器。

我的想法是每一个客户端都可以作为一个服务器，而不是要规定一个远程服务器，在有客户退出时服务器可以进行转接，这样可以降低服务器的成本，而不是一定需要一个服务器去同步所有的客户端。

（吴）支持undo、redo似乎是一个比较难的操作。

（吴）对于不同客户端进行更改操作时造成的冲突，我们可以选用如下几种方案的一种：

1. 避免冲突，如禁止编写同一块区域。（现在大多数厂商的产品实现的就是这一种方案）。
2. 使用时间戳，将时间等级更高的写入，或是根据权限来订制规则。

（吴）其他难点主要是分布式相关，如我们需要将节点是否成功传输数据和同步数据作为一个非常重要的考虑范围，比如在异步发送数据时，可能会因为网络延迟等原因导致数据没有按照我们想要的顺序到达，这里就会出现一个显示乱序的问题。





（吴）关于难点和解决方案大家可以看看知乎这篇文章https://www.zhihu.com/question/274573543

文章中给出来一下结论：

- 如果你只是一个内部小项目，实时性要求不高，但对准确性要求比较高

- - 推荐用 merge 或 diff3 工具，出现同一行冲突时由用户来解决，这样能避免自动合并有可能出错的问题





- 如果想具备一定的实时性，流量不大，不想实现太复杂，且对少量的冲突可以忍受

- - 推荐用 Myer’s diff，后端只开一个 Node 进程





- 如果想具备实时性，且有多台后端服务同时处理

- - 可以用 Operational Transformation 或 Myer’s diff，但需要注意分布式带来的问题





- 如果需要很精细的控制，如支持富文本编辑等非单纯文本格式

- - 只能使用 Operational Transformation，但要自己实现操作合并算法，比如 XML 可以参考[这篇文章](https://link.zhihu.com/?target=http%3A//www.codecommit.com/blog/java/understanding-and-applying-operational-transformation)

# **#选题讨论区#**

## **；选题一：分布式GPU系统->单GPU虚拟化**

### **&项目目标（暂定）：**

1. 保底项目：TODO
2. （柯）基于#docker #k8s #NIVIDIA 插件实现vGPU，关键是API劫持

### **&项目需要（aka劝退信息）：**

1. （柯）现在项目涉及到容器知识
2. （柯）语言未知，语言占比未知
3. （柯）基本的OS概念
4. （柯）网络知识，随着项目深入，会涉及云
5. （余）了解GPU的基本结构，会基本的CUDA编程——{（柯）CUDA编程核心还是C}
6. （余）了解常用的硬件虚拟化手段。（？为什么有这个）->(知道其它硬件虚拟化的方法才能类比达到GPU上，当然如果从零开始可以实现的话当然也没有问题)
7. （余）了解英伟达在它的硬件方面有没有作出限制，例如对其他的GPU虚拟化的部署作出硬件层面上的限制，只允许它研发的已有的虚拟化部署，就像安卓程序很难跑在ios上。——{（柯）只能从其开源的工具调用其GPU，毕竟各家厂商GPU架构和API不太一样}
8. （柯）这是OrionX的招聘信息，可见大致需要的能力                 ![img](https://docimg4.docs.qq.com/image/-DghEzAiNFaLDageiHTDFA.png?w=974&h=552)        

## **；选题二：无人机自动寻路**

调研：1.无人机飞控 2.类似的已有实现

问题：创新点？应用场景（要考虑隐私问题）？

## **；选题三：物联网OS**



## **；选题四：使用k8s做个有趣的项目**



## **；选题五：挣大钱——实时协作系统**

核心功能：

1. 纯文本实时编辑——代码
2. 聊天框
3. 权限
4. 文件系统——库的创立
5. 修改历史溯源
6. 先web再插件
7. 再连接时，实时更新
8. 知识图谱、NLP...把DisGraph的图搜索效果加入
9. 可视频对话

案例：

https://floobits.com/

https://aws.amazon.com/cn/cloud9/

### **&项目目标（暂定）：**

1. 实现实时协作系统的基本功能——每个节点数据通过多次访问拉取更新后的数据，服务端实现协调更新数据分布到整个系统。（应用即可为一个实时的代码编辑器）
2. 对于实时编辑器这一块的话国外的一些大厂的应用做的比较完善，如果我们往这方面走的话可能得多作出一些创新，不过我觉得更应该重视的是实时协作系统这块，并不一定要局限于做一个实时编辑器，我们实现的根本基础应该是多个客户端的数据及时交互与统一，DisGraph做到的是新增、获取、搜索、删除文件，我们应该在相关方面作出更进一步的创新，否则该项目意义不大。

## **；选题六：移动端SSH**

?(余)这个是指用移动端控制PC或服务器还是在PC上用ssh连接移动端啊？

（吴）一开始的想法是移动端实现连接同步数据形成一个设备操作系统+多个设备硬件资源。





# **#vGPU任务发布区#**

| **任务名**                   | **备注**                                                     | **急迫？重要？** | **猎人及自定ddl** | **进展** |
| ---------------------------- | ------------------------------------------------------------ | ---------------- | ----------------- | -------- |
| 了解k8s                      | 典型应用对标虚拟机为什么OrionX用了这个                  ![img](https://docimg5.docs.qq.com/image/wBS55yub3AusuauY3ZIcPg.png?w=540&h=70) | 0，1             | 柯，3.13晚九点    | 已完成   |
| 基于现有信息改造vGPU选题区块 | 保证内容对应、不重复                                         | 1，1             | 柯，3.13晚十点    | 已完成   |

#  

# **#关于分布式GPU系统->单GPU虚拟化->GPU池化的可行性调研#**

## **；进展**

【3.5】（余）基于数值计算实验需要提出“分布式GPU”，较为类似的项目有https://github.com/LuxGraph/Lux（A distributed multi-GPU system for fast graph processing.）

【3.7】老师提出，将GPU虚拟化后再做分布式会更有意义，建议从单块GPU虚拟化入手。

另一方面，从趋势上看，容器化是一个趋势，目前急需解决的是在容器中提供池化的GPU资源。

【3.13】基于（柯）的调研，可以利用GaiaGPU的开源框架，研讨API劫持。



## **；vGPU的背景与目的：**

- （柯）就深度学习来看：

- - AI深入各行各业，单片高性能GPU价格昂贵，物理上不可随意分割组装，易造成碎片化浪费，于是，深度学习上云形成趋势，且任务基本采用容器化技术。

容器化优势：快速启动，可扩展，易部署

| **特性**   | **容器**           | **虚拟机**   |
| ---------- | ------------------ | ------------ |
| 启动       | 秒级               | 分钟级       |
| 硬盘使用   | 一般为MB           | 一般为GB     |
| 性能       | 接近原生           | 弱于         |
| 系统支持量 | 单机支持上千个容器 | 一般是几十个 |

- - 随之而来的痛点问题

  - - 容器的GPU利用率不够高，特别是推理任务；
    - 为了提高GPU的利用率、避免算力浪费，需要在单个GPU上运行多个容器；
    - 业内已有方案（NV的vGPU 或MPS、基于rCUDA的方案等）存在各种问题，标准容器下GPU不可共享，MPS容器无法完成故障隔离，rCUDA、vCUDA等用了API remoting的要更新CUDA库（基本上没人继续支持开源项目的迭代）。

- （余）矩阵乘法和图形渲染本质上都是调用GPU内的函数，我觉得重要的是可以让两个GPU跑一个kernel函数
- （柯）这篇文章[https://cloudtweaks.com/2016/06/virtual-reality/ ](https://cloudtweaks.com/2016/06/virtual-reality/)介绍了vGPU在虚拟现实生态的应用，比如VR需要实时的图形计算，如果有了vGPU，那么用户不必购入昂贵的硬件，直接在云上申请一个GPU（一般是进行GPU切片化管理，避免资源浪费，这里不一定真是一个）进行调用。那么作为服务公司，也许一个性能不错的GPU便可至少同时给两三个用户进行调用。

【而（余）的意思是】：一般来说，我们榨不干一个GPU的算力，但当涉及到大型计算项目时，一个不一定满足得了需求，我需要多个GPU去跑一个类型的计算（“让两个GPU跑一个kernel函数”）。

【虚拟化目的及意义】：类似于科大的VLAB同时给很多同学提供同量级服务，一个GPU同时被多个用户使用而不受影响（这也是虚拟化的定义），这样可以避免资源的浪费（只要有动态资源自动化调用便有OS）；而当某实验室需要多个GPU跑同一类计算时，可以直接在云上申请调度多个GPU进行自用，而我们在远端整合闲置的GPU资源以回应该申请，这样也可以避免资源的浪费。

​                 ![img](https://docimg10.docs.qq.com/image/hZDt-qshkbe-YSHf2KEOlQ.png?w=1060&h=347)        

- （柯）Orion产品介绍里的图，（余）的意思是“化零为整”，我补充描述了“化整为零”，我认为VR需要“隔空取物”（这太棒了）

​                 ![img](https://docimg1.docs.qq.com/image/6AOlgpo8-yKdPcnkb6IFOA.png?w=1081&h=729)        

​                 ![img](https://docimg4.docs.qq.com/image/S1hRaKgHn0aHADF4uGcW0A.png?w=1101&h=775)                         ![img](https://docimg9.docs.qq.com/image/l173lgbYD3PnbeDvHnXiWA.png?w=872&h=606)                         ![img](https://docimg2.docs.qq.com/image/nbIhXGNsbV9hLjI3n78cmg.png?w=870&h=547)        

- -*欢迎提出你的调研结果与想法...*-



## **；vGPU项目的技术路线：**

### **&实现vGPU：**

- （柯）

-非容器化的几种方式：

1. GPU直通模式，即GPU透传 

2. 1. 不够灵活，还是能分细粒度的技术好
   2. 当然，不排除其实用性

3. API remoting

4. LoGV的半虚拟，VMware的全虚拟

5. GPU SR-IOV，目前主要是AMD在采用此种方案

6. 1. SR-IOV（Single Root I/O Virtualization）
   2. 【在进行进一步调研】

7. GPU分片虚拟化，包括Intel GVT-g（开源）和NVIDIA GRID vGPU

8. 1. 分片虚拟化与透传的区别是，分片虚拟化把会影响性能的访问直接透传给虚拟机，把性能无关和功能性的MMIO访问做拦截并在mdev模块内做模拟

9. （丁）基于设备仿真的虚拟化方式                 ![img](https://docimg9.docs.qq.com/image/RqGpp3rhnKO5dUKekDCxtA.png?w=1280&h=857.8110944527735)        

10. 1. 性能较为受限（参考QEMU）

-容器化：

现在最新的技术，是基于容器

**vGPU device plugin** 基于NVIDIA官方插件([NVIDIA/k8s-device-plugin](https://gitee.com/link?target=https%3A%2F%2Fgithub.com%2FNVIDIA%2Fk8s-device-plugin))，在保留官方功能的基础上，实现了对物理GPU进行切分，并对显存和计算单元进行限制，从而模拟出多张小的vGPU卡。在k8s集群中，基于这些切分后的vGPU进行调度，使不同的容器可以安全的共享同一张物理GPU，提高GPU的利用率。此外，插件还可以对显存做虚拟化处理（使用到的显存可以超过物理上的显存），运行一些超大显存需求的任务，或提高共享的任务数，可参考[性能测试报告](https://gitee.com/teacherandchang/k8s-device-plugin#性能测试)。

- （柯）OrionX也是k8s+NV插件

- - OrionX 产品介绍  https://blog.csdn.net/m0_49711991/article/details/107979798
  - 算力资源池化解决方案技术白皮书 https://virtaitech.com/product.pdf
  - [使用k8s容器化部署Orion vGPU组件](https://github.com/virtaitech/orion/blob/master/orion-kubernetes-deploy) 
  - [Kubernetes-Orion-Plugin 在k8s集群中调度vGPU资源](https://github.com/virtaitech/orion/blob/master/doc/Orion-k8s-device-plugin.md)

- （柯）新思路：阿里云研制的cGPU项目说：适配开源标准的Kubernetes和NVIDIA Docker方案。也就是他们的v化是基于容器实现，而不是Hypervisor，同时使用了NV的container toolkit

- - 【什么是GPU容器共享技术cGPU】 [https://help.aliyun.com/document_detail/203715.htm?spm=a2c4g.11186623.0.0.223229echdCtcc#concept-2041879 ](https://help.aliyun.com/document_detail/203715.htm?spm=a2c4g.11186623.0.0.223229echdCtcc#concept-2041879)                 ![img](https://docimg7.docs.qq.com/image/7y7smtSntoms3IXWtkJ66g.png?w=688&h=342)        

- （丁）找到一个用k8s做vGPU的项目 https://github.com/4paradigm/k8s-device-plugin

- （柯）关于18年腾讯与北大实验室发表的GaiaGPU论文的调研

- - 原论文（自己加了些注释）GaiaGPU_Sharing_GPUs_in_Container_Clouds.pdf

  - - 乱逛发现的中文解读，对一些工具进行了解释（有兴趣或精力的话还是建议看原文）[https://github.com/pokerfaceSad/pokerfaceSad.github.io/blob/abac8763546ceb0688af261d780670a8c78f41f6/2020/02/07/%E8%AE%BA%E6%96%87%E7%AC%94%E8%AE%B0%E3%80%8AGaiaGPU%20Sharing%20GPUs%20in%20Container%20Clouds%E3%80%8B/index.html](https://github.com/pokerfaceSad/pokerfaceSad.github.io/blob/abac8763546ceb0688af261d780670a8c78f41f6/2020/02/07/论文笔记《GaiaGPU Sharing GPUs in Container Clouds》/index.html)

  - GaiaGPU部署 https://github.com/wang-junjian/wang-junjian.github.io/blob/6c8c04653ca16369570fdee48fe7ad32e9defbcb/_posts/2022-01-28-gaiagpu-sharing-gpus-in-container-clouds.markdown

  - - GPU-manager https://github.com/tkestack/gpu-manager
    - vCUDA-controller https://github.com/tkestack/vcuda-controller

  - 总结：框架展示得很清晰，但vCUDA那块说得很含糊，[“API劫持是可以玩出很多花样的”](https://github.com/zw0610/zw0610.github.io/blob/590807456e6fc7af194d0a247984927d294437d7/notes-cn/gpu-sharing-3.md)

- （柯）一些人的见解

- - [https://github.com/zw0610/zw0610.github.io/tree/590807456e6fc7af194d0a247984927d294437d7 ](https://github.com/zw0610/zw0610.github.io/tree/590807456e6fc7af194d0a247984927d294437d7)

  - - ​                 ![img](https://docimg8.docs.qq.com/image/6VryohDuEkEy8J1P-ssqNA.png?w=337&h=364)        
    - 我就是那个“既不懂GPU也不懂DL的人”QAQ                 ![img](https://docimg9.docs.qq.com/image/NscaOCQuPpDv-whza4xmIQ.png?w=907&h=259)        

### **&vGPU->GPU池化**

- （柯）OrionX也是

OrionX的GPU资源池化演进图（破解OrionX（逃）->（认真））

​                 ![img](https://docimg9.docs.qq.com/image/AToM-d77lTkw4TAn-B-QEA.png?w=911&h=593)        

- -*欢迎提出你的调研结果与想法...*-