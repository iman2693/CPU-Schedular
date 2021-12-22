from queue import Queue
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
#style.use('classic')
class Process:  # Class for the process
    def __init__(self, pid, arrival_time,
                 burst_time):  # pid: Process id, arrival_time: Arrival time, burst_time: Burst time
        self.pid = pid
        self.arrival = arrival_time
        self.burst = burst_time
        self.end=False
    def endprocess(self):
        self.end=True
    def printP(self):
        print(self.pid ,' ' , self.arrival , ' ' , self.burst)

def DrawGantt(Listt,pplist,Algo):

    Max_x=Listt[len(Listt)-1][2]
    fig, gnt = plt.subplots()
    gnt.set_xlabel(Algo)
    gnt.set_ylim(0, (len(pplist)+1)*15)
    gnt.set_xlim(0,Max_x)
    ytick=[]
    for i in range(len(pplist)):
        ytick.append(15*(i+1))
    gnt.set_yticks(ytick)
    label=['P'+str(v) for v in range(1,len(plist)+1)]
    gnt.set_yticklabels(label)
    sortedlist=[]
    for j in range(len(pplist)):
        templist=[]
        for i in range(len(Listt)):
            if Listt[i][0]=='P{0}'.format(j+1):
                templist.append((Listt[i][1],Listt[i][2]-Listt[i][1]))
        sortedlist.append(templist)
    for i in range(len(plist)-1,-1,-1):
        gnt.broken_barh(sortedlist[i], (((i+1)*15)-5, 9), facecolors='tab:blue')
    plt.savefig("gantt-{0}.png".format(Algo))
def AverageWaitTime(pplist,List):
    sum=0
    List.sort(key=lambda x:x[2],reverse=True)
    EndList=[]
    for i in range(len(pplist)):
        for j in range(len(List)):
            if 'P'+str(pplist[i].pid)==List[j][0]:
                EndList.append((List[j][0],List[j][2]))
                break
    EndList.sort(key=lambda x:x[0],reverse=False)
    pplist.sort(key=lambda x: x.pid, reverse=False)

    for i in range(len(pplist)):
        sum+=EndList[i][1]-pplist[i].arrival-pplist[i].burst
    print(sum/len(pplist))
def TurnAroundTime(pplist,List):
    sum = 0
    List.sort(key=lambda x: x[2], reverse=True)
    EndList = []
    for i in range(len(pplist)):
        for j in range(len(List)):
            if 'P' + str(pplist[i].pid) == List[j][0]:
                EndList.append((List[j][0], List[j][2]))
                break
    EndList.sort(key=lambda x: x[0], reverse=False)
    pplist.sort(key=lambda x: x.pid, reverse=False)
    for i in range(len(pplist)):
        sum+=EndList[i][1]-pplist[i].arrival
    print(sum/len(pplist))
def OutAlgorithm(List,pplist,x):
    List.sort(key=lambda x: x[2], reverse=True)
    End=List[0][2]
    print((len(pplist)*x)/End)
def UsingCpu(List,pplist,cs):
    List.sort(key=lambda x: x[2], reverse=True)
    End = List[0][2]
    print(((End-((len(List)-1)*cs))/End)*100,'%')
def AverageResponse(List,pplist):
    sum = 0
    List.sort(key=lambda x: x[2], reverse=False)
    Response = []
    for i in range(len(pplist)):
        for j in range(len(List)):
            if 'P' + str(pplist[i].pid) == List[j][0]:
                Response.append((List[j][0], List[j][2]))
                break
    pplist.sort(key=lambda x:x.pid,reverse=False)
    for i in range(len(pplist)):
        sum+=Response[i][1]-pplist[i].arrival
    print(sum/len(pplist))

def LCFS(plist,cs):
    pplist=plist
    plist.sort(key=lambda x:x.burst,reverse=False)
    time = 0
    chart = []
    Stack=[]
    while True:
        for i in range(len(plist)):
            if plist[i].arrival<=time and plist[i].end==False and (plist[i] not in Stack):
                #queue.put_nowait(plist[i])
                Stack.append(plist[i])

        flag = True
        for i in range(len(plist)):
            if plist[i].end==False:
                flag=False
                break
        if flag==True:
            break
        if len(Stack)>0:
            test=Stack.pop()
            chart.append(['P{0}'.format(test.pid),time,time+test.burst])
            time+=test.burst
            test.endprocess()
            time+=cs
        else:
            time+=1
    print('LCFS: ',chart)
    DrawGantt(chart, plist, 'LCFS')
    print('ET (LCFS) = ', end=' ')
    AverageWaitTime(pplist=pplist,List=chart)
    print('Turn Around Time (LCFS) = ', end=' ')
    TurnAroundTime(pplist,chart)
    print('Out Of Algorithm 10ms (LCFS) = ', end=' ')
    OutAlgorithm(chart,pplist,x=10)
    print('Using Cpu (LCFS) = ', end=' ')
    UsingCpu(chart,pplist,cs)
    print('Average Response (LCFS) = ', end=' ')
    AverageResponse(chart,pplist)
    print('\n\n')

def FCFS(plist,cs):
    pplist=plist
    time=0
    chart=[]
    queue=Queue()
    while True:
        for i in range(len(plist)):
            if plist[i].arrival<=time and plist[i].end==False:
                queue.put_nowait(plist[i])

        flag = True
        for i in range(len(plist)):
            if plist[i].end==False:
                flag=False
                break
        if flag==True:
            break
        if not queue.empty():
            while not queue.empty():
                test=queue.get_nowait()
                chart.append(['P{0}'.format(test.pid),time,time+test.burst])
                time+=test.burst
                test.endprocess()
                time+=cs
        else:
            time+=1
    print('FCFS: ' , chart)
    DrawGantt(chart, plist,'FCFS')
    print('ET (FCFS) = ',end=' ')
    AverageWaitTime(pplist=pplist, List=chart)
    print('Turn Around Time (FCFS) = ', end=' ')
    TurnAroundTime(pplist, chart)
    print('Out Of Algorithm 10ms (FCFS) = ', end=' ')
    OutAlgorithm(chart, pplist, x=10)
    print('Using Cpu (FCFS) = ', end=' ')
    UsingCpu(chart, pplist, cs)
    print('Average Response (FCFS) = ', end=' ')
    AverageResponse(chart, pplist)
    print('\n\n')
def SJF(plist,cs):
    pplist=plist
    plist.sort(key=lambda x:x.burst,reverse=False)
    time=0
    chart=[]
    queue=Queue()
    while True:
        for i in range(len(plist)):
            if plist[i].arrival<=time and plist[i].end==False:
                queue.put_nowait(plist[i])

        flag = True
        for i in range(len(plist)):
            if plist[i].end==False:
                flag=False
                break
        if flag==True:
            break
        if not queue.empty():
            while not queue.empty():
                queue=Queue()
                for i in range(len(plist)):
                    if plist[i].arrival<=time and plist[i].end==False:
                        queue.put_nowait(plist[i])

                test=queue.get_nowait()
                chart.append(['P{0}'.format(test.pid),time,time+test.burst])
                time+=test.burst
                test.endprocess()
                time+=cs
        else:
            time+=1
    print('SJF: ',chart)
    DrawGantt(chart, plist,'SJF')
    print('ET (SJF) = ', end=' ')
    AverageWaitTime(pplist=pplist, List=chart)
    print('Turn Around Time (SJF) = ', end=' ')
    TurnAroundTime(pplist, chart)
    print('Out Of Algorithm 10ms (SJF) = ', end=' ')
    OutAlgorithm(chart, pplist, x=10)
    print('Using Cpu (SJF) = ', end=' ')
    UsingCpu(chart, pplist, cs)
    print('Average Response (SJF) = ', end=' ')
    AverageResponse(chart, pplist)
    print('\n\n')
def SRT(plist,cs):
    pplist=plist
    time = 0
    chart = []
    while True:
        Processs = []
        UnProcess = []
        for i in range(len(plist)):
            if plist[i].arrival<=time and plist[i].burst>0 and (plist[i] not in Processs):
                Processs.append(plist[i])
            if plist[i].arrival>time and plist[i].burst>0 and (plist[i] not in UnProcess):
                UnProcess.append(plist[i])

        Processs.sort(key=lambda x:x.burst,reverse=False)
        UnProcess.sort(key=lambda x:x.arrival,reverse=False)
        if len(Processs)>0 and len(UnProcess)>0:
            if Processs[0].burst+Processs[0].arrival -UnProcess[0].arrival >0:
                chart.append(['P{0}'.format(Processs[0].pid), time, time + (UnProcess[0].arrival - Processs[0].arrival)])
                time+=(UnProcess[0].arrival-Processs[0].arrival)
                Processs[0].burst-=(UnProcess[0].arrival-Processs[0].arrival)
                time+=cs
            else:
                chart.append(['P{0}'.format(Processs[0].pid), time, time + Processs[0].burst])
                time += Processs[0].burst
                Processs[0].burst=0
                time+=cs
        elif len(Processs)>0 and len(UnProcess)==0:
            Processs.sort(key=lambda x: x.burst, reverse=False)
            chart.append(['P{0}'.format(Processs[0].pid), time, time + Processs[0].burst])
            time+=Processs[0].burst
            Processs[0].burst=0
            time+=cs
        if len(UnProcess)==0 and len(Processs)==0:
            break
    print('SRT : ',chart)
    DrawGantt(chart,plist,Algo='SRTF')
    print('ET (SRT) = ', end=' ')
    AverageWaitTime(pplist=pplist, List=chart)
    print('Turn Around Time (SRT) = ', end=' ')
    TurnAroundTime(pplist, chart)
    print('Out Of Algorithm 10ms (SRT) = ', end=' ')
    OutAlgorithm(chart, pplist, x=10)
    print('Using Cpu (SRT) = ', end=' ')
    UsingCpu(chart, pplist, cs)
    print('Average Response (SRT) = ', end=' ')
    AverageResponse(chart, pplist)

    print('\n\n')
def shiftCL(alist):  # alist is queue list 1,2,3=> 2,3,1 => 3,1,2
    temp = alist[0]  # first process in the list
    for i in range(len(alist) - 1):  # -1
        alist[i] = alist[i + 1]  # any shft will add +1
    alist[len(alist) - 1] = temp  # -1 is the last place in the list ex. 0-4 =>5 elements -1 = 4
    return alist
def RR(tq, plist,cs):  # Round Robin(RR) (plist: process list, tq: Quantum time)
    pplist=plist
    global gchart
    gchart=[]
    qqueue = []
    n=len(plist)
    time = 0  # we start arrival_time time 0
    ap = 0  # arrived processes
    done = 0  # done processes, to count the number of processes finished
    q = tq  # time quantum
    start = 1
    t=0
    while (done < n):  # still more processes
        t+=1
        for i in range(n):  # process next in line
            if time >= plist[i].arrival and (plist[i] not in qqueue) :  # to check for a new arrivil process with out checking P1
                qqueue.append(plist[i])
                ap += 1
        rp=0
        for i in range(len(qqueue)):
            if qqueue[i].burst>0:
                rp+=1

        if rp < 1 :  # in case
            # of there is no arrival
            time += 1
            continue
        if t!=1:
            qqueue = shiftCL(qqueue)
        if start:
            if qqueue[0].burst > 0:
                if qqueue[0].burst > q:
                    gchart.append(['P{0}'.format(qqueue[0].pid), time, time + q])
                    time += q
                    qqueue[0].burst -= q
                else:
                    gchart.append(['P{0}'.format(qqueue[0].pid), time, time + qqueue[0].burst])
                    time += qqueue[0].burst
                    qqueue[0].end=True
                    qqueue[0].burst=0
                    done += 1
                    rp -= 1
                time+=cs
    print('RR :' ,gchart)
    DrawGantt(gchart, plist,'RR')
    print('ET (RR) = ', end=' ')
    AverageWaitTime(pplist=pplist, List=gchart)
    print('Turn Around Time (RR) = ', end=' ')
    TurnAroundTime(pplist, gchart)
    print('Out Of Algorithm 10ms (RR) = ', end=' ')
    OutAlgorithm(gchart, pplist, x=10)
    print('Using Cpu (RR) = ', end=' ')
    UsingCpu(gchart, pplist, cs)
    print('Average Response (RR) = ', end=' ')
    AverageResponse(gchart, pplist)

    print('\n\n')
#Test For FCFS
# plist.append(Process(1, 0, 5))
# plist.append(Process(2, 1, 3))
# plist.append(Process(3, 3, 6))
# plist.append(Process(4, 5, 1))
# plist.append(Process(5, 6, 4))

# plist.append(Process(1,15,1))
# plist.append(Process(2,7,1))
# plist.append(Process(3,0,2))
# plist.append(Process(4,1,3))

# plist.append(Process(1,0,9))
# plist.append(Process(2,0,2))
# plist.append(Process(3,0,2))
plist = []
plist.append(Process(1,5,3))
plist.append(Process(2,1,1))
plist.append(Process(3,0,2))
plist.append(Process(4,1.5,1))
plist.append(Process(5,2,2))

# plist.append(Process(1,3,10))
# plist.append(Process(2,1,1))
# plist.append(Process(3,5,2))
# plist.append(Process(4,4,1))
# plist.append(Process(5,2,5))

plist.sort(key=lambda x:x.arrival , reverse=False)
FCFS(plist,cs=0.5)

#Test For RR
plist = []
# plist.append(Process(1,5,3))
# plist.append(Process(2,1,1))
# plist.append(Process(3,0,2))
# plist.append(Process(4,1.5,1))
# plist.append(Process(5,2,2))

plist.append(Process(1,0,10))
plist.append(Process(2,2,19))
plist.append(Process(3,33,3))
plist.append(Process(4,34,7))
plist.append(Process(5,35,12))

# plist.append(Process(1,0,5))
# plist.append(Process(2,1,6))
# plist.append(Process(3,2,3))
# plist.append(Process(4,3,1))
# plist.append(Process(5,4,5))
# plist.append(Process(6,6,4))
plist.sort(key=lambda x:x.arrival , reverse=False)
RR(10,plist,cs=1.0)


# Test For LCFS
plist = []
plist.append(Process(1,5,3))
plist.append(Process(2,1,1))
plist.append(Process(3,0,2))
plist.append(Process(4,1.5,1))
plist.append(Process(5,2,2))
# plist.append(Process(1,0,1.5))
# plist.append(Process(2,1,1.5))
# plist.append(Process(3 ,2,1.5))
# plist.append(Process(4,3,1.5))
# plist.append(Process(5,4,1.5))
plist.sort(key=lambda x:x.arrival , reverse=False)
LCFS(plist,cs=0.5)


# Test For SJF
plist = []
# plist.append(Process(1,5,3))
# plist.append(Process(2,1,1))
# plist.append(Process(3,0,2))
# plist.append(Process(4,1.5,1))
# plist.append(Process(5,2,2))

plist.append(Process(1,0,9))
plist.append(Process(2,2,4))
plist.append(Process(3,0,8))
plist.append(Process(4,3,2))
plist.append(Process(5,5,1))
plist.sort(key=lambda x:x.arrival , reverse=False)
SJF(plist,cs=1)

#Test For SRT
plist=[]
plist.append(Process(1,0,9))
plist.append(Process(2,2,4))
plist.append(Process(3,0,8))
plist.append(Process(4,3,2))
plist.append(Process(5,5,1))
plist.sort(key=lambda x:x.arrival , reverse=False)
SRT(plist,cs=0)
