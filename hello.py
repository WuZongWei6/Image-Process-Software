import tkinter as tk
import tkinter.messagebox
from PIL import Image
from PIL import ImageTk
from PIL import ImageFilter
from tkinter import filedialog
import numpy as np
import os
from PIL import ImageEnhance
import sys


#按钮功能实现
#打开图片
def open_image():
    global picture
    global picture_path
    picture_file=filedialog.askopenfilename(parent=window,initialdir="C:/",title='选择一张图片')
    picture_path=picture_file#保存路径
    picture=Image.open(picture_file)
    pic__=resize(400,300,picture)
    pic=ImageTk.PhotoImage(pic__)
    picture_label1.config(image=pic)
    picture_label1.image=pic
#灰度图
def changeToGrey():
    global picture
    global savepicture
    savepicture=picture.convert('L')
    pic__=resize(400,300,savepicture)
    pic = ImageTk.PhotoImage(pic__)
    picture_label2.config(image=pic)
    picture_label2.image = pic
#黑白图
def changeToblack():
    global picture
    global savepicture
    savepicture=picture.convert('1')
    pic__ = resize(400, 300, savepicture)
    pic = ImageTk.PhotoImage(pic__)
    picture_label2.config(image=pic)
    picture_label2.image = pic
#高斯模糊
def changeToGaos():
    global picture
    global savepicture
    temppicture=resize(400,300,picture)
    radius = 5
    pixels = np.array(temppicture)
    copyArray = np.copy(pixels)
    row = copyArray.shape[0]
    col = copyArray.shape[1]
    for i in range(radius, row - radius):
        for j in range(radius, col - radius):
            tempArray = pixels[i - radius:i + radius + 1, j - radius:j + radius + 1]
            number = (tempArray.size / 3) - 1
            average = ((tempArray.sum(axis=1).sum(axis=0)) - pixels[i][j]) / number
            copyArray[i][j][0] = average[0]
            copyArray[i][j][1] = average[1]
            copyArray[i][j][2] = average[2]
    for i in range(0, radius):  # 处理上面
        for j in range(0, col):
            if j - radius < 0:  # 特殊处理左上角右上角
                tempArray = pixels[:i + radius + 1, :j + radius + 1]
            elif j + radius > col - 1:
                tempArray = pixels[:i + radius + 1, j - radius:]
            else:
                tempArray = pixels[:i + radius + 1, j - radius:j + radius + 1]
            number = (tempArray.size / 3) - 1
            average = ((tempArray.sum(axis=1).sum(axis=0)) - pixels[i][j]) / number
            copyArray[i][j][0] = average[0]
            copyArray[i][j][1] = average[1]
            copyArray[i][j][2] = average[2]
    for i in range(row - radius - 1, row):  # 处理下面
        for j in range(0, col):
            if j - radius < 0:  # 特殊处理左下角右下角
                tempArray = pixels[i - radius:, :j + radius + 1]
            elif j + radius > col - 1:
                tempArray = pixels[i - radius:, j - radius:]
            else:
                tempArray = pixels[i - radius:, j - radius:j + radius + 1]
            number = (tempArray.size / 3) - 1
            average = ((tempArray.sum(axis=1).sum(axis=0)) - pixels[i][j]) / number
            copyArray[i][j][0] = average[0]
            copyArray[i][j][1] = average[1]
            copyArray[i][j][2] = average[2]
    for i in range(radius, row - radius):
        for j in range(0, radius):  # 处理左边
            tempArray = pixels[i - radius:i + radius + 1, :j + radius + 1]
            number = (tempArray.size / 3) - 1
            average = ((tempArray.sum(axis=1).sum(axis=0)) - pixels[i][j]) / number
            copyArray[i][j][0] = average[0]
            copyArray[i][j][1] = average[1]
            copyArray[i][j][2] = average[2]
        for k in range(col - radius, col):  # 处理右边
            tempArray = pixels[i - radius:i + radius + 1, k - radius:]
            number = (tempArray.size / 3) - 1
            average = ((tempArray.sum(axis=1).sum(axis=0)) - pixels[i][k]) / number
            copyArray[i][k][0] = average[0]
            copyArray[i][k][1] = average[1]
            copyArray[i][k][2] = average[2]
    savepicture=Image.fromarray(copyArray)
    pic__ = resize(400, 300, savepicture)
    pic = ImageTk.PhotoImage(pic__)
    picture_label2.config(image=pic)
    picture_label2.image = pic
#手绘图
def changeToShouhui():
    global picture
    global savepicture
    temppicture=resize(300,200,picture)
    new=Image.new("L",temppicture.size,255)
    width, height = temppicture.size
    img = temppicture.convert("L")
    # 定义画笔的大小
    Pen_size = 3
    # 色差扩散器
    Color_Diff = 6
    for i in range(Pen_size + 1, width - Pen_size - 1):
        for j in range(Pen_size + 1, height - Pen_size - 1):
            # 原始的颜色
            originalColor = 255
            lcolor = sum([img.getpixel((i - r, j)) for r in range(Pen_size)]) // Pen_size
            rcolor = sum([img.getpixel((i + r, j)) for r in range(Pen_size)]) // Pen_size

            # 通道----颜料
            if abs(lcolor - rcolor) > Color_Diff:
                originalColor -= (255 - img.getpixel((i, j))) // 4
                new.putpixel((i, j), originalColor)

            ucolor = sum([img.getpixel((i, j - r)) for r in range(Pen_size)]) // Pen_size
            dcolor = sum([img.getpixel((i, j + r)) for r in range(Pen_size)]) // Pen_size

            # 通道----颜料
            if abs(ucolor - dcolor) > Color_Diff:
                originalColor -= (255 - img.getpixel((i, j))) // 4
                new.putpixel((i, j), originalColor)

            acolor = sum([img.getpixel((i - r, j - r)) for r in range(Pen_size)]) // Pen_size
            bcolor = sum([img.getpixel((i + r, j + r)) for r in range(Pen_size)]) // Pen_size

            # 通道----颜料
            if abs(acolor - bcolor) > Color_Diff:
                originalColor -= (255 - img.getpixel((i, j))) // 4
                new.putpixel((i, j), originalColor)

            qcolor = sum([img.getpixel((i + r, j - r)) for r in range(Pen_size)]) // Pen_size
            wcolor = sum([img.getpixel((i - r, j + r)) for r in range(Pen_size)]) // Pen_size

            # 通道----颜料
            if abs(qcolor - wcolor) > Color_Diff:
                originalColor -= (255 - img.getpixel((i, j))) // 4
                new.putpixel((i, j), originalColor)
    print(new.getchannel())
    savepicture=new
    pic__ = resize(400, 300, savepicture)
    pic = ImageTk.PhotoImage(pic__)
    picture_label2.config(image=pic)
    picture_label2.image = pic
#轮廓图
def changeToLunkuo():
    global picture
    global savepicture
    savepicture=picture.filter(ImageFilter.CONTOUR)
    pic__ = resize(400, 300, savepicture)
    pic = ImageTk.PhotoImage(pic__)
    picture_label2.config(image=pic)
    picture_label2.image = pic
#深度边缘加强
def changeToEdge():
    global picture
    global savepicture
    savepicture = picture.filter(ImageFilter.EDGE_ENHANCE_MORE)
    pic__ = resize(400, 300, savepicture)
    pic = ImageTk.PhotoImage(pic__)
    picture_label2.config(image=pic)
    picture_label2.image = pic
#浮雕图
def changeToFudiao():
    global picture
    global savepicture
    savepicture = picture.filter(ImageFilter.EMBOSS)
    pic__ = resize(400, 300, savepicture)
    pic = ImageTk.PhotoImage(pic__)
    picture_label2.config(image=pic)
    picture_label2.image = pic
#RGB通道交换
def changeRGB():
    global picture
    global savepicture
    get1=R_entry1.get()
    get2=B_entry1.get()
    get3=G_entry1.get()
    if get1=="" or get2=="" or get3=="":
        tk.messagebox.showinfo("警告", "请按一定的顺序输入字母rgb！")
        return
    if get1==get2 or get1==get3 or get2==get3:
        tk.messagebox.showinfo("警告", "rgb字母请勿重复！")
        return
    if get1!='r' and get1!='R' and get1!='g' and get1!='G' and get1!='b' and get1!='B':
        tk.messagebox.showinfo("警告","请按一定的顺序输入字母rgb！")
        return
    if get2!='r' and get2!='R' and get2!='g' and get2!='G' and get2!='b' and get2!='B':
        tk.messagebox.showinfo("警告","请按一定的顺序输入字母rgb！")
        return
    if get3!='r' and get3!='R' and get3!='g' and get3!='G' and get3!='b' and get3!='B':
        tk.messagebox.showinfo("警告","请按一定的顺序输入字母rgb！")
        return
    r,g,b=picture.split()

    if (get1=='r' and get2=='g' and get3=='b') or (get1=='R' and get2=='G' and get3=='B'):
        savepicture = Image.merge("RGB", (r, g, b))
    elif (get1=='r' and get2=='b' and get3=='g') or (get1=='R' and get2=='B' and get3=='G'):
        savepicture = Image.merge("RGB", (r, b, g))
    elif (get1=='g' and get2=='r' and get3=='b') or (get1=='G' and get2=='R' and get3=='B'):
        savepicture = Image.merge("RGB", (g, r, b))
    elif (get1=='b' and get2=='r' and get3=='g') or (get1=='B' and get2=='R' and get3=='G'):
        savepicture = Image.merge("RGB", (b, r, g))
    elif (get1=='g' and get2=='b' and get3=='r') or (get1=='G' and get2=='B' and get3=='R'):
        savepicture = Image.merge("RGB", (g, b, r))
    else:
        savepicture = Image.merge("RGB", (b, g, r))
    pic__ = resize(400, 300, savepicture)
    pic = ImageTk.PhotoImage(pic__)
    picture_label2.config(image=pic)
    picture_label2.image = pic
#九宫格图片
def divide():
    image = picture.copy()
    #将图片填充为正方形
    width, height = image.size
    new_image_length = width if width > height else height
    # 生成新图片[白底]
    new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
    if width > height:#原图宽大于高，则填充图片的竖直维度  #(x,y)二元组表示粘贴上图相对下图的起始位置,是个坐标点。
        new_image.paste(image, (0, int((new_image_length - height) / 2)))
    else:
        new_image.paste(image, (int((new_image_length - width) / 2), 0))
    image = new_image
    #分割图片
    width, height = image.size
    item_width = int(width / 3)
    box_list = []
    # (left, upper, right, lower)
    for i in range(0, 3):
        for j in range(0, 3):
            # print((i*item_width,j*item_width,(i+1)*item_width,(j+1)*item_width))
            box = (j * item_width, i * item_width, (j + 1) * item_width, (i + 1) * item_width)
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    index = 1
    #保存图片
    for img in image_list:
        #if not os.path.exists("D:\\pictures"):
        #    os.mkdir("D:\\pictures")
        name=os.path.splitext(os.path.basename(picture_path))[0]
        img.save(os.path.join(os.getcwd(), name+str(index) + '.png'), 'PNG')
        index += 1
    #tk.messagebox.showinfo(title="提示",message="九宫格图片已保存在程序当前路径下！")
    tk.messagebox.showinfo("提示","九宫格图片已保存在当前程序路径下！")
#RGB倍数
def changeRGBsize():
    global picture
    global savepicture
    get1 = R_entry2.get()
    get2 = B_entry2.get()
    get3 = G_entry2.get()
    if get1 == "" or get2 == "" or get3 == "":
        tk.messagebox.showinfo("警告", "请输入rgb改变倍数")
        return
    if (type(eval(get1))!=int and type(eval(get1))!=float )or(type(eval(get2))!=int and type(eval(get2))!=float)or(type(eval(get3))!=int and type(eval(get3))!=float):
        tk.messagebox.showinfo("警告", "请输入正确的数字！")
        return
    get1=float(get1)
    get2=float(get2)
    get3=float(get3)
    r,g,b=picture.split()
    newr=r.point(lambda i:i*get1)
    newg=g.point(lambda i:i*get2)
    newb=b.point(lambda i:i*get3)
    savepicture=Image.merge("RGB",(newr,newg,newb))
    pic__ = resize(400, 300, savepicture)
    pic = ImageTk.PhotoImage(pic__)
    picture_label2.config(image=pic)
    picture_label2.image = pic
#保存图片
def save_result():
    global savepicture
    getx_string = tk.StringVar()
    gety_string = tk.StringVar()
    def save_afterresult():
        getx=getx_entry.get()
        gety=gety_entry.get()
        if getx=="" or gety=="":
            tk.messagebox.showinfo("警告", "请输入保存的尺寸！")
            return
        if not getx.isdigit() or not gety.isdigit() :
            tk.messagebox.showinfo("警告", "请输入正确的数字！")
            return
        getx=int(getx)
        gety=int(gety)
        fname = tkinter.filedialog.asksaveasfilename(title="保存图片", filetypes=[("PNG", ".png")])
        temppicture=resize(int(getx),int(gety),savepicture)
        temppicture.save(str(fname) + '.png', 'PNG')
        size_window.destroy()
        return
    size_window=tk.Toplevel(window)
    size_window.geometry("350x80+800+400")
    size_window.title("请输入处理后图片保存的尺寸")
    size_window.resizable(width=False, height=False)

    size_window.grab_set()

    x_label=tk.Label(size_window,text="请输入长度x：")
    y_label=tk.Label(size_window,text="请输入宽度y：")
    x_label.place(x=5,y=15,anchor='nw')
    y_label.place(x=5,y=45,anchor='nw')
    getx_entry=tk.Entry(size_window,textvariable=getx_string,width=20)
    getx_entry.place(x=90,y=15,anchor='nw')
    gety_entry=tk.Entry(size_window,textvariable=gety_string,width=20)
    gety_entry.place(x=90,y=45,anchor='nw' )

    getsize_button=tk.Button(size_window,text='保存图片',height=2,width=8,
                             font=("华文彩云",16),fg='red',command=save_afterresult)
    getsize_button.place(x=240,y=10,anchor='nw')

#原图
def changeToOriginal():
    global picture
    global savepicture
    savepicture=picture.copy()
    pic__ = resize(400, 300, savepicture)
    pic = ImageTk.PhotoImage(pic__)
    picture_label2.config(image=pic)
    picture_label2.image = pic
#亮度调整
def changeLiangdu(num):
    global picture
    global savepicture
    enh_bri = ImageEnhance.Brightness(picture)
    beishu=float(num)
    savepicture=enh_bri.enhance(beishu)
    pic__ = resize(400, 300, savepicture)
    pic = ImageTk.PhotoImage(pic__)
    picture_label2.config(image=pic)
    picture_label2.image = pic
#对比度调整
def changeDuibi(num):
    global picture
    global savepicture
    enh_con = ImageEnhance.Contrast(picture)
    beishu = float(num)
    savepicture = enh_con.enhance(beishu)
    pic__ = resize(400, 300, savepicture)
    pic = ImageTk.PhotoImage(pic__)
    picture_label2.config(image=pic)
    picture_label2.image = pic
#锐度调整
def changeRuidu(num):
    global picture
    global savepicture
    enh_sha=ImageEnhance.Sharpness(picture)
    beishu=float(num)
    savepicture=enh_sha.enhance(beishu)
    pic__ = resize(400, 300, savepicture)
    pic = ImageTk.PhotoImage(pic__)
    picture_label2.config(image=pic)
    picture_label2.image = pic
#色度调整
def changeSedu(num):
    global picture
    global savepicture
    enh_col = ImageEnhance.Color(picture)
    beishu = float(num)
    savepicture = enh_col.enhance(beishu)
    pic__ = resize(400, 300, savepicture)
    pic = ImageTk.PhotoImage(pic__)
    picture_label2.config(image=pic)
    picture_label2.image = pic


#按钮功能实现


#大小变换
def resize(w_box,h_box,pil_image):
    w,h=pil_image.size
    f1=1.0*w_box/w
    f2=1.0*h_box/h
    factor=min([f1,f2])
    width=int(w*factor)
    height=int(h*factor)
    return pil_image.resize((width,height),Image.ANTIALIAS)



if __name__=="__main__":
    picture_path = os.getcwd() + "\\资源文件(勿删！)\\img.png"
    # picture_path="C:\\Users\\WZW\\Desktop\\homework\\Python\\picture_pro\\img.png"
    savepicture = Image.open(os.getcwd() + "\\资源文件(勿删！)\\imgresult.png")
    # savepicture=Image.open("C:\\Users\\WZW\\Desktop\\homework\\Python\\picture_pro\\imgresult.png")
    picture = Image.open(os.getcwd() + "\\资源文件(勿删！)\\img.png")
    # picture=Image.open("C:\\Users\\WZW\\Desktop\\homework\\Python\\picture_pro\\img.png")

    window=tk.Tk()
    window.title("图片处理软件")
    window.configure(background='white')
    window.resizable(width=False,height=False)
    window.geometry("1000x600+400+200")

    canvas=tk.Canvas(window,bg='white',height=600,width=1000)
    canvas.place(x=0,y=0,anchor="nw")
    im=Image.open(os.getcwd()+"\\资源文件(勿删！)\\decorate1.gif")
    #im=Image.open("C:\\Users\\WZW\\Desktop\\homework\\Python\\picture_pro\\decorate1.gif")
    resizeim=resize(1500,780,im)
    image_file=ImageTk.PhotoImage(resizeim)
    image=canvas.create_image(0,-180,anchor='nw',image=image_file)

    rect0=canvas.create_rectangle(5,320,5+220,295+260)
    rect1=canvas.create_rectangle(240,320,170+265,295+260)
    rect2=canvas.create_rectangle(450,320,370+440,295+260)
    rect21=canvas.create_rectangle(520,335,550+250,305+125)
    rect22=canvas.create_rectangle(520,445,550+250,405+135)
    rect3=canvas.create_rectangle(825,320,825+153,295+260)
    #装饰背景

    #打开按钮和保存按钮
    open_button=tk.Button(window,text='打开图片',width=13,height=2,relief='groove',
                      command=open_image)
    open_button.place(x=30,y=30,anchor='nw')#open_picture要定义

    save_button=tk.Button(window,text='保存图片',width=13,height=2,relief='groove',command=save_result)
    save_button.place(x=30,y=90,anchor='nw')#save_picture要定义

    original_button=tk.Button(window,text="原图",width=13,height=2,relief='groove',command=changeToOriginal)
    original_button.place(x=30,y=150,anchor='nw')
    #打开和保存按钮

    #最左边一列按钮
    text1=tk.Label(window,height=2,width=8,text='常规处理',fg='light green',
                   bg='dark green',font='Helvetica 14 bold italic')
    text1.place(x=290,y=335,anchor='nw')
    grey_button=tk.Button(window,height=2,width=10,text="灰度图",relief='solid',command=changeToGrey)
    grey_button.place(x=255,y=395,anchor='nw')
    black_button=tk.Button(window,height=2,width=10,text="黑白图",relief='solid',command=changeToblack)
    black_button.place(x=255,y=445,anchor='nw')
    gaos_button=tk.Button(window,height=2,width=10,text="高斯模糊",relief='solid',command=changeToGaos
                      )
    gaos_button.place(x=255,y=495,anchor='nw')
    lunkuo_button=tk.Button(window,height=2,width=10,text="轮廓图",relief='solid',command=changeToLunkuo)
    lunkuo_button.place(x=342,y=395,anchor='nw')
    edge_button=tk.Button(window,height=2,width=10,text="深度边缘增强",relief='solid',command=changeToEdge)
    edge_button.place(x=342,y=445,anchor='nw')
    fudiao_button=tk.Button(window,height=2,width=10,text="浮雕图",relief='solid',command=changeToFudiao)
    fudiao_button.place(x=342,y=495,anchor='nw')
    #最左边一列按钮

    #中间按钮
    text2=tk.Label(window,height=10,width=5,text='R\nG\nB\n处\n理\n',fg='light green',
                   bg='dark green',font="Helvetica 12 bold italic")
    text2.place(x=458,y=345,anchor='nw')
    R_string1=tk.StringVar()
    G_string1=tk.StringVar()
    B_string1=tk.StringVar()
    text21=tk.Label(window,height=3,width=15,text='请输入RGB通道顺\n序再进行通道交换',
                    bg='red',font="Verdana 10 bold")
    text21.place(x=530,y=355,anchor='nw')
    R_entry1=tk.Entry(window,width=5,textvariable=R_string1)
    R_entry1.place(x=675,y=350,anchor='nw')
    G_entry1=tk.Entry(window,width=5,textvariable=G_string1)
    G_entry1.place(x=715,y=350,anchor='nw')
    B_entry1=tk.Entry(window,width=5,textvariable=B_string1)
    B_entry1.place(x=755,y=350,anchor='nw')
    rgb_button1=tk.Button(window,height=2,width=10,text='RGB通道交换',relief='solid',command=changeRGB)
    rgb_button1.place(x=695,y=377,anchor='nw')
    #下方
    R_string2=tk.StringVar()
    G_string2=tk.StringVar()
    B_string2=tk.StringVar()
    text22=tk.Label(window,height=3,width=15,text='请输入RGB各通道\n放大倍数再进行修改',
                    bg='red',font="Verdana 10 bold")
    text22.place(x=530,y=465,anchor='nw')
    R_entry2=tk.Entry(window,width=5,textvariable=R_string2)
    R_entry2.place(x=675,y=460,anchor='nw')
    G_entry2=tk.Entry(window,width=5,textvariable=G_string2)
    G_entry2.place(x=715,y=460,anchor='nw')
    B_entry2=tk.Entry(window,width=5,textvariable=B_string2)
    B_entry2.place(x=755,y=460,anchor='nw')
    rgb_button2=tk.Button(window,height=2,width=10,text='RGB倍数修改',relief='solid',command=changeRGBsize)
    rgb_button2.place(x=695,y=487,anchor='nw')
    #中间按钮
    #最右边按钮
    text3=tk.Label(window,height=2,width=8,text='特效处理',fg='light green',
                     bg='dark green',font='Helvetica 14 bold italic')
    text3.place(x=850,y=340,anchor='nw')

    shouhui_button=tk.Button(window,height=2,width=10,text="手绘素描图",relief='solid'
                          ,command=changeToShouhui)
    shouhui_button.place(x=860,y=415,anchor='nw')

    jiugongge_button=tk.Button(window,height=2,width=10,text="九宫格",relief='solid',
                          command=divide)
    jiugongge_button.place(x=860,y=480,anchor='nw')
    #最右边按钮
    #亮度对比度
    scale_text=tk.Label(window,height=2,width=8,text='图片调整',fg='light green',
               bg='dark green',font='Helvetica 14 bold italic')
    scale_text.place(x=70,y=335,anchor='nw')

    liangdu_scale=tk.Scale(window,label="亮度(倍数)",from_=0,to=20,orient=tk.HORIZONTAL,
                           length=95,showvalue=1,command=changeLiangdu)
    liangdu_scale.place(x=10,y=400,anchor='nw')

    duibi_scale=tk.Scale(window,label="对比度（倍数）",from_=-20,to=20,orient=tk.HORIZONTAL,
                           length=95,showvalue=1,command=changeDuibi)
    duibi_scale.place(x=118,y=400,anchor='nw')

    ruidu_scale=tk.Scale(window,label="锐度（倍数）",from_=0,to=20,orient=tk.HORIZONTAL,
                       length=95,showvalue=1,command=changeRuidu)
    ruidu_scale.place(x=10,y=475,anchor='nw')

    sedu_scale=tk.Scale(window,label="色度（倍数）",from_=-20,to=20,orient=tk.HORIZONTAL,
                       length=95,showvalue=1,command=changeSedu)
    sedu_scale.place(x=118,y=475,anchor='nw')
    #亮度对比度



    #放置图片
    frame=tk.Frame(window,width=900,height=290,bg='white')
    frame.place(x=160,y=0,anchor='nw')
    im1=Image.open(os.getcwd()+"\\资源文件(勿删！)\\img.png")
    #im1=Image.open("C:\\Users\\WZW\\Desktop\\homework\\Python\\picture_pro\\img.png")
    #im1.thumbnail((400,400))
    im1resize=resize(400,300,im1)
    img1=ImageTk.PhotoImage(im1resize)

    im2=Image.open(os.getcwd()+"\\资源文件(勿删！)\\imgresult.png")
    #im2=Image.open("C:\\Users\\WZW\\Desktop\\homework\\Python\\picture_pro\\imgresult.png")
    im2resize=resize(400,300,im2)
    img2=ImageTk.PhotoImage(im2resize)
    #两个放置图片的Label
    picture_label1=tk.Label(frame,image=img1)
    picture_label1.place(x=0,y=0,anchor='nw')
    picture_label2=tk.Label(frame,image=img2)
    picture_label2.place(x=420,y=0,anchor='nw')

    #两个放置图片的Label

    window.mainloop()
