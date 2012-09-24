# coding:utf-8
#!/usr/bin/python
# 考试参数设定
# 科目A,(考试时间15-25min) 4个 科目B(10-20min) 3个,科目C(5-15min) 2个
# 输入模拟参数：
# 科目A 最小时间 最大时间 考场数
# 科目B 最小时间 最大时间 考场数
# 科目C 最小时间 最大时间 考场数
# 考试人数 ，进场时间最大间隔
# 科目A 考试概率 
# 科目B 考试概率
# 科目C 考试概率
# 考试方案 1,2,3
# 生成考场
# 生成考生及考试科目
# 演示时间扩大倍数

from Queue import Queue
import random
import threading
import time
import types

mconfig = raw_input('是否采用默认参数,是输入y:')
if mconfig == 'y':
    # 考试人数 ，进场时间最大间隔
    Snum = 20
    Jtime = 3
    # 科目A 考试概率 
    # 科目B 考试概率
    # 科目C 考试概率
    Apro = 100
    Bpro= 90
    Cpro = 80
    # 考场考试时间
    Amin = 15
    Amax = 25
    Bmin = 10
    Bmax = 20
    Cmin = 5
    Cmax = 15
    # 考场个数
    Anum = 4
    Bnum = 3
    Cnum = 2
    # 提前进场时间
    ttime = 20
else:
    # 考试人数 ，进场时间最大间隔
    Snum = raw_input('请输入考试人数,>1,默认20: ')
    if not Snum.isdigit() or int(Snum) < 1:
        Snum = 20
    else:
        Snum = int(Snum)
    
    Jtime =raw_input('请输入入场间隔时间,>1,默认3: ')
    if not Jtime.isdigit() or int(Jtime) < 1:
        Jtime = 3
    else:
        Jtime = int(Jtime)

    # 科目A 考试概率 
    Apro = raw_input('请输入A科目考试概率,1-100,默认100: ')
    if not Apro.isdigit() or int(Apro) < 1 or int(Apro) >100:
        Apro = 100
    else:
        Apro = int(Apro)
    
    # 科目B 考试概率
    Bpro= raw_input('请输入B科目考试概率,1-100,默认90: ')
    if not Bpro.isdigit() or int(Bpro) < 1 or int(Bpro) >100:
        Bpro = 90
    else:
        Bpro = int(Bpro)
    
    # 科目C 考试概率
    Cpro = raw_input('请输入C科目考试概率,1-100,默认80: ')
    if not Cpro.isdigit() or int(Cpro) < 1 or int(Cpro) >100:
        Cpro = 80
    else:
        Cpro = int(Cpro)

    # 考场考试时间
    Amin = raw_input('请输入A科目考试最小时间, >1, 默认15: ')
    if not Amin.isdigit() or int(Amin) < 1:
        Amin = 15
    else:
        Amin = int(Amin)
    Amax = raw_input('请输入A科目考试最小时间, >1, >最小时间，默认最小时间+10: ')
    if not Amax.isdigit() or int(Amax) < 1 or int(Amax) <= Amin:
        Amax = Amin + 10 
    else:
        Amax = int(Amax)
    
    Bmin = raw_input('请输入B科目考试最小时间, >1, 默认10: ')
    if not Bmin.isdigit() or int(Bmin) < 1:
        Bmin = 10
    else:
        Bmin = int(Bmin)
    Bmax = raw_input('请输入B科目考试最小时间, >1, >最小时间, 默认最小时间+10: ')
    if not Bmax.isdigit() or int(Bmax) < 1 or int(Bmax) <= Bmin:
        Bmax = Bmin + 10 
    else:
        Bmax = int(Bmax)
        
    Cmin = raw_input('请输入C科目考试最小时间, >1, 默认5: ')
    if not Cmin.isdigit() or int(Cmin) < 1:
        Cmin = 5
    else:
        Cmin = int(Cmin)
    Cmax = raw_input('请输入C科目考试最小时间, >1, >最小时间, 默认最小时间+10: ')
    if not Cmax.isdigit() or int(Cmax) < 1 or int(Cmax) <= Cmin:
        Cmax = Cmin + 10 
    else:
        Cmax = int(Cmax)
        
    # 考场个数
    Anum = raw_input('请输入A科目考场个数，默认4: ')
    if not Anum.isdigit() or int(Anum) < 1:
        Anum = 4
    else:
        Anum = int(Anum)
        
    Bnum = raw_input('请输入B科目考场个数，默认3: ')
    if not Bnum.isdigit() or int(Bnum) < 1:
        Bnum = 3
    else:
        Bnum = int(Bnum)
        
    Cnum = raw_input('请输入C科目考场个数，默认2: ')
    if not Cnum.isdigit() or int(Cnum) < 1:
        Cnum = 2
    else:
        Cnum = int(Cnum)
        
    # 提前进场时间
    ttime = raw_input('请输入提前入场时间,这个值与间隔时间的比值太小会导致部分考场提前关闭,默认20: ')
    if not ttime.isdigit() or int(ttime) < 20:
        ttime = 20
    else:
        ttime = int(ttime) 

# 考场规则模式
emodle =  raw_input('请输入考场规则模式a或b或c,默认a: ')
if emodle!= 'a' or emodle != 'b' or emodle != 'c':
    emodle = 'a' 
    
# 考试开始时间
estime = 0
# 学生及科目考试名单
Slist = []
Alist = []
Blist = []
Clist = []
# list锁
listlock = threading.RLock()

class Yujiao(threading.Thread):
    def __init__(self,Y_name,type):
        threading.Thread.__init__(self,name = Y_name)
        self.type = type
        self.status = True
    
    def run(self):
        self.yujiao()
    
    def yujiao(self):
        names = globals()
        names['%sklist' % self.getName()]
        names['%sylist' % self.getName()]
        global Slist
        global Alist
        global Blist
        global Clist
        global estime
        global emodle
        names['%smin' % self.type]
        names['%smax' % self.type]
        if len(names['%sylist' % self.getName()])==0:
            listlock.acquire()
            if len(names['%slist' % self.type])==0:
                #print '没有学生需要考试'+self.type+','+self.getName()+'预叫关闭'
                #print '距离开始开始时间'+str(int(time.time()-estime))+'分钟'
                listlock.release()  
                #self.stop()
            else:
                # 判断侯考室里是否有人没有参加过此考试
                if emodle == 'b':
                    canexam = list(set(names['%slist' % self.type])&set(Slist))
                else:
                    canexam = list(set(Slist)&set(names['%slist' % self.type]))
                if len(canexam)==0:
                    listlock.release() 
                    #print '考场'+self.getName()+'预叫: '+'等待其他考场结束' 
                    time.sleep(1)
                    self.yujiao()
                else:
                    names['%sylist' % self.getName()].append(canexam[0])
                    #print '考场'+self.getName()+'预叫: '+ canexam[0]
                    Slist.remove(canexam[0])
                    listlock.release() 
                    self.yujiao()
        else:
            time.sleep(1)
            self.yujiao()
    
    def stop(self):
        self.status = False
        

class Kaochang(threading.Thread):
    def __init__(self,K_name,type):
        threading.Thread.__init__(self,name = K_name)
        self.type = type
        self.status = True
        
    def run(self):
        self.kaoshi()       
                                                    
    def kaoshi(self): 
        names = globals()
        names['%sklist' % self.getName()]
        names['%sylist' % self.getName()]
        global Slist
        global Alist
        global Blist
        global Clist
        global estime
        global emodel
        names['%smin' % self.type]
        names['%smax' % self.type]
        names['%swait' % self.getName()] 
        min = names['%smin' % self.type]
        max = names['%smax' % self.type]  
        listlock.acquire()
        # 判断预叫位是否有人
        if len(names['%sylist' % self.getName()])==0:
            # 判断是否还有人需要考试
            if len(names['%slist' % self.type])==0:
                print self.getName()+'考场关闭, 距离开始开始时间'+str(int(time.time()-estime))+'分钟'
                print self.getName()+'考官等待时间共'+str(names['%swait' % self.getName()] )+'分钟'
                listlock.release()  
                #self.stop()                
            else:
                listlock.release() 
                #print '考场'+self.getName()+'等待叫号'
                names['%swait' % self.getName()]  = names['%swait' % self.getName()] +1
                time.sleep(1)
                self.kaoshi()
        else:
            # 进入考场
            names['%sklist' % self.getName()] = names['%sylist' % self.getName()]
            names['%sylist' % self.getName()] = []
            # 从科目list中删除
            names['%slist' % self.type].remove(names['%sklist' % self.getName()][0])
            print '考场'+self.getName()+": "+ names['%sklist' % self.getName()][0] 
            #print '本科目剩余考生:'
            #print names['%slist' % self.type]
            listlock.release()  
              
            #考试时间
            time.sleep(random.randrange(min,max))
            #print names['%sklist' % self.getName()][0]+'完成考试'+self.type
            listlock.acquire() 
            # 判断是否考完三个科目
            if names['%sklist' % self.getName()][0] not in Alist and names['%sklist' % self.getName()][0] not in Blist and names['%sklist' % self.getName()][0] not in Clist:
                print names['%sklist' % self.getName()][0]+'完成所有考试离开考场' 
                print '距离开始开始时间'+str(int(time.time()-estime))+'分钟'
            else:
                # c方案插队
                if emodle == 'c':
                    tolist = [names['%sklist' % self.getName()][0]]
                    tolist.extend(Slist)
                    Slist = tolist
                else:
                    Slist.append(names['%sklist' % self.getName()][0])                      
            listlock.release()
            self.kaoshi() 
    
    def stop(self):
        self.status = False
        
        
class Dengjichu(threading.Thread):
    def __init__(self,D_name):
        threading.Thread.__init__(self,name = D_name)
    
    def run(self):
        global Snum
        global Jtime
        global Slist
        global Alist
        global Blist
        global Clist
        global Apro
        global Bpro
        global Cpro
        global listlock
        for i in range(Snum):
            student = 'stu'+str(i+1)
            listlock.acquire() 
            Slist.append(student)
            random.randrange(100)
            if random.randrange(100)<Apro:
                Alist.append(student)
            if random.randrange(100)<Bpro:
                Blist.append(student)
            if random.randrange(100)<Cpro:
                Clist.append(student) 
            listlock.release()
            time.sleep(random.randrange(1,Jtime+1))
        print '考生进场结束,目前侯考室考生名单:'
        print Slist
        print '目前考生参加A科目考试名单(部分已参加完):'
        print Alist
        print '目前考生参加B科目考试名单(部分已参加完):'
        print Blist
        print '目前考生参加C科目考试名单(部分已参加完):'
        print Clist
        

# main thread
def main():
    global ttime
    global estime
    # 考生进程
    djc = Dengjichu('Djc')    
    djc.start();
    print '考生进场开始:'
    time.sleep(ttime)
    print '考试开始:'
    estime = time.time()
    names = globals()
    for a in range(1,Anum+1):
        names['A%sklist' % a] = []
        names['A%sylist' % a] = []
        names['A%swait' % a] = 0
        names['A%syj' % a] = Yujiao('A%s' % a,'A')
        names['A%syj' % a].start()
        names['A%skc' % a] = Kaochang('A%s' % a,'A')
        names['A%skc' % a].start()
    for b in range(1,Bnum+1):
        names['B%sklist' % b] = []
        names['B%sylist' % b] = []
        names['B%swait' % b] = 0
        names['B%syj' % b] = Yujiao('B%s' % b,'B')
        names['B%syj' % b].start()
        names['B%skc' % b] = Kaochang('B%s' % b,'B')
        names['B%skc' % b].start()
    for c in range(1,Cnum+1):
        names['C%sklist' % c] = []
        names['C%sylist' % c] = []
        names['C%swait' % c] = 0
        names['C%syj' % c] = Yujiao('C%s' % c,'C')
        names['C%syj' % c].start()
        names['C%skc' % c] = Kaochang('C%s' % c,'C')
        names['C%skc' % c].start()


if __name__ == '__main__':    
    main() 
    names = globals()
    