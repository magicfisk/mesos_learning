#!/usr/bin/env python2.7
#coding=utf-8
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
            #更新状态，表明任务开始
            update = Dict()
            update.task_id.value = task.task_id.value
            update.state = 'TASK_RUNNING'
            update.timestamp = time.time()
            driver.sendStatusUpdate(update)
            #解析数据
            data=decode_data(task.data)
            data=data.split('\n')
            #初始化统计量
            left=0
            right=0
            ans=''
            #计算
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
            #返回计算结果
            ans=str(left)+' '+str(right)
            driver.sendFrameworkMessage(encode_data(ans))
            
            #更新状态，表明计算结束
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
