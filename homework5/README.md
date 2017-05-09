# 第5次作业
## 简述linux对ip包的处理
![pic1](https://github.com/magicfisk/mesos_learning/raw/master/homework5/ip.jpg)
### 接受ip包
* 如图，左边为ip包从外面进入，进入后有一个路由过程，判断ip包是否为发往本机的ip包
* 若是，则通过ip_local_input链路，进入本机
* 若否，则通过ip_forward转发
### 发送ip包
* 右边为ip包发出，ip包从高层输入，要经过ip_output，封装各种ip包头，检查mtu、ttl等，然后进入ip_finish_output,等待发送。
* 转发的ip包和主机发出的ip包在ip_finish_output汇合
* 再之后通过发送路由，确定该ip包是否是局域网内，通过arp协议获得物理地址（局域网内），或者网关地址（局域网外）
### 结合iptable
![pic2](https://github.com/magicfisk/mesos_learning/raw/master/homework5/iptables.gif)
* filter (过滤器)：主要跟进入 Linux 本机的封包有关。
* nat (地址转换)：是 Network Address Translation 的缩写， 这个表格主要在进行来源与目的之 IP 或 port 的转换。 
* mangle (破坏者)：这个表格主要是与特殊的封包的路由旗标有关， 早期仅有 PREROUTING 及 OUTPUT 链，不过从 kernel 2.4.18 之后加入了 INPUT 及 FORWARD 链
* iptable在linux内核的对ip包处理的各个链路上进行包操作
## 使用iptable
* 基本语法
```
iptables [-AI 链名] -j [ACCEPT|DROP|REJECT|LOG]

基本选项与参数：
-AI 链名：针对某的链进行规则的 "插入" 或 "累加"
    -A ：新增加一条规则，该规则增加在原本规则的最后面。例如原本已经有四条规则，
         使用 -A 就可以加上第五条规则！
    -I ：插入一条规则。如果没有指定此规则的顺序，默认是插入变成第一条规则。
         例如原本有四条规则，使用 -I 则该规则变成第一条，而原本四条变成 2~5 号
    链 ：有 INPUT, OUTPUT, FORWARD 等

-j ：后面接动作，主要的动作有接受(ACCEPT)、丢弃(DROP)、拒绝(REJECT)及记录(LOG)

```
* 功能性参数
```
-io 网络接口：设定封包进出的接口规范
    -i ：封包所进入的那个网络接口，例如 eth0, lo 等接口。需与 INPUT 链配合；
    -o ：封包所传出的那个网络接口，需与 OUTPUT 链配合；

-p 协定：设定此规则适用于哪种封包格式
   主要的封包格式有： tcp, udp, icmp 及 all 。

-s 来源 IP/网域：设定此规则之封包的来源项目，可指定单纯的 IP 或包括网域，例如：
   IP  ：192.168.0.100
   网域：192.168.0.0/24, 192.168.0.0/255.255.255.0 均可。
   若规范为『不许』时，则加上 ! 即可，例如：
   -s ! 192.168.100.0/24 表示不许 192.168.100.0/24 之封包来源；

-d 目标 IP/网域：同 -s ，只不过这里指的是目标的 IP 或网域。	 
```
### 拒绝某ip的访问
```
iptables -A INPUT -p all -s 10.2.213.245 -j REJECT
```
* ssh立刻就断了，需要更换ip重新登入
* 删除规则
```
iptables -D INPUT 2
```
### 拒绝来自某一特定mac地址的访问
* 参数
```
[-m state] [--state 状态]
-m ：一些 iptables 的外挂模块，主要常见的有：
     state ：状态模块
     mac   ：网络卡硬件地址 (hardware address)
	 
--state ：一些封包的状态，主要有：
     INVALID    ：无效的封包，例如数据破损的封包状态
     ESTABLISHED：已经联机成功的联机状态；
     NEW        ：想要新建立联机的封包状态；
     RELATED    ：这个最常用！表示这个封包是与我们主机发送出去的封包有关
```
* 获取一台同局域网的mac地址02:00:2b:40:00:01
* 命令
```
iptables -A INPUT -p all -m mac --mac-source 02:00:2b:40:00:01 -j REJECT
```
* 成功！ 无法ping通
### 只开放本机的http服务，其余协议与端口均拒绝
* 参数
```
[-s 来源IP/网域] [--sport 埠口范围] [-d 目标IP/网域] [--dport 埠口范围]
--sport 埠口范围：限制来源的端口号码，端口号码可以是连续的，例如 1024:65535
--dport 埠口范围：限制目标的端口号码。
```
* 端口的概念只在tcp和udp协议下存在，故要加上 -p tcp/udp 选项
* iptable规则最最早匹配上的规则，故使用组合来屏蔽和放行端口
* 命令
```
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --sport 80 -j ACCEPT
iptables -A INPUT -p tcp -j DROP
```
### 拒绝回应来自某一特定IP地址的ping命令
* 命令
```
iptables -A INPUT -s 172.16.6.249 -p icmp --icmp-type 8 -j ACCEPT
```
* 测试成功
## 解释Linux网络设备工作原理
### bridge
#### 桥接
![pic2](https://github.com/magicfisk/mesos_learning/raw/master/homework5/exchange.jpg)
* 桥接就是把一台机器上的若干个网络接口连接起来，现实中的交换机就是一种设备，能连接不同局域网。
* 如图，每一个端口输入的包，会被复制到其他端口输出（初始）
* 网桥会记录输入包的mac地址，在下次收到发往该mac的包时，直接转发，而不是广播
#### linux bridge
![pic2](https://github.com/magicfisk/mesos_learning/raw/master/homework5/bridge.jpg)
* bridge的作用其实是一个虚拟的网桥，其行为和标准的网桥应该是类似的。连接了多个网卡（物理或者虚拟），并且能将报文转发到相应的出口，但也有不同的地方：linux内核的机器本身就是一台主机，有可能就是网络报文的目的地。其收到的报文除了转发和丢弃，还可能被送到网络协议栈的上层（网络层），从而被自己消化。
* 如图网桥设备br0绑定了eth0和eth1。对于网络协议栈的上层来说，只看得到br0，因为桥接是在数据链路层实现的，上层不需要关心桥接的细节。于是协议栈上层需要发送的报文被送到br0，网桥设备的处理代码再来判断报文该被转发到eth0或是eth1，或者两者皆是；反过来，从eth0或从eth1接收到的报文被提交给网桥的处理代码，在这里会判断报文该转发、丢弃、或提交到协议栈上层。
* Bridge 可以设置 IP 地址。通常来说 IP 地址是三层协议的内容，不应该出现在二层设备 Bridge 上。但是 Linux 里 Bridge 是通用网络设备抽象的一种，只要是网络设备就能够设定 IP 地址。当一个 bridge0 拥有 IP 后，Linux 便可以通过路由表或者 IP 表规则在三层定位 bridge0，此时相当于 Linux 拥有了另外一个隐藏的虚拟网卡和 Bridge 的隐藏端口相连，这个网卡就是名为 bridge0 的通用网络设备，IP 可以看成是这个网卡的。当有符合此 IP 的数据到达 bridge0 时，内核协议栈认为收到了一包目标为本机的数据，此时应用程序可以通过 Socket 接收到它。
### vlan
* 虚拟局域网（VLAN）是一组逻辑上的设备和用户，这些设备和用户并不受物理位置的限制，可以根据功能、部门及应用等因素将它们组织起来，相互之间的通信就好像它们在同一个网段中一样，由此得名虚拟局域网。VLAN的划分，使得广播域的范围可以人为设定，提高了安全性。同时因为广播域的缩小，在一定情况下，广播包涉及的机器会更加精准，提高广播效率。
* Linux 里的 VLAN 设备是对 802.1.q 协议的一种内部软件实现，模拟现实世界中的 802.1.q 交换机。Linux 里 802.1.q VLAN 设备是以母子关系成对出现的，母设备相当于现实世界中的交换机TRUNK 口，用于连接上级网络，子设备相当于普通接口用于连接下级网络。可以把 VLAN 母子设备作为一个整体想象为现实世界中的 802.1.q 交换机，下级接口通过子设备连接到寄主 Linux 系统网络里，上级接口同过主设备连接到上级网络，当母设备是物理网卡时上级网络是外界真实网络，当母设备是另外一个 Linux 虚拟网络设备时上级网络仍然是寄主 Linux 系统网络。需要注意的是母子 VLAN 设备拥有相同的 MAC 地址，可以把它当成现实世界中 802.1.q 交换机的 MAC，因此多个 VLAN 设备会共享一个 MAC。当一个母设备拥有多个 VLAN 子设备时，子设备之间是隔离的，不存在 Bridge 那样的交换转发关系
### veth
* VETH 设备总是成对出现，送到一端请求发送的数据总是从另一端以请求接受的形式出现。该设备不能被用户程序直接操作，但使用起来比较简单。创建并配置正确后，向其一端输入数据，VETH 会改变数据的方向并将其送入内核网络核心，完成数据的注入，在另一端能读到此数据。同时每个veth都可以被赋予IP地址，并参与三层网络路由过程。
## 说明在calico容器网络中，一个数据包从源容器发送到目标容器接收的具体过程。
### Calico 架构与核心组件
![pic3](https://github.com/magicfisk/mesos_learning/raw/master/homework5/calico_arch.png)
* Felix，Calico agent，跑在每台需要运行 workload 的节点上，主要负责配置路由及 ACLs 等信息来确保 endpoint 的连通状态；
* etcd，分布式键值存储，主要负责网络元数据一致性，确保 Calico 网络状态的准确性
* BGP Client(BIRD), 主要负责把 Felix 写入 kernel 的路由信息分发到当前 Calico 网络，确保 workload 间的通信的有效性；
* BGP Route Reflector(BIRD), 大规模部署时使用，摒弃所有节点互联的 mesh 模式，通过一个或者多个 BGP Route Reflector 来完成集中式的路由分发
* Calico 在每一个计算节点利用 Linux kernel 实现了一个高效的 vRouter 来负责数据转发 而每个 vRouter 通过 BGP 协议负责把自己上运行的 workload 的路由信息像在整个 Calico 网络内传播。小规模部署可以直接互联，大规模下可通过指定的 BGP route reflector 来完成。保证最终所有的 workload 之间的数据流量都是通过 IP 包的方式完成互联的。
* Calico 基于 iptables 还提供了丰富而灵活的网络 policy, 保证通过各个节点上的 ACLs 来提供 workload 的多租户隔离、安全组以及其他可达性限制等功能。
### Calico Docker network
#### CNM模型
* CNM模型是docker通信的一个抽象模型，calico是基于此来实现容器网络
![pic4](https://github.com/magicfisk/mesos_learning/raw/master/homework5/cnm-model.jpg)
* Sandbox，包含容器网络栈的配置，包括 interface，路由表及 DNS配置，对应的实现如：Linux Network Namespace；一个 Sandbox 可以包含多个 Network；
* Endpoint，做为 Sandbox 接入 Network 的介质，对应的实现如：veth pair，TAP；一个 Endpoint 只能属于一个 Network，也只能属于一个 Sandbox；
* Network，一组可以相互通信的 Endpoints；对应的实现如：Linux bridge，VLAN；Network 有大量 Endpoint 资源组成；
#### calico容器网络细节
![pic5](https://github.com/magicfisk/mesos_learning/raw/master/homework5/docker-calico-network.png)
* 当容器创建时，calico为容器生成veth pair，一端作为容器网卡加入到容器的网络命名空间，并设置IP和掩码，一端直接暴露在宿主机上，并通过设置路由规则，将容器IP暴露到宿主机的通信路由上。于此同时，calico为每个主机分配了一段子网作为容器可分配的IP范围，这样就可以根据子网的CIDR为每个主机生成比较固定的路由规则。
* 当容器需要跨主机通信时，主要经过下面的简单步骤：
* 1.容器流量通过veth pair到达宿主机的网络命名空间上。
* 2.根据容器要访问的IP所在的子网CIDR和主机上的路由规则，找到下一跳要到达的宿主机IP。
* 3.流量到达下一跳的宿主机后，根据当前宿主机上的路由规则，直接到达对端容器的veth pair插在宿主机的一端，最终进入容器。
## 调研除calico以外的任意一种容器网络方案，比较其与calico的优缺点。
* weave通过在docker集群的每个主机上启动虚拟的路由器，将主机作为路由器，形成互联互通的网络拓扑，在此基础上，实现容器的跨主机通信。
![pic6](https://github.com/magicfisk/mesos_learning/raw/master/homework5/weave-host-topology.png)
* 如上图所示，在每一个部署Docker的主机（可能是物理机也可能是虚拟机）上都部署有一个W（即weave router，它本身也可以以一个容器的形式部署）。weave网络是由这些weave routers组成的对等端点（peer）构成，并且可以通过weave命令行定制网络拓扑。
* 当容器通过weave进行跨主机通信时，其网络通信模型可以参考下图：
![pic6](https://github.com/magicfisk/mesos_learning/raw/master/homework5/docker-weave-network.png)
* 对每一个weave网络中的容器，weave都会创建一个网桥，并且在网桥和每个容器之间创建一个veth pair，一端作为容器网卡加入到容器的网络命名空间中，并为容器网卡配置ip和相应的掩码，一端连接在网桥上，最终通过宿主机上weave router将流量转发到对端主机上。
* 基本流程：
* 容器流量通过veth pair到达宿主机上weave router网桥上。
* weave router在混杂模式下使用pcap在网桥上截获网络数据包，并排除由内核直接通过网桥转发的数据流量，例如本子网内部、本地容器之间的数据以及宿主机和本地容器之间的流量。捕获的包通过UDP转发到所其他主机的weave router端。
* 在接收端，weave router通过pcap将包注入到网桥上的接口，通过网桥的上的veth pair，将流量分发到容器的网卡上。
### calico和weave的比较
#### weave
* 优点：weave默认基于UDP承载容器之间的数据包，并且可以完全自定义整个集群的网络拓扑，比较灵活
* 缺点1：
weave自定义容器数据包的封包解包方式，不够通用，传输效率比较低，性能上的损失也比较大。
* 缺点2：集群配置比较负载，需要通过weave命令行来手工构建网络拓扑，在大规模集群的情况下，加重了管理员的负担。
#### calico
* 优点：跨主机通信时，整个通信路径完全没有使用NAT或者UDP封装，性能上的损耗确实比较低
* 缺点1：calico目前只支持TCP、UDP、ICMP、ICMPv6协议，如果使用其他四层协议（例如NetBIOS协议），建议使用weave、原生overlay等其他overlay网络实现。
* 缺点2：基于三层实现通信，在二层上没有任何加密包装，因此只能在私有的可靠网络上使用。
* 缺点3：流量隔离基于iptables实现，并且从etcd中获取需要生成的隔离规则，有一些性能上的隐患。
