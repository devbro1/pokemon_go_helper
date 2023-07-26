import subprocess
import time
from screen_controller import ScreenController

screen_reader = ScreenController()

for i in range(100):
    
    # screen_reader.takeScreenshot()
    # print(screen_reader.readFullScreen())
    
    #hold on first one
    subprocess.call(['adb', 'shell', 'input', 'swipe', '280', '790', '280', '790', '500'])
    time.sleep(0.3)
    subprocess.call(['adb', 'shell', 'input', 'tap', '790', '790'])
    time.sleep(0.3)
    
    y = '1356'
    subprocess.call(['adb', 'shell', 'input', 'tap', '280', y])
    time.sleep(0.3)
    subprocess.call(['adb', 'shell', 'input', 'tap', '790', y])
    time.sleep(0.3)
    
    subprocess.call(['adb', 'shell', 'input', 'tap', '280', '1904'])
    time.sleep(0.3)
    subprocess.call(['adb', 'shell', 'input', 'tap', '790', '1904'])
    time.sleep(0.3)
    
    #press delete and confirm it
    subprocess.call(['adb', 'shell', 'input', 'tap', '500', '2133'])
    time.sleep(1)
    subprocess.call(['adb', 'shell', 'input', 'tap', '500', '1314'])
    time.sleep(1)