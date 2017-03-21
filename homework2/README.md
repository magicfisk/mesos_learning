# 第二次作业
## 一、mesos
### 1.mesos的组成结构
![mesos](https://github.com/magicfisk/mesos_learning/blob/master/homework2/mesos.png)<br>
#### mesos的主要部件有<br>
* master：管理节点，负责接受slave和framework的注册，管理资源的初始分配<br>
* slave(agent)：接受master对任务的调度，将对应executor运行,定期向master汇报资源情况<br>
* Framework：包括两个实体，scheduler和executor<br>
* scheduler：注册到master，接受master提供的Resource offer信息，决定在提供的slave上运行什么executor，或者是放弃不用<br>
* executor：由slave实际负责加载运行，但由scheduler管理<br>
#### 辅助的部件<br>
* zookeeper：选举master的部件，在master掉线后，提供master的候选人，恢复状态<br>
### 部件的代码位置
* master：mesos-1.1.0/src/master<br>
* slave：mesos-1.1.0/src/slave<br>
* scheduler：mesos-1.1.0/src/scheduler<br>
* executor：mesos-1.1.0/src/executor<br>
* zookeeper：mesos-1.1.0/src/zookeeper<br>
### mesos工作流程
(1)注册<br>
* framework启动后，向master注册<br>
* slave启动后也向master注册<br>
(2)资源分配和运行<br>
![offer](https://github.com/magicfisk/mesos_learning/blob/master/homework2/offer.png)<br>
* slave定期向master报告自己的资源情况<br>
* master通过Resource Offer机制，告诉framework可以调用的资源<br>
* framework根据自己的task情况，决定是否使用master提供的资源，并回复master关于task和资源的匹配情况<br>
* master获得framework的分配结果，向slave发送对应的task<br>
* slave得到task后，加载executor，运行相应的程序<br>
## Spark On Mesos
![Spark](https://github.com/magicfisk/mesos_learning/blob/master/homework2/spark.png)<br>
  mesos取代了spark原来结构中的Cluster Manager,用户向spark提交任务,mesos决定任务在那个slave上执行,Slave从spark中获取SparkContext用于任务执行<br>
### 与操作系统的比较<br>
#### 相同
* mesos架构和操作系统同样对资源进行了封装，用户不用在意底层硬件的结构，只要关注硬件的数目
* 涉及到底层的操作，最终还是要靠mesos或者内核来实现（例如操作系统中的IO操作，mesos中的任务调度），保证了安全性
#### 不同
* 操作系统中因为资源是集中的，用户只需要关心自己获得资源总量即可。而mesos的分布式系统，资源的分散，使得用户需要对资源评估，是否能满足单个任务。mesos中用户负担的任务更加重。
* mesos系统中，用户需要考虑个别agent挂掉的情况，而操作系统中，无需担心
* 分布式系统使得系统的算法也会发生改变。
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
### 背景
在粒子系统中，我们需要对每一个粒子进行轨迹计算，来获得整体的逼真的细节。粒子轨迹的计算有非常好的可并行性，适合分布式系统。<br>
### 问题化简
把一个粒子的轨迹看作一个抛物线，给出了每个粒子的抛物线方程，统计粒子最后落在负半轴还是正半轴。（就是右计算零点233）<br>
### 细节
代码在mypy\examples中，make_data为数据制造器，基于pymesos实现<br>
测试生成了10000组数据，分成10个任务(第11个任务为空),分发到3个机器上运行<br>
### 运行
![running](https://github.com/magicfisk/mesos_learning/blob/master/homework2/running.png)<br>
命令行中成功返回了最终的统计结果<br>
![runing2](https://github.com/magicfisk/mesos_learning/blob/master/homework2/runing2.png)<br>
在mesos资源查看网页中，能看到任务分到不同机器上运行<br>
### 代码
只对核心功能代码进行描述，具体见mypy/examples下相关代码
#### scheduler

```
class MinimalScheduler(Scheduler):

    def __init__(self, executor):
        self.executor = executor
        self.Task_launched=0
        self.Task_finished=0
        self.file_end=False
        self.right=0
        self.left=0
        self.f1=open('data.txt','r')
```
* 初始化变量，Task_launched已经分发的任务，Task_finished为已经结束的任务，file_end表示文件读完，f1为文件，right和left为统计变量

```
    def resourceOffers(self, driver, offers):
    
        def get_data(self):
            tmp1='';
            for x in range(1,TASK_MaxNum):
                tmp=self.f1.readline();
                if tmp=='':
                    self.file_end=True
                    break
                tmp1=tmp1+tmp
            return tmp1    
```
* 读入数据的函数，作为resourceOffers的一个子函数

```
        for offer in offers:
            cpus = self.getResource(offer.resources, 'cpus')
            mem = self.getResource(offer.resources, 'mem')
            if cpus < TASK_CPU or mem < TASK_MEM or self.file_end:
                continue
            self.Task_launched=self.Task_launched+1
```
* 准备分发任务前的准备，将计数器增加
```
            task = Dict()
            task_id = str(uuid.uuid4())
            task.task_id.value = task_id
            task.agent_id.value = offer.agent_id.value
            task.name = 'task {}'.format(task_id)
            task.executor = self.executor
            
            task.data = encode_data(get_data(self))  #读入数据，并且存入task
			
            task.resources = [
                dict(name='cpus', type='SCALAR', scalar={'value': TASK_CPU}),
                dict(name='mem', type='SCALAR', scalar={'value': TASK_MEM}),
            ]
```
* 对task的封装

```
            driver.launchTasks(offer.id, [task], filters) 
```
* 调度任务

```
    def statusUpdate(self, driver, update):       
        print ('%d Task has finished,%d task has launched' %(self.Task_finished,self.Task_launched))
        #如果所有任务结束，并且文件读完则停止framework
        if self.file_end:
            if self.Task_finished==self.Task_launched:
                print ('\nthere is %d balls in the left,and %d balls in the right\n' % (self.left,self.right))
                driver.stop()
```
* 状态更新回调函数

```
    def frameworkMessage(self, driver, executorId, slaveId, message):
        ans=decode_data(message)
        print ('get an ans %s' %ans)
        ans=ans.split(' ')
        self.left=self.left+int(ans[0])
        self.right=self.right+int(ans[1])
        self.Task_finished=self.Task_finished+1
```
* 接受agent计算结果并且统计的函数

```
def main(master):
	...
	
```
* 完成对环境变量的封装
#### executor
```
class MinimalExecutor(Executor):
    def launchTask(self, driver, task):
        def run_task(task):
            
            update = Dict()
            update.task_id.value = task.task_id.value
            update.state = 'TASK_RUNNING'
            update.timestamp = time.time()
            driver.sendStatusUpdate(update)
```
* 更新状态，表明任务开始
```
            data=decode_data(task.data)
            data=data.split('\n')
			left=0
            right=0
            ans=''
```
* 解析数据、初始化变量
        
```
            for x in data:
                if x=='':
                    break
                tmp=x.split(' ')
                a=float(tmp[0])
                b=float(tmp[1])
                c=float(tmp[2])
                deta=math.sqrt(b*b-4*a*c)
                pt=(-deta-b)*0.5/a
                if pt>0:
                    right=right+1
                else:
                    left=left+1
```
* 计算
```
            ans=str(left)+' '+str(right)
            driver.sendFrameworkMessage(encode_data(ans))
```
* 返回计算结果

```
            update = Dict()
            update.task_id.value = task.task_id.value
            update.state = 'TASK_FINISHED'
            update.timestamp = time.time()
            driver.sendStatusUpdate(update)
```
* 更新状态，表明计算结束
