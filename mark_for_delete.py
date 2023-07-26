import subprocess
from screen_controller import ScreenController
import time

text = ""
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","
text += ","


text = text.replace("\n",",")
screen_reader = ScreenController()

count=0
for selector in text.split(','):
    count += 1
    if selector == "":
        continue
    
    print("labeling "+str(count)+ ": " + selector)
    time.sleep(1)
    subprocess.call(['adb', 'shell', 'input', 'tap', '500', '500'])
    time.sleep(1)
    # for i in range(40):
    #     subprocess.call(['adb', 'shell', 'input', 'keyevent', '67']) #backspace
        
    subprocess.call(['adb', 'shell', 'input', 'keycombination', '113', '29']) #ctrl+a
    subprocess.call(['adb', 'shell', 'input', 'keyevent', '67']) #backspace
    
    selector = "!xxs&!xs&!xl&!xxl&!shiny&!lucky&!4*&!legendary&!do not delete&" + selector
    subprocess.call(['adb', 'shell', 'input', 'text', selector.replace('&','\&') + "\n"])
    
    time.sleep(1)
    
    screen_reader.takeScreenshot('screen_list.png')
    if(screen_reader.readSelectCount() != 1):
        print("not 1 match!!!")
        continue

    # # select pokemon
    subprocess.call(['adb', 'shell', 'input', 'tap', '200', '915'])
    subprocess.call(['adb', 'shell', 'input', 'tap', '200', '915'])
    
    time.sleep(1)
    # add label
    screen_reader.tagDelete()
    
    screen_reader.goBack()