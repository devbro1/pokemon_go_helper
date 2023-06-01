from PIL import Image
import subprocess
import pytesseract
import re

class ScreenReader:
    def __init__():
        pass

    def takeScreenshot(self):
        subprocess.call(['adb', 'shell', 'screencap', '-p', '/sdcard/screenshot.png'])
        subprocess.call(['adb', 'pull', '/sdcard/screenshot.png', 'screenshot.png'])

        return Image.open('screenshot.png')

    def readScreenShots(self, color, tries = 5, width= 640, height = 1000, bg_color = (255,255,255)):

        rc = Image.new("RGB",(width,height),bg_color)

        for i in range(tries):
            image = self.takeScreenshot()
            for x in range(width):
                for y in range(height):
                    pixel = image.getpixel((x,y))
                    if(pixel == color):
                        rc.putpixel((x,y),(0,0,0))
        
        return

    def readName(self):
        image = self.readScreenShots((76,104,107))
        cropped_img = image.crop((398, 1039, 681, 1108))
        rc = re.sub(r'\s', '', pytesseract.image_to_string(cropped_img))

        return rc

    def readCP(self):
        image = self.readScreenShots((255,255,255))
        cropped_img = image.crop((250, 253, 800, 351))
        rc = re.sub(r'\D', '', pytesseract.image_to_string(cropped_img))

        return rc
    
    def readIVs(self):
        image = self.takeScreenshot()
        x = [ 2, 26, 46, 74, 99, 128, 146, 167, 193, 219, 247, 263, 290, 312, 338,360 ]
        for i in range(16):
            pixel = image.getPixel((x,10))  # TODO: this is not perfect yet

        if res['b'] == 121:
            return 15
        elif res['b'] == 226:
            return i

    raise Exception("Could not figure out IV")
        


            
