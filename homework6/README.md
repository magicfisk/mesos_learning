# 第6次作业
## paxos算法
### 概念：
* Proposer ：提议者
* Acceptor：决策者
* Client：产生议题者
* Learner：最终决策学习者
* 关键角色为提议者和决策者
### prepare阶段
1.proposer选择一个提案编号n并将prepare请求pre(n)发送给所有acceptors<br>
2.acceptor收到prepare消息后，如果提案的编号大于它已经回复的所有prepare消息，则acceptor将自己上次accept的提案回复给proposer（n',v'）（没有则发送ok），并承诺不再回复小于n的提案<br>
### accept阶段
对于propose：<br>
1.propose收到半数以上的回复，若所有人的回复都是ok，那么propose发送accept(n,v)给所有回复的人,v是client提供给自己的值<br>
2.若propose收到的回复中有不是ok的，选择（ni,vi）中ni最大对应的vi，发送accept（n,vi）给所有回复的人。<br>
3.propose收到的回复不到一半，则提议失败，增加自己的提案编号n，回到prepare中的1 <br>
对于accpetor：<br>
收到的accept(n,v)
1.其中n小于自己接受过的n，则丢弃<br>
2.n大于自己接受的n，接受，并且回复accept-ok<br>
对于propose：
1.收到半数的accept-ok，提议成功，通知learner更新<br>
2.没有收到半数的accpet-ok，提议失败，修改n，回到prepare的1阶段<br>
### 算法正确性
* 上述算法只有在accept的回复全部为ok的时候，才能采纳新的value。<br>
* 只有被半数以上acceptor接受的value才能被认可。<br>
* prepare阶段要求回复的人必须大于一半，所以若存在被认可的值，则一定会被返回（两个大于一半的集合一定有交集）<br>
* 任何大于编号大于被认可提案的提案提出值一定是认可的值<br>
* 只要被认可值产生后，这个值就会被确定，从而一致。<br>
### 算法的缺陷
* 存在活锁问题：
容易发现在认可的值确定之前，各种提案的编号不断上升，而导致产生超过半数的accept-ok。<br>
![pic2](https://github.com/magicfisk/mesos_learning/raw/master/homework6/lock.jpg)<br>
如上图：
* 1，2，3回复了1的pre(n1)
* 3，4，5回复了5的pre(n5)，3从接受1改为接受5
* 1，2回复了accept(n1,v1)，但3因为5的原因不回应，1失败，重新发起prepare
* 1，2，3回复了1的pre(n1')，3从接受5变为接受1
* 4，5回复了5的accept(n5，v5)，5失败，重新发起prepare
* 3改为接受5，1失败，3改，5失败……。所以永远也不可能达成一致。
* 解决方案：指定一个leader，来负责发送propose，控制执行顺序，保证propose不会互相干扰。leader下线，需要执行选举算法，选举一个新的leader
## 模拟Raft协议工作的一个场景并叙述处理过程
* 集群被分成2个子网，无法互相通信
![pic3](https://github.com/magicfisk/mesos_learning/raw/master/homework6/net1.jpg)<br>
* 其中B为原leader，C为子网中新竞选出来的leader
![pic4](https://github.com/magicfisk/mesos_learning/raw/master/homework6/net2.jpg)<br>
* client向B发送消息set3，B只能收到A的回应，没有大于一半，所以B无法更新值
![pic5](https://github.com/magicfisk/mesos_learning/raw/master/homework6/net3.jpg)<br>
* client向C发送消息set8，C能收到半数以上的回应，C向client发送更新成功的信号
![pic6](https://github.com/magicfisk/mesos_learning/raw/master/homework6/net4.jpg)<br>
* 网络恢复后，B,C同时发送心跳信号，这是A，B发现了一个更高级的leader，两者同时变为未提交状态，接受C的提交信息，之后A,B的状态则变成和C一致
## mesos的容错机制和验证
