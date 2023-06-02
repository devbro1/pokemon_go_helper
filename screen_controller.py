from PIL import Image
import subprocess
import pytesseract
import re

class ScreenController:
    def __init__(self):
        pass

    def takeScreenshot(self):
        subprocess.call(['adb', 'shell', 'screencap', '-p', '/sdcard/screenshot.png'])
        subprocess.call(['adb', 'pull', '/sdcard/screenshot.png', 'screenshot.png'])

        return Image.open('screenshot.png')

    def readScreenShots(self, color, color_tolarence=5, tries = 1, width= 1080, height = 2340, bg_color = (255,255,255)):

        rc = Image.new("RGB",(width,height),bg_color)

        for i in range(tries):
            image = self.takeScreenshot()
            for x in range(width):
                for y in range(height):
                    pixel = image.getpixel((x,y))
                    # if(pixel[0] == 255):
                    #     print(pixel)
                    if(abs(pixel[0] - color[0]) <= color_tolarence and abs(pixel[1] - color[1]) <= color_tolarence and abs(pixel[2] - color[2]) <= color_tolarence):
                        rc.putpixel((x,y),(0,0,0,255))
        return rc

    def readName(self):
        image = self.readScreenShots(color = (77,105,107,255),color_tolarence=7)
        image.save("name.jpg")
        cropped_img = image.crop((330, 1039, 720, 1108))
        cropped_img.save("name_cropped.jpg")
        rc = re.sub(r'\s', '', pytesseract.image_to_string(cropped_img))

        return rc

    def readCP(self):
        image = self.readScreenShots((255,255,255))
        image.save("cp.jpg")
        cropped_img = image.crop((250, 253, 800, 351))
        cropped_img.save("cp_cropped.jpg")
        rc = re.sub(r'\D', '', pytesseract.image_to_string(cropped_img))

        return rc
    
    def readIV(self,image):
        x = [ 2, 26, 46, 74, 99, 128, 146, 167, 193, 219, 247, 263, 290, 312, 338,360 ]
        for i in range(16):
            pixel = image.getPixel((x,10))

        if pixel == (255,128,121,255):
            return 15
        elif pixel[2] == 226: #blue value
            return i

        raise Exception("Could not figure out IV")

    def readIVs(self):
        image = self.takeScreenshot()


    def gotoNext(self):
        subprocess.call(['adb', 'shell', 'input', 'swipe', '930','1485','100','1485','100'])

    def tagDelete(self):
        subprocess.call(['adb', 'shell', 'input', 'tap', '920','2130']) #open menu
        subprocess.call(['adb', 'shell', 'input', 'tap', '920','1350']) #tags
        subprocess.call(['adb', 'shell', 'input', 'tap', '920','770']) #delete
        subprocess.call(['adb', 'shell', 'input', 'tap', '535','1950']) #done
        


            
