# ��������ҵ
## 1.��װdocker
![pic1](https://github.com/magicfisk/mesos_learning/tree/master/homework3/install.jpg)
## docker��������
### docker run
* �﷨
```
docker run  [OPTIONS] IMAGE[:TAG] [COMMAND] [ARG...]
```
* ����һ���µ�����������ӵ���Լ����ļ�ϵͳ������
* IMAGE[:TAG]ֵ��������
* commandΪ�������к�ִ�е�ָ��
* argΪcommand����

* ����options
```
-d			  ��̨ (ǰ̨Ĭ��)
-a, --attach value	  ����������stdin��stdout��stderr
-t			  ʹ���նˡ������� -iһ��ʹ�á�
-i			  ��STDIN������������������ -tһ��ʹ�á�
-m, --memory string    	  �ڴ�����(��λ:b, k, m or g)
-c, --cpu-shares int   	  CPU���ȼ� (���Ȩ��)
-u, --user string	  �����û���
-w,--workdir string	  ���ù���Ŀ¼ Ĭ��Ϊ��Ŀ¼
-e,--env value		  ���û�������
-p			  �������˿ں������˿�����ת�� -p ip:80:80
-h,--hostname string      ������������
-v, --volume value	  ���ر���Ŀ¼��Ŀ¼ǰ���Ǳ���Ŀ¼�������Ǿ���Ŀ¼
				����docker run --rm-i -t -v /home/hyzhou/docker:/data:rw ubuntu:14.04 /bin/bash
--volumes-from		  ���������ع���Ŀ¼
--name string		  ��������
--dns	              	  ����������DNS������
--net	        	  �����������������ӷ�ʽbridge,none,Container:<name|id>,host
--ip/--ip6		  ������ip��ַ
```
����Ϊȫ��option
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
* �﷨
```
docker start [OPTIONS] CONTAINER [CONTAINER...]
```
* ���������˵�û�����е�����
Options����
```
  -a, --attach               ����������stdout��stderr���ź�
      --detach-keys string   ����key sequence�����뿪����
  -i, --interactive          ����������stdin
```
### docker commit
* �﷨
```
docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]
```
* ����һ���µľ���
* CONTAINER��Ҫ�����ݵľ�������
* REPOSITORY����ֿ⣬�����Ǳ��ػ���Զ��
* options
```
  -a, --author string    ����
  -c, --change value     ʹ��Dockerfile�е�ָ��
  -m, --message string   ˵��
  -p, --pause            �ύʱ��ͣ������Ĭ�Ͽ���
```
### docker build
* �﷨
```
 docker build [OPTIONS] PATH | URL | -
```
* ����dockerfile�����¾���
* PATH | URL | - Ϊdockerfile·��
* options
```
      --build-arg value         ���û�������
      --cgroup-parent string    ���ø�cgroup
      --cpu-period int          cpuʹ������
      --cpu-quota int           cpuʹ����
  -c, --cpu-shares int          ���ȼ�
      --cpuset-cpus string      �������е�cpu���
      --cpuset-mems string      ����ʹ���ڴ�ı��
      --disable-content-trust   ����������֤
  -f, --file string             dockerfile���֣�Ĭ��ΪPATH/Dockerfile
      --force-rm                �Ƴ��м�����ľ��������Ƿ�ɹ�build
      --isolation string        ָ�������ķ��༼��
      --label value             ����Ԫ����
  -m, --memory string           �ڴ�����
      --memory-swap string      �����������ƣ�-1Ϊ������
      --no-cache                ��ʹ��cache
      --pull                    ���Ǵ������°汾�ľ���
  -q, --quiet                   �ɹ�ʱ����ӡID
      --rm                      �Ƴ��м�����ľ��񣬵��ɹ�buildʱ
      --shm-size string        	�����ڴ�/dev/shm�Ĵ�С,Ĭ��64MB
  -t, --tag value               ���ƺͱ�ǩ
      --ulimit value            ulimit����shell����������ռ�õ���Դ
```
### docker images
* �﷨
```
docker images [OPTIONS] [REPOSITORY[:TAG]]
```
* �г����صľ���
* [REPOSITORY[:TAG]]�п����趨�ؼ���
* options
```
  -a, --all             չʾ���У�Ĭ�������м���̾���
      --digests         ��ʾժҪ
  -f, --filter value    ���������������
      --format string   ��goģ���ʽ�����
      --no-trunc        ��Ҫ�ü������id��
  -q, --quiet           ֻ��ӡ����ID
```
### docker network
* docker network��6�������
#### docker network connect
* �﷨
```
docker network connect [OPTIONS] NETWORK CONTAINER
```
* ��һ��������������
* networkΪ�������������
* containerΪ��������
* options��
```
      --alias value           Ϊ��������������
      --ip string             IP Address
      --ip6 string            IPv6 Address
      --link value            ��ӵ�����������������
      --link-local-ip value   Ϊ�������ӱ�������
```
#### docker network create
* �﷨
```
docker network create [OPTIONS] NETWORK
```
* ��������
* networkΪ��������
* options
```
      --aux-address value    ���������õ�����ipv4��6��ַ
  -d, --driver string        ָ������������Ĭ��Ϊbridge
      --gateway value        IPv4��IPv6����������
      --internal             �����ⲿ���ʸ�����
      --ip-range value       ��һ�ε�ַ�з���ip
      --ipam-driver string   ip��ַ��������
      --ipam-opt value       ip��ַ����������ѡ��
      --ipv6                 ʹ��ipv6
      --label value          ����Ԫ����
  -o, --opt value            ��������ѡ��
      --subnet value         CIDR��ʽ������
```
##### docker network disconnect
* �﷨
```
docker network disconnect [OPTIONS] NETWORK CONTAINER
```
* �Ͽ�����
options
```
  -f, --force   ǿ�ƶϿ�
```
#### docker network inspect
* �﷨
```
docker network inspect [OPTIONS] NETWORK [NETWORK...]
```
* չʾ����ϸ��
* Options
```
  -f, --format string 	����goģ���ʽ�����
```
#### docker network ls
* �﷨
```
docker network ls [OPTIONS]
```
* �г�����
* options��
```
  -f, --filter value   ɸѡ���
      --no-trunc       ���ض����
  -q, --quiet          ֻ��ӡ����ID
```
#### docker network rm
* �﷨
```
docker network rm NETWORK [NETWORK...]
```
* �Ƴ�һЩ����
## ����һ����������Ϊubuntu��docker������������м���nginx������
* ��������
```
sudo run docker -it --name mydocker ubuntu /bin/bash
```
* ���뾵���
```
apt-get update
apt-get install nginx -y
apt-get install vim -y
nginx -t //�ҵ������ļ�
vi /etc/nginx/nginx.conf
```
* �޸������ļ�
��htmlģ���£�ɾ��virtual host
����
```
	server {
		listen 80;
		location / {
		root /home;
		index index.html;
		}}
```
* ��/home/ ���½�index.html��дһ�������Լ���Ϣ��html�ļ�
* �ڸ�Ŀ¼���½�һ�����нű� run.sh
```
nginx
tail -f /var/log/nginx/access.log
```
* �˳�docker
* ִ������,���澵��
```
docker commit mydocker mydocker:v4
```
* ���Ч��
```
docker run -it --net=host mydocker:v4 /bin/bash /run.sh
```
* �������Ͻ�80�˿�ת����8888�˿���
* ����http://162.105.174.33:8888/ ������ҳ
![pic2](https://github.com/magicfisk/mesos_learning/tree/master/homework3/index.jpg)
* �����Լ�������,Ĭ��Ϊbridge
```
docker network create mynet
```
* �����µľ��񣬲������ԭ�����жϿ�
```
docker run -it --net=bridge --name mydocker -d -p 80:80 mydocker:v4 /bin/bash /run.sh
docker network disconnect bridge mydocker
```
* ��ʱ��ҳ�޷���
* ����mynet
```
docker network connect mynet mydocker
```
* ��ʱ��ҳ������
* ��������
```
docker network inspect mynet //���������Ϣ
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
* ��������
```
root@oo-lab:~# curl 172.18.0.1:80
<!DOCTYPE html>
<p>ѧ�ţ�1400012801</p>
<p>���֣�Ҷ�ȴ�</p>
<p>����һ��</p>
</html>`
```

## �����������Ϻ�docker�ĵ�������null,bridge,host,overlay����ģʽ������
### noneģʽ
Docker����ӵ���Լ���Network Namespace����û���κ��������ã�������ip��·����Ϣ������Ҫ�Լ��ֶ����
### hostģʽ
һ����������ʱ�ᴴ���Լ���Network Namespace�����ں�����������и��룬��ʱhostģʽ��������������һ��nemaspace��ʹ��������ip���˿�
### containerģʽ
����ͬ�����ᴴ���Լ���namespace����ʱ������һ����������һ��namespace
### bridgeģʽ
Ĭ�ϵ�����ģʽ��ÿ��docker�����Լ���namespace��������ip�������������ӵ�docker0�����������ϡ�docker0��docker�Լ����������硣������ʽ�������������Ĺ�����ʽ��docker���Ȼ��һ�����������Σ���172.17.0.0/16������ 172.17.42.1/16�����docker0���ţ��е����صĹ�������������ip��ָ��������ӵ��������docker��
### overlayģʽ
* overlayģʽ��docker�к�swarm��Ⱥ��������صġ�
* overlayģʽ�ṩ�˿�����������Ļ�����ʡ�
* �ڶ���overlayģʽ�У�ֱ�ӵ���swarm��ʵ��overlayģʽ
```
docker swarm init --advertise-addr 172.16.6.153
```
* �õ�join����
```
docker swarm join \
    --token SWMTKN-1-4u0sy656s8vxum227x29gqzhqizafk1o9lpgwu4kdpwfpcerz2-chl8std2ky8yvhy2n851e2m9j \
    172.16.6.153:2377
```
* ������һ̨������ִ������
```
Error response from daemon: Timeout was reached before node was joined. The attempt to join the swarm will continue in the background. Use the "docker info" command to see the current swarm status of your node.
```
* ���˵�ë��(GG)
* ��manager�ϲ鿴�ڵ�,���Կ�������ڵ�
```
docker node ls
ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
7kuftpv9nz94acl3nfy281jkh *  oo-lab    Ready   Active        Leader
```
## �Ķ�mesos�и�����docker�����Ĵ��룬̸̸mesos��������docker���н����ģ�������docker����run������������ʲô��
* docker.cpp�Ǹ��𹹽�docker���������
* spec.cpp��info��Ϣ��װ��c++��
* executor.cpp������docker�Ĵ��룬����framework�е�executor������ִ��docker�а�װ����������
* mesos��docker�Ľ����൱��mesos������һ��executor��Ȼ����ø���docker����������docker������ֱ������dockerû��ʲô��������ֻ�ǰ���һ��������Զ�̵���

### docker run
* ���containnerInfo�Ƿ����
* ��ʼ�����������
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
* �����Դ��Ϣ�����趨��Ӧ���������벻���ˣ�
* ��黷�����������趨�������
* ����mesos sandbox��ز���
* ��������Ϣ�����趨�������
* ��sandbox��Ŀ¼���������У�ͨ�����صķ�ʽ
* ���־�volume���������ĸ�����mesosֻ֧��һ��������docker����
* ����������Ϣ
* ����hostname
* ����docker��option��Ϣ
* ����˿�ӳ��
* ����Ӳ����Ϣ
* ���������в���
* ������������
* ����������ϣ�д����־
* �������߳�ϵͳ��������
* �½����߳�ʵ��
* �������߳�


## дһ��framework���������ķ�ʽ����task������ǰ�汣���nginx��������������ΪHOST��
* ����agent���̣�����ѡ��--containerizers=docker,mesos
* ��pymesos���޸Ĵ���
* ���ÿ����Ϣ��������һ��MesosSchedulerDriver
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
* MinimalScheduler��ʵ��
```
class MinimalScheduler(Scheduler):
    def __init__(self):
        self.Task_launched=False

        

#mesos�ṩ��Դʱ�Ĵ�����            
    def resourceOffers(self, driver, offers):    

                
        filters = {'refuse_seconds': 5}
        #�ַ�����
        for offer in offers:
		cpus = self.getResource(offer.resources, 'cpus')
		mem = self.getResource(offer.resources, 'mem')
			
		#ֻ����һ��
		if self.Task_launched:
		continue
				
		#��Դ���	
		if cpus < TASK_CPU or mem < TASK_MEM:
			continue
		self.Task_launched=True	

		#����docker��Ϣ
		DockerInfo = Dict()
		DockerInfo.image = 'mydocker:v4'
		DockerInfo.network = 'HOST'

		#����������Ϣ
		ContainerInfo = Dict()
		ContainerInfo.type = 'DOCKER'
		ContainerInfo.docker = DockerInfo
			
		#��������
		CommandInfo = Dict()
		CommandInfo.shell = False
		CommandInfo.value = '/bin/bash'
		CommandInfo.arguments = ['/run.sh']
			
		#����task
		task = Dict()
		task_id = str(uuid.uuid4())
		task.task_id.value = task_id
		task.agent_id.value = offer.agent_id.value
		task.name = 'mydocker'
			
		#���������������task
		task.container = ContainerInfo
		task.command = CommandInfo

		task.resources = [
              	  dict(name='cpus', type='SCALAR', scalar={'value': TASK_CPU}),
           	     dict(name='mem', type='SCALAR', scalar={'value': TASK_MEM}),
        	    ]
		
		driver.launchTasks(offer.id, [task], filters) #��������

    #״̬���»ص�
    def statusUpdate(self, driver, update):
		return
       
	#������Դ  
    def getResource(self, res, name):
        for r in res:
            if r.name == name:
                return r.scalar.value
        return 0.0
```
* ���нű�
```
python scheduler.py 172.16.6.153
```
* ���Կ���agent������
![pic3](https://github.com/magicfisk/mesos_learning/tree/master/homework3/agent.jpg)
* docker����
![pic4](https://github.com/magicfisk/mesos_learning/tree/master/homework3/docker.jpg)
* ��ҳ��������
![pic2](https://github.com/magicfisk/mesos_learning/tree/master/homework3/index.jpg)

