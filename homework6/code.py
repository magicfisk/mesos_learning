import subprocess, sys, os, socket, signal, json, time
import urllib.request, urllib.error
from sys import argv

def etcd(ip,list):
	args = ['etcd', '--name', 'p'+ip[-1], '--initial-advertise-peer-urls', 'http://'+ip+':2380','--listen-peer-urls', 'http://'+ip+ ':2380','--listen-client-urls', 'http://'+ip+':2379,http://127.0.0.1:2379','--advertise-client-urls', 'http://'+ip+':2379','--initial-cluster-token', 'etcd-cluster-hw5','--initial-cluster', list ,'--initial-cluster-state', 'new']
	subprocess.Popen(args)
	
def update_host(n):
	f=open("tmp-host","w")
	err=0
	for i in range(0,n):
		tag=os.system('etcdctl get /leader/192.0.1.10' + str(i))
		if tag==0:
			f.write("192.0.1.10" + str(i)+" host0\n")
			break
	cnt=1
	for i in range(0,n):
		tag=os.system('etcdctl get /follower/192.0.1.10' + str(i))
		if tag==0:
			f.write("192.0.1.10" + str(i)+" host"+str(cnt)+"\n")
			cnt=cnt+1
	f.close()
	os.system("cp tmp-host /etc/hosts")
	os.system("sudo cp tmp-host /mnt/hosts")

def main():

	script,ip,nodeN = argv
	os.system('ssh-keygen -f /home/admin/.ssh/id_rsa -t rsa -N ""')
	os.system('sudo -S bash -c "cat /home/admin/.ssh/id_rsa.pub >> /mnt/authorized_keys"')
	os.system("/etc/init.d/ssh start")
	n=int(nodeN)
	leader_flag=0
	list="p0=http://192.0.1.100:2380"
	for i in range(1,n):
		list=list+",p"+str(i)+"=http://192.0.1.10"+str(i)+":2380"
	
	print(list)
	etcd(ip,list)
	stats_url = 'http://127.0.0.1:2379/v2/stats/self'
	stats_request = urllib.request.Request(stats_url)
	while True:
		try:
			stats_reponse = urllib.request.urlopen(stats_request)
		except urllib.error.URLError as e:
			print('[WARN] ', e.reason)
			print('[WARN] Wating etcd...')

		else:
			stats_json = stats_reponse.read().decode('utf-8')
			data = json.loads(stats_json)

			if data['state'] == 'StateLeader':
				if leader_flag == 0:
					leader_flag = 1

					args = ['jupyter', 'notebook', '--NotebookApp.token=', '--ip=0.0.0.0', '--port=8888']
					subprocess.Popen(args)
					
				os.system('etcdctl set /leader/' + ip + ' ' + "1 --ttl 5")

			elif data['state'] == 'StateFollower':
				leader_flag = 0
				os.system('etcdctl set /follower/' + ip + ' ' + "1 --ttl 5")
		update_host(n)
		time.sleep(1)


if __name__ == '__main__':
	main()
