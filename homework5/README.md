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
* 结合基本语法实现一下操作
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
```
iptables -A INPUT -p all -m mac --mac-source 02:00:34:91:00:05 -j REJECT
```
* 没用T.T
* 研究发现这台服务器原来挂掉了，助教给重启了
* 然而助教并不是重启，是图方便重新给了一台233
* 因此这台服务器和原来两台不在一个局域网
* 访问服务器时，经过多个网关。同时mac地址是链路层的，而不属于ip层，ip包到达时，获得的mac地址应该是网关的
* mac过滤只对局域网有效！！
* 获取另外一台同局域网的mac地址02:00:2b:40:00:01
```
iptables -A INPUT -p all -m mac --mac-source 02:00:2b:40:00:01 -j REJECT
```
* 成功！ 无法ping通

