from screen_controller import ScreenController
import time
import subprocess


screen_reader = ScreenController()

for i in range(30):
    print("current i:" + str(i))
    print("ignore existing gift")
    subprocess.call(['adb', 'shell', 'input', 'tap', '520','1220'])
    time.sleep(4)
    subprocess.call(['adb', 'shell', 'input', 'tap', '520','2130'])
    time.sleep(2)
    print("sending gift")
    subprocess.call(['adb', 'shell', 'input', 'tap', '180','1810'])
    time.sleep(1)
    subprocess.call(['adb', 'shell', 'input', 'tap', '500','840'])
    print("adding sticker")
    time.sleep(2)
    subprocess.call(['adb', 'shell', 'input', 'tap', '500','1725'])
    time.sleep(2)
    subprocess.call(['adb', 'shell', 'input', 'tap', '770','1285'])
    time.sleep(1)
    subprocess.call(['adb', 'shell', 'input', 'tap', '130','1650'])
    print("send gift")
    time.sleep(2)
    subprocess.call(['adb', 'shell', 'input', 'tap', '500','1940'])
    time.sleep(7)
    print("go to next friend")
    screen_reader.gotoNext()
    time.sleep(5)
