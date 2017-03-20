# 第二次作业
## 一、mesos
### 1.mesos的组成结构
@插入图片<br>
mesos的主要部件有<br>
master：管理节点，负责接受slave和framework的注册，管理资源的初始分配<br>
slave(agent)：接受master对任务的调度，将对应executor运行,定期向master汇报资源情况<br>
Framework：包括两个实体，scheduler和executor<br>
scheduler：注册到master，接受master提供的Resource offer信息，决定在提供的slave上运行什么executor，或者是放弃不用<br>
executor：由slave实际负责加载运行，但由scheduler管理<br>
辅助的部件<br>
zookeeper：选举master的部件，在master掉线后，提供master的候选人，恢复状态<br>
### 部件的代码位置
master：mesos-1.1.0/src/master<br>
slave：mesos-1.1.0/src/slave<br>
scheduler：mesos-1.1.0/src/scheduler<br>
executor：mesos-1.1.0/src/executor<br>
zookeeper：mesos-1.1.0/src/zookeeper<br>
### mesos工作流程
(1)注册<br>
framework启动后，向master注册<br>
slave启动后也向master注册<br>
(2)资源分配和运行<br>
@插入图片<br>
slave定期向master报告自己的资源情况<br>
master通过Resource Offer机制，告诉framework可以调用的资源<br>
framework根据自己的task情况，决定是否使用master提供的资源，并回复master关于task和资源的匹配情况<br>
master获得framework的分配结果，向slave发送对应的task<br>
slave得到task后，加载executor，运行相应的程序<br>
## Spark On Mesos
@插入图片<br>
mesos取代了spark原来结构中的Cluster Manager<br>
用户向spark提交任务<br>
mesos决定任务在那个slave上执行<br>
Slave从spark中获取SparkContext用于任务执行<br>
### 与操作系统的比较<br>
@@待补<br>
## master和slave的初始化过程
### master的初始化
代码位置mesos-1.1.0/src/master/master.cpp 、main.cpp<br>
master的起始位置是main.cpp<br>
master的初始化主要过程为(忽略了日志等操作)：<br>
```
(1)Validate flags
   处理命令行参数，设置环境变量
(2)Libprocess
   初始化底层的通信协议库，mesos基于Libprocess实现master和slave的通信
(3)Version process
   用于返回http请求的版本号
(4)Firewall rules
   设置防火墙的相关规则
(5)Modules
   加载用户运行时需要的库，模型的加载使得mesos有较好可扩展性，无需每次都编译来加载新的库函数
(6)Anonymous modules
   加载匿名模型
(7)Hooks
   初始化hook模块
(8)Allocator
   创建一个分配模块
(8)Registry storage
   存储空间的初始化和确认
(9)Master contendor
   竞争leader
(10)Master detector
    检测当前master的模块
(11)Authorizer
   认证模块
(12)Slave removal rate limiter
   用于流量限制的初始化，防止master被过量的slave请求淹没？
(13)Master process
  Master* master =
    new Master(
      allocator.get(),
      registrar,
      &files,
      contender,
      detector,
      authorizer_,
      slaveRemovalLimiter,
      flags);
   利用上述参数构建一个新的master实例。
```
在master.cpp中，master类中自带一个Initialize类函数，但没有找到调用的地方<br>
### slave的初始化<br>
部分同master，不再展开<br>
```
(1)Windows socket stack.
   若在windows环境中，初始化windows的scoket栈
(2)Validate flags
(3)Libprocess
(4)Version process
(5)Firewall rules
(6)Modules
(7)Anonymous modules
(8)contender/detector
(9)Hooks.
(10)Systemd support
   如果是linux系统，初始化systemmd，启动各种服务
(11)Fetcher and Containerizer.
   初始化fetcher用于资源下载，初始化containerizer作为slave的容器
(12)Master detector.
(13)Authorizer.
(14)Garbage collector
   初始化垃圾回收器
(17)Status update manager
   状态更新管理器
(18)Resource estimator
   资源评估器
(19)QoS controller
   初始化Qos控制器，用于服务质量控制(?)
(20)slave process.
  Slave* slave = new Slave(
      id,
      flags,
      detector,
      containerizer.get(),
      &files,
      &gc,
      &statusUpdateManager,
      resourceEstimator.get(),
      qosController.get(),
      authorizer_);
   利用上述参数构建一个新的slave实例。
```
## Mesos的资源调度算法
### 1.算法简述
mesos采用的资源调度算法为DRF<br>
并行计算的资源是多维的，主要为cpu和内存，而task对于不同资源需求的比例也不同，如何公平得分配资源？<br>
DRF引入了dominant resource的概念，即占系统比例最大的资源。例如集群有4个cpu，16G内存，一个task需要2个cpu，4G内存<br>
那么这个task的dominant resource为cpu（占总资源的50%），而不是内存（占总资源25%）<br>
DRF的核心思想是保证每个framework获得的dominant resource占系统比例差不多<br>

DRF的算法流程为：<br>
* 找到一个dominant resource分配最少的framework<br>
* 分配framework下一个task需要的资源<br>
* 重新计算dominant resource，回到第一步<br>

DRF针对任务的优先级，引入了权重的概念。在挑选framework时，framework的dominant resource除以权重，使得高优先级的框架有更多的资源，而低优先级的框架也能分到少量资源<br>
### 代码
位置：mesos-1.1.0\src\master\allocator<br>
从allocator.cpp可以看出，默认是采用HierarchicalDRFAllocator<br>
其中sorter.cpp中实现了framework的排序和分配<br>
hierarchical.cpp实现了framework，slave的管理和状态的维护<br>
hierarchical中实现了filter功能，允许framework事先拒绝一些过小的资源，避免反复询问的通信浪费<br>
### 看法
DRF解决了多维度的资源分配的公平性，当时却不一定解决了整体系统的利用率的，对于一些资源需求比例畸形的任务，DRF不一定有很高的效率<br>
## 写一个完成简单工作的框架(语言自选，需要同时实现scheduler和executor)并在Mesos上运行
背景：在粒子系统中，我们需要对每一个粒子进行轨迹计算，来获得整体的逼真的细节。粒子轨迹的计算有非常好的可并行性，适合分布式系统。<br>
化简：把一个粒子的轨迹看作一个抛物线，给出了每个粒子的抛物线方程，统计粒子最后落在负半轴还是正半轴。（就是右计算零点233）<br>
代码在mypy\examples中，make_data为数据制造器，在pymesos的scheduler上重载了一些api实现了新的功能，具体见代码<br>

