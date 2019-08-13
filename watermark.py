from PIL import Image, ImageDraw, ImageFont
import math
# import matplotlib.pyplot as plt


def watermark(fileName, text, s):
         # 输入要打水印的图片名称
         # 输入要打得水印
         # 保存到指定目录
    im = Image.open(fileName)  # 打开要打水印的相片

    imageW, imageH = im.size  # 获取图片尺寸
    textImageW = int(imageW * 1.5)  # 确定写文字图片的尺寸，如前所述，要比照片大，我取1.5倍
    textImageH = int(imageH * 1.5)
    blank = Image.new("RGB", (textImageW, textImageH), "white")  # 创建用于添加文字的空白图像
    d = ImageDraw.Draw(blank)  # 创建draw对象

    if imageW < 400:
        k = 32
    elif imageW < 600:
        k = 48
    elif imageW < 800:
        k = 64
    elif imageW < 1000:
        k = 80
    elif imageW < 1200:
        k = 100
    elif imageW < 1400:
        k =128
    elif imageW < 1800:
        k= 156
    elif imageW < 2200:
        k = 192
    elif imageW < 2600:
        k = 256
    elif imageW < 3100:
        k = 300
    print ("fontsize:",k)


    Font = ImageFont.truetype("C:\Windows\Fonts\SHOWG.TTF",k)  #创建Font对象，k之为字号
    textW,textH = Font.getsize(text)            #获取文字尺寸
    d.ink = 0 + 0 * 256 + 0 * 256 * 256         #黑色
    d.text([(textImageW-textW)/2,(textImageH-textH)/2],text,font = Font)#将文字写在空白图像正中间



    #旋转文字
    textRotate = blank.rotate(30)
    #textRotate.show()



    rLen = math.sqrt((textW/2)**2+(textH/2)**2)
    oriAngle = math.atan(textH/textW)
    cropW = rLen*math.cos(oriAngle + math.pi/6) *2   #被截取区域的宽高
    cropH = rLen*math.sin(oriAngle + math.pi/6) *2
    box = [int((textImageW-cropW)/2-1),int((textImageH-cropH)/2-1)-50,int((textImageW+cropW)/2+1),int((textImageH+cropH)/2+1)]
    textIm = textRotate.crop(box)  #截取文字图片


    pasteW,pasteH = textIm.size
    #旋转后的文字图片粘贴在一个新的blank图像上
    textBlank = Image.new("RGB",(imageW,imageH),"white")
    pasteBox = (int((imageW-pasteW)/2-1),int((imageH-pasteH)/2-1))
    textBlank.paste(textIm,pasteBox)

    #图像合并，水印完成。可改变alpha值，改变水印的深浅程度
    waterImage = Image.blend(im,textBlank,0.2)
    #显示并保存
    # plt.figure("waterImage")
    # plt.imshow(waterImage)
    #plt.show()
    waterImage.save(s)