#!/usr/bin/env python2.7
#coding=utf-8
from __future__ import print_function

import sys
import uuid
import time
import socket
import signal
import getpass
from threading import Thread
from os.path import abspath, join, dirname

from pymesos import MesosSchedulerDriver, Scheduler, encode_data ,decode_data
from addict import Dict

TASK_CPU = 0.1
TASK_MEM = 32
EXECUTOR_CPUS = 0.1
EXECUTOR_MEM = 32
TASK_MaxNum=1000

class MinimalScheduler(Scheduler):
    def __init__(self):
        self.Task_launched=0

        

#mesos提供资源时的处理函数            
    def resourceOffers(self, driver, offers):    

                
        filters = {'refuse_seconds': 5}
        #分发任务
        for offer in offers:
			cpus = self.getResource(offer.resources, 'cpus')
			mem = self.getResource(offer.resources, 'mem')
			if self.Task_launched>7:
                continue
			if cpus < TASK_CPU or mem < TASK_MEM:
                continue
			
			ip = Dict()
			ip.key = 'ip'
			ip.value = '192.0.1.10' + str(self.Task_launched)

			volume = Dict()
			volume.key = 'volume'
			volume.value = '/mnt/:/mnt/'
			
			NetworkInfo = Dict()
			NetworkInfo.name = 'calico_docker_net'

			DockerInfo = Dict()
			DockerInfo.image = 'hw6:final'
			DockerInfo.network = 'USER'
			DockerInfo.parameters = [ip,volume]

			ContainerInfo = Dict()
			ContainerInfo.type = 'DOCKER'
			ContainerInfo.docker = DockerInfo
			ContainerInfo.network_infos = [NetworkInfo]
			
			CommandInfo = Dict()
			CommandInfo.shell = False
			CommandInfo.value = 'python3'
			CommandInfo.arguments = [ip,'8']		

			task = Dict()
			task_id = 'con' + str(self.Task_launched)
			task.task_id.value = task_id
			task.agent_id.value = offer.agent_id.value
			task.name = 'con'
				
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
       
    def getResource(self, res, name):
        for r in res:
            if r.name == name:
                return r.scalar.value
        return 0.0

        
def main(master):
    #设置executor、scheduler的参数
    
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

    def signal_handler(signal, frame):
        driver.stop()

    def run_driver_thread():
        driver.run()

    driver_thread = Thread(target=run_driver_thread, args=())
    driver_thread.start()

    print('Scheduler running, Ctrl+C to quit.')
    signal.signal(signal.SIGINT, signal_handler)

    while driver_thread.is_alive():
        time.sleep(1)


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) != 2:
        print("Usage: {} <mesos_master>".format(sys.argv[0]))
        sys.exit(1)
    else:
        main(sys.argv[1])
