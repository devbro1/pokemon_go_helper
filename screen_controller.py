from PIL import Image
import subprocess
import pytesseract
import re
import time
from pokemon import Pokemon


class ScreenController:
    def __init__(self):
        pass

    def takeScreenshot(self, path = 'screenshot.png'):
        subprocess.call(['adb', 'shell', 'screencap', '-p', '/sdcard/screenshot.png'])
        subprocess.call(['adb', 'pull', '/sdcard/screenshot.png', path])

        self.image = Image.open(path)
        return self.image

    def getScreenshot(self):
        return self.image
    
    def setScreenshot(self, image):
        self.image = image
    
    def takeScreenshot_test(self):

        return Image.open('screenshot_2lines.png')

    def readScreenShots(self, color, image, color_tolarence=5, tries = 1, bg_color = (255,255,255)):
        width, height = image.size
        rc = Image.new("RGB",(image.size),bg_color)

        for i in range(tries):
            for x in range(width):
                for y in range(height):
                    pixel = image.getpixel((x,y))
                    # if(pixel[0] == 255):
                    #     print(pixel)
                    if(abs(pixel[0] - color[0]) <= color_tolarence and abs(pixel[1] - color[1]) <= color_tolarence and abs(pixel[2] - color[2]) <= color_tolarence):
                        rc.putpixel((x,y),(0,0,0,255))
        return rc

    def readName(self):
        image = self.getScreenshot()
        image = image.crop((330, 1039, 730, 1118))
        image = self.readScreenShots(color = (77,105,107,255),image=image,color_tolarence=10)
        #cropped_img.save("name_cropped.jpg")
        rc = re.sub(r'\s', '', pytesseract.image_to_string(image,config=r'--oem 1 --psm 7'))
        
        image.save("name"+rc+".jpg")
        return rc

    def readHP(self):
        image = self.getScreenshot()
        x=430
        y=1100
        image = image.crop((x,y, x+210, y+200))
        image = self.readScreenShots(color = (120,138,127,255), image=image, color_tolarence=20)
        #image.save("hp.jpg")
        #cropped_img.save("hp_cropped.jpg")
        rc = re.sub(r'\s', '', pytesseract.image_to_string(image))

        try:
            rc = re.search(r'\/(\d+)HP',rc).group(1)
        except:
            rc = '???'

        return rc

    def readFullScreen(self):
        image = self.getScreenshot()
        image = self.readScreenShots(color = (255,255,255), image=image)
        return pytesseract.image_to_string(image)

    def readCP(self):
        image = self.getScreenshot()
        image = image.crop((250, 253, 800, 351))
        image = self.readScreenShots(color = (255,255,255), image=image)
        #image.save("cp.jpg")
        #cropped_img.save("cp_cropped.jpg")
        rc = re.sub(r'\D', '', pytesseract.image_to_string(image))

        return rc
    
    def readIV(self,image):
        #xs = [ 2, 26, 46, 74, 99, 128, 146, 167, 193, 219, 247, 263, 290, 312, 338,352 ]
        xs = [350,338,312,290,263,247,219,193,167,146,128,99,74,46,26,2]
        for i,x in enumerate(xs):
            pixel = image.getpixel((x,10))

            if pixel == (212,133,124,255):
                return 15
            elif pixel == (225, 151, 60, 255):
                return 16-i

        return 0
        raise Exception("Could not figure out IV")

    def readIVs(self):
        image = self.getScreenshot()
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

        # img_attack.save('img_attack.png')
        # img_defense.save('img_defense.png')
        # img_hp.save('img_hp.png')

        attack = self.readIV(img_attack)
        defense = self.readIV(img_defense)
        hp = self.readIV(img_hp)

        return (attack,defense,hp)

    def toggleFavorite(self):
        subprocess.call(['adb', 'shell', 'input', 'tap', '970','330']) #open menu

    def gotoNext(self,speed=500):
        x = '1485'
        subprocess.call(['adb', 'shell', 'input', 'swipe', '930',x,'100',x,str(speed)])
        time.sleep(1)
        
    def goBack(self):
        subprocess.call(['adb', 'shell', 'input', 'tap', '540','2150']) #open menu

    def tagDelete(self):
        subprocess.call(['adb', 'shell', 'input', 'tap', '920','2130']) #open menu
        time.sleep(1)
        subprocess.call(['adb', 'shell', 'input', 'tap', '920','1350']) #tags
        time.sleep(1)
        subprocess.call(['adb', 'shell', 'input', 'tap', '920','770']) #delete
        time.sleep(1)
        subprocess.call(['adb', 'shell', 'input', 'tap', '535','1950']) #done
        time.sleep(1)
    
    def getPokemon(self):
        details = {}
        details['name'] = self.readName()
        details['cp'] = self.readCP()
        details['hp'] = self.readHP()
        (details['attack'],details['defense'],details['health']) = self.readIVs()
        
        return Pokemon(details)
    
    def pressFight(button=1):
        if(button==1):
            subprocess.call(['adb', 'shell', 'input', 'tap', '520','2050']) #middle
        elif(button==2):
            subprocess.call(['adb', 'shell', 'input', 'tap', '330','2050']) #left
        elif(button==3):
            subprocess.call(['adb', 'shell', 'input', 'tap', '710','2050']) #right
