from PIL import Image
import subprocess
import pytesseract
import re

class ScreenController:
    def __init__(self):
        pass

    def takeScreenshot_old(self):
        subprocess.call(['adb', 'shell', 'screencap', '-p', '/sdcard/screenshot.png'])
        subprocess.call(['adb', 'pull', '/sdcard/screenshot.png', 'screenshot.png'])

        return Image.open('screenshot.png')
    
    def takeScreenshot(self):

        return Image.open('screenshot_2lines.png')

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

    def readHP(self):
        image = self.readScreenShots(color = (120,138,127,255),color_tolarence=20)
        image.save("hp.jpg")
        x=430
        y=1220
        cropped_img = image.crop((x,y, x+210, y+50))
        cropped_img.save("hp_cropped.jpg")
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
        #xs = [ 2, 26, 46, 74, 99, 128, 146, 167, 193, 219, 247, 263, 290, 312, 338,352 ]
        xs = [350,338,312,290,263,247,219,193,167,146,128,99,74,46,26,2]
        for i,x in enumerate(xs):
            print(i)
            pixel = image.getpixel((x,10))
            print(pixel)

            if pixel == (212,133,124,255):
                return 15
            elif pixel == (225, 151, 60, 255):
                return 16-i

        return 0
        raise Exception("Could not figure out IV")

    def readIVs(self):
        image = self.takeScreenshot()
        offset=0

        pixel = (255,255,255,255)
        while pixel == (255,255,255,255):
            offset += 1
            pixel = image.getpixel((55,2050-offset))

        offset += -20
        width=353
        height=20
        img_attack = image.crop((138, 1730-offset, 138+width, 1730+height-offset))
        img_defense = image.crop((138, 1831-offset, 138+width, 1831+height-offset))
        img_hp = image.crop((138, 1935-offset, 138+width, 1935+height-offset))

        img_attack.save('img_attack.png')
        img_defense.save('img_defense.png')
        img_hp.save('img_hp.png')

        attack = self.readIV(img_attack)
        defense = self.readIV(img_defense)
        hp = self.readIV(img_hp)

        return (attack,defense,hp)


    def gotoNext(self):
        subprocess.call(['adb', 'shell', 'input', 'swipe', '930','1485','100','1485','100'])

    def tagDelete(self):
        subprocess.call(['adb', 'shell', 'input', 'tap', '920','2130']) #open menu
        subprocess.call(['adb', 'shell', 'input', 'tap', '920','1350']) #tags
        subprocess.call(['adb', 'shell', 'input', 'tap', '920','770']) #delete
        subprocess.call(['adb', 'shell', 'input', 'tap', '535','1950']) #done
        


            
