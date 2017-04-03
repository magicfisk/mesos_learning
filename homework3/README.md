# 第三次作业
## 1.安装docker
![pic1](https://github.com/magicfisk/mesos_learning/tree/master/homework3/install.jpg)
## docker基本命令
### docker run
* 语法
```
docker run  [OPTIONS] IMAGE[:TAG] [COMMAND] [ARG...]
```
* 运行一个新的容器，容器拥有自己的文件系统、网络
* IMAGE[:TAG]值镜像名字
* command为镜像运行后执行的指令
* arg为command参数

* 常用options
```
-d			  后台 (前台默认)
-a, --attach value	  连接容器的stdin、stdout、stderr
-t			  使用终端。经常和 -i一起使用。
-i			  打开STDIN和容器交互。经常和 -t一起使用。
-m, --memory string    	  内存限制(单位:b, k, m or g)
-c, --cpu-shares int   	  CPU优先级 (相对权重)
-u, --user string	  设置用户名
-w,--workdir string	  设置工作目录 默认为根目录
-e,--env value		  设置环境变量
-p			  将主机端口和容器端口设置转发 -p ip:80:80
-h,--hostname string      容器的主机名
-v, --volume value	  挂载本地目录，目录前面是本机目录，后面是镜像目录
				例子docker run --rm-i -t -v /home/hyzhou/docker:/data:rw ubuntu:14.04 /bin/bash
--volumes-from		  从容器挂载共享目录
--name string		  容器名字
--dns	              	  设置容器的DNS服务器
--net	        	  设置容器的网络连接方式bridge,none,Container:<name|id>,host
--ip/--ip6		  容器的ip地址
```
以下为全体option
```
      --add-host value              Add a custom host-to-IP mapping (host:ip) (default [])
  -a, --attach value                Attach to STDIN, STDOUT or STDERR (default [])
      --blkio-weight value          Block IO (relative weight), between 10 and 1000
      --blkio-weight-device value   Block IO weight (relative device weight) (default [])
      --cap-add value               Add Linux capabilities (default [])
      --cap-drop value              Drop Linux capabilities (default [])
      --cgroup-parent string        Optional parent cgroup for the container
      --cidfile string              Write the container ID to the file
      --cpu-percent int             CPU percent (Windows only)
      --cpu-period int              Limit CPU CFS (Completely Fair Scheduler) period
      --cpu-quota int               Limit CPU CFS (Completely Fair Scheduler) quota
  -c, --cpu-shares int              CPU shares (relative weight)
      --cpuset-cpus string          CPUs in which to allow execution (0-3, 0,1)
      --cpuset-mems string          MEMs in which to allow execution (0-3, 0,1)
  -d, --detach                      Run container in background and print container ID
      --detach-keys string          Override the key sequence for detaching a container
      --device value                Add a host device to the container (default [])
      --device-read-bps value       Limit read rate (bytes per second) from a device (default [])
      --device-read-iops value      Limit read rate (IO per second) from a device (default [])
      --device-write-bps value      Limit write rate (bytes per second) to a device (default [])
      --device-write-iops value     Limit write rate (IO per second) to a device (default [])
      --disable-content-trust       Skip image verification (default true)
      --dns value                   Set custom DNS servers (default [])
      --dns-opt value               Set DNS options (default [])
      --dns-search value            Set custom DNS search domains (default [])
      --entrypoint string           Overwrite the default ENTRYPOINT of the image
  -e, --env value                   Set environment variables (default [])
      --env-file value              Read in a file of environment variables (default [])
      --expose value                Expose a port or a range of ports (default [])
      --group-add value             Add additional groups to join (default [])
      --health-cmd string           Command to run to check health
      --health-interval duration    Time between running the check
      --health-retries int          Consecutive failures needed to report unhealthy
      --health-timeout duration     Maximum time to allow one check to run
      --help                        Print usage
  -h, --hostname string             Container host name
  -i, --interactive                 Keep STDIN open even if not attached
      --io-maxbandwidth string      Maximum IO bandwidth limit for the system drive (Windows only)
      --io-maxiops uint             Maximum IOps limit for the system drive (Windows only)
      --ip string                   Container IPv4 address (e.g. 172.30.100.104)
      --ip6 string                  Container IPv6 address (e.g. 2001:db8::33)
      --ipc string                  IPC namespace to use
      --isolation string            Container isolation technology
      --kernel-memory string        Kernel memory limit
  -l, --label value                 Set meta data on a container (default [])
      --label-file value            Read in a line delimited file of labels (default [])
      --link value                  Add link to another container (default [])
      --link-local-ip value         Container IPv4/IPv6 link-local addresses (default [])
      --log-driver string           Logging driver for the container
      --log-opt value               Log driver options (default [])
      --mac-address string          Container MAC address (e.g. 92:d0:c6:0a:29:33)
  -m, --memory string               Memory limit
      --memory-reservation string   Memory soft limit
      --memory-swap string          Swap limit equal to memory plus swap: '-1' to enable unlimited swap
      --memory-swappiness int       Tune container memory swappiness (0 to 100) (default -1)
      --name string                 Assign a name to the container
      --network string              Connect a container to a network (default "default")
      --network-alias value         Add network-scoped alias for the container (default [])
      --no-healthcheck              Disable any container-specified HEALTHCHECK
      --oom-kill-disable            Disable OOM Killer
      --oom-score-adj int           Tune host's OOM preferences (-1000 to 1000)
      --pid string                  PID namespace to use
      --pids-limit int              Tune container pids limit (set -1 for unlimited)
      --privileged                  Give extended privileges to this container
  -p, --publish value               Publish a container's port(s) to the host (default [])
  -P, --publish-all                 Publish all exposed ports to random ports
      --read-only                   Mount the container's root filesystem as read only
      --restart string              Restart policy to apply when a container exits (default "no")
      --rm                          Automatically remove the container when it exits
      --runtime string              Runtime to use for this container
      --security-opt value          Security Options (default [])
      --shm-size string             Size of /dev/shm, default value is 64MB
      --sig-proxy                   Proxy received signals to the process (default true)
      --stop-signal string          Signal to stop a container, SIGTERM by default (default "SIGTERM")
      --storage-opt value           Storage driver options for the container (default [])
      --sysctl value                Sysctl options (default map[])
      --tmpfs value                 Mount a tmpfs directory (default [])
  -t, --tty                         Allocate a pseudo-TTY
      --ulimit value                Ulimit options (default [])
  -u, --user string                 Username or UID (format: <name|uid>[:<group|gid>])
      --userns string               User namespace to use
      --uts string                  UTS namespace to use
  -v, --volume value                Bind mount a volume (default [])
      --volume-driver string        Optional volume driver for the container
      --volumes-from value          Mount volumes from the specified container(s) (default [])
  -w, --workdir string              Working directory inside the container
```
### docker start
* 语法
```
docker start [OPTIONS] CONTAINER [CONTAINER...]
```
* 启动创建了但没有运行的容器
Options包括
```
  -a, --attach               连接容器的stdout、stderr和信号
      --detach-keys string   重载key sequence用于离开容器
  -i, --interactive          连接容器的stdin
```
### docker commit
* 语法
```
docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]
```
* 创建一个新的镜像
* CONTAINER需要被备份的镜像名字
* REPOSITORY镜像仓库，可以是本地或是远程
* options
```
  -a, --author string    作者
  -c, --change value     使用Dockerfile中的指令
  -m, --message string   说明
  -p, --pause            提交时暂停容器，默认开启
```
### docker build
* 语法
```
 docker build [OPTIONS] PATH | URL | -
```
* 利用dockerfile创建新镜像
* PATH | URL | - 为dockerfile路径
* options
```
      --build-arg value         设置环境变量
      --cgroup-parent string    设置父cgroup
      --cpu-period int          cpu使用周期
      --cpu-quota int           cpu使用量
  -c, --cpu-shares int          优先级
      --cpuset-cpus string      设置运行的cpu编号
      --cpuset-mems string      设置使用内存的标号
      --disable-content-trust   跳过镜像验证
  -f, --file string             dockerfile名字，默认为PATH/Dockerfile
      --force-rm                移除中间产生的镜像，无论是否成功build
      --isolation string        指定容器的分类技术
      --label value             设置元数据
  -m, --memory string           内存限制
      --memory-swap string      交换分区限制，-1为无限制
      --no-cache                不使用cache
      --pull                    总是创建最新版本的镜像
  -q, --quiet                   成功时不打印ID
      --rm                      移除中间产生的镜像，当成功build时
      --shm-size string        	共享内存/dev/shm的大小,默认64MB
  -t, --tag value               名称和标签
      --ulimit value            ulimit用于shell启动进程所占用的资源
```
### docker images
* 语法
```
docker images [OPTIONS] [REPOSITORY[:TAG]]
```
* 列出本地的镜像
* [REPOSITORY[:TAG]]中可以设定关键字
* options
```
  -a, --all             展示所有，默认隐藏中间过程镜像
      --digests         显示摘要
  -f, --filter value    根据条件过滤输出
      --format string   用go模板格式化输出
      --no-trunc        不要裁剪输出（id）
  -q, --quiet           只打印镜像ID
```
### docker network
* docker network有6个子命令、
#### docker network connect
* 语法
```
docker network connect [OPTIONS] NETWORK CONTAINER
```
* 将一个容器接入网络
* network为接入网络的名字
* container为容器名字
* options：
```
      --alias value           为容器添加网络别名
      --ip string             IP Address
      --ip6 string            IPv6 Address
      --link value            添加到其他容器的连接上
      --link-local-ip value   为容器增加本地连接
```
#### docker network create
* 语法
```
docker network create [OPTIONS] NETWORK
```
* 创建网络
* network为网络名字
* options
```
      --aux-address value    网络驱动用到辅助ipv4或6地址
  -d, --driver string        指定网络驱动，默认为bridge
      --gateway value        IPv4或IPv6的子网网关
      --internal             限制外部访问该网络
      --ip-range value       从一段地址中分配ip
      --ipam-driver string   ip地址管理驱动
      --ipam-opt value       ip地址管理驱动的选项
      --ipv6                 使用ipv6
      --label value          设置元数据
  -o, --opt value            网络驱动选项
      --subnet value         CIDR格式的子网
```
##### docker network disconnect
* 语法
```
docker network disconnect [OPTIONS] NETWORK CONTAINER
```
* 断开网络
options
```
  -f, --force   强制断开
```
#### docker network inspect
* 语法
```
docker network inspect [OPTIONS] NETWORK [NETWORK...]
```
* 展示网络细节
* Options
```
  -f, --format string 	采用go模板格式化输出
```
#### docker network ls
* 语法
```
docker network ls [OPTIONS]
```
* 列出网络
* options：
```
  -f, --filter value   筛选结果
      --no-trunc       不截断输出
  -q, --quiet          只打印镜像ID
```
#### docker network rm
* 语法
```
docker network rm NETWORK [NETWORK...]
```
* 移除一些网络
## 创建一个基础镜像为ubuntu的docker镜像，随后再其中加入nginx服务器
* 创建镜像
```
sudo run docker -it --name mydocker ubuntu /bin/bash
```
* 进入镜像后
```
apt-get update
apt-get install nginx -y
apt-get install vim -y
nginx -t //找到配置文件
vi /etc/nginx/nginx.conf
```
* 修改配置文件
在html模块下，删除virtual host
加入
```
	server {
		listen 80;
		location / {
		root /home;
		index index.html;
		}}
```
* 在/home/ 下新建index.html，写一个包含自己信息的html文件
* 在根目录下新建一个运行脚本 run.sh
```
nginx
tail -f /var/log/nginx/access.log
```
* 退出docker
* 执行命令,保存镜像
```
docker commit mydocker mydocker:v4
```
* 检查效果
```
docker run -it --net=host mydocker:v4 /bin/bash /run.sh
```
* 在燕云上将80端口转发到8888端口上
* 输入http://162.105.174.33:8888/ 看到网页
![pic2](https://github.com/magicfisk/mesos_learning/tree/master/homework3/index.jpg)
* 创建自己的网络,默认为bridge
```
docker network create mynet
```
* 创建新的镜像，并将其从原网络中断开
```
docker run -it --net=bridge --name mydocker -d -p 80:80 mydocker:v4 /bin/bash /run.sh
docker network disconnect bridge mydocker
```
* 此时网页无法打开
* 连接mynet
```
docker network connect mynet mydocker
```
* 此时网页正常打开
* 宿主访问
```
docker network inspect mynet //获得网关信息
{
        "Name": "mynet",
        "Id": "f9c6122e1d8066eab52e8caf76f0f1da9c30b8c0f5126ddc2115183e934e8442",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1/16"
                }
            ]
        },
        "Internal": false,
        "Containers": {
            "6c5766a72fcbd7052bf8bc6d191db4773be94298a3b187766c217a5e20885d35": {
                "Name": "mydocker",
                "EndpointID": "012de7562bb05cded38c7c5495293fe45e201ba96b0cf02591aeb64a70c9c34d",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
```
* 宿主访问
```
root@oo-lab:~# curl 172.18.0.1:80
<!DOCTYPE html>
<p>学号：1400012801</p>
<p>名字：叶钊达</p>
<p>到此一游</p>
</html>`
```

## 请查阅相关资料和docker文档，阐述null,bridge,host,overlay网络模式的区别
### none模式
Docker容器拥有自己的Network Namespace，但没有任何网络配置（网卡，ip，路由信息），需要自己手动添加
### host模式
一般容器创建时会创建自己的Network Namespace，用于和宿主网络进行隔离，当时host模式容器和宿主共用一个nemaspace，使用宿主的ip，端口
### container模式
容器同样不会创建自己的namespace，有时和另外一个容器共用一个namespace
### bridge模式
默认的网络模式。每个docker都有自己的namespace，并设置ip，并将容器连接到docker0的虚拟网桥上。docker0是docker自己创建的网络。工作方式类似物理交换机的工作形式，docker会先获得一个子网的网段（如172.17.0.0/16），将 172.17.42.1/16分配给docker0网桥，承担网关的工作，子网其他ip会分给其他连接到他上面的docker。
### overlay模式
* overlay模式在docker中和swarm集群是密切相关的。
* overlay模式提供了跨机器的容器的互相访问。
* 第二代overlay模式中，直接调用swarm来实现overlay模式
```
docker swarm init --advertise-addr 172.16.6.153
```
* 得到join命令
```
docker swarm join \
    --token SWMTKN-1-4u0sy656s8vxum227x29gqzhqizafk1o9lpgwu4kdpwfpcerz2-chl8std2ky8yvhy2n851e2m9j \
    172.16.6.153:2377
```
* 在另外一台机器上执行命令
```
Error response from daemon: Timeout was reached before node was joined. The attempt to join the swarm will continue in the background. Use the "docker info" command to see the current swarm status of your node.
```
* 出了点毛病(GG)
* 在manager上查看节点,可以看到管理节点
```
docker node ls
ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
7kuftpv9nz94acl3nfy281jkh *  oo-lab    Ready   Active        Leader
```
## 阅读mesos中负责与docker交互的代码，谈谈mesos是怎样与docker进行交互的，并介绍docker类中run函数大致做了什么。
* docker.cpp是负责构建docker运行命令的
* spec.cpp将info信息包装成c++类
* executor.cpp是运行docker的代码，就是framework中的executor，负责执行docker中包装出来的命令
* mesos和docker的交互相当于mesos建立了一个executor，然后调用各种docker命令来管理docker，和人直接运行docker没有什么本质区别，只是包了一个壳用于远程调用

### docker run
* 检查containnerInfo是否存在
* 开始构建命令参数
```
  vector<string> argv;
  argv.push_back(path);
  argv.push_back("-H");
  argv.push_back(socket);
  argv.push_back("run");

  if (dockerInfo.privileged()) {
    argv.push_back("--privileged");
  }
```
* 检查资源信息，并设定对应参数（代码不贴了）
* 检查环境变量，并设定命令参数
* 加入mesos sandbox相关参数
* 检查挂载信息，并设定命令参数
* 将sandbox的目录加入容器中，通过挂载的方式
* 检查分卷（volume）？驱动的个数，mesos只支持一个（还是docker？）
* 加入网络信息
* 加入hostname
* 加入docker的option信息
* 加入端口映射
* 加入硬盘信息
* 加入命令行参数
* 加入容器名字
* 参数构建完毕，写入日志
* 设置子线程系统环境变量
* 新建子线程实体
* 运行子线程


## 写一个framework，以容器的方式运行task，运行前面保存的nginx服务器镜像，网络为HOST。
* 重启agent进程，加入选项--containerizers=docker,mesos
* 在pymesos上修改代码
* 设置框架信息，并创建一个MesosSchedulerDriver
```
    framework = Dict()
    framework.user = getpass.getuser()
    framework.name = "mydocker"
    framework.hostname = socket.gethostname()

    driver = MesosSchedulerDriver(
        MinimalScheduler(),
        framework,
        master,
        use_addict=True,
    )
```
* MinimalScheduler类实现
```
class MinimalScheduler(Scheduler):
    def __init__(self):
        self.Task_launched=False

        

#mesos提供资源时的处理函数            
    def resourceOffers(self, driver, offers):    

                
        filters = {'refuse_seconds': 5}
        #分发任务
        for offer in offers:
		cpus = self.getResource(offer.resources, 'cpus')
		mem = self.getResource(offer.resources, 'mem')
			
		#只运行一个
		if self.Task_launched:
		continue
				
		#资源检查	
		if cpus < TASK_CPU or mem < TASK_MEM:
			continue
		self.Task_launched=True	

		#设置docker信息
		DockerInfo = Dict()
		DockerInfo.image = 'mydocker:v4'
		DockerInfo.network = 'HOST'

		#设置容器信息
		ContainerInfo = Dict()
		ContainerInfo.type = 'DOCKER'
		ContainerInfo.docker = DockerInfo
			
		#设置命令
		CommandInfo = Dict()
		CommandInfo.shell = False
		CommandInfo.value = '/bin/bash'
		CommandInfo.arguments = ['/run.sh']
			
		#创建task
		task = Dict()
		task_id = str(uuid.uuid4())
		task.task_id.value = task_id
		task.agent_id.value = offer.agent_id.value
		task.name = 'mydocker'
			
		#将命令和容器加入task
		task.container = ContainerInfo
		task.command = CommandInfo

		task.resources = [
              	  dict(name='cpus', type='SCALAR', scalar={'value': TASK_CPU}),
           	     dict(name='mem', type='SCALAR', scalar={'value': TASK_MEM}),
        	    ]
		
		driver.launchTasks(offer.id, [task], filters) #调度任务

    #状态更新回调
    def statusUpdate(self, driver, update):
		return
       
	#解析资源  
    def getResource(self, res, name):
        for r in res:
            if r.name == name:
                return r.scalar.value
        return 0.0
```
* 运行脚本
```
python scheduler.py 172.16.6.153
```
* 可以看到agent在运行
![pic3](https://github.com/magicfisk/mesos_learning/tree/master/homework3/agent.jpg)
* docker运行
![pic4](https://github.com/magicfisk/mesos_learning/tree/master/homework3/docker.jpg)
* 网页正常访问
![pic2](https://github.com/magicfisk/mesos_learning/tree/master/homework3/index.jpg)

