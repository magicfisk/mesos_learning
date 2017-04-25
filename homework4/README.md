# 第四次作业
## HDFS
### 前提和设计目标
* 硬件错误是常态,而非异常情况,因此错误检测和快速、自动的恢复是HDFS的核心架构目标。
* 跑在HDFS上的应用与一般的应用不同,它们主要是以流式读为主,做批量处理（不保证延迟,追求高吞吐量）
* HDFS以支持大数据集合为目标,一个存储在上面的典型文件大小一般都在千兆至T字节,一个单一HDFS能支撑数以千万计的文件
* HDFS应用对文件要求的是write-one-read-many访问模型。一个文件经过创建、写,关闭之后就不需要改变,化简了数据一致性问题
* 移动计算的代价比之移动数据的代价低。HDFS提供给应用将计算移动到数据附近的接口。
* 在异构的硬件和软件平台上的可移植性。
### HDFS基本概念
#### 数据块
* HDFS默认的最基本的存储单位是64M的数据块,这个数据块可以理解和一般的文件里面的分块是一样的
#### 元数据节点 namenode
* 用来管理文件系统的命名空间,它将所有的文件和文件夹的元数据保存在一个文件系统树中。
#### 数据节点 datanode
* 就是用来存储数据文件的
#### 从元数据节点 secondarynamenode
* 周期性将元数据节点的命名空间镜像文件和修改日志合并,以防日志文件过大
* 合并后的命名空间镜像文件在从元数据节点中叶保存一份,以防元数据节点失效的时候用于恢复。
### HDFS构架
![pic1](https://github.com/magicfisk/mesos_learning/raw/master/homework4/HDFS-A.gif)
* HDFS采用master/slave架构,有一个Namenode和一定数目的Datanode组成
* Namenode是一个中心服务器,负责管理文件系统的namespace和客户端对文件的访问（只有一个！！）
* Datanode在集群中一般是一个节点一个,负责管理节点上它们附带的存储
* 一个文件分成一个或多个block,这些block存储在Datanode集合里
* Namenode执行文件系统的namespace操作,同时决定block到具体Datanode节点的映射
* Datanode在Namenode的指挥下进行block的创建、删除和复制
* 用户对数据的读写是直接在Datenode上的,无需通过namenode
### 数据
* HDFS将每个文件存储成block序列,除了最后一个block,所有的block都是同样的大小。文件的所有block为了容错都会被复制多份
* HDFS采用one-write机制,不能修改文件,只能创建和追加
* 在大多数情况下,replication因子是3,HDFS的存放策略是将一个副本存放在本地机架上的节点,一个副本放在同一机架上的另一个节点,最后一个副本放在不同机架上的一个节点。
* 为了降低整体的带宽消耗和读延时,HDFS会尽量让reader读最近的副本。如果在reader的同一个机架上有一个副本,那么就读该副本。如果一个HDFS集群跨越多个数据中心,那么reader也将首先尝试读本地数据中心的副本。
### 空间的回收
* 用户或者应用删除某个文件,这个文件并没有立刻从HDFS中删除。相反,HDFS将这个文件重命名,并转移到/trash目录。以便快速恢复
* 超过一定时间,Namenode就会将该文件从namespace中删除,也将释放关联该文件的数据块。


### 使用方式
#### shell
```
bin/hadoop fs <args>
```
通过上述形式的命令来调度hadoop进行相关操作
#### web
* 在部署hadoop的机器上，会启动一个web服务器，通过访问web网页来查看文件

## GlusterFS
### 亮点
GlusterFS采用弹性哈希算法在存储池中定位数据,而不是采用集中式或分布式元数据服务器索引。在其他的Scale-Out存储系统中,元数据服务器通常会导致I/O性能瓶颈和单点故障问题。GlusterFS中,所有在Scale-Out存储配置中的存储系统都可以智能地定位任意数据分片,不需要查看索引或者向其他服务器查询。这种设计机制完全并行化了数据访问,实现了真正的线性性能扩展。
### 框架
![pic2](https://github.com/magicfisk/mesos_learning/raw/master/homework4/GlusterFS_inside.png)
#### 外部结构
* 由存储服务器（BrickServer）、客户端以及NFS/Samba 存储网关组成
* GlusterFS 架构中没有元数据服务器组件
#### 内部结构
* GlusterFS内部采用模块化、堆栈式的架构,可通过灵活的配置支持高度定制化的应用环境。

### 存储
#### 概念
* Brick：存储基本单位
* Volume：多个brick组成的虚拟存储空间，可以被挂载
#### Volume
##### distribute volume
* 文件通过hash算法分布到所有brick server。如果有一个磁盘坏了，对应的数据也丢失，文件级RAID 0，不具有容错能力
##### stripe volume
* 类似RAID0，文件分成数据块以Round Robin方式分布到brick server上，并发粒度是数据块，支持超大文件，大文件性能高
##### replica volume
* 文件同步复制到多个brick上，文件级RAID 1，具有容错能力，写性能下降，读性能提升
##### 其他
上述几个特性的组合

### glusterfs整体工作流程
* 在客户端,用户通过glusterfs的mount point来读写数据,对于用户来说,,集群系统的存在对用户是完全透明的,用户感觉不到是操作本地系统还是远端的集群系统
* 用户的这个操作被递交给 本地linux系统的VFS来处理
* VFS将数据递交给FUSE内核文件系统，fuse文件系统则是将数据通过/dev/fuse这个设备文件递交给了glusterfs client端，相当于文件系统代理
* client对数据进行一些指定的处理，通过网络将数据递交给Glusterfs Server
* Glusterfs Server将数据写入相应位置

### 使用方式
* 见下面配置

## 联合文件系统
### AUFS概念
* AUFS是一种Union File System，将多个目录合并成一个虚拟文件系统,成员目录称为虚拟文件系统的一个分支（branch）
* 每个branch可以指定 readwrite/whiteout‐able/readonly权限,只读（ro）,读写（rw）,写隐藏（wo）。
* 一般情况下,aufs只有最上层的branch具有读写权限,其余branch均为只读权限。只读branch只能逻辑上修改。
### AUFS读写
* 修改一个文件,而该文件位于低层branch时,顶层branch会直接复制低层branch的文件至顶层再进行修改,而低层的文件不变
* 当容器删除一个低层branch文件时,只是在顶层branch对该文件进行重命名并隐藏,实际并未删除文件,只是不可见
### AUFS的性能
* AUFS会把所有的分支mount起来,所以,在查找文件上是比较慢了（O(n)）
* AUFS找到了文件,以后的读写和操作原文件基本上是一样的
### docker和AUFS
* Docker镜像（Image）是由一个或多个AUFS branch组成,并且所有的branch均为只读权限。
* 在运行容器的时候,创建一个AUFS branch位于image层之上,具有rw权限,并把这些branch联合挂载到一个挂载点下。
* 创建多个容器时,只需创建多个容器运行目录,使用aufs把容器运行目录挂载在Image目录之上,大大节约了资源
### 使用方式
```
sudo mount -t aufs -o br=/a:/b:/c none /aufs
```
* 上述命令可以把a,b,c挂载到aufs文件夹下,其中a为最上层,c为最下层
## 安装配置GlusterFS
### 安装
```
sudo apt-get install -y software-properties-common
sudo add-apt-repository ppa:gluster/glusterfs-3.8
sudo apt-get update
sudo apt-get install -y glusterfs-server
```
* 上述命令安装了服务端
```
apt-get install -y glusterfs-client
```
* 安装客户端
### 启动
```
sudo service glusterfs-server start
```
* 启动服务
```
sudo service glusterfs-server status

● glusterfs-server.service - LSB: GlusterFS server
   Loaded: loaded (/etc/init.d/glusterfs-server; bad; vendor preset: enabled)
   Active: active (running) since Sat 2017-04-15 16:30:30 EDT; 2 days ago
     Docs: man:systemd-sysv-generator(8)
  Process: 11880 ExecStop=/etc/init.d/glusterfs-server stop (code=exited, statu
  Process: 12232 ExecStart=/etc/init.d/glusterfs-server start (code=exited, sta
    Tasks: 34
   Memory: 83.0M
      CPU: 41.507s
   CGroup: /system.slice/glusterfs-server.service
           ├─11512 /usr/sbin/glusterfsd -s 172.16.6.153 --volfile-id gvol0.172.
           ├─12239 /usr/sbin/glusterd -p /var/run/glusterd.pid
           └─12473 /usr/sbin/glusterfs -s localhost --volfile-id gluster/gluste

Apr 15 16:30:28 oo-lab systemd[1]: Starting LSB: GlusterFS server...
Apr 15 16:30:28 oo-lab glusterfs-server[12232]:  * Starting glusterd service gl
Apr 15 16:30:30 oo-lab glusterfs-server[12232]:    ...done.
Apr 15 16:30:30 oo-lab systemd[1]: Started LSB: GlusterFS server.
```
* 确认服务启动
### 添加信任的服务端
```
gluster peer probe 172.16.6.153

gluster pool list   //查看存储列表
UUID                                    Hostname        State
3a362a72-95ef-44e3-8f34-5af9c00767b3    172.16.6.153    Connected
d44f85da-69fd-499a-8b50-f009a078e99e    localhost       Connected

```

### 创建volume，挂载
```
mkdir -p /data/gluster/gvol0
gluster volume create gvol0 replica 2 172.16.6.249:/data/gluster/gvol0 172.16.6.153:/data/gluster/gvol0 force
gluster volume start gvol0 //启动卷
```
* 将/data/gluster/gvol0作为brick，在任意一台机器上运行第二条命令，创建一个复制卷
```
mount -t glusterfs 172.16.6.249:/gvol0 /mnt/glusterfs
```
* 将创建的目录挂载在本地的/mnt/glusterfs目录下

### 测试
* 在/mnt/glusterfs下
```
vi index.html //写入一个主页
```
* 在服务器上查看文件存入
```
root@oo-lab:/data/gluster/gvol0# ls
index.html
```
* 破坏一个服务器上的文件夹
```
Broadcast message from systemd-journald@oo-lab (Mon 2017-04-17 21:33:54 EDT):

data-gluster-gvol0[33275]: [2017-04-18 01:33:54.693674] M [MSGID: 113075] [posix-helpers.c:1821:posix_health_check_thread_proc] 0-gvol0-posix: health-check failed, going down
```
* 文件依旧能在挂载点看到
```
root@oo-lab:/mnt/glusterfs# ls
index.html
```

### 在docker中挂载上述分布式系统
* 由于docker中无法直接将volume挂载，所以选择将volume先挂载在宿主上,再挂入docker
```
docker run -it --net=host -v /mnt/glusterfs/:/home/ mydocker:v1 /bin/bash ./run.sh
```
* 在其他挂载地点修改index文件，刷新网页，可以发现网页被修改，说明成功载入分布式文件系统
![pic3](https://github.com/magicfisk/mesos_learning/raw/master/homework4/index.jpg)

## 仿照Docker镜像工作机制完成一次镜像制作
* docker和aufs在上面部分已经阐述了其关系
### 查看docker的挂载文件位置
* 开启一个docker，使得在后台运行,并查看挂载
```
docker run -it --name tst ubuntu
exit
docker start tst
df -h
```
* 多了2行，其中none为docker镜像的挂载，shm为docker的配置文件
```
none                           19G   13G  5.2G  71% /var/lib/docker/aufs/mnt/12c918da5e9fec89c325ad67d19932d108af18f3349ee047941fb4c8c76fb3b1

shm                            64M     0   64M   0% /var/lib/docker/containers/8e8d2a1b74b1945ddd9ad5983dd9ab58a0beb5844873d734ef07849dea23244a/shm
```

* 在/var/lib/docker/aufs/layers可以看到layers信息
```
cat 12c918da5e9fec89c325ad67d19932d108af18f3349ee047941fb4c8c76fb3b1

12c918da5e9fec89c325ad67d19932d108af18f3349ee047941fb4c8c76fb3b1-init
ab222f2619b921e9fb847be0bbff321728ad9771c92b64c3c80a4fe544ecfecf
d1cbd4588f47064a894634352814687466491c80af12e84743de30977bf3b712
6dd88e0bdb25db5f73166f3448e66c13ae2c4ca4b1e6461defa11da9b5085ff6
d4a4666fac88e2ea29315327d19e471f536bb9bfd843888723fca3f2b3ea8359
70c35b47cf4fd87c4558d11b772aa60a97b0ac4bba862860f5820c006dfe314c
```
* 可以看到顶层为12c918da5e9fec89c325ad67d19932d108af18f3349ee047941fb4c8c76fb3b1-init
* 容器的层数据存放在/var/lib/docker/aufs/diff目录
* 事实上12c918da5e9fec89c325ad67d19932d108af18f3349ee047941fb4c8c76fb3b1才是读写层，带init的是用来初始化的
```
cp ab222f2619b921e9fb847be0bbff321728ad9771c92b64c3c80a4fe544ecfecf /my_img/i2 -r
cp d1cbd4588f47064a894634352814687466491c80af12e84743de30977bf3b712 /my_img/i3 -r
cp 6dd88e0bdb25db5f73166f3448e66c13ae2c4ca4b1e6461defa11da9b5085ff6 /my_img/i4 -r
cp d4a4666fac88e2ea29315327d19e471f536bb9bfd843888723fca3f2b3ea8359 /my_img/i5 -r
cp 70c35b47cf4fd87c4558d11b772aa60a97b0ac4bba862860f5820c006dfe314c /my_img/i6 -r
```
* 把数据全部复制出来
* 安装vim包，复制软件安装层
```
root@docker exec -it tst /bin/bash
docker@apt-get update
docker@apt install vim -y
docker@exit
root@cd /var/lib/docker/aufs/diff
root@cp 12c918da5e9fec89c325ad67d19932d108af18f3349ee047941fb4c8c76fb3b1 /my_img/i1 -r
```
* 并全部挂载在一个目录下面
```
mkdir /mydocker_mnt
mount -t aufs -o br=/my_img/i1=ro:/my_img/i2=ro:/my_img/i3=ro:/my_img/i4=ro:/my_img/i5=ro:/my_img/i6=ro none /mydocker_mnt
```
* 利用import命令从tar包中获取镜像,进入镜像
```
tar -c . | docker import - mydocker_new:v3
docker run -it mydocker_new:v3 /bin/bash
vi 1.txt
```
* 成功运行vim
![pic4](https://github.com/magicfisk/mesos_learning/raw/master/homework4/vi.jpg)

