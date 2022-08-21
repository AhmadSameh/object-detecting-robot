import keyboard
import serial
import time

time.sleep(1)
arduino = serial.Serial(port='COM17', baudrate=9600, timeout=.1)
up_press = False
down_press = False
moving = False

volt = ""
current = ""

while True:
    if arduino.isOpen():
        if keyboard.is_pressed("w") and keyboard.is_pressed("a"):
            arduino.write(bytes("wa\n", encoding='utf-8'))
            moving = True
            print("wa")
        elif keyboard.is_pressed("s") and keyboard.is_pressed("a"):
            arduino.write(bytes("sa\n", encoding='utf-8'))
            moving = True
            print("sa")
        elif keyboard.is_pressed("w") and keyboard.is_pressed("d"):
            arduino.write(bytes("wd\n", encoding='utf-8'))
            moving = True
            print("wd")
        elif keyboard.is_pressed("s") and keyboard.is_pressed("d"):
            arduino.write(bytes("sd\n", encoding='utf-8'))
            moving = True
            print("sd")
        elif keyboard.is_pressed("w"):
            arduino.write(bytes("w\n", encoding='utf-8'))
            moving = True
            print("w")
        elif keyboard.is_pressed("s"):
            arduino.write(bytes("s\n", encoding='utf-8'))
            moving = True
            print("s")
        elif keyboard.is_pressed("a"):
            arduino.write(bytes("a\n", encoding='utf-8'))
            moving = True
            print("a")
        elif keyboard.is_pressed("d"):
            arduino.write(bytes("d\n", encoding='utf-8'))
            moving = True
            print("d")
        elif moving:
            arduino.write(bytes("n\n", encoding='utf-8'))
            moving = False
            print("n")
        if keyboard.is_pressed("UP") and not up_press:
            up_press = True
            arduino.write(bytes("UP\n", encoding='utf-8'))
            print("up")
        elif not keyboard.is_pressed("UP"):
            up_press = False
        if keyboard.is_pressed("DOWN") and not down_press:
            down_press = True
            arduino.write(bytes("DOWN\n", encoding='utf-8'))
            print("up")
        elif not keyboard.is_pressed("DOWN"):
            down_press = False
    line = arduino.readline().decode().rstrip()
    line_split = line.split(",")
    if len(line_split) == 2:
        volt = line_split[0]
        current = line_split[1]

    print("Volt: ", volt, " Current: ", current)
