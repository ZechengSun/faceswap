import tkinter.filedialog
from faceswap import *
from watermark import *
#from screenshot import *
from tkinter.simpledialog import *
import os
import tkinter
import tkinter.messagebox
from PIL import Image, ImageTk
import threading

#存放图片绝对路径
a=[]
b=[]



def update_now():
    try:
        os.system('update.exe')
    except:
        pass

def restart():
    del a[:],b[:]
    save_btn.config(state=tkinter.DISABLED)

    pics(".\\logo\\add.png", 0)
    pics(".\\logo\\add.png", 1)
    pics(".\\logo\\Ely.png", 2)


    lb.config(text='Welcome to faceswap')
    try:
        os.remove("output.jpg")
    except:
        return 0

# #当前文件夹下是否存在output.jpg
# def exist_output():
#     for root, dirs, files in os.walk(".", topdown=False):
#         for name in files:
#             b.append(os.path.join(root, name))
#         for name in dirs:
#             b.append(os.path.join(root, name))
#     j=0
#     for i in b:
#         if (i == '.\\output.jpg'):
#            j+=1
#     return j


def default():
    s = askstring('请输入合成图片的名称', '图片名称(.png)：')
    if s != None:
        if s != "":
            watermark("output.jpg", "Ely's work", ".\\result\\" + str(s) + ".jpg")
              # img=Image.open("output.jpg")
              # logo=Image.open("logo1.png")
              # #图层
              # layer=Image.new('RGBA',img.size,(255,255,255,0))
              # layer.paste(logo,(img.size[0]-logo.size[0],img.size[1]-logo.size[1]))
              # #覆盖
              # img_after=Image.composite(layer,img,layer)

            lb.config(text='保存在result文件夹下')
        else:
            lb.config(text='名字为空，保存失败！')
    else:
        lb.config(text='保存失败！')



def diy():
    default_dir = r".\\"
    try:
        fname = tkinter.filedialog.asksaveasfilename(title=u'保存文件',\
                                                     initialdir=(os.path.expanduser(default_dir)), \
                                                     filetypes=[("JPG", ".jpg")])
        watermark("output.jpg", "Ely's work",str(fname) + '.jpg')
        lb.config(text='保存成功！')
    except :
        return 0

#按键“save”逻辑,保存output.jpg
def save():
    if CheckVar1.get()==1:
        diy()
    else:
        default()


#创建Image对象并进行缩放
def pics(pic,i):
        # 图像处理
        # 创建Image对象并进行缩放
        im = Image.open(pic)
        w, h = im.size
        # 这里假设用来显示图片的Label组件尺寸为400*600
        if w > 400:
            h = int(h * 400 / w)
            w = 400
        if h > 600:
            w = int(w * 600 / h)
            h = 600

        im = im.resize((w,h))
        # 创建PhotoImage对象，并设置Label组件图片
        im1 = ImageTk.PhotoImage(im)

        if i==0:

            lbPic1['image'] = im1
            lbPic1.image = im1

        elif i==1:

            lbPic2['image'] = im1
            lbPic2.image = im1

        elif i==2:

            lbPic3['image'] = im1
            lbPic3.image = im1

def xz(num):
    filename = tkinter.filedialog.askopenfilename(title='请选择头部图片', \
                                                   filetypes=[("PNG", ".png"), ("JPG", ".jpg")])
    if filename != '':
        if num==0:
            del a[:]
            a.append(filename)
        else:
            del b[:]
            b.append(filename)
        pics(filename, num)


    else:
        lb.config(text='您没有选择任何图片')

    if len(a)&len(b)==1:

        try:
            main(a[0], b[0])
        except:
            r = messagebox.showerror('提示', '请更换未识别到人脸的图片')
            print('showerror:', r)
        else:
            pics("output.jpg", 2)
            save_btn.config(state=tkinter.NORMAL)
            lb.config(text='点击save保存换脸图')


def play1(event):
    if event.x & event.y >=0:
        xz(0)

def play2(event):
    if event.x & event.y >=0:
        xz(1)

def tips1(event):
    if event.x & event.y >=0:
        lb.config(text='点击"+"选择头部')

def tips2(event):
    if event.x & event.y >= 0:
        lb.config(text='点击"+"选择脸部')

# def tips3(event):
#     if event.x & event.y >= 0:
#         lb.config(text='点击"restart"清空数据')

def tips4(event):
    if event.x & event.y >= 0:
        lb.config(text='点击"save"保存换脸图')


t=threading.Thread(target=update_now,args=())
t.start()
# 创建tkinter应用程序窗口
root = Tk()


# 设置窗口大小和位置
root.geometry('430x800+40+30')
# 不允许改变窗口大小
root.resizable(False, False)
# 设置窗口标题
root.title('faceswap2.0')

x=Frame(bg = "#FFB6C1")
x.place(x=0, y=0, width=1000, height=1000)

# 用来显示图片的Label组件
lbPic1 = tkinter.Label(root, bg = "#F08080",text='head', width=100, height=0)
lbPic1.bind('<Enter>',tips1)
lbPic1.bind('<Button-1>',play1)
lbPic1.focus_set()
lbPic1.place(x=50, y=110, width=300, height=200)

lbPic2 = tkinter.Label(root,bg = "#F08080", text='face', width=100, height=0)
lbPic2.bind('<Enter>',tips2)
lbPic2.bind('<Button-1>',play2)
lbPic2.focus_set()
lbPic2.place(x=50, y=320, width=300, height=200)

lbPic3 = tkinter.Label(root, bg = "#FFB6C1",text='result', width=100, height=0)
lbPic3.place(x=50, y=530, width=300, height=200)



#设置欢迎标签  #d3fbfb
lb = Label(root,text='Welcome to faceswap',\
        bg='#ff6481',\
        fg='blue',\
        font=('华文新魏',32),\
        width=20,\
        height=2,\
        relief=SUNKEN)
lb.pack()

#设置作者标签
lbl=Label(root,bg = "#FFB6C1",text='作者：孙泽程\n联系方式：956149535@qq.com\n有建议、合作或借鉴可联系我，不可侵权')
lbl.place(relx=0,rely=0.92,relwidth=1,relheight=0.1)



# #设置restart按钮
# add_btn= Button(root, bg = "#FFB6C1",text='restart',\
#                       command=lambda:restart() )
# add_btn.bind('<Enter>',tips3)
# add_btn.focus_set()
# add_btn.place(x=360, y=350, width=50, height=30)

#设置保存按钮
save_btn=Button(root,bg = "#FFB6C1", text='save',\
             command=lambda:save(),\
             fg="red",\
             )
save_btn.bind('<Enter>',tips4)
save_btn.focus_set()
save_btn.place(x=360, y=450, width=50, height=30)
#打勾选择
CheckVar1 = IntVar()
ch1 = Checkbutton(root,bg = "#FFB6C1",text='自定义\n保存',variable = CheckVar1,onvalue=1,offvalue=0)
ch1.place(x=360, y=480)

mainmenu = Menu(root)
menuFile = Menu(mainmenu)  # 菜单分组 menuFile
mainmenu.add_cascade(label="menu",menu=menuFile)
# menuFile.add_command(label="新建",command=new)
menuFile.add_command(label="check for updates",command=update_now)
#menuFile.add_command(label="screenshot",command=window_capture("window_capture.jpg"))
menuFile.add_command(label="restart",command=restart)
menuFile.add_separator()  # 分割线
menuFile.add_command(label="quit",command=root.destroy)

root.config(menu=mainmenu)
def popupmenu(event):
    mainmenu.post(event.x_root, event.y_root)
root.bind('Button-3',popupmenu) # 根窗体绑定鼠标右击响应事件

restart()

# # 启动消息主循环
root.mainloop()