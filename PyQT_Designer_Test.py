from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush, QImage, QPalette, QPixmap
from PyQt5 import uic
import time
import sys

from PyQt5.uic.properties import QtGui

import PyQT_Thread


form_class = uic.loadUiType("Layout.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.textLabel_1.setText("Dev91")
        self.pushButton_1.clicked.connect(self.btn_1_clicked)
        self.pushButton_2.clicked.connect(self.threadStart)
        self.pushButton_3.clicked.connect(self.threadStop)
        self.pushButton_4.clicked.connect(self.createdDialog)


        # 배경 화면 세팅
        self.p_image = QImage("cloud_background.jpg")
        # .scaled(QSize(self.width(), self.height()))

        self.palette = QPalette()
        self.palette.setBrush(10, QBrush(self.p_image))
        self.setPalette(self.palette)

        # 쓰레드 인스턴스 생성
        self.th_1 = PyQT_Thread.TestThread(self)
        self.th_2 = PyQT_Thread.TestThread(self, 1)  # 그냥 시간차 둬볼려고 했움...
        self.th_3 = PyQT_Thread.TestThread(self, th_time=0.1)  # 이미지가 창 크기에 따라 조정되게

        self.img_w = 0
        self.img_h = 0

        # 쓰레드 이벤트 연결
        self.th_1.threadEvent.connect(self.threadEventHandler_1)
        self.th_2.threadEvent.connect(self.threadEventHandler_2)
        self.th_3.threadEvent.connect(self.threadEventHandler_3)

    def btn_1_clicked(self):
        self.img = QPixmap("Dev_Large_Clear.png").scaled(self.imageLabel_1.width(), self.imageLabel_1.height())
        # self.img
        self.imageLabel_1.setPixmap(self.img)
        self.textBrowser_1.append("=======")
        if not self.th_3.isRun:
            print('이미지 : 쓰레드 시작')
            self.th_3.isRun = True
            self.th_3.start()

    def createdDialog(self):
        dp_image = QImage("clear_image.png")
        dialog_palette = QPalette()
        dialog_palette.setBrush(10, QBrush(dp_image))

        self.dialog = QDialog()
        self.dialog.setPalette(dialog_palette)
        self.dialog.show()

    @pyqtSlot()
    def threadStart(self):
        if not self.th_1.isRun:
            print('메인 : 쓰레드 시작')
            self.th_1.isRun = True
            self.th_1.start()

        if not self.th_2.isRun:
            print('서브 : 쓰레드 시작')
            self.th_2.isRun = True
            self.th_2.start()
 
    @pyqtSlot()
    def threadStop(self):
        if self.th_1.isRun:
            print('메인 : 쓰레드 정지')
            self.th_1.isRun = False
        
        if self.th_2.isRun:
            print('서브 : 쓰레드 정지')
            self.th_2.isRun = False

    @pyqtSlot(int)
    def threadEventHandler_1(self, n):
        print('메인 : threadEvent(self,' + str(n) + ')')
        self.lcdNumber_1.display(n)
        self.textBrowser_1.append("Main Count : " + str(n))

    @pyqtSlot(int)
    def threadEventHandler_2(self, n):
        print('서브 : threadEvent(self,' + str(n) + ')')
        self.lcdNumber_2.display(n)
        self.textBrowser_1.append("Sub Count : " + str(n))
    
    @pyqtSlot()
    def threadEventHandler_3(self):
        if self.imageLabel_1.width() != self.img_w or self.imageLabel_1.height() != self.img_h:
            print('이미지 : threadEvent()')
            self.img_w = self.imageLabel_1.width()
            self.img_h = self.imageLabel_1.height()
            self.img = QPixmap("Dev_Large_Clear.png").scaled(self.img_w, self.img_h)
            self.imageLabel_1.setPixmap(self.img)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showFullScreen()
    app.exec_()