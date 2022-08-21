import time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QThread, QRunnable
from PyQt5.QtWidgets import QMainWindow, QDialog, QFileDialog, QShortcut
from PyQt5.QtGui import QImage, QPixmap, QKeySequence
from frontend import Ui_MainWindow
from stitch_frontend import Ui_Stitch
import cv2 as cv
from stitch import stitch_images
import threading
import keyboard
import serial
import numpy as np

class Interface(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.capture = False
        self.img_num = 1
        self.update2 = pyqtSignal(str)
        self.speed = 1
        self.current = 0.0
        self.volt = 0.0
        self.ui.CapBtn.clicked.connect(self.capture_frame)
        self.ui.StchBtn.clicked.connect(self.show_stitched)
        self.on_color = 'rgba( 9, 237, 235, 255)'
        self.off_color = 'rgba(0, 88, 174, 255)'
        self.thread2 = threading.Thread(target=self.move2)
        self.threadOn = True
        self.thread2.start()
        self.thread = Worker1('n')
        self.thread.update_direction.connect(self.move)        
        
        self.worker2 = Worker2()
        self.worker2.start()
        self.worker2.ImageUpdate.connect(self.display_image)
        
    def capture_frame(self):
        self.capture = True

    def move2(self):
        arduino = serial.Serial(port='COM17', baudrate=9600, timeout=.1)
        volt = ""
        current = ""
        up_press = False
        down_press = False
        moving = False
        while True:
            if arduino.isOpen():
                if keyboard.is_pressed('UP') and not up_press:
                    up_press = True
                    self.speed += 1
                    self.speed = 3 if self.speed > 3 else self.speed
                    self.thread.start()
                    arduino.write(bytes("UP\n", encoding='utf-8'))
                elif not keyboard.is_pressed('UP'):
                    up_press = False
                if keyboard.is_pressed('DOWN') and not down_press:
                    down_press = True
                    self.speed -= 1
                    self.speed = 1 if self.speed < 1 else self.speed
                    self.thread.start()
                    arduino.write(bytes("DOWN\n", encoding='utf-8'))
                elif not keyboard.is_pressed('down'):
                    down_press = False
                if keyboard.is_pressed("w") and keyboard.is_pressed("a"):
                    arduino.write(bytes("wa\n", encoding='utf-8'))
                    self.thread.direction = 'wa'
                    self.thread.start()
                    moving = True
                elif keyboard.is_pressed("s") and keyboard.is_pressed("a"):
                    arduino.write(bytes("sa\n", encoding='utf-8'))
                    self.thread.direction = 'sa'
                    self.thread.start()
                    moving = True
                elif keyboard.is_pressed("w") and keyboard.is_pressed("d"):
                    arduino.write(bytes("wd\n", encoding='utf-8'))
                    self.thread.direction = 'wd'
                    self.thread.start()
                    moving = True
                elif keyboard.is_pressed("s") and keyboard.is_pressed("d"):
                    arduino.write(bytes("sd\n", encoding='utf-8'))
                    self.thread.direction = 'sd'
                    self.thread.start()
                    moving = True
                elif keyboard.is_pressed("w"):
                    arduino.write(bytes("w\n", encoding='utf-8'))
                    self.thread.direction = 'w'
                    self.thread.start()
                    moving = True
                elif keyboard.is_pressed("s"):
                    arduino.write(bytes("s\n", encoding='utf-8'))
                    self.thread.direction = 's'
                    self.thread.start()
                    moving = True
                elif keyboard.is_pressed("a"):
                    arduino.write(bytes("a\n", encoding='utf-8'))
                    self.thread.direction = 'a'
                    self.thread.start()
                    moving = True
                elif keyboard.is_pressed("d"):
                    arduino.write(bytes("d\n", encoding='utf-8'))
                    self.thread.direction = 'd'
                    self.thread.start()
                    moving = True
                elif moving:
                    arduino.write(bytes("n\n", encoding='utf-8'))
                    self.thread.direction = 'n'
                    self.thread.start()
                    moving = False
            line = arduino.readline().decode().rstrip()
            line_split = line.split(",")
            if len(line_split) == 2:
                self.volt = line_split[0]
                self.current = line_split[1]

    @QtCore.pyqtSlot(str)
    def move(self, direction):
        self.ui.ALCD.display(self.current)
        self.ui.VLCD.display(self.volt)
        self.indicate_connection()
        self.indicate_speed()
        self.stop_move_car(self.off_color)
        self.forward_left_movement(self.off_color)
        self.forward_right_movement(self.off_color)
        self.backward_left_movement(self.off_color)
        self.backward_right_movement(self.off_color)
        self.left_movement(self.off_color)
        self.right_movement(self.off_color)
        self.backward_movement(self.off_color)
        self.forward_movement(self.off_color)
        if direction == 'front left':
            self.forward_left_movement(self.on_color)
        elif direction == 'left':
            self.left_movement(self.on_color)
        elif direction == 'right':
            self.right_movement(self.on_color)
        elif direction == 'front':
            self.forward_movement(self.on_color)
        elif direction == 'back':
            self.backward_movement(self.on_color)   
        elif direction == 'back left':
            self.backward_left_movement(self.on_color)
        elif direction == 'front right':
            self.forward_right_movement(self.on_color)
        elif direction == 'back right':
            self.backward_right_movement(self.on_color)
        elif direction == 'stop':
            self.stop_move_car(self.on_color)        
    
    @QtCore.pyqtSlot(np.ndarray)                
    def display_image(self, img, window=1):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        if self.capture:
            title = 'img{NUM}.jpg'
            title = title.replace('{NUM}', str(self.img_num))
            cv.imwrite(title, img)
            self.img_num += 1
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
        
    def forward_right_movement(self, color1):
        styleSheet = """
        QFrame{
        background-color: qconicalgradient(cx:0.3, cy:0.1, angle:135, stop:0.499 rgba(0, 0, 0, 0), stop:0.5 {COLOR});
	        border: none;
        }
        """
        newStyleSheet = styleSheet.replace("{COLOR}", color1)
        self.ui.UpperRight.setStyleSheet(newStyleSheet)
    
    def backward_left_movement(self, color1):
        styleSheet = """
        QFrame{
	        border: none;
	        background-color: qconicalgradient(cx:0.7, cy:0.9, angle:315, stop:0.499 rgba(0, 0, 0, 0), stop:0.5 {COLOR});
        }
        """
        newStyleSheet = styleSheet.replace("{COLOR}", color1)
        self.ui.LowerLeft.setStyleSheet(newStyleSheet)
        
    def backward_right_movement(self, color1):
        styleSheet = """
        QFrame{
        background-color: qconicalgradient(cx:0.3, cy:0.9, angle:45, stop:0.499 rgba(0, 0, 0, 0), stop:0.5 {COLOR});
	        border: none;
        }
        """
        newStyleSheet = styleSheet.replace("{COLOR}", color1)
        self.ui.LowerRight.setStyleSheet(newStyleSheet)
    
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

    def closeEvent(self, event):
        self.threadOn = False
        self.thread.join()
        event.accept()
        sys.exit()
    
    def indicate_connection(self):
        styleSheet = """
        QFrame{
	        background-color: {COLOR};
	        border-radius: 40px;
	        border: 3px solid #ffbe00
        }
        """
        color = 'red'
        newStyleSheet = styleSheet.replace("{COLOR}", color)
        self.ui.OnOff.setStyleSheet(newStyleSheet)

    def indicate_speed(self):
        self.low_speed()
        if self.speed == 1:
            self.mid_speed('#858517')
            self.high_speed('#6b0000')
        elif self.speed == 2:
            self.mid_speed('#ffff00')
            self.high_speed('#6b0000')
        elif self.speed == 3:
            self.mid_speed('#ffff00')
            self.high_speed('red')
            
    def low_speed(self):
        styleSheet = """
        QFrame{
	        background-color: {COLOR};
	        border: none;
        }
        """
        newStyleSheet = styleSheet.replace("{COLOR}", '#00ff00')
        self.ui.LowSpd1.setStyleSheet(newStyleSheet)
        self.ui.LowSpd2.setStyleSheet(newStyleSheet)
        
    def mid_speed(self, color):
        styleSheet = """
        QFrame{
	        background-color: {COLOR};
	        border: none;
        }
        """
        newStyleSheet = styleSheet.replace("{COLOR}", color)
        self.ui.MidSpd1.setStyleSheet(newStyleSheet)
        self.ui.MidSpd2.setStyleSheet(newStyleSheet)
        
    def high_speed(self, color):
        styleSheet = """
        QFrame{
	        background-color: {COLOR};
	        border: none;
        }
        """
        newStyleSheet = styleSheet.replace("{COLOR}", color)
        self.ui.HiSpd1.setStyleSheet(newStyleSheet)
        self.ui.HiSpd2.setStyleSheet(newStyleSheet)
    
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
                
class Worker1(QThread):
    update_direction = pyqtSignal(str)
    def __init__(self, direction, parent = None):
        super(Worker1, self).__init__(parent)
        self.direction = direction
        
    def run(self):
        if keyboard.is_pressed("w") and keyboard.is_pressed("a"):
            self.update_direction.emit('front left')
        elif keyboard.is_pressed("s") and keyboard.is_pressed("a"):
            self.update_direction.emit('back left')
        elif keyboard.is_pressed("w") and keyboard.is_pressed("d"):
            self.update_direction.emit('front right')
        elif keyboard.is_pressed("s") and keyboard.is_pressed("d"):
            self.update_direction.emit('back right')
        elif keyboard.is_pressed("w"):
            self.update_direction.emit('front')
        elif keyboard.is_pressed("s"):
            self.update_direction.emit('back')
        elif keyboard.is_pressed("a"):
            self.update_direction.emit('left')
        elif keyboard.is_pressed("d"):
            self.update_direction.emit('right')
        else:
            self.update_direction.emit('stop')

class Worker2(QThread):
    ImageUpdate = pyqtSignal(np.ndarray)
    def run(self):
        cap = cv.VideoCapture(0)
        while cap.isOpened():
            _, frame = cap.read()
            self.ImageUpdate.emit(frame)
        cap.release()
   
if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    interface = Interface()
    interface.show()
    #interface.capture_video()
    sys.exit(app.exec_())
