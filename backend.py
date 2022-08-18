from textwrap import shorten
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QDialog, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from frontend import Ui_MainWindow
from stitch_frontend import Ui_Stitch
import cv2 as cv
from stitch import stitch_images

class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.capture = False
        self.ui.StchBtn.clicked.connect(self.show_stitched)
        
    def display_image(self, img, window=1):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        if self.capture:
            cv.imwrite('img.jpg', img)
            self.capture = False
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.ui.Cam.setPixmap(QPixmap.fromImage(img))
        self.ui.Cam.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    
    def capture_video(self):
        cap = cv.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            frame = cv.flip(frame, 1)
            self.display_image(frame, 1)
            cv.waitKey()
        cap.release()
        
    def show_stitched(self):
        stitched = StitchDlg(self)
        stitched.exec()
    
class StitchDlg(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_Stitch()
        self.ui.setupUi(self)
        self.img_locations = []
        self.ui.Img1Btn.clicked.connect(lambda: self.choose_file(self.ui.Img1Btn))
        self.ui.Img2Btn.clicked.connect(lambda: self.choose_file(self.ui.Img2Btn))
        self.ui.Img3Btn.clicked.connect(lambda: self.choose_file(self.ui.Img3Btn))
        self.ui.Img4Btn.clicked.connect(lambda: self.choose_file(self.ui.Img4Btn))
        self.ui.Img5Btn.clicked.connect(lambda: self.choose_file(self.ui.Img5Btn))
    
    def display_stitched(self):
        img = stitch_images(self.img_locations)
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.ui.Stitched.setPixmap(QPixmap.fromImage(img))
        self.ui.Stitched.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        
    def choose_file(self, btn):
        img = QFileDialog.getOpenFileName(self, 'open file', '', 'Images (*.jpg)')
        if img:
            self.img_locations.append(img[0])
            btn.setText('FILE SELECTED!')
            if len(self.img_locations) == 5:
                self.display_stitched()
            
if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    interface = Interface()
    interface.show()
    interface.capture_video()
    sys.exit(app.exec_())
