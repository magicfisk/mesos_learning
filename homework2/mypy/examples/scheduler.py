#!/usr/bin/env python2.7
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

    def __init__(self, executor):
        self.executor = executor
        self.Task_launched=0
        self.Task_finished=0
        self.file_end=False
        self.right=0
        self.left=0
        self.f1=open('data.txt','r')
        

            
    def resourceOffers(self, driver, offers):
    
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
            task.data = encode_data(get_data(self))

            task.resources = [
                dict(name='cpus', type='SCALAR', scalar={'value': TASK_CPU}),
                dict(name='mem', type='SCALAR', scalar={'value': TASK_MEM}),
            ]

            driver.launchTasks(offer.id, [task], filters)

    def getResource(self, res, name):
        for r in res:
            if r.name == name:
                return r.scalar.value
        return 0.0

    def statusUpdate(self, driver, update):
        logging.debug('Status update TID %s %s',
                      update.task_id.value,
                      update.state)            
        print ('%d %d' %(self.Task_finished,self.Task_launched))
        if self.file_end:
            if self.Task_finished==self.Task_launched:
                print ('\nthere is %d balls in the left,and %d balls in the right\n' % (self.left,self.right))
                driver.stop() 

          
    def frameworkMessage(self, driver, executorId, slaveId, message):
        ans=decode_data(message)
        print ('get an ans %s\n' %ans)
        ans=ans.split(' ')
        self.left=self.left+int(ans[0])
        self.right=self.right+int(ans[1])
        self.Task_finished=self.Task_finished+1
        
        
def main(master):
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
