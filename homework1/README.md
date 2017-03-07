第一次作业
===============
1.mesos的架构
----------------
mesos是一个二级调度架构的框架。mesos本身不对资源的分配进行具体的布置。<br>
mesos的作用是整合资源，将这些资源预分配给调度框架，调度框架针对具体的算法进行再次调度<br>
mesos相当于一个底层的资源管理器，负责资源的管理。<br>
调度框架是在mesos上一层，负责资源分配的细节<br>
2.数据中心操作系统的概念
----------------
数据中心操作系统的管理员可以通过各种工具和技术的结合，在单个数据中心操作系统就能完成对多个服务器的管理工作，这样能让工作更有效率。(来自百度百科）<br>
数据中心操作系统就是将多台服务器的资源整合，使得对用户而言，拥有一台很多资源的机器，无需关心跨机器的资源调度和使用的细节<br>
3.虚拟机和容器
--
虚拟机在硬件层面与主机进行了隔离，运行自己的内核，拥有自己的整套运行环境<br>
容器与主机共享内核，在内核层面与主机隔离，只携带运行服务时需要的上下文环境<br>
容器比虚拟机更加灵活，资源占用小，一般是用于特定服务的运行<br>
虚拟机比容器更加安全，有着更多的功能和扩展性<br>
4.mesos的安装和配置
--
利用git clone 下载mesos的代码，使用checkout切换为1.1.0版本<br>
按照mesos的文档运行命令

```
# Change working directory.
$ cd mesos

# Bootstrap (Only required if building from git repository).
$ ./bootstrap

# Configure and build.
$ mkdir build
$ cd build
$ ../configure
$ make

# Run test suite.
$ make check

# Install (Optional).
$ make install
```

运行测试代码
```
# Change into build directory.
$ cd build

# Start mesos master (Ensure work directory exists and has proper permissions).
$ ./bin/mesos-master.sh --ip=127.0.0.1 --work_dir=/var/lib/mesos

# Start mesos agent (Ensure work directory exists and has proper permissions).
$ ./bin/mesos-agent.sh --master=127.0.0.1:5050 --work_dir=/var/lib/mesos

# Visit the mesos web page.
$ http://127.0.0.1:5050

# Run C++ framework (Exits after successfully running some tasks.).
$ ./src/test-framework --master=127.0.0.1:5050

# Run Java framework (Exits after successfully running some tasks.).
$ ./src/examples/java/test-framework 127.0.0.1:5050

# Run Python framework (Exits after successfully running some tasks.).
$ ./src/examples/python/test-framework 127.0.0.1:5050
```
其中c的framework在make install执行前是无法完成的

5.spark的配置
--
下载编译过的官方包，放在/usr/local 目录下，改名为spark.tar.gz，解压<br>
进入conf，新建spark-env.conf，并且修改<br>
```
export MESOS_NATIVE_JAVA_LIBRARY=/usr/local/lib/libmesos.so
export SPARK_EXECUTOR_URI=/usr/local/spark.tar.gz
```
新建spark-defaults.conf
```
spark.executor.uri	/usr/local/spark.tar.gz
spark.mesos.executor.home /usr/local/spark.tar.gz
spark.master	mesos://127.0.0.1:5050
```

运行wordcount测试
```
./bin/spark-submit \
  --class org.apache.spark.examples.JavaWordCount \
  --master mesos://127.0.0.1:5050 \
  --total-executor-cores 2 \
  ./spark-examples_2.11-2.1.0.jar \
  ./txt
```
生成了一个100w句的文本，大小为20M左右<br>
分别以1、2、4个core运行<br>
时间分别如下<br>
![time-cpu-1](https://github.com/magicfisk/mesos_learning/blob/master/homework1/time-cpu-1.png)
![time-cpu-2](https://github.com/magicfisk/mesos_learning/blob/master/homework1/time-cpu-2.png)
![time-cpu-4](https://github.com/magicfisk/mesos_learning/blob/master/homework1/time-cpu-4.png)

资源显示如下<br>
![cpu-1](https://github.com/magicfisk/mesos_learning/blob/master/homework1/cpu-1.jpg)
![cpu-2](https://github.com/magicfisk/mesos_learning/blob/master/homework1/cpu-2.jpg)
![cpu-4](https://github.com/magicfisk/mesos_learning/blob/master/homework1/cpu-4.jpg)
从结果可以发现，2个cpu最快，4个cpu比1个cpu反而更慢，通信代价更大
6.联机测试
---
![tasks](https://github.com/bacTlink/OS-practice/raw/master/%E7%AC%AC1%E6%AC%A1%E4%BD%9C%E4%B8%9A/Tasks.png)
magicfisk的slaver
![Union](https://github.com/bacTlink/OS-practice/raw/master/%E7%AC%AC1%E6%AC%A1%E4%BD%9C%E4%B8%9A/Union.png)
agent截图已经下线，并没有上镜T.T
7.安装的看法
---
mesos的编译资源消耗略大<br>
开始mesos无法找到master的ip，靠重装虚拟机解决<br>
spark的配置文件中spark.executor.uri 一开始使用官网的地址，导致运行错误<br>

