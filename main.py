from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys
from tasks import Periodic_Task,APeriodic_Task
import pyqtgraph as pg
import numpy as np


class Dialog(QDialog):


    def __init__(self):
        self.num = 0
        self.task_index = 0
        self.periodictasks = []
        self.aperiodictasks = []
        self.scheduler = 'Jackson'
        self.tasktype = 'Periodic'
        self.taskname = ''
        self.task_arr_ph = 0
        self.task_deadl = 1
        self.task_comp = 1
        self.task_period = 1
        self.sched = []
        self.task_precedence = []
        super(Dialog, self).__init__()
        self.createFormGroupBox()
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.OKfunction)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Form Layout - pythonspot.com")

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Form layout")
        button = QPushButton('Add Task', self)
        button.setToolTip('Push This Button to Add Tasks')
        self.layout = QFormLayout()
        self.algotypebox = QComboBox(parent= self)
        self.algotypebox .addItem('Jackson(EDD)\'s (Aperiodic)')
        self.algotypebox.addItem('Horn(EDF)\'s (Aperiodic)')
        self.algotypebox.addItem('Bratley (Aperiodic)')
        self.algotypebox.addItem('LDF (Aperiodic)')
        self.algotypebox.addItem('EDF* (Aperiodic)')
        self.algotypebox.addItem('RM (Periodic)')
        self.algotypebox.addItem('EDF (Periodic)')
        self.algotypebox.addItem('DM (Periodic)')
        self.algotypebox.addItem('Polling Server (Mixed)')
        self.algotypebox.addItem('Background Scheduling (Mixed)')
        self.task_num_box = QComboBox(parent=self)
        self.task_num_box.addItem(str(self.num))
        self.task_num_box.activated[str].connect(self.task_num_box_act)
        self.layout.addRow(QLabel('Select Scheduling Algorithm'), self.algotypebox)
        self.layout.addRow(QLabel(""), button)
        self.formGroupBox.setLayout(self.layout)
        self.typebox = QComboBox(parent=self)
        self.typebox.addItem('Periodic')
        self.typebox.addItem('Aperiodic')
        self.tname_box = QLineEdit()
        self.Arr_ph_box = QLineEdit()
        self.period_box = QLineEdit()
        self.deadline_box = QLineEdit()
        self.Ctime_box = QLineEdit()
        self.prec_box = QLineEdit()
        self.algotypebox.activated[str].connect(self.algotypeboxactivated)
        self.typebox.activated[str].connect(self.tasktypeactivated)
        self.tname_box.textChanged[str].connect(self.tname_boxactivated)
        self.Arr_ph_box.textChanged[str].connect(self.Arr_ph_boxactivated)
        self.period_box.textChanged[str].connect(self.period_boxactivated)
        self.deadline_box.textChanged[str].connect(self.deadline_boxactivated)
        self.Ctime_box.textChanged[str].connect(self.Ctime_boxactivated)
        self.prec_box.textChanged[str].connect(self.prec_box_activated)
        self.layout.addRow(QLabel("Task number :"), self.task_num_box)
        self.layout.addRow(QLabel("Name:"), self.tname_box )
        self.layout.addRow(QLabel("Type:"), self.typebox )
        self.layout.addRow(QLabel("Arrival/Phase:"), self.Arr_ph_box )
        self.layout.addRow(QLabel("Period:"), self.period_box )
        self.layout.addRow(QLabel("Deadline:"), self.deadline_box )
        self.layout.addRow(QLabel("Computation Time:"), self.Ctime_box )
        self.layout.addRow(QLabel("Precedence:"), self.prec_box)
        button.clicked.connect(self.on_click)







    @pyqtSlot()
    def on_click(self):
        self.num = self.num + 1
        self.task_num_box.addItem(str(self.num))
        if(self.tasktype== 'Periodic'):
            self.periodictasks.append(Periodic_Task(name= self.taskname, phase = self.task_arr_ph, deadline= self.task_deadl, compute= self.task_comp, period= self.task_period))
        if(self.tasktype== 'Aperiodic'):
            self.aperiodictasks.append(APeriodic_Task(name = self.taskname, arrival= self.task_arr_ph, compute= self.task_comp, deadline= self.task_deadl, precedence= self.task_precedence))
        print(self.periodictasks[self.num-1].name , self.periodictasks[self.num-1].deadline , self.periodictasks[self.num-1].compute , self.periodictasks[self.num-1].period)

    def algotypeboxactivated(self, text):
        self.scheduler = text

    def tasktypeactivated(self,text):
        self.tasktype = text

    def tname_boxactivated(self,text):
        self.taskname = text

    def Arr_ph_boxactivated(self,text):
        self.task_arr_ph = int(text)

    def period_boxactivated(self,text):
        self.task_period = int(text)

    def deadline_boxactivated(self,text):
        self.task_deadl = int(text)

    def Ctime_boxactivated(self,text):
        self.task_comp = int(text)

    def prec_box_activated(self,text):
        self.task_precedence = text

    def task_num_box_act(self,text):
        self.task_index = int(text)


    def OKfunction(self):
        print("OK")
        self.sched = ['t0', 't0', 't1', 't1', 't1', 't1', 't0', 't0', 't1', 't1', 't1', 't1', 't0', 't0', 't1', 't0', 't0', 't1',
         't1', 't1', 't0', 't0', 't1', 't1', 't1', 't1', 't0', 't0', 't1', 't1', 't1', 't1', 't0', 't0', 'idle']
        x = np.linspace(start=0, stop=len(self.sched), num=1e+4)
        y = []
        t=0
        for e in x:
            if(self.sched[t] == 't0'):
                y.append(1)
            else:
                y.append(0)
            if(e>t+1):
                t = t+1
        plt1 = pg.plot(x,y)
        plt1.showGrid(x=True, y=True)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())