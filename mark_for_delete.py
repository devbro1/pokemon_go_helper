import subprocess
from screen_controller import ScreenController
import time

text = "Ludicolo&CP29&HP18,Lotad&CP23&HP22,Lotad&CP277&HP76,Lotad&CP282&HP80,Lotad&CP395&HP86"



text = text.replace("\n",",")
screen_reader = ScreenController()

count=0
for selector in text.split(','):
    count += 1
    print("labeling "+str(count)+ ": " + selector)
    time.sleep(1)
    subprocess.call(['adb', 'shell', 'input', 'tap', '500', '500'])
    time.sleep(1)
    for i in range(30):
        subprocess.call(['adb', 'shell', 'input', 'keyevent', '67']) #backspace
    
    subprocess.call(['adb', 'shell', 'input', 'text', selector.replace('&','\&') + "\n"])
    time.sleep(1)
    
    screen_reader.takeScreenshot('screen_list.png')
    if(screen_reader.readSelectCount() != 1):
        continue

    # # select pokemon
    subprocess.call(['adb', 'shell', 'input', 'tap', '200', '915'])
    subprocess.call(['adb', 'shell', 'input', 'tap', '200', '915'])
    
    time.sleep(1)
    # add label
    screen_reader.tagDelete()
    
    screen_reader.goBack()