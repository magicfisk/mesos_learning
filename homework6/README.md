# 第6次作业
## paxos算法
### 概念：
* Proposer ：提议者
* Acceptor：决策者
* Client：产生议题者
* Learner：最终决策学习者
* 关键角色为提议者和决策者
### prepare阶段
1.proposer选择一个提案编号n并将prepare请求pre(n)发送给所有acceptors<br>
2.acceptor收到prepare消息后，如果提案的编号大于它已经回复的所有prepare消息，则acceptor将自己上次accept的提案回复给proposer（n',v'）（没有则发送ok），并承诺不再回复小于n的提案<br>
### accept阶段
对于propose：<br>
1.propose收到半数以上的回复，若所有人的回复都是ok，那么propose发送accept(n,v)给所有回复的人,v是client提供给自己的值<br>
2.若propose收到的回复中有不是ok的，选择（ni,vi）中ni最大对应的vi，发送accept（n,vi）给所有回复的人。<br>
3.propose收到的回复不到一半，则提议失败，增加自己的提案编号n，回到prepare中的1 <br>
对于accpetor：<br>
收到的accept(n,v)
1.其中n小于自己接受过的n，则丢弃<br>
2.n大于自己接受的n，接受，并且回复accept-ok<br>
对于propose：
1.收到半数的accept-ok，提议成功，通知learner更新<br>
2.没有收到半数的accpet-ok，提议失败，修改n，回到prepare的1阶段<br>
### 算法正确性
* 上述算法只有在accept的回复全部为ok的时候，才能采纳新的value。<br>
* 只有被半数以上acceptor接受的value才能被认可。<br>
* prepare阶段要求回复的人必须大于一半，所以若存在被认可的值，则一定会被返回（两个大于一半的集合一定有交集）<br>
* 任何大于编号大于被认可提案的提案提出值一定是认可的值<br>
* 只要被认可值产生后，这个值就会被确定，从而一致。<br>
### 算法的缺陷
* 存在活锁问题：
容易发现在认可的值确定之前，各种提案的编号不断上升，而导致产生超过半数的accept-ok。<br>
![pic1](https://github.com/magicfisk/mesos_learning/raw/master/homework6/lock.png)<br>
如上图：
* 1，2，3回复了1的pre(n1)
* 3，4，5回复了5的pre(n5)，3从接受1改为接受5
* 1，2回复了accept(n1,v1)，但3因为5的原因不回应，1失败，重新发起prepare
* 1，2，3回复了1的pre(n1')，3从接受5变为接受1
* 4，5回复了5的accept(n5，v5)，5失败，重新发起prepare
* 3改为接受5，1失败，3改，5失败……。所以永远也不可能达成一致。
* 解决方案：指定一个leader，来负责发送propose，控制执行顺序，保证propose不会互相干扰。leader下线，需要执行选举算法，选举一个新的leader
## 模拟Raft协议工作的一个场景并叙述处理过程
* 集群被分成2个子网，无法互相通信，raft如何处理
* 其中B为原leader，C为子网中新竞选出来的leader
![pic2](https://github.com/magicfisk/mesos_learning/raw/master/homework6/net1.jpg)<br>
---
* client向B发送消息set3，B只能收到A的回应，没有大于一半，所以B无法更新值
![pic3](https://github.com/magicfisk/mesos_learning/raw/master/homework6/net2.jpg)<br>
---
* client向C发送消息set8，C能收到半数以上的回应，C向client发送更新成功的信号
![pic4](https://github.com/magicfisk/mesos_learning/raw/master/homework6/net3.jpg)<br>
---
* 网络恢复后，B,C同时发送心跳信号，这时A，B发现了一个更高级的leader，两者同时变为未提交状态，接受C的提交信息，之后A,B的状态则变成和C一致
![pic5](https://github.com/magicfisk/mesos_learning/raw/master/homework6/net4.jpg)<br>
## mesos的容错机制和验证
### 容错机制
* mesos的容错机制体现在四个方面：master出错、slave出错，executor出错，framework崩溃
* master出错
Mesos使用热备份（hot-standby）设计来实现Master节点集合。一个Master节点与多个备用（standby）节点运行在同一集群中，并由开源软件Zookeeper来监控。Zookeeper会监控Master集群中所有的节点，并在Master节点发生故障时管理新Master的选举。Mesos的状态信息实际上驻留在Framework调度器和Slave节点集合之中。当一个新的Master当选后，Zookeeper会通知Framework和选举后的Slave节点集合，以便使其在新的Master上注册。新的Master可以根据Framework和Slave节点集合发送过来的信息，重建内部状态。<br>
* slave
Mesos实现了Slave的恢复功能，当Slave和master失去连接时，可以让执行器/任务继续运行。当任务执行时，Slave会将任务的监测点元数据存入本地磁盘。当Master重新连接Slave，启动slaver进程后，因为此时没有可以响应的消息，所以重新启动的Slave进程会使用检查点数据来恢复状态，并重新与执行器/任务连接。当slave多次无响应，重连接失败，master会删除这个slave节点。
* executor出错
当Slave节点上的进程失败时，mesos会通知framework，让framework决定下一步的处理。<br>
* framework崩溃
Framework调度器的容错是通过Framework将调度器注册2份或者更多份到Master来实现。当一个调度器发生故障时，Master会通知另一个调度来接管。这个需要调度器自己实现。
### 验证
#### master出错
* 安装、配置zookeeper
* 修改zookeeper的配置文件
```
vi /etc/zookeeper/conf/myid
内容为master id,分别设置为1，2，3

vi/etc/zookeeper/conf/zoo.cfg
设置选举端口和通信端口
server.1=172.16.6.2:2888:3888
server.2=172.16.6.153:2888:3888
server.3=172.16.6.249:2888:3888
```
* 启动master
```
mesos master --zk=zk://172.16.6.249:2181,172.16.6.153:2181,172.16.6.2:2181/mesos --quorum=2 --ip=172.16.6.2  --hostname=mas1 --work_dir=/var/lib/mesos --log_dir=/var/log/mesos
mesos master --zk=zk://172.16.6.249:2181,172.16.6.153:2181,172.16.6.2:2181/mesos --quorum=2 --ip=172.16.6.153 --hostname=mas2 --work_dir=/var/lib/mesos --log_dir=/var/log/mesos
mesos master --zk=zk://172.16.6.249:2181,172.16.6.153:2181,172.16.6.2:2181/mesos --quorum=2 --ip=172.16.6.249 --hostname=mas3 --work_dir=/var/lib/mesos --log_dir=/var/log/mesos
```
* 如果我们kill掉leader，在log中我们能看到
```
I0529 04:20:10.016351 60160 network.hpp:432] ZooKeeper group memberships changed
I0529 04:20:10.021173 60160 network.hpp:480] ZooKeeper group PIDs: {  }
I0529 04:20:11.354900 60159 detector.cpp:152] Detected a new leader: (id='2')
I0529 04:20:11.355798 60159 group.cpp:697] Trying to get '/mesos/json.info_0000000002' in ZooKeeper
I0529 04:20:11.358307 60159 zookeeper.cpp:259] A new leading master (UPID=master@172.16.6.153:5050) is detected
I0529 04:20:11.358961 60159 master.cpp:2017] Elected as the leading master!
I0529 04:20:11.359378 60159 master.cpp:1560] Recovering from registrar
I0529 04:20:11.362989 60163 log.cpp:553] Attempting to start the writer
```
* zookeeper从备选的master中重新选举了一个leader
#### slave出错、executor出错
* 验证的结果是task-lost和task-fail，目前来看，这和framework的算法有关，由用户自行处理
#### framework崩溃
* kill的结果直接就是框架结束了，若要实现容错，需要自己注册多个框架，这里就不验证了
## 综合作业
* 总体思路
1.利用etcd的kv对来保存host和ip的对应<br>
2.每个ip在需要为自己在kv对中维护自己ip对应的alive标记，设置ttl，在挂了之后标记自动失效<br>
3.leader节点利用2中的信息，需要维护hostname和ip的对应<br>
4.每个主机都要读取leader维护的hostname-ip表，并更新自己本地的host<br>
5.利用分布文件系统共享ssh的id_rsa.pub，实现免密登入<br>



