import subprocess,time


ip=""
while True:
        f=open("/mnt/hosts")
        nip=f.readline()
        f.close()
        nip=nip.split(" ")
        nip=nip[0];
        print("check ip:"+ip+" nip:"+nip+"\n")
        if not ip==nip:
                print("updata\n")
                if ip!="":
                        http.kill()

                args = ['configurable-http-proxy', \
                '--default-target=http://'+nip+':8888', \
                '--ip=192.0.1.110', '--port=8888']
                http = subprocess.Popen(args)
                ip=nip
        time.sleep(5)