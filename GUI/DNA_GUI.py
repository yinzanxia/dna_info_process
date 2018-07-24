# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 09:38:10 2018

@author: mayn
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 09:13:56 2018

@author: mayn
"""
'''
from tkinter import *           # 导入 Tkinter 库
root = Tk()                     # 创建窗口对象的背景色
                                # 创建两个列表
li     = ['C','python','php','html','SQL','java']
movie  = ['CSS','jQuery','Bootstrap']
listb  = Listbox(root)          #  创建两个列表组件
listb2 = Listbox(root)
for item in li:                 # 第一个小部件插入数据
    listb.insert(0,item)
 
for item in movie:              # 第二个小部件插入数据
    listb2.insert(0,item)
 
listb.pack()                    # 将小部件放置到主窗口中
listb2.pack()
root.mainloop()                 # 进入消息循环

'''



#import numpy as np
import DNA_File
import DNA_Object
import tkinter
from tkinter import *
from tkinter import filedialog
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt



def selectPath():
    path_ = tkinter.filedialog.askopenfilename()
    path.set(path_)
    

 
def feedBack():
    msg = '反馈位置：'  + lb.get(lb.curselection())
    postition = '(x:' + x_input.get() + ', y:' + y_input.get() + ', z:' + z_input.get() + ', rotation:' + rotation_input.get() + ')'
    msg = msg + postition + ' success!'
    fb_label.configure(text = msg)
    feedback_pos[lb.get(lb.curselection())] = postition
    
    print(feedback_pos)
    return

'''
def drawPic():
    try:sampleCount=int(inputEntry.get())

    except:
        sampleCount=50
        print('请输入整数')
        inputEntry.delete(0,END)
        inputEntry.insert(0,'50')       

    #清空图像，以使得前后两次绘制的图像不会重叠
    drawPic.f.clf()
    drawPic.a=drawPic.f.add_subplot(111)       

    #在[0,100]范围内随机生成sampleCount个数据点
    x=np.random.randint(0,100,size=sampleCount)
    y=np.random.randint(0,100,size=sampleCount)
    color=['b','r','y','g']       

    #绘制这些随机点的散点图，颜色随机选取
    drawPic.a.scatter(x,y,s=3,color=color[np.random.randint(len(color))])
    drawPic.a.set_title('Demo: Draw N Random Dot')
    drawPic.canvas.show()
'''

def showLocation(event):
    x = event.x
    y = event.y
    locLabel.configure(text=(x,y))
    locLabel.place(height=40,width=60,x=x,y=y)
    
def onPress(event):
    #print("my pos:", event.button, event.xdata, event.ydata)
    x_input.delete(0,tkinter.END)
    x_input.insert(0,str(event.xdata))
    
    y_input.delete(0,tkinter.END)
    y_input.insert(0,str(event.ydata))
    
    dna_plt=fig.add_subplot(111)
    dna_plt.plot(event.xdata, event.ydata, '*')
    canvas.show()
  
'''
def onMotion(event):
    if event.inaxes is None:
        return
    else:
        fb_type = lb.get(lb.curselection())        
        if fb_type == '床':            
            dx = int(bed_x.get()) / 2
            dy = int(bed_y.get()) / 2
        elif fb_type == '衣柜':
            dx = int(wardrobe_x.get()) / 2
            dy = int(wardrobe_y.get()) / 2
        elif fb_type == '沙发':
            dx = int(sofa_x.get()) / 2
            dy = int(sofa_y.get()) / 2                
        elif fb_type == '餐桌':
            dx = int(table_x.get()) / 2
            dy = int(table_y.get()) / 2
        elif fb_type == '书桌':
            dx = int(desk_x.get()) / 2
            dy = int(desk_y.get()) / 2               
        else:
            dx = 0
            dy = 0          
        
        x = [event.xdata - dx, event.xdata + dx, event.xdata + dx, event.xdata - dx]
        y = [event.ydata - dy, event.ydata - dy, event.ydata + dy, event.ydata + dy]
        polygon.set_xy(list(zip(x,y)))
        event.canvas.draw()
'''
def onMotion(event):
    if event.inaxes is None:
        return
    else:  
        circ._set_radius(v.get() * 500)
        circ._set_xy([event.xdata, event.ydata])
        #circ.set_center((event.xdata, event.ydata))
        #circ.set([event.xdata, event.ydata])
        event.canvas.draw()
    
def drawDNA():
    try:        
        dna = DNA_File.load_dna_by_file_name(path.get())
        room_num, room_list = DNA_Object.get_room_list_from_dna(dna)
        door_num, door_pos = DNA_Object.get_door_list_from_dna(dna)
        window_num, window_pos = DNA_Object.get_window_list_from_dna(dna)
        wall_num, wall_pos = DNA_Object.get_wall_list_from_dna(dna)
    except:
        return
       

    #清空图像，以使得前后两次绘制的图像不会重叠
    plt.style.use('ggplot')
    fig.clf()
    dna_plt=fig.add_subplot(111)    
    
    for i in range(room_num):
        area_center, area = DNA_Object.get_room_area(room_list[i])
        dna_plt.plot(area['x'], area['y'], linewidth='0.5', color='k')      
    
    for i in range(wall_num):
        dna_plt.plot(wall_pos['x'][i], wall_pos['y'][i], alpha=0.7, color='b', linewidth=1, solid_capstyle='round', zorder=2)
        
    for i in range(window_num):
        dna_plt.plot(window_pos['x'][i], window_pos['y'][i], alpha=0.7, color='c', linewidth='0.5', solid_capstyle='round', zorder=2)
    
    for i in range(door_num):
        dna_plt.plot(door_pos['x'][i], door_pos['y'][i], alpha=0.7, color='r', linewidth='0.5', solid_capstyle='round', zorder=2)
    
    dna_plt.add_patch(circ)
    title = 'Id'+str(dna['solutionId'])
    dna_plt.set_title(title)
    #plt.xlim((-15000, 20000))
    #plt.ylim((-15000, 20000))
    canvas.show()    
   


if __name__ == '__main__':   
    matplotlib.use('TkAgg')

    root = tkinter.Tk()  

    #在Tk的GUI上放置一个画布，并用.grid()来调整布局
    fig = Figure(figsize=(7,5), dpi=100) 
    canvas = FigureCanvasTkAgg(fig, master=root)  
    canvas.show() 
    canvas.get_tk_widget().grid(row=0, columnspan=4)  
    canvas.mpl_connect('button_release_event', onPress)
    canvas.mpl_connect('motion_notify_event', onMotion)
    #polygon = plt.Polygon([[150, 150], [350, 400], [200, 600]], facecolor='g', alpha=0.5)
    #circ = mpatches.Circle((0, 0), 100, color = 'g', alpha=0.5)
    circ = mpatches.RegularPolygon((0, 0), 30, 100, color = 'g', alpha=0.5)
       

    root.bind("<Motion>", showLocation)

    #放置标签、文本框和按钮等部件，并设置文本框的默认值和按钮的事件函数      
    path = tkinter.StringVar()
    tkinter.Label(root, text='目标路径:').grid(row=1,column=0)
    tkinter.Entry(root, textvariable=path).grid(row=1,column=1)
    tkinter.Button(root,text='Json文件选择',command=selectPath).grid(row=1,column=2)   
    tkinter.Button(root,text='画图',command=drawDNA).grid(row=1,column=3,columnspan=1)
    tkinter.Label(root, text='          ').grid(row=1, column=4)
    
    fb_label = tkinter.Label(root)
    fb_label.grid(row = 2, column=0, columnspan = 4)
    
    x_label = tkinter.Label(root, text='x:')
    x_label.grid(row=3, column=0)
    x_input = tkinter.Entry(root)
    x_input.grid(row=3, column=1)
    
    y_label = tkinter.Label(root, text='y:')
    y_label.grid(row=4, column=0)
    y_input = tkinter.Entry(root)
    y_input.grid(row=4, column=1)
    
    z_label = tkinter.Label(root, text='z:')
    z_label.grid(row=5, column=0)
    z_input = tkinter.Entry(root)
    z_input.grid(row=5, column=1)
    z_input.insert(0, '0')
    
    rotation_label = tkinter.Label(root, text='rotation:')
    rotation_label.grid(row=6, column=0)
    rotation_input = tkinter.Entry(root)
    rotation_input.grid(row=6, column=1)
    rotation_input.insert(0, '0')
    
    
    feedback_btn = tkinter.Button(root, text='反馈位置', command=feedBack)
    feedback_btn.grid(row=3,column=2, rowspan=4, columnspan=4)         
    
    split_label = tkinter.Label(root)
    split_label.grid(row=7, column=0, columnspan=4)
    split_label.configure(text='--------------------------------------------------------------------------------------------------------------')
    
    
    fur_label = tkinter.Label(root, text='家具类型')
    fur_label.grid(row=8, column=0, rowspan=5)
    #scrolly=tkinter.Scrollbar(root)
    #scrolly.grid(row=7, column=1)
    
    myList = ['床', '衣柜', '沙发', '餐桌', '书桌']
    lb = tkinter.Listbox(root, selectmode = tkinter.SINGLE, height=6 )
    #lb.configure(yscrollcommand=scrolly.set)
    for item in myList:
        lb.insert(tkinter.END,item)    
    lb.select_set(0)    
    lb.grid(row=8,column=1, rowspan=5)
    #scrolly.configure(command=lb.yview)
    '''
    tkinter.Label(root, text='床尺寸x-y:').grid(row=8,column=2)
    bed_x = tkinter.Entry(root)
    bed_x.grid(row=8,column=3)
    bed_x.insert(0, '1800')
    bed_y = tkinter.Entry(root)
    bed_y.grid(row=8,column=4)
    bed_y.insert(0, '2000')

    tkinter.Label(root, text='衣柜尺寸x-y:').grid(row=9,column=2)
    wardrobe_x = tkinter.Entry(root)
    wardrobe_x.grid(row=9,column=3)
    wardrobe_x.insert(0, '600')
    wardrobe_y = tkinter.Entry(root)
    wardrobe_y.grid(row=9,column=4)
    wardrobe_y.insert(0, '2000')
    
    tkinter.Label(root, text='沙发尺寸x-y:').grid(row=10,column=2)
    sofa_x = tkinter.Entry(root)
    sofa_x.grid(row=10,column=3)
    sofa_x.insert(0, 3000)
    sofa_y = tkinter.Entry(root)
    sofa_y.grid(row=10,column=4)
    sofa_y.insert(0, 800)
    
    tkinter.Label(root, text='餐桌尺寸x-y:').grid(row=11,column=2)
    table_x = tkinter.Entry(root)
    table_x.grid(row=11,column=3)
    table_x.insert(0, 800)
    table_y = tkinter.Entry(root)
    table_y.grid(row=11,column=4)
    table_y.insert(0, 1200)
    
    tkinter.Label(root, text='书桌尺寸x-y:').grid(row=12,column=2)
    desk_x = tkinter.Entry(root)
    desk_x.grid(row=12,column=3)
    desk_x.insert(0, 1200)
    desk_y = tkinter.Entry(root)
    desk_y.grid(row=12,column=4)
    desk_y.insert(0, 700)   
    '''
    
    cursor_size = [('直径1米',1), ('直径2米',2), ('直径3米',3)]
    v = IntVar()
    v.set(1)
    b1 = tkinter.Radiobutton(root, text='直径1米', variable=v, value=1)
    b1.grid(row=8, column=2)
    b2 = tkinter.Radiobutton(root, text='直径2米', variable=v, value=2)
    b2.grid(row=9, column=2)
    b3 = tkinter.Radiobutton(root, text='直径3米', variable=v, value=3)
    b3.grid(row=10,column=2)
              
    
    locLabel = tkinter.Label(root)
    locLabel.grid(row = 9, column = 0)        
        
    
    feedback_pos = {}
    for i in range(len(myList)):
        feedback_pos[myList[i]] = ''
        
        
    

    #启动事件循环
    root.mainloop()