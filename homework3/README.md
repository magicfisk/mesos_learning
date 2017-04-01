#��������ҵ
##1.��װdocker
@����ͼƬ
##docker��������
###docker run
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
-d						  ��̨ (ǰ̨Ĭ��)
-a, --attach value		  ����������stdin��stdout��stderr
-t				          ʹ���նˡ������� -iһ��ʹ�á�
-i						  ��STDIN������������������ -tһ��ʹ�á�
-m, --memory string    	  �ڴ�����(��λ:b, k, m or g)
-c, --cpu-shares int   	  CPU���ȼ� (���Ȩ��)
-u, --user string		  �����û���
-w,--workdir string		  ���ù���Ŀ¼ Ĭ��Ϊ��Ŀ¼
-e,--env value			  ���û�������
-p						  �������˿ں������˿�����ת�� -p ip:80:80
-h,--hostname string      ������������
-v, --volume value		  ���ر���Ŀ¼��Ŀ¼ǰ���Ǳ���Ŀ¼�������Ǿ���Ŀ¼
							����docker run --rm-i -t -v /home/hyzhou/docker:/data:rw ubuntu:14.04 /bin/bash
--volumes-from			  ���������ع���Ŀ¼
--name string			  ��������
--dns	              	  ����������DNS������
--net	        	  	  �����������������ӷ�ʽbridge,none,Container:<name|id>,host
--ip/--ip6				  ������ip��ַ
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
###docker start
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
###docker commit
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
###docker build
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
###docker images
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
###docker network
* docker network��6�������
####docker network connect
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
####docker network create
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
#####docker network disconnect
* �﷨
```
docker network disconnect [OPTIONS] NETWORK CONTAINER
```
* �Ͽ�����
options
```
  -f, --force   ǿ�ƶϿ�
```
####docker network inspect
* �﷨
```
docker network inspect [OPTIONS] NETWORK [NETWORK...]
```
* չʾ����ϸ��
* Options
```
  -f, --format string 	����goģ���ʽ�����
```
####docker network ls
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
####docker network rm
* �﷨
```
docker network rm NETWORK [NETWORK...]
```
* �Ƴ�һЩ����
##����һ����������Ϊubuntu��docker������������м���nginx������
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
@����ͼƬ
* �����Լ�������,Ĭ��Ϊbridge
```
docker network create mynet
```
* �����µľ���
```
docker run -it --net=bridge --name mydocker -d -p 80:80 mydocker:v4 /bin/bash /run.sh
docker network disconnect bridge mydocker
```
* ��ʱ��ҳ�޷���
```
docker network connect mynet mydocker
```
��ʱ��ҳ������
##�����������Ϻ�docker�ĵ�������null,bridge,host,overlay����ģʽ������
###



