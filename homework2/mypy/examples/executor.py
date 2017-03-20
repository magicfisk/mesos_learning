#!/usr/bin/env python2.7
from __future__ import print_function

import sys
import time
import math
from threading import Thread

from pymesos import MesosExecutorDriver, Executor, decode_data ,encode_data
from addict import Dict


class MinimalExecutor(Executor):
    def launchTask(self, driver, task):
        def run_task(task):
            update = Dict()
            update.task_id.value = task.task_id.value
            update.state = 'TASK_RUNNING'
            update.timestamp = time.time()
            driver.sendStatusUpdate(update)
            data=decode_data(task.data)
            data=data.split('\n')
            
            left=0
            right=0
            ans=''
            for x in data:
                if x=='':
                    break
                tmp=x.split(' ')
                a=float(tmp[0])
                b=float(tmp[1])
                c=float(tmp[2])
                deta=math.sqrt(b*b-4*a*c)
                pt=(-deta-b)*0.5/a
                if pt>0:
                    right=right+1
                else:
                    left=left+1
            
            ans=str(left)+' '+str(right)
            driver.sendFrameworkMessage(encode_data(ans))

            update = Dict()
            update.task_id.value = task.task_id.value
            update.state = 'TASK_FINISHED'
            update.timestamp = time.time()
            driver.sendStatusUpdate(update)

        thread = Thread(target=run_task, args=(task,))
        thread.start()


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    driver = MesosExecutorDriver(MinimalExecutor(), use_addict=True)
    driver.run()
