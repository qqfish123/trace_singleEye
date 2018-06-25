from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import serial
import time
from zongheyanshi import Ui_dialog
from PyQt5.QtWidgets import QFileDialog
import cv2

#ff 02 05 f4 01  //500 低档
#ff 02 05 dc 05  //1500中档
#ff 02 05 C4 09  //2500高档
Xlow="ff 02 05 f4 01"
Xmid="ff 02 05 dc 05"
Xhig="ff 02 05 C4 09"
Xsettime=2;

def genCMD(bdint,channel):
    if (bdint>2500 | bdint<500) | (channel<1 | channel>5):
        print('Error input number!')
        return "00"
    else:
        h = hex(bdint)  # 500~1500~2500 转动速度和差值有关，1500代表停止
        hstr = str(h)
        chstr=str(hex(channel))
        channelstr='0'+chstr[2]
        dataH = '0' + hstr[2]
        dataL = hstr[3:5]
        cmdstr="ff "+"02 "+channelstr+" "+dataL+" "+dataH
        print(cmdstr)
        return cmdstr

class MainWindow(QMainWindow, Ui_dialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.capVIS = cv2.VideoCapture(0)
        self.timer_cameraVIS = QTimer(self)
        self.timer_cameraVIS.timeout.connect(self.show_picVIS)
        self._bVISbutton = False
        self._bVISDetect = False
        self._bVISImgsave = False
        # the ball control parameters
        self.port='com5'
        self.speed=500
        self.paradef=1500
        self.paramax=2500
        self.paramin=500

    def show_picVIS(self):
        if self._bVISbutton == True:
            success, frame = self.capVIS.read()
            if success:
                show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
                self.label.setPixmap(QPixmap.fromImage(showImage))
                if self._bVISDetect == True:
                    """mat = detect(frame)
                    show = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
                    showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
                    self.label_2.setPixmap(QPixmap.fromImage(showImage))"""
                if self._bVISImgsave == True:
                    """self._sVISFilename = "./VISimg/" + time.strftime("%Y%m%d-%H_%M_%S",
                                                                     time.localtime(time.time())) + ".jpg"
                    cv2.imwrite(self._sVISFilename, frame)"""
                self.timer_cameraVIS.start(1)
    def bOpenCap(self):
        print('打开视频')
        self.textBrowser.append("打开视频")
        self._bVISbutton = not self._bVISbutton
        if self._bVISbutton == True:
            self.pushButton.setText("关闭相机")
            success, frame = self.capVIS.read()
            if success:
                show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
                self.label.setPixmap(QPixmap.fromImage(showImage))
                self.timer_cameraVIS.start(1)
        else:
            self.pushButton.setText("打开相机")
    def bObjectDetect(self):
        print('目标检测')
        self.textBrowser.append("目标检测")
        self._bVISDetect = not self._bVISDetect
        if self._bVISDetect == True:
            self.pushButton_2.setText("停止检测")
        else:
            self.pushButton_2.setText("目标识别")
    def bSaveCapImg(self):
        print('图像存储')
        self.textBrowser.append("图像存储")
        self._bVISImgsave = not self._bVISImgsave
        if self._bVISImgsave == True:
            self.pushButton_3.setText("停止存储")
        else:
            self.pushButton_3.setText("图像存储")
    def bExit(self):
        print('退出')
    def bOpenAudio(self):
        print('打开声频')
        self.textBrowser.append("打开声频")
    def bCloseAudio(self):
        print('关闭声频')
        self.textBrowser.append("关闭声频")
    def bYTLeftPlus(self):
        print('云台←+')
        self.textBrowser.append("云台←+")
    def bYTLeft(self):
        print("云台←")
        self.textBrowser.append("云台←")
        setpara = self.paradef + self.speed
        ch = 4
        temp = genCMD(setpara, ch)
        cmd_send = bytearray.fromhex(temp)
        print(cmd_send)
        self.ser.write(cmd_send)
        time.sleep(Xsettime)
        setpara = self.paradef
        temp = genCMD(setpara, ch)
        cmd_send = bytearray.fromhex(temp)
        print(cmd_send)
        self.ser.write(cmd_send)
        time.sleep(0.1)
    def bYTRightPlus(self):
        print("云台→+")
        self.textBrowser.append("云台→+")
    def bYTRight(self):
        print("云台→")
        self.textBrowser.append("云台→")
        setpara = self.paradef + self.speed
        ch = 4
        temp = genCMD(setpara, ch)
        cmd_send = bytearray.fromhex(temp)
        print(cmd_send)
        self.ser.write(cmd_send)
        time.sleep(Xsettime)
        setpara = self.paradef
        temp = genCMD(setpara, ch)
        cmd_send = bytearray.fromhex(temp)
        print(cmd_send)
        self.ser.write(cmd_send)
        time.sleep(0.1)
    def bYTReset(self):
        print('云台归零')
        self.textBrowser.append("云台归零")
    def bYTUp(self):
        print('云台↑')
        self.textBrowser.append("云台↑")
    def bYTUpPlus(self):
        print('云台↑+')
        self.textBrowser.append("云台↑+")
    def bYTDown(self):
        print('云台↓')
        self.textBrowser.append("云台↓")
    def bYTDownPlus(self):
        print('云台↓+')
        self.textBrowser.append("云台↓+")
    def cYTVelChange(self):
        print('云台速度')
        self.textBrowser.append("云台速度")
    def cYTComChange(self):
        print('云台端口')
        self.textBrowser.append("云台端口")
        self.port = self.comboBox_2.currentText()
        print(self.port)
    def bYTRollLeft(self):
        print('云台横滚←')
        self.textBrowser.append("云台横滚←")
        setpara=self.paradef-self.speed
        ch=1
        temp=genCMD(setpara,ch)
        cmd_send = bytearray.fromhex(temp)
        print(cmd_send)
        self.ser.write(cmd_send)
        time.sleep(Xsettime)
        setpara = self.paradef
        temp = genCMD(setpara, ch)
        cmd_send = bytearray.fromhex(temp)
        print(cmd_send)
        self.ser.write(cmd_send)
        time.sleep(0.1)


    def bYTRollRight(self):
        print('云台横滚→')
        self.textBrowser.append("云台横滚→")
        setpara = self.paradef + self.speed
        ch = 1
        temp = genCMD(setpara, ch)
        cmd_send = bytearray.fromhex(temp)
        print(cmd_send)
        self.ser.write(cmd_send)
        time.sleep(Xsettime)
        setpara = self.paradef
        temp = genCMD(setpara, ch)
        cmd_send = bytearray.fromhex(temp)
        print(cmd_send)
        self.ser.write(cmd_send)
        time.sleep(0.1)

    def bYTRollReset(self):
        print('云台横滚归零')
        self.textBrowser.append("云台横滚归零")
    def bYTFocusLeft(self):
        print('云台焦距←')
        self.textBrowser.append("云台焦距←")
    def bYTFocusReset(self):
        print('云台焦距归零')
        self.textBrowser.append("云台焦距归零")
    def bYTFocusRight(self):
        print('云台焦距→')
        self.textBrowser.append("云台焦距→")
    def bOpenCom(self):
        print("打开端口")
        self.textBrowser.append("打开端口")

        self.ser =serial.Serial(self.port,9600,timeout=0.5)
        self.ser.stopbits = 1
        self.ser.parity = serial.PARITY_NONE

        if self.ser.isOpen():
            print('open uart: ' + self.port)
        else:
            print('error: not open uart!')
    def bCloseCom(self):
        print("关闭端口")
        self.textBrowser.append("关闭端口")
        self.ser.close()
        if self.ser.isOpen():
            print('close failed! ')
            self.ser.close()
        else:
            print('UART Closed!')
    def rYTMode1(self):
        print("云台模式1")
        self.textBrowser.append("云台模式1:头朝下")
        setpara = self.paramax
        ch = 5
        temp = genCMD(setpara, ch)
        cmd_send = bytearray.fromhex(temp)
        print(cmd_send)
        self.ser.write(cmd_send)
        time.sleep(0.1)
    def rYTMode2(self):
        print("云台模式2")
        self.textBrowser.append("云台模式2:跟随机头方向")
        setpara = self.paradef
        ch = 5
        temp = genCMD(setpara, ch)
        cmd_send = bytearray.fromhex(temp)
        print(cmd_send)
        self.ser.write(cmd_send)
        time.sleep(0.1)
    def rYTMode3(self):
        print("云台模式3")
        self.textBrowser.append("云台模式3:锁定或回中")
        setpara = self.paramin
        ch = 5
        temp = genCMD(setpara, ch)
        cmd_send = bytearray.fromhex(temp)
        print(cmd_send)
        self.ser.write(cmd_send)
        time.sleep(0.1)
if __name__=='__main__':
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())