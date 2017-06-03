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
* 总体思路<br>
1.利用etcd的kv对来保存host和ip的对应<br>
2.每个ip在需要为自己在kv对中维护自己ip对应的alive标记，设置ttl，在挂了之后标记自动失效<br>
3.leader节点维护leader目录下自己的alive标记，follwer节点维护follwer目录下的alive标记<br>
4.每个主机都要读取alive标记，可以计算出host表<br>
5.利用分布文件系统共享ssh的id_rsa.pub，实现免密登入<br>
### 准备工作
* 创建一个docker镜像，装好python、etcd、jupyter、vim、openssh-serverd等等
```
FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y wget

RUN wget -P /root https://github.com/coreos/etcd/releases/download/v3.1.7/etcd-v3.1.7-linux-amd64.tar.gz && tar -zxf /root/etcd-v3.1.7-linux-amd64.tar.gz -C /root
RUN ln -s /root/etcd-v3.1.7-linux-amd64/etcd /usr/local/bin/etcd && ln -s /root/etcd-v3.1.7-linux-amd64/etcdctl /usr/local/bin/etcdctl

RUN apt-get update
RUN apt-get install -y ssh
RUN apt-get install -y openssh-server
RUN apt-get install -y python3-pip
RUN apt-get install -y vim
RUN pip3 install jupyter
RUN apt-get install -y sudo
ADD /mnt/code.py /home/admin/code.py
RUN useradd admin
RUN echo "admin:admin" | chpasswd
RUN echo "admin   ALL=(ALL)       ALL" >> /etc/sudoers
RUN mkdir /var/run/sshd

# 开放22端口并运行jupyter
EXPOSE 22
USER admin
WORKDIR /home/admin

CMD ["/bin/bash"]
```
* 为每个容器编写一个守护程序
```
import subprocess, sys, os, socket, signal, json, time
import urllib.request, urllib.error
from sys import argv

#通过ip和集群的list列表，启动etcd集群
def etcd(ip,list):
	args = ['etcd', '--name', 'p'+ip[-1], '--initial-advertise-peer-urls', 'http://'+ip+':2380','--listen-peer-urls', 'http://'+ip+ ':2380','--listen-client-urls', 'http://'+ip+':2379,http://127.0.0.1:2379','--advertise-client-urls', 'http://'+ip+':2379','--initial-cluster-token', 'etcd-cluster-hw5','--initial-cluster', list ,'--initial-cluster-state', 'new']
	subprocess.Popen(args)

#通过etcd的集群，计算host表
def update_host(n):
	f=open("tmp-host","w")
	err=0
	for i in range(0,n):
		tag=os.system('etcdctl get /leader/192.0.1.10' + str(i))
		if tag==0: #如果值存在，则返回值为0，否则为1024
			f.write("192.0.1.10" + str(i)+" host0\n")
			break
	cnt=1
	for i in range(0,n):
		tag=os.system('etcdctl get /follower/192.0.1.10' + str(i))
		if tag==0:
			f.write("192.0.1.10" + str(i)+" host"+str(cnt)+"\n")
			cnt=cnt+1
	f.close()
	os.system("cp tmp-host /etc/hosts") #将计算出来的值拷贝到本机hosts
	

def main():

	script,ip,nodeN = argv #获取参数，本机ip和总节点数目
	
	os.system('ssh-keygen -f /home/admin/.ssh/id_rsa -t rsa -N ""') #为本机的ssh访问产生密钥
	os.system('sudo -S bash -c "cat /home/admin/.ssh/id_rsa.pub >> /mnt/authorized_keys"') #将公钥拷贝到分布式文件系统中
	os.system("/etc/init.d/ssh start") #启动ssh服务
	
	n=int(nodeN)
	leader_flag=0
	list="p0=http://192.0.1.100:2380"
	#构造集群列表
	for i in range(1,n):
		list=list+",p"+str(i)+"=http://192.0.1.10"+str(i)+":2380"
	
	#启动etcd服务
	etcd(ip,list)
	
	stats_url = 'http://127.0.0.1:2379/v2/stats/self'
	stats_request = urllib.request.Request(stats_url)
	
	#以下部分为守护进程的代码
	while True:
		try:
			stats_reponse = urllib.request.urlopen(stats_request)
		except urllib.error.URLError as e:
			print('[WARN] ', e.reason)
			print('[WARN] Wating etcd...')

		else:
			stats_json = stats_reponse.read().decode('utf-8')
			data = json.loads(stats_json)
			#利用etcd集群的接口，判断自己是不是leader
			if data['state'] == 'StateLeader':
				if leader_flag == 0: #如果是第一次成为leader，需要启动jupyter
					leader_flag = 1

					args = ['jupyter', 'notebook', '--NotebookApp.token=', '--ip=0.0.0.0', '--port=8888']
					subprocess.Popen(args)
				# 更新自己leader的alive标记	
				os.system('etcdctl set /leader/' + ip + ' ' + "1 --ttl 30")
				#leader负责将host表拷贝到联合文件系统中，方便外面查看
				os.system("sudo cp tmp-host /mnt/hosts")
				
			elif data['state'] == 'StateFollower':
				# 更新自己作为follwer的alive标记
				os.system('etcdctl set /follower/' + ip + ' ' + "1 --ttl 30")
		#更新完标记后，每个主机计算最新的host表
		update_host(n)
		#守护进程的频率为10s一次
		time.sleep(10)


if __name__ == '__main__':
	main()
```
* 计算host的原理<br>
利用etcdctl get命令，我们试图去访问alive标记，如果节点存在，则访问成功，否则访问失败<br>
所以先访问leader目录下的标记，确定host0<br>
然后根据follwer目录下，进行顺序访问，确定其余的host<br>
由于etcd能够保证kv值一致，所以所有主机计算出来的host-ip表也是一致的<br>
* alive更新<br>
因为kv有ttl，所以一旦主机死了，kv就会失效<br>
守护程序每10s更新一次alive，而ttl设置为30s，所以只要主机健康，就不会掉线<br>
* 如何达成ssh的免密码访问<br>
原理：ssh服务通过本地的authorized_keys文件确定信任的主机，A主机将rsa加密中的公钥存在B主机的authorized_keys文件中，A登入B时候，B发送一个通过公钥加密的随机字符串，A返回利用私钥解密的字符串，B验证字符串正确，然后放行A。<br>
关键：只要authorized_keys中有来访者的公钥就可以免密登入<br>
实现：<br>
1.需要修改sshd的配置文件,使得authorized_keys的文件位置重定位到/mnt/中，即所有集群共享用一个authorized_keys。<br>
2.每个主机启动后，将自己的公钥加入/mnt/authorized_keys中，这样所有其他主机都能成为信任对象。<br>
* mesos的framework，基本可以参照以往的作业，此处不详细展开
* http转发，在/mnt/目录中，有leader帮忙拷贝的host文件，通过host文件，可以看到leader的ip，然后就可以转发了
```
nohup configurable-http-proxy --default-target=http://192.0.1.100:8888 --ip=172.16.6.153 --port=8888
```
### 容错验证
* 登入jupter界面,可以看到host表中已经维护好<br>
![pic6](https://github.com/magicfisk/mesos_learning/raw/master/homework6/init.jpg)<br>
* 利用ssh登入其他主机，可以看到只用yes，不用密码<br>
![pic7](https://github.com/magicfisk/mesos_learning/raw/master/homework6/ssh.jpg)<br>
* 这时，我们将docker中一个容器stop掉（103），经过30s的等待，重新查看host表<br>
![pic8](https://github.com/magicfisk/mesos_learning/raw/master/homework6/host.jpg)<br>
* 我们发现host表更新了，少了我们stop的主机<br>
* 我们把leader给stop掉<br>
![pic9](https://github.com/magicfisk/mesos_learning/raw/master/homework6/mnt.jpg)<br>
在分布式文件系统中检查到100成为了新的leader，我们到100所在的机器下，进行http转发
```
configurable-http-proxy --default-target=http://192.0.1.100:8888 --ip=172.16.6.153 --port=8888
```
* 登入jupter界面,可以看到我们的新leader很好的在工作
![pic10](https://github.com/magicfisk/mesos_learning/raw/master/homework6/new-leader.jpg)<br>
* ssh也照样正常工作
![pic11](https://github.com/magicfisk/mesos_learning/raw/master/homework6/ssh2.jpg)<br>
### 补充-自动转发
* 在转发端口的机器下起一个ip为192.0.1.110的docker容器
* 运行转发代码
```
import subprocess,time

ip=""
while True:
        f=open("/mnt/hosts") #读取master维护的hosts表
        nip=f.readline()
        f.close()
        nip=nip.split(" ")
        nip=nip[0]; #获得当前master的ip
        print("check ip:"+ip+" nip:"+nip+"\n")
        if not ip==nip:  #不一样就要重新转发
                print("updata\n")
                if ip!="":
                        http.kill()

                args = ['configurable-http-proxy', \
                '--default-target=http://'+nip+':8888', \
                '--ip=192.0.1.110', '--port=8888']
                http = subprocess.Popen(args)
                ip=nip
        time.sleep(5) #5s检查一次
```
* 在宿主机上直接用
```
nohup configurable-http-proxy --default-target=http://192.0.1.110:8888 --ip=172.16.6.153 --port=8888
```
* 进行转发
* 能看到检测到ip变化，并重新转发的过程
![pic11](https://github.com/magicfisk/mesos_learning/raw/master/homework6/http.jpg)
