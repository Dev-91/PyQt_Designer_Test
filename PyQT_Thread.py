from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore  # QtCore를 명시적으로 보여주기 위해
from PyQt5 import uic
import time


class TestThread(QThread):
    # 쓰레드의 커스텀 이벤트
    # 데이터 전달 시 형을 명시해야 함
    threadEvent = QtCore.pyqtSignal(int)
 
    def __init__(self, parent=None, th_time=0.2, delay_time=0):
        super().__init__()
        
        self.n = 0
        self.main = parent
        self.isRun = False
        self.delay_time = delay_time
 
    def run(self):
        time.sleep(self.delay_time)
        while self.isRun:
            # print('쓰레드 : ' + str(self.n))
 
            # 'threadEvent' 이벤트 발생
            # 파라미터 전달 가능(객체도 가능)
            self.threadEvent.emit(self.n)
 
            self.n += 1
            # self.sleep(1)
            time.sleep(0.2)