from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDialog, QFileDialog, QShortcut
from PyQt5.QtGui import QImage, QPixmap, QKeySequence
from frontend import Ui_MainWindow
from stitch_frontend import Ui_Stitch
import cv2 as cv
from stitch import stitch_images
import threading
import keyboard
import serial

class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.capture = False
        self.ui.StchBtn.clicked.connect(self.show_stitched)
        self.on_color = 'rgba( 9, 237, 235, 255)'
        self.off_color = 'rgba(0, 88, 174, 255)'
        self.thread = threading.Thread(target=self.connection)
        #self.thread.start()
        
    def connection(self):
        print('TEST')
        arduino = serial.Serial(port='COM17', baudrate=9600, timeout=.1)
        while True:
            if 1:
                if keyboard.is_pressed("w") and keyboard.is_pressed("a"):
                    arduino.write(bytes("wa\n", encoding='utf-8'))
                    print("wa")
                elif keyboard.is_pressed("s") and keyboard.is_pressed("a"):
                    arduino.write(bytes("sa\n", encoding='utf-8'))
                    print("sa")
                elif keyboard.is_pressed("w") and keyboard.is_pressed("d"):
                    arduino.write(bytes("wd\n", encoding='utf-8'))
                    print("wd")
                elif keyboard.is_pressed("s") and keyboard.is_pressed("d"):
                    arduino.write(bytes("sd\n", encoding='utf-8'))
                    print("sd")
                elif keyboard.is_pressed("w"):
                    arduino.write(bytes("w\n", encoding='utf-8'))
                    print("w")
                elif keyboard.is_pressed("s"):
                    arduino.write(bytes("s\n", encoding='utf-8'))
                    print("s")
                elif keyboard.is_pressed("a"):
                    arduino.write(bytes("a\n", encoding='utf-8'))
                    print("a")
                elif keyboard.is_pressed("d"):
                    arduino.write(bytes("d\n", encoding='utf-8'))
                    print("d")
                else:
                    arduino.write(bytes("n\n", encoding='utf-8'))
                    #self.stop_move_car(self.on_color)
                    print("n")
                
        
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
            _, frame = cap.read()
            frame = cv.flip(frame, 1)
            self.display_image(frame, 1)
            cv.waitKey()
        cap.release()
        
    def show_stitched(self):
        stitched = StitchDlg(self)
        stitched.exec()
    
    def left_movement(self, color1):
        styleSheet = """
        QFrame{
	        background-color: qconicalgradient(cx:0.5, cy:0.5, angle:45, stop:0.749 rgba(0, 88, 174, 0), stop:0.75 {COLOR});
	        border: none;
        }
        """
        newStyleSheet = styleSheet.replace("{COLOR}", color1)
        self.ui.Left.setStyleSheet(newStyleSheet)
    
    def right_movement(self, color1):
        styleSheet = """
        QFrame{
	        background-color: qconicalgradient(cx:0.5, cy:0.5, angle:225, stop:0.75 {COLOR}, stop:0.749 rgba(0, 0, 0, 0));
	        border: none;
        }
        """
        newStyleSheet = styleSheet.replace("{COLOR}", color1)
        self.ui.Right.setStyleSheet(newStyleSheet)
        
    def forward_movement(self, color1):
        styleSheet = """
        QFrame{
        background-color: qconicalgradient(cx:0.5, cy:0.5, angle:315, stop:0.749 rgba(0, 0, 0, 0), stop:0.75 {COLOR});
	    border: none;
        }
        """
        newStyleSheet = styleSheet.replace("{COLOR}", color1)
        self.ui.Up.setStyleSheet(newStyleSheet)    
    
    def backward_movement(self, color1):
        styleSheet = """
        QFrame{
	        background-color: qconicalgradient(cx:0.5, cy:0.5, angle:135, stop:0.749 rgba(0, 0, 0, 0), stop:0.75 {COLOR});
	        border: none;
        }
        """
        newStyleSheet = styleSheet.replace("{COLOR}", color1)
        self.ui.Down.setStyleSheet(newStyleSheet)
        
    def forward_left_movement(self, color1):
        styleSheet = """
        QFrame{
        	border: none;
	        background-color: qconicalgradient(cx:0.7, cy:0.1, angle:225, stop:0.499 rgba(0, 0, 0, 0), stop:0.5 {COLOR});
        }
        """
        newStyleSheet = styleSheet.replace("{COLOR}", color1)
        self.ui.UpperLeft.setStyleSheet(newStyleSheet)
    
    def stop_move_car(self, color):
        styleSheet = """
        QFrame{
	    background-color: {COLOR};
	    border: none;
	    border-radius: 30px;
        }

        """
        newStyleSheet = styleSheet.replace("{COLOR}", color)
        self.ui.Center.setStyleSheet(newStyleSheet)
            
    
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
    interface.thread.start()
    interface.capture_video()
    sys.exit(app.exec_())
