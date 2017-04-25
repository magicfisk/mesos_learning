# ���Ĵ���ҵ
## HDFS
### ǰ������Ŀ��
* Ӳ�������ǳ�̬,�����쳣���,��˴�����Ϳ��١��Զ��Ļָ���HDFS�ĺ��ļܹ�Ŀ�ꡣ
* ����HDFS�ϵ�Ӧ����һ���Ӧ�ò�ͬ,������Ҫ������ʽ��Ϊ��,��������������֤�ӳ�,׷�����������
* HDFS��֧�ִ����ݼ���ΪĿ��,һ���洢������ĵ����ļ���Сһ�㶼��ǧ����T�ֽ�,һ����һHDFS��֧������ǧ��Ƶ��ļ�
* HDFSӦ�ö��ļ�Ҫ�����write-one-read-many����ģ�͡�һ���ļ�����������д,�ر�֮��Ͳ���Ҫ�ı�,����������һ��������
* �ƶ�����Ĵ��۱�֮�ƶ����ݵĴ��۵͡�HDFS�ṩ��Ӧ�ý������ƶ������ݸ����Ľӿڡ�
* ���칹��Ӳ�������ƽ̨�ϵĿ���ֲ�ԡ�
### HDFS��������
#### ���ݿ�
* HDFSĬ�ϵ�������Ĵ洢��λ��64M�����ݿ�,������ݿ��������һ����ļ�����ķֿ���һ����
#### Ԫ���ݽڵ� namenode
* ���������ļ�ϵͳ�������ռ�,�������е��ļ����ļ��е�Ԫ���ݱ�����һ���ļ�ϵͳ���С�
#### ���ݽڵ� datanode
* ���������洢�����ļ���
#### ��Ԫ���ݽڵ� secondarynamenode
* �����Խ�Ԫ���ݽڵ�������ռ侵���ļ����޸���־�ϲ�,�Է���־�ļ�����
* �ϲ���������ռ侵���ļ��ڴ�Ԫ���ݽڵ���Ҷ����һ��,�Է�Ԫ���ݽڵ�ʧЧ��ʱ�����ڻָ���
### HDFS����
![pic1](https://github.com/magicfisk/mesos_learning/raw/master/homework4/HDFS-A.gif)
* HDFS����master/slave�ܹ�,��һ��Namenode��һ����Ŀ��Datanode���
* Namenode��һ�����ķ�����,��������ļ�ϵͳ��namespace�Ϳͻ��˶��ļ��ķ��ʣ�ֻ��һ��������
* Datanode�ڼ�Ⱥ��һ����һ���ڵ�һ��,�������ڵ������Ǹ����Ĵ洢
* һ���ļ��ֳ�һ������block,��Щblock�洢��Datanode������
* Namenodeִ���ļ�ϵͳ��namespace����,ͬʱ����block������Datanode�ڵ��ӳ��
* Datanode��Namenode��ָ���½���block�Ĵ�����ɾ���͸���
* �û������ݵĶ�д��ֱ����Datenode�ϵ�,����ͨ��namenode
### ����
* HDFS��ÿ���ļ��洢��block����,�������һ��block,���е�block����ͬ���Ĵ�С���ļ�������blockΪ���ݴ��ᱻ���ƶ��
* HDFS����one-write����,�����޸��ļ�,ֻ�ܴ�����׷��
* �ڴ���������,replication������3,HDFS�Ĵ�Ų����ǽ�һ����������ڱ��ػ����ϵĽڵ�,һ����������ͬһ�����ϵ���һ���ڵ�,���һ���������ڲ�ͬ�����ϵ�һ���ڵ㡣
* Ϊ�˽�������Ĵ������ĺͶ���ʱ,HDFS�ᾡ����reader������ĸ����������reader��ͬһ����������һ������,��ô�Ͷ��ø��������һ��HDFS��Ⱥ��Խ�����������,��ôreaderҲ�����ȳ��Զ������������ĵĸ�����
### �ռ�Ļ���
* �û�����Ӧ��ɾ��ĳ���ļ�,����ļ���û�����̴�HDFS��ɾ�����෴,HDFS������ļ�������,��ת�Ƶ�/trashĿ¼���Ա���ٻָ�
* ����һ��ʱ��,Namenode�ͻὫ���ļ���namespace��ɾ��,Ҳ���ͷŹ������ļ������ݿ顣


### ʹ�÷�ʽ
#### shell
```
bin/hadoop fs <args>
```
ͨ��������ʽ������������hadoop������ز���
#### web
* �ڲ���hadoop�Ļ����ϣ�������һ��web��������ͨ������web��ҳ���鿴�ļ�

## GlusterFS
### ����
GlusterFS���õ��Թ�ϣ�㷨�ڴ洢���ж�λ����,�����ǲ��ü���ʽ��ֲ�ʽԪ���ݷ�������������������Scale-Out�洢ϵͳ��,Ԫ���ݷ�����ͨ���ᵼ��I/O����ƿ���͵���������⡣GlusterFS��,������Scale-Out�洢�����еĴ洢ϵͳ���������ܵض�λ�������ݷ�Ƭ,����Ҫ�鿴����������������������ѯ��������ƻ�����ȫ���л������ݷ���,ʵ��������������������չ��
### ���
![pic2](https://github.com/magicfisk/mesos_learning/raw/master/homework4/GlusterFS_inside.png)
#### �ⲿ�ṹ
* �ɴ洢��������BrickServer�����ͻ����Լ�NFS/Samba �洢�������
* GlusterFS �ܹ���û��Ԫ���ݷ��������
#### �ڲ��ṹ
* GlusterFS�ڲ�����ģ�黯����ջʽ�ļܹ�,��ͨ����������֧�ָ߶ȶ��ƻ���Ӧ�û�����

### �洢
#### ����
* Brick���洢������λ
* Volume�����brick��ɵ�����洢�ռ䣬���Ա�����
#### Volume
##### distribute volume
* �ļ�ͨ��hash�㷨�ֲ�������brick server�������һ�����̻��ˣ���Ӧ������Ҳ��ʧ���ļ���RAID 0���������ݴ�����
##### stripe volume
* ����RAID0���ļ��ֳ����ݿ���Round Robin��ʽ�ֲ���brick server�ϣ��������������ݿ飬֧�ֳ����ļ������ļ����ܸ�
##### replica volume
* �ļ�ͬ�����Ƶ����brick�ϣ��ļ���RAID 1�������ݴ�������д�����½�������������
##### ����
�����������Ե����

### glusterfs���幤������
* �ڿͻ���,�û�ͨ��glusterfs��mount point����д����,�����û���˵,,��Ⱥϵͳ�Ĵ��ڶ��û�����ȫ͸����,�û��о������ǲ�������ϵͳ����Զ�˵ļ�Ⱥϵͳ
* �û�������������ݽ��� ����linuxϵͳ��VFS������
* VFS�����ݵݽ���FUSE�ں��ļ�ϵͳ��fuse�ļ�ϵͳ���ǽ�����ͨ��/dev/fuse����豸�ļ��ݽ�����glusterfs client�ˣ��൱���ļ�ϵͳ����
* client�����ݽ���һЩָ���Ĵ���ͨ�����罫���ݵݽ���Glusterfs Server
* Glusterfs Server������д����Ӧλ��

### ʹ�÷�ʽ
* ����������

## �����ļ�ϵͳ
### AUFS����
* AUFS��һ��Union File System�������Ŀ¼�ϲ���һ�������ļ�ϵͳ,��ԱĿ¼��Ϊ�����ļ�ϵͳ��һ����֧��branch��
* ÿ��branch����ָ�� readwrite/whiteout�\able/readonlyȨ��,ֻ����ro��,��д��rw��,д���أ�wo����
* һ�������,aufsֻ�����ϲ��branch���ж�дȨ��,����branch��Ϊֻ��Ȩ�ޡ�ֻ��branchֻ���߼����޸ġ�
### AUFS��д
* �޸�һ���ļ�,�����ļ�λ�ڵͲ�branchʱ,����branch��ֱ�Ӹ��ƵͲ�branch���ļ��������ٽ����޸�,���Ͳ���ļ�����
* ������ɾ��һ���Ͳ�branch�ļ�ʱ,ֻ���ڶ���branch�Ը��ļ�����������������,ʵ�ʲ�δɾ���ļ�,ֻ�ǲ��ɼ�
### AUFS������
* AUFS������еķ�֧mount����,����,�ڲ����ļ����ǱȽ����ˣ�O(n)��
* AUFS�ҵ����ļ�,�Ժ�Ķ�д�Ͳ���ԭ�ļ���������һ����
### docker��AUFS
* Docker����Image������һ������AUFS branch���,�������е�branch��Ϊֻ��Ȩ�ޡ�
* ������������ʱ��,����һ��AUFS branchλ��image��֮��,����rwȨ��,������Щbranch���Ϲ��ص�һ�����ص��¡�
* �����������ʱ,ֻ�贴�������������Ŀ¼,ʹ��aufs����������Ŀ¼������ImageĿ¼֮��,����Լ����Դ
### ʹ�÷�ʽ
```
sudo mount -t aufs -o br=/a:/b:/c none /aufs
```
* ����������԰�a,b,c���ص�aufs�ļ�����,����aΪ���ϲ�,cΪ���²�
## ��װ����GlusterFS
### ��װ
```
sudo apt-get install -y software-properties-common
sudo add-apt-repository ppa:gluster/glusterfs-3.8
sudo apt-get update
sudo apt-get install -y glusterfs-server
```
* �������װ�˷����
```
apt-get install -y glusterfs-client
```
* ��װ�ͻ���
### ����
```
sudo service glusterfs-server start
```
* ��������
```
sudo service glusterfs-server status

�� glusterfs-server.service - LSB: GlusterFS server
   Loaded: loaded (/etc/init.d/glusterfs-server; bad; vendor preset: enabled)
   Active: active (running) since Sat 2017-04-15 16:30:30 EDT; 2 days ago
     Docs: man:systemd-sysv-generator(8)
  Process: 11880 ExecStop=/etc/init.d/glusterfs-server stop (code=exited, statu
  Process: 12232 ExecStart=/etc/init.d/glusterfs-server start (code=exited, sta
    Tasks: 34
   Memory: 83.0M
      CPU: 41.507s
   CGroup: /system.slice/glusterfs-server.service
           ����11512 /usr/sbin/glusterfsd -s 172.16.6.153 --volfile-id gvol0.172.
           ����12239 /usr/sbin/glusterd -p /var/run/glusterd.pid
           ����12473 /usr/sbin/glusterfs -s localhost --volfile-id gluster/gluste

Apr 15 16:30:28 oo-lab systemd[1]: Starting LSB: GlusterFS server...
Apr 15 16:30:28 oo-lab glusterfs-server[12232]:  * Starting glusterd service gl
Apr 15 16:30:30 oo-lab glusterfs-server[12232]:    ...done.
Apr 15 16:30:30 oo-lab systemd[1]: Started LSB: GlusterFS server.
```
* ȷ�Ϸ�������
### ������εķ����
```
gluster peer probe 172.16.6.153

gluster pool list   //�鿴�洢�б�
UUID                                    Hostname        State
3a362a72-95ef-44e3-8f34-5af9c00767b3    172.16.6.153    Connected
d44f85da-69fd-499a-8b50-f009a078e99e    localhost       Connected

```

### ����volume������
```
mkdir -p /data/gluster/gvol0
gluster volume create gvol0 replica 2 172.16.6.249:/data/gluster/gvol0 172.16.6.153:/data/gluster/gvol0 force
gluster volume start gvol0 //������
```
* ��/data/gluster/gvol0��Ϊbrick��������һ̨���������еڶ����������һ�����ƾ�
```
mount -t glusterfs 172.16.6.249:/gvol0 /mnt/glusterfs
```
* ��������Ŀ¼�����ڱ��ص�/mnt/glusterfsĿ¼��

### ����
* ��/mnt/glusterfs��
```
vi index.html //д��һ����ҳ
```
* �ڷ������ϲ鿴�ļ�����
```
root@oo-lab:/data/gluster/gvol0# ls
index.html
```
* �ƻ�һ���������ϵ��ļ���
```
Broadcast message from systemd-journald@oo-lab (Mon 2017-04-17 21:33:54 EDT):

data-gluster-gvol0[33275]: [2017-04-18 01:33:54.693674] M [MSGID: 113075] [posix-helpers.c:1821:posix_health_check_thread_proc] 0-gvol0-posix: health-check failed, going down
```
* �ļ��������ڹ��ص㿴��
```
root@oo-lab:/mnt/glusterfs# ls
index.html
```

### ��docker�й��������ֲ�ʽϵͳ
* ����docker���޷�ֱ�ӽ�volume���أ�����ѡ��volume�ȹ�����������,�ٹ���docker
```
docker run -it --net=host -v /mnt/glusterfs/:/home/ mydocker:v1 /bin/bash ./run.sh
```
* ���������صص��޸�index�ļ���ˢ����ҳ�����Է�����ҳ���޸ģ�˵���ɹ�����ֲ�ʽ�ļ�ϵͳ
![pic3](https://github.com/magicfisk/mesos_learning/raw/master/homework4/index.jpg)

## ����Docker�������������һ�ξ�������
* docker��aufs�����沿���Ѿ����������ϵ
### �鿴docker�Ĺ����ļ�λ��
* ����һ��docker��ʹ���ں�̨����,���鿴����
```
docker run -it --name tst ubuntu
exit
docker start tst
df -h
```
* ����2�У�����noneΪdocker����Ĺ��أ�shmΪdocker�������ļ�
```
none                           19G   13G  5.2G  71% /var/lib/docker/aufs/mnt/12c918da5e9fec89c325ad67d19932d108af18f3349ee047941fb4c8c76fb3b1

shm                            64M     0   64M   0% /var/lib/docker/containers/8e8d2a1b74b1945ddd9ad5983dd9ab58a0beb5844873d734ef07849dea23244a/shm
```

* ��/var/lib/docker/aufs/layers���Կ���layers��Ϣ
```
cat 12c918da5e9fec89c325ad67d19932d108af18f3349ee047941fb4c8c76fb3b1

12c918da5e9fec89c325ad67d19932d108af18f3349ee047941fb4c8c76fb3b1-init
ab222f2619b921e9fb847be0bbff321728ad9771c92b64c3c80a4fe544ecfecf
d1cbd4588f47064a894634352814687466491c80af12e84743de30977bf3b712
6dd88e0bdb25db5f73166f3448e66c13ae2c4ca4b1e6461defa11da9b5085ff6
d4a4666fac88e2ea29315327d19e471f536bb9bfd843888723fca3f2b3ea8359
70c35b47cf4fd87c4558d11b772aa60a97b0ac4bba862860f5820c006dfe314c
```
* ���Կ�������Ϊ12c918da5e9fec89c325ad67d19932d108af18f3349ee047941fb4c8c76fb3b1-init
* �����Ĳ����ݴ����/var/lib/docker/aufs/diffĿ¼
* ��ʵ��12c918da5e9fec89c325ad67d19932d108af18f3349ee047941fb4c8c76fb3b1���Ƕ�д�㣬��init����������ʼ����
```
cp ab222f2619b921e9fb847be0bbff321728ad9771c92b64c3c80a4fe544ecfecf /my_img/i2 -r
cp d1cbd4588f47064a894634352814687466491c80af12e84743de30977bf3b712 /my_img/i3 -r
cp 6dd88e0bdb25db5f73166f3448e66c13ae2c4ca4b1e6461defa11da9b5085ff6 /my_img/i4 -r
cp d4a4666fac88e2ea29315327d19e471f536bb9bfd843888723fca3f2b3ea8359 /my_img/i5 -r
cp 70c35b47cf4fd87c4558d11b772aa60a97b0ac4bba862860f5820c006dfe314c /my_img/i6 -r
```
* ������ȫ�����Ƴ���
* ��װvim�������������װ��
```
root@docker exec -it tst /bin/bash
docker@apt-get update
docker@apt install vim -y
docker@exit
root@cd /var/lib/docker/aufs/diff
root@cp 12c918da5e9fec89c325ad67d19932d108af18f3349ee047941fb4c8c76fb3b1 /my_img/i1 -r
```
* ��ȫ��������һ��Ŀ¼����
```
mkdir /mydocker_mnt
mount -t aufs -o br=/my_img/i1=ro:/my_img/i2=ro:/my_img/i3=ro:/my_img/i4=ro:/my_img/i5=ro:/my_img/i6=ro none /mydocker_mnt
```
* ����import�����tar���л�ȡ����,���뾵��
```
tar -c . | docker import - mydocker_new:v3
docker run -it mydocker_new:v3 /bin/bash
vi 1.txt
```
* �ɹ�����vim
![pic4](https://github.com/magicfisk/mesos_learning/raw/master/homework4/vi.jpg)

