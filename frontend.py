# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'project.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1001, 637)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QWidget{\n"
"    background-color: #00365f;\n"
"}")
        self.centralwidget.setObjectName("centralwidget")
        self.Cam = QtWidgets.QLabel(self.centralwidget)
        self.Cam.setGeometry(QtCore.QRect(390, 20, 601, 601))
        self.Cam.setStyleSheet("QLabel{\n"
"    border-radius: 20px;\n"
"    border: 5px solid #ffbe00;\n"
"}")
        self.Cam.setText("")
        self.Cam.setObjectName("Cam")
        self.SpdFram = QtWidgets.QFrame(self.centralwidget)
        self.SpdFram.setGeometry(QtCore.QRect(50, 310, 271, 81))
        self.SpdFram.setStyleSheet("QFrame{\n"
"    border-radius: 20px;\n"
"    border: 5px solid #ffbe00;\n"
"}")
        self.SpdFram.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.SpdFram.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SpdFram.setObjectName("SpdFram")
        self.HiSpd1 = QtWidgets.QFrame(self.SpdFram)
        self.HiSpd1.setGeometry(QtCore.QRect(180, 10, 31, 61))
        self.HiSpd1.setStyleSheet("QFrame{\n"
"    background-color: #6b0000;\n"
"    border: none;\n"
"}\n"
"\n"
"QFrame:hover{\n"
"    background-color: red;\n"
"}")
        self.HiSpd1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.HiSpd1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.HiSpd1.setObjectName("HiSpd1")
        self.LowSpd2 = QtWidgets.QFrame(self.SpdFram)
        self.LowSpd2.setGeometry(QtCore.QRect(60, 10, 31, 61))
        self.LowSpd2.setStyleSheet("QFrame{\n"
"    background-color: #1b611a;\n"
"    border: none;\n"
"}\n"
"QFrame:hover{\n"
"    background-color: #04ff00;\n"
"}")
        self.LowSpd2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.LowSpd2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.LowSpd2.setObjectName("LowSpd2")
        self.MidSpd2 = QtWidgets.QFrame(self.SpdFram)
        self.MidSpd2.setGeometry(QtCore.QRect(140, 10, 31, 61))
        self.MidSpd2.setStyleSheet("QFrame{\n"
"    background-color: #858517;\n"
"    border: none;\n"
"}\n"
"\n"
"QFrame:hover{\n"
"    background-color: #ffff00;\n"
"}")
        self.MidSpd2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MidSpd2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MidSpd2.setObjectName("MidSpd2")
        self.HiSpd2 = QtWidgets.QFrame(self.SpdFram)
        self.HiSpd2.setGeometry(QtCore.QRect(220, 10, 31, 61))
        self.HiSpd2.setStyleSheet("QFrame{\n"
"    background-color: #6b0000;\n"
"    border: none;\n"
"}\n"
"\n"
"QFrame:hover{\n"
"    background-color: red;\n"
"}")
        self.HiSpd2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.HiSpd2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.HiSpd2.setObjectName("HiSpd2")
        self.LowSpd1 = QtWidgets.QFrame(self.SpdFram)
        self.LowSpd1.setGeometry(QtCore.QRect(20, 10, 31, 61))
        self.LowSpd1.setStyleSheet("QFrame{\n"
"    background-color: #1b611a;\n"
"    border: none;\n"
"}\n"
"QFrame:hover{\n"
"    background-color: #04ff00;\n"
"}")
        self.LowSpd1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.LowSpd1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.LowSpd1.setObjectName("LowSpd1")
        self.MidSpd1 = QtWidgets.QFrame(self.SpdFram)
        self.MidSpd1.setGeometry(QtCore.QRect(100, 10, 31, 61))
        self.MidSpd1.setStyleSheet("QFrame{\n"
"    background-color: #858517;\n"
"    border: none;\n"
"}\n"
"\n"
"QFrame:hover{\n"
"    background-color: #ffff00;\n"
"}")
        self.MidSpd1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MidSpd1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MidSpd1.setObjectName("MidSpd1")
        self.DirFrm = QtWidgets.QFrame(self.centralwidget)
        self.DirFrm.setGeometry(QtCore.QRect(60, 30, 261, 261))
        self.DirFrm.setStyleSheet("QFrame{\n"
"    border-radius: 130px;\n"
"    border: 5px solid #ffbe00;\n"
"}")
        self.DirFrm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.DirFrm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.DirFrm.setObjectName("DirFrm")
        self.frame_3 = QtWidgets.QFrame(self.DirFrm)
        self.frame_3.setGeometry(QtCore.QRect(50, 60, 60, 60))
        self.frame_3.setStyleSheet("QFrame{\n"
"    border: none;\n"
"    background-color: qconicalgradient(cx:0.7, cy:0.1, angle:225, stop:0.499 rgba(0, 0, 0, 0), stop:0.5 rgba(0, 88, 174, 255));\n"
"}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.frame_10 = QtWidgets.QFrame(self.DirFrm)
        self.frame_10.setGeometry(QtCore.QRect(100, 100, 60, 60))
        self.frame_10.setStyleSheet("QFrame{\n"
"    background-color: #0058ae;\n"
"    border: none;\n"
"    border-radius: 30px;\n"
"}\n"
"\n"
"QFrame:hover{\n"
"    background-color: #09edeb;\n"
"}")
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.frame_5 = QtWidgets.QFrame(self.DirFrm)
        self.frame_5.setGeometry(QtCore.QRect(150, 60, 60, 60))
        self.frame_5.setStyleSheet("QFrame{\n"
"background-color: qconicalgradient(cx:0.3, cy:0.1, angle:135, stop:0.499 rgba(0, 0, 0, 0), stop:0.5 rgba(0, 88, 174, 255));\n"
"    border: none;\n"
"}\n"
"\n"
"QFrame:hover{\n"
"    background-color: qconicalgradient(cx:0.3, cy:0.1, angle:135, stop:0.499 rgba(0, 0, 0, 0), stop:0.5 rgba( 9, 237, 235, 255));\n"
"}")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.frame_4 = QtWidgets.QFrame(self.DirFrm)
        self.frame_4.setGeometry(QtCore.QRect(180, 100, 60, 60))
        self.frame_4.setStyleSheet("QFrame{\n"
"    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:225, stop:0.75 rgba(0, 88, 174, 255), stop:0.749 rgba(0, 0, 0, 0));\n"
"    border: none;\n"
"}")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.frame_7 = QtWidgets.QFrame(self.DirFrm)
        self.frame_7.setGeometry(QtCore.QRect(50, 140, 60, 60))
        self.frame_7.setStyleSheet("QFrame{\n"
"    border: none;\n"
"    background-color: qconicalgradient(cx:0.7, cy:0.9, angle:315, stop:0.499 rgba(0, 0, 0, 0), stop:0.5 rgba(0, 88, 174, 255));\n"
"}")
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.frame_9 = QtWidgets.QFrame(self.DirFrm)
        self.frame_9.setGeometry(QtCore.QRect(150, 140, 60, 60))
        self.frame_9.setStyleSheet("QFrame{\n"
"background-color: qconicalgradient(cx:0.3, cy:0.9, angle:45, stop:0.499 rgba(0, 0, 0, 0), stop:0.5 rgba(0, 88, 174, 255));\n"
"    border: none;\n"
"}")
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.frame_6 = QtWidgets.QFrame(self.DirFrm)
        self.frame_6.setGeometry(QtCore.QRect(20, 100, 60, 60))
        self.frame_6.setStyleSheet("QFrame{\n"
"    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:45, stop:0.749 rgba(0, 88, 174, 0), stop:0.75 rgba(0, 88, 174, 255));\n"
"    border: none;\n"
"}")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.frame_2 = QtWidgets.QFrame(self.DirFrm)
        self.frame_2.setGeometry(QtCore.QRect(100, 20, 60, 60))
        self.frame_2.setStyleSheet("QFrame{\n"
"background-color: qconicalgradient(cx:0.5, cy:0.5, angle:315, stop:0.749 rgba(0, 0, 0, 0), stop:0.75 rgba(0, 88, 174, 255));\n"
"    border: none;\n"
"}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.frame = QtWidgets.QFrame(self.DirFrm)
        self.frame.setGeometry(QtCore.QRect(100, 180, 60, 60))
        self.frame.setStyleSheet("QFrame{\n"
"    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:135, stop:0.749 rgba(0, 0, 0, 0), stop:0.75 rgba(0, 88, 174, 255));\n"
"    border: none;\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.CapBtn = QtWidgets.QPushButton(self.centralwidget)
        self.CapBtn.setGeometry(QtCore.QRect(40, 400, 121, 81))
        self.CapBtn.setStyleSheet("QPushButton{\n"
"    background-color: #ffbe00;\n"
"    border-radius: 30px;\n"
"}")
        self.CapBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("capture.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CapBtn.setIcon(icon)
        self.CapBtn.setIconSize(QtCore.QSize(60, 60))
        self.CapBtn.setObjectName("CapBtn")
        self.OnOff = QtWidgets.QFrame(self.centralwidget)
        self.OnOff.setGeometry(QtCore.QRect(240, 400, 80, 80))
        self.OnOff.setStyleSheet("QFrame{\n"
"    background-color: #6b0000;\n"
"    border-radius: 40px;\n"
"    border: 3px solid #ffbe00\n"
"}\n"
"\n"
"QFrame:hover{\n"
"    background-color: red;\n"
"}")
        self.OnOff.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.OnOff.setFrameShadow(QtWidgets.QFrame.Raised)
        self.OnOff.setObjectName("OnOff")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(40, 500, 121, 61))
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_2.setGeometry(QtCore.QRect(220, 500, 121, 61))
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 570, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel{\n"
"    color: #ffbe00;\n"
"}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(250, 570, 55, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("QLabel{\n"
"    color: #ffbe00;\n"
"}")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Robot"))
        self.label.setText(_translate("MainWindow", "A"))
        self.label_2.setText(_translate("MainWindow", "V"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
