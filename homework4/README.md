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
@ 插入图片
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
@ 图片
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
### AUFS概览
* AUFS是一种Union File System,所谓UnionFS就是把不同物理位置的目录合并mount到同一个目录中。
```
sudo mount -t aufs -o br=/a:/b:/c none /aufs
```
* 上述命令可以把a,b,c挂载到aufs文件夹下,其中c为最上层,a为最下层
### AUFS概念
* 将多个目录合并成一个虚拟文件系统,成员目录称为虚拟文件系统的一个分支（branch）
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

## 安装
gluster volume create gvol0 replica 2 172.16.6.249:/data/gluster/gvol0 172.16.6.153:/data/gluster/gvol0 force

mount -t glusterfs 172.16.6.249:/gvol0 /mnt/glusterfs
mount -t glusterfs 172.16.6.153:/gvol0 /mnt/glusterfs


docker run -it --net=host -v /mnt/glusterfs/:/home/ mydocker:v1 /bin/bash ./run.sh