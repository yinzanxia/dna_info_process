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



import numpy as np

from tkinter import *

import matplotlib

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure

 

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

 

if __name__ == '__main__':    

	

	matplotlib.use('TkAgg')

	root = Tk()  

    #在Tk的GUI上放置一个画布，并用.grid()来调整布局

	drawPic.f = Figure(figsize=(5,4), dpi=100)

 

	drawPic.canvas = FigureCanvasTkAgg(drawPic.f, master=root) 

	drawPic.canvas.show() 

	drawPic.canvas.get_tk_widget().grid(row=0, columnspan=3)    

    

    #放置标签、文本框和按钮等部件，并设置文本框的默认值和按钮的事件函数

	Label(root,text='请输入样本数量：').grid(row=1,column=0)

	inputEntry=Entry(root)

	inputEntry.grid(row=1,column=1)

	inputEntry.insert(0,'50')

	Button(root,text='画图',command=drawPic).grid(row=1,column=2,columnspan=3)

       

    #启动事件循环

	root.mainloop()