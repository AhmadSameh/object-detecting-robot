# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stitch_label.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Stitch(object):
    def setupUi(self, Stitch):
        Stitch.setObjectName("Stitch")
        Stitch.resize(981, 531)
        Stitch.setStyleSheet("QDialog{\n"
"    background-color: #00365f;\n"
"}")
        self.Stitched = QtWidgets.QLabel(Stitch)
        self.Stitched.setGeometry(QtCore.QRect(360, 20, 601, 491))
        self.Stitched.setStyleSheet("QLabel{\n"
"    border-radius: 20px;\n"
"    border: 5px solid #ffbe00;\n"
"}")
        self.Stitched.setText("")
        self.Stitched.setObjectName("Stitched")
        self.Img1Btn = QtWidgets.QPushButton(Stitch)
        self.Img1Btn.setGeometry(QtCore.QRect(60, 40, 131, 71))
        self.Img1Btn.setStyleSheet("QPushButton{\n"
"    background-color: #ffbe00;\n"
"    border-radius: 30px;\n"
"    color: #00365f;\n"
"}")
        self.Img1Btn.setObjectName("Img1Btn")
        self.Img2Btn = QtWidgets.QPushButton(Stitch)
        self.Img2Btn.setGeometry(QtCore.QRect(60, 140, 131, 71))
        self.Img2Btn.setStyleSheet("QPushButton{\n"
"    background-color: #ffbe00;\n"
"    border-radius: 30px;\n"
"    color: #00365f;\n"
"}")
        self.Img2Btn.setObjectName("Img2Btn")
        self.Img3Btn = QtWidgets.QPushButton(Stitch)
        self.Img3Btn.setGeometry(QtCore.QRect(60, 230, 131, 71))
        self.Img3Btn.setStyleSheet("QPushButton{\n"
"    background-color: #ffbe00;\n"
"    border-radius: 30px;\n"
"    color: #00365f;\n"
"}")
        self.Img3Btn.setObjectName("Img3Btn")
        self.Img4Btn = QtWidgets.QPushButton(Stitch)
        self.Img4Btn.setGeometry(QtCore.QRect(60, 320, 131, 71))
        self.Img4Btn.setStyleSheet("QPushButton{\n"
"    background-color: #ffbe00;\n"
"    border-radius: 30px;\n"
"    color: #00365f;\n"
"}")
        self.Img4Btn.setObjectName("Img4Btn")
        self.Img5Btn = QtWidgets.QPushButton(Stitch)
        self.Img5Btn.setGeometry(QtCore.QRect(60, 410, 131, 71))
        self.Img5Btn.setStyleSheet("QPushButton{\n"
"    background-color: #ffbe00;\n"
"    border-radius: 30px;\n"
"    color: #00365f;\n"
"}")
        self.Img5Btn.setObjectName("Img5Btn")

        self.retranslateUi(Stitch)
        QtCore.QMetaObject.connectSlotsByName(Stitch)

    def retranslateUi(self, Stitch):
        _translate = QtCore.QCoreApplication.translate
        Stitch.setWindowTitle(_translate("Stitch", "Dialog"))
        self.Img1Btn.setText(_translate("Stitch", "Select File!"))
        self.Img2Btn.setText(_translate("Stitch", "Select File!"))
        self.Img3Btn.setText(_translate("Stitch", "Select File!"))
        self.Img4Btn.setText(_translate("Stitch", "Select File!"))
        self.Img5Btn.setText(_translate("Stitch", "Select File!"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Stitch = QtWidgets.QDialog()
    ui = Ui_Stitch()
    ui.setupUi(Stitch)
    Stitch.show()
    sys.exit(app.exec_())
