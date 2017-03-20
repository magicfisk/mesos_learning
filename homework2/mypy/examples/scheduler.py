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
#初始化变量，Task_launched已经分发的任务，Task_finished为已经结束的任务，file_end表示文件读完，f1为文件，right和left为统计变量
    def __init__(self, executor):
        self.executor = executor
        self.Task_launched=0
        self.Task_finished=0
        self.file_end=False
        self.right=0
        self.left=0
        self.f1=open('data.txt','r')
        

#mesos提供资源时的处理函数            
    def resourceOffers(self, driver, offers):
    #读入数据
        def get_data(self):
            tmp1='';
            for x in range(1,TASK_MaxNum):
                tmp=self.f1.readline();
                if tmp=='':
                    self.file_end=True
                    break
                tmp1=tmp1+tmp
            return tmp1       
    

                
        filters = {'refuse_seconds': 5}
        #分发任务
        for offer in offers:
            cpus = self.getResource(offer.resources, 'cpus')
            mem = self.getResource(offer.resources, 'mem')
            if cpus < TASK_CPU or mem < TASK_MEM or self.file_end:
                continue
            self.Task_launched=self.Task_launched+1

            task = Dict()
            task_id = str(uuid.uuid4())
            task.task_id.value = task_id
            task.agent_id.value = offer.agent_id.value
            task.name = 'task {}'.format(task_id)
            task.executor = self.executor
            #读入数据，并且存入task
            task.data = encode_data(get_data(self))  

            task.resources = [
                dict(name='cpus', type='SCALAR', scalar={'value': TASK_CPU}),
                dict(name='mem', type='SCALAR', scalar={'value': TASK_MEM}),
            ]

            driver.launchTasks(offer.id, [task], filters) #调度任务

    #状态更新回调
    def statusUpdate(self, driver, update):       
        print ('%d Task has finished,%d task has launched' %(self.Task_finished,self.Task_launched))
        #如果所有任务结束，并且文件读完则停止framework
        if self.file_end:
            if self.Task_finished==self.Task_launched:
                print ('\nthere is %d balls in the left,and %d balls in the right\n' % (self.left,self.right))
                driver.stop()
    
    #获许资源数量
    def getResource(self, res, name):
        for r in res:
            if r.name == name:
                return r.scalar.value
        return 0.0

    #统计
    def frameworkMessage(self, driver, executorId, slaveId, message):
        ans=decode_data(message)
        print ('get an ans %s' %ans)
        ans=ans.split(' ')
        self.left=self.left+int(ans[0])
        self.right=self.right+int(ans[1])
        self.Task_finished=self.Task_finished+1
        
def main(master):
    #设置executor、scheduler的参数
    executor = Dict()
    executor.executor_id.value = 'MinimalExecutor'
    executor.name = executor.executor_id.value
    executor.command.value = '%s %s' % (
        sys.executable,
        abspath(join(dirname(__file__), 'executor.py'))
    )
    executor.resources = [
        dict(name='mem', type='SCALAR', scalar={'value': EXECUTOR_MEM}),
        dict(name='cpus', type='SCALAR', scalar={'value': EXECUTOR_CPUS}),
    ]
    
    framework = Dict()
    framework.user = getpass.getuser()
    framework.name = "MinimalFramework"
    framework.hostname = socket.gethostname()

    driver = MesosSchedulerDriver(
        MinimalScheduler(executor),
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
