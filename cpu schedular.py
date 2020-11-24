from PyQt5 import QtCore, QtGui, QtWidgets
from queue import Queue
import matplotlib.pyplot as plt
from matplotlib import style
import csv
style.use("ggplot")

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

class Ui_Form(object):
    def DrawGantt(self,Listt, pplist, Algo):

        Max_x = Listt[len(Listt) - 1][2]
        fig, gnt = plt.subplots()
        gnt.set_xlabel(Algo)
        gnt.set_ylim(0, (len(pplist) + 1) * 15)
        gnt.set_xlim(0, Max_x)
        ytick = []
        for i in range(len(pplist)):
            ytick.append(15 * (i + 1))
        gnt.set_yticks(ytick)
        label = ['P' + str(v) for v in range(1, len(pplist) + 1)]
        gnt.set_yticklabels(label)
        sortedlist = []
        for j in range(len(pplist)):
            templist = []
            for i in range(len(Listt)):
                if Listt[i][0] == 'P{0}'.format(j + 1):
                    templist.append((Listt[i][1], Listt[i][2] - Listt[i][1]))
            sortedlist.append(templist)
        for i in range(len(pplist) - 1, -1, -1):
            gnt.broken_barh(sortedlist[i], (((i + 1) * 15) - 5, 9), facecolors='tab:blue')
        plt.savefig("gantt-{0}.png".format(Algo))

    def AverageWaitTime(self,pplist, List):
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
            sum += EndList[i][1] - pplist[i].arrival - pplist[i].burst
        print(sum / len(pplist))

    def TurnAroundTime(self,pplist, List):
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
            sum += EndList[i][1] - pplist[i].arrival
        print(sum / len(pplist))

    def OutAlgorithm(self,List, pplist, x):
        List.sort(key=lambda x: x[2], reverse=True)
        End = List[0][2]
        print((len(pplist) * x) / End)

    def UsingCpu(self,List, pplist, cs):
        List.sort(key=lambda x: x[2], reverse=True)
        End = List[0][2]
        print(((End - ((len(List) - 1) * cs)) / End) * 100, '%')

    def AverageResponse(self,List, pplist):
        sum = 0
        List.sort(key=lambda x: x[2], reverse=False)
        Response = []
        for i in range(len(pplist)):
            for j in range(len(List)):
                if 'P' + str(pplist[i].pid) == List[j][0]:
                    Response.append((List[j][0], List[j][2]))
                    break
        pplist.sort(key=lambda x: x.pid, reverse=False)
        for i in range(len(pplist)):
            sum += Response[i][1] - pplist[i].arrival
        print(sum / len(pplist))

    def LCFS(self,plist, cs):
        pplist = plist
        plist.sort(key=lambda x: x.burst, reverse=False)
        time = 0
        chart = []
        Stack = []
        while True:
            for i in range(len(plist)):
                if plist[i].arrival <= time and plist[i].end == False and (plist[i] not in Stack):
                    # queue.put_nowait(plist[i])
                    Stack.append(plist[i])

            flag = True
            for i in range(len(plist)):
                if plist[i].end == False:
                    flag = False
                    break
            if flag == True:
                break
            if len(Stack) > 0:
                test = Stack.pop()
                chart.append(['P{0}'.format(test.pid), time, time + test.burst])
                time += test.burst
                test.endprocess()
                time += cs
            else:
                time += 1
        print('LCFS: ', chart)
        self.DrawGantt(chart, plist, 'LCFS')
        print('ET (LCFS) = ', end=' ')
        self.AverageWaitTime(pplist=pplist, List=chart)
        print('Turn Around Time (LCFS) = ', end=' ')
        self.TurnAroundTime(pplist, chart)
        print('Out Of Algorithm 10ms (LCFS) = ', end=' ')
        self.OutAlgorithm(chart, pplist, x=10)
        print('Using Cpu (LCFS) = ', end=' ')
        self.UsingCpu(chart, pplist, cs)
        print('Average Response (LCFS) = ', end=' ')
        self.AverageResponse(chart, pplist)
        print('\n\n')

    def FCFS(self,plist, cs):
        pplist = plist
        time = 0
        chart = []
        queue = Queue()
        while True:
            for i in range(len(plist)):
                if plist[i].arrival <= time and plist[i].end == False:
                    queue.put_nowait(plist[i])

            flag = True
            for i in range(len(plist)):
                if plist[i].end == False:
                    flag = False
                    break
            if flag == True:
                break
            if not queue.empty():
                while not queue.empty():
                    test = queue.get_nowait()
                    chart.append(['P{0}'.format(test.pid), time, time + test.burst])
                    time += test.burst
                    test.endprocess()
                    time += cs
            else:
                time += 1
        print('FCFS: ', chart)
        self.DrawGantt(chart, plist, 'FCFS')
        print('ET (FCFS) = ', end=' ')
        self.AverageWaitTime(pplist=pplist, List=chart)
        print('Turn Around Time (FCFS) = ', end=' ')
        self.TurnAroundTime(pplist, chart)
        print('Out Of Algorithm 10ms (FCFS) = ', end=' ')
        self.OutAlgorithm(chart, pplist, x=10)
        print('Using Cpu (FCFS) = ', end=' ')
        self.UsingCpu(chart, pplist, cs)
        print('Average Response (FCFS) = ', end=' ')
        self.AverageResponse(chart, pplist)
        print('\n\n')

    def SJF(self,plist, cs):
        pplist = plist
        plist.sort(key=lambda x: x.burst, reverse=False)
        time = 0
        chart = []
        queue = Queue()
        while True:
            for i in range(len(plist)):
                if plist[i].arrival <= time and plist[i].end == False:
                    queue.put_nowait(plist[i])

            flag = True
            for i in range(len(plist)):
                if plist[i].end == False:
                    flag = False
                    break
            if flag == True:
                break
            if not queue.empty():
                while not queue.empty():
                    test = queue.get_nowait()
                    chart.append(['P{0}'.format(test.pid), time, time + test.burst])
                    time += test.burst
                    test.endprocess()
                    time += cs
            else:
                time += 1
        print('SJF: ', chart)
        self.DrawGantt(chart, plist, 'SJF')
        print('ET (SJF) = ', end=' ')
        self.AverageWaitTime(pplist=pplist, List=chart)
        print('Turn Around Time (SJF) = ', end=' ')
        self.TurnAroundTime(pplist, chart)
        print('Out Of Algorithm 10ms (SJF) = ', end=' ')
        self.OutAlgorithm(chart, pplist, x=10)
        print('Using Cpu (SJF) = ', end=' ')
        self.UsingCpu(chart, pplist, cs)
        print('Average Response (SJF) = ', end=' ')
        self.AverageResponse(chart, pplist)
        print('\n\n')

    def SRT(self,plist, cs):
        pplist = plist
        time = 0
        chart = []
        while True:
            Processs = []
            UnProcess = []
            for i in range(len(plist)):
                if plist[i].arrival <= time and plist[i].burst > 0 and (plist[i] not in Processs):
                    Processs.append(plist[i])
                if plist[i].arrival > time and plist[i].burst > 0 and (plist[i] not in UnProcess):
                    UnProcess.append(plist[i])

            Processs.sort(key=lambda x: x.burst, reverse=False)
            UnProcess.sort(key=lambda x: x.arrival, reverse=False)
            if len(Processs) > 0 and len(UnProcess) > 0:
                if Processs[0].burst + Processs[0].arrival - UnProcess[0].arrival > 0:
                    chart.append(
                        ['P{0}'.format(Processs[0].pid), time, time + (UnProcess[0].arrival - Processs[0].arrival)])
                    time += (UnProcess[0].arrival - Processs[0].arrival)
                    Processs[0].burst -= (UnProcess[0].arrival - Processs[0].arrival)
                    time += cs
                else:
                    chart.append(['P{0}'.format(Processs[0].pid), time, time + Processs[0].burst])
                    time += Processs[0].burst
                    Processs[0].burst = 0
                    time += cs
            elif len(Processs) > 0 and len(UnProcess) == 0:
                Processs.sort(key=lambda x: x.burst, reverse=False)
                chart.append(['P{0}'.format(Processs[0].pid), time, time + Processs[0].burst])
                time += Processs[0].burst
                Processs[0].burst = 0
                time += cs
            if len(UnProcess) == 0 and len(Processs) == 0:
                break
        print('SRT : ', chart)
        self.DrawGantt(chart, plist, Algo='SRTF')
        print('ET (SRT) = ', end=' ')
        self.AverageWaitTime(pplist=pplist, List=chart)
        print('Turn Around Time (SRT) = ', end=' ')
        self.TurnAroundTime(pplist, chart)
        print('Out Of Algorithm 10ms (SRT) = ', end=' ')
        self.OutAlgorithm(chart, pplist, x=10)
        print('Using Cpu (SRT) = ', end=' ')
        self.UsingCpu(chart, pplist, cs)
        print('Average Response (SRT) = ', end=' ')
        self.AverageResponse(chart, pplist)

        print('\n\n')

    def shiftCL(self,alist):  # alist is queue list 1,2,3=> 2,3,1 => 3,1,2
        temp = alist[0]  # first process in the list
        for i in range(len(alist) - 1):  # -1
            alist[i] = alist[i + 1]  # any shft will add +1
        alist[len(alist) - 1] = temp  # -1 is the last place in the list ex. 0-4 =>5 elements -1 = 4
        return alist

    def RR(self,tq, plist, cs):  # Round Robin(RR) (plist: process list, tq: Quantum time)
        pplist = plist
        global gchart
        gchart = []
        qqueue = []
        n = len(plist)
        time = 0  # we start arrival_time time 0
        ap = 0  # arrived processes
        done = 0  # done processes, to count the number of processes finished
        q = tq  # time quantum
        start = 1
        t = 0
        while (done < n):  # still more processes
            t += 1
            for i in range(n):  # process next in line
                if time >= plist[i].arrival and (
                        plist[i] not in qqueue):  # to check for a new arrivil process with out checking P1
                    qqueue.append(plist[i])
                    ap += 1
            rp = 0
            for i in range(len(qqueue)):
                if qqueue[i].burst > 0:
                    rp += 1

            if rp < 1:  # in case
                # of there is no arrival
                time += 1
                continue
            if t != 1:
                qqueue = self.shiftCL(qqueue)
            if start:
                if qqueue[0].burst > 0:
                    if qqueue[0].burst > q:
                        gchart.append(['P{0}'.format(qqueue[0].pid), time, time + q])
                        time += q
                        qqueue[0].burst -= q
                    else:
                        gchart.append(['P{0}'.format(qqueue[0].pid), time, time + qqueue[0].burst])
                        time += qqueue[0].burst
                        qqueue[0].end = True
                        qqueue[0].burst = 0
                        done += 1
                        rp -= 1
                    time += cs
        print('RR :', gchart)
        self.DrawGantt(gchart, plist, 'RR')
        print('ET (RR) = ', end=' ')
        self.AverageWaitTime(pplist=pplist, List=gchart)
        print('Turn Around Time (RR) = ', end=' ')
        self.TurnAroundTime(pplist, gchart)
        print('Out Of Algorithm 10ms (RR) = ', end=' ')
        self.OutAlgorithm(gchart, pplist, x=10)
        print('Using Cpu (RR) = ', end=' ')
        self.UsingCpu(gchart, pplist, cs)
        print('Average Response (RR) = ', end=' ')
        self.AverageResponse(gchart, pplist)

        print('\n\n')

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(529, 567)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(120, 40, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(150, 140, 101, 31))
        self.label_2.setObjectName("label_2")
        self.Quantom = QtWidgets.QLineEdit(Form)
        self.Quantom.setGeometry(QtCore.QRect(280, 140, 61, 31))
        self.Quantom.setObjectName("Quantom")
        self.CS = QtWidgets.QLineEdit(Form)
        self.CS.setGeometry(QtCore.QRect(280, 190, 61, 31))
        self.CS.setObjectName("CS")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(150, 200, 101, 16))
        self.label_3.setObjectName("label_3")
        self.Calculate = QtWidgets.QPushButton(Form)
        self.Calculate.setGeometry(QtCore.QRect(200, 260, 93, 28))
        self.Calculate.setDefault(True)
        self.Calculate.setObjectName("Calculate")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(80, 330, 401, 101))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.TAT = QtWidgets.QLabel(Form)
        self.TAT.setGeometry(QtCore.QRect(190, 380, 81, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.TAT.setFont(font)
        self.TAT.setText("")
        self.TAT.setObjectName("TAT")
        self.OA = QtWidgets.QLabel(Form)
        self.OA.setGeometry(QtCore.QRect(190, 420, 81, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.OA.setFont(font)
        self.OA.setText("")
        self.OA.setObjectName("OA")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(80, 410, 401, 101))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def start(self):
        if len(self.CS.text())>0 and len(self.Quantom.text())>0:
            cs=float(self.CS.text())
            q=float(self.Quantom.text())
            filename = 'Data.csv'
            with open(filename, 'r') as p:
                # reads csv into a list of lists
                process = [list(map(float, rec)) for rec in csv.reader(p, delimiter=',')]
            plist = []
            for i in range(len(process)):
                plist.append(Process(int(process[i][0]), process[i][1], process[i][2]))
            plist.sort(key=lambda x: x.arrival, reverse=False)
            self.FCFS(plist, cs)

            plist = []
            for i in range(len(process)):
                plist.append(Process(int(process[i][0]), process[i][1], process[i][2]))
            plist.sort(key=lambda x: x.arrival, reverse=False)
            self.RR(q, plist, cs)

            plist = []
            for i in range(len(process)):
                plist.append(Process(int(process[i][0]), process[i][1], process[i][2]))
            plist.sort(key=lambda x: x.arrival, reverse=False)
            self.LCFS(plist, cs)

            plist = []
            for i in range(len(process)):
                plist.append(Process(int(process[i][0]), process[i][1], process[i][2]))
            plist.sort(key=lambda x: x.arrival, reverse=False)
            self.SJF(plist, cs)

            plist = []
            for i in range(len(process)):
                plist.append(Process(int(process[i][0]), process[i][1], process[i][2]))
            plist.sort(key=lambda x: x.arrival, reverse=False)
            self.SRT(plist, cs)
            self.label_4.setVisible(True)
            self.label_5.setVisible(True)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Input == > in Data.csv File"))
        self.label_2.setText(_translate("Form", "Quantom :"))
        self.label_3.setText(_translate("Form", "ChangeProcess :"))
        self.Calculate.setText(_translate("Form", "Calculate"))
        self.label_4.setText(_translate("Form", "Gantt Charts Saved In Your Computer"))
        self.label_5.setText(_translate("Form", "You Can See Result On Command Line"))
        self.label_5.setVisible(False)
        self.label_4.setVisible(False)
        self.Calculate.clicked.connect(self.start)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
