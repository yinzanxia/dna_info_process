# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 10:54:40 2018

@author: mayn
"""

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

import numpy as np
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as msgbox
from tkinter import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import requests
import json
import RoomResponse


'''请求批量Room列表'''    
def requestRoomList():
    my_url = 'http://'+ host_ip.get() + '/ai/room/feedback/list?page='+page_idx_entry.get()+'&limit='+page_size_entry.get()
    try:
        '''请求Room列表'''
        resp = requests.get(my_url)
        #print(resp.status_code, resp.url, resp.text)
        resp_text = json.loads(resp.text)
        if RoomResponse.isResponseOK(resp_text) == False:
            err_code = "Code[%d]" % resp_text["code"]
            err_msg = "请求["+my_url+"]失败！"+err_code+" 请检查IP地址，确保服务端已启动！"
            msgbox.showerror("Error", err_msg)
            return 
        
        
        '''解析Room列表'''
        room_list = RoomResponse.getRoomListFromResponse(resp_text)
        
        
        '''刷新界面中列表组件显示内容'''
        room_fb_flag.clear()
        room_lb.delete(0, tkinter.END) #删除列表中所有记录       
        for item in room_list:
            room_lb.insert(tkinter.END, item["id"])  
            room_fb_flag[item["id"]] = False
        room_lb.select_set(0)  
        
        
        next_page_idx = int(page_idx_entry.get()) + 1
        page_idx_entry.delete(0, tkinter.END)
        page_idx_entry.insert(0, str(next_page_idx))
        msgbox.showinfo("Info", "Room请求成功!")
    except:
        err_msg = "请求Room列表失败！"
        msgbox.showerror("Error", err_msg)
        return
    

'''检查列表中是否有room被选中'''     
def isRoomListSelected(room_lb):
    flag = False
    for i in range(room_lb.size()):
        if (room_lb.selection_includes(i)):
            flag = True
            break
    return flag


'''获取选中的Room的详细信息 ''' 
def getRoomInfo():
    global response_text
    if isRoomListSelected(room_lb) == False:
        msgbox.showerror("Error", "请批量导入Room列表并选中一个Room!")
    else:
        cur_id = room_lb.get(room_lb.curselection())
        my_url = 'http://'+ host_ip.get() + '/ai/room/feedback/detail?id='+str(cur_id)
        try:
            
            '''请求数据'''
            resp = requests.get(my_url)
            response_text = json.loads(resp.text)
            #print(response_text)
            if RoomResponse.isResponseOK(response_text) == False:
                err_code = "Code[%d]" % response_text["code"]
                err_msg = "请求["+my_url+"]失败！"+err_code+" 请检查IP地址，确保服务端已启动！"
                msgbox.showerror("Error", err_msg)
                return 
            
            '''解析数据'''
            show_text = RoomResponse.getRoomDetailShowInfo(response_text)
            cur_room_info_label.configure(text=show_text)
            drawDNA(response_text)
            
            '''重置位置信息'''
            fur_option.current(0)
            x_input.delete(0, END)
            x_input.insert(0, '0')
            y_input.delete(0, END)
            y_input.insert(0, '0')
            
            msgbox.showinfo("Info", "获取Room详细信息成功!")
        except:
            err_msg = "获取Room详细信息失败！"
            msgbox.showerror("Error", err_msg)
        
    
'''反馈家具位置按钮回调函数'''
def feedBack():
    global response_text
    if  fur_option.get() == '-1':
        msgbox.showerror("Error", "请选择正确的家具类型ID!")
        return
    else:   
        cur_id = RoomResponse.getIdFromShowText(cur_room_info_label["text"])       
        cur_id_num = int(cur_id[3:])
        msg = cur_id + '反馈位置： [category'  + fur_option.get() +'] '
        postition = '(x:' + x_input.get() + ', y:' + y_input.get() + ', z:' + z_input.get() + ', rotation:' + rotation_input.get() + ')'
        msg = msg + postition + ' success!'
        #feedback_pos[fur_input.get()] = postition      
        room_fb_flag[cur_id_num] = True
        #my_feedback = RoomResponse.deepCopyResponseText(response_text)
        my_child = {}
        my_child[fur_option.get()] = {}
        my_child[fur_option.get()]['x'] = x_input.get()
        my_child[fur_option.get()]['y'] = y_input.get()
        my_child[fur_option.get()]['z'] = z_input.get()
        my_child[fur_option.get()]['rotation'] = rotation_input.get()
        RoomResponse.encodeFeedBack(response_text, my_child)
        print(response_text)
        msgbox.showinfo("Info", msg)
        return

def showFeedBackList():
    msg = ''
    for ikey, flag in room_fb_flag.items():
        msg = msg + str(ikey)
        if flag == True:
            msg += ': Finished\n'
        else:
            msg += ': ToDo\n'
    print(msg)
    msgbox.showinfo("Info", msg)


def onPress(event):
    #print("my pos:", event.button, event.xdata, event.ydata)
    x_input.delete(0,tkinter.END)
    x_input.insert(0,str(event.xdata))
    
    y_input.delete(0,tkinter.END)
    y_input.insert(0,str(event.ydata))
    
    dna_plt=fig.add_subplot(111)
    dna_plt.plot(event.xdata, event.ydata, '*')
    canvas.show()
  

def onMotion(event):
    if event.inaxes is None:        
        return
    else:  
        
        cur_str = d_radius_option.get()        
        start_idx = cur_str.find("直径") + len("直径")
        end_idx = cur_str.find("米")
        number = float(cur_str[start_idx:end_idx])
        circ._set_radius(number * 500)
        circ._set_xy([event.xdata, event.ydata])
        event.canvas.draw()
        
        return
    
def drawDNA(response_text):
    try:      
        door_num, door_pos = RoomResponse.getDoorInfoFromRoom(response_text)
        shape_point_num, shape_pos = RoomResponse.getWallShapeInfoFromRoom(response_text, "shapes")
        wall_num, wall_pos = RoomResponse.getWallShapeInfoFromRoom(response_text, "walls")
        window_num, window_pos = RoomResponse.getWindowInfoFromRoom(response_text)
        #print(window_num, window_pos)
        
    except:
        msgbox.showerror("Error", "绘图失败!")
        return       
    

    #清空图像，以使得前后两次绘制的图像不会重叠
    plt.style.use('ggplot')       
    
    '''
    if len(fig.axes) > 0:
        tmp = fig.axes[0]
        #print('hello1',fig.axes, tmp.patches)
        if len(tmp.patches) > 0:
            tmp.patches[0].remove()            
    '''    
    #fig.clf()     
    #dna_plt=fig.add_subplot(111)
    
    dna_plt.clear()      
        
    #print(shape_pos)
    
    dna_plt.plot(shape_pos['x'], shape_pos['y'], linewidth='0.5', color='k')  
    dna_plt.plot(wall_pos['x'], wall_pos['y'], linewidth='0.5', color='b')   
    
    for i in range(window_num):
        #print(window_pos['x'][i])
        dna_plt.plot(window_pos['x'][i], window_pos['y'][i], alpha=0.7, color='g', linewidth='0.8', solid_capstyle='round', zorder=2)
    for i in range(door_num):           
        dna_plt.plot(door_pos['x'][i], door_pos['y'][i], alpha=0.7, color='r', linewidth='0.8', solid_capstyle='round', zorder=2)
   
    #dna_plt.xlim((-5000, 5000))
    #dna_plt.ylim((-5000, 5000))    
    dna_plt.add_patch(circ)
    #print("hello2", fig.axes, fig.axes[0].patches)
    #dna_plt.remove(circ)    
    #cursor = Cursor(dna_plt, useblit=True, color='r', linewidth=2)
    canvas.show() 


if __name__ == '__main__':   
    matplotlib.use('TkAgg')

    root = tkinter.Tk()  
    
    #room列表部件
    tkinter.Label(root, text='Room列表:').grid(row=0,column=0)
    room_list = []
    room_lb = tkinter.Listbox(root, selectmode = tkinter.SINGLE, height=20 )
    #lb.configure(yscrollcommand=scrolly.set)
    for item in room_list:
        room_lb.insert(tkinter.END,item)    
    room_lb.select_set(0)    
    room_lb.grid(row=0,column=0, rowspan=6)

    
    #请求按钮
    tkinter.Button(root,text='请求Room列表',command=requestRoomList).grid(row=1,column=1, sticky=E+W)   
    tkinter.Button(root,text='获取选中Room信息',command=getRoomInfo).grid(row=2,column=1, sticky=E+W)
    #tkinter.Button(root,text='绘制选中Room',command=drawDNA).grid(row=3,column=1, sticky=E+W)   
    tkinter.Button(root,text='反馈家具位置',command=feedBack).grid(row=4,column=1, sticky=E+W)
    tkinter.Button(root,text='查看已反馈的Room', command=showFeedBackList).grid(row=5,column=1,sticky=E+W)
    cur_room_label = tkinter.Label(root, text='当前处理的Room：')
    cur_room_label.grid(row=6, column=0, sticky=E+W)
    cur_room_info_label = tkinter.Label(root, text='')
    cur_room_info_label.grid(row=6, column=1, columnspan=4, sticky=W)
    

    #在Tk的GUI上放置一个画布，并用.grid()来调整布局
    fig = Figure(figsize=(5,4), dpi=100) 
    dna_plt = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=root)  
    canvas.show() 
    canvas.get_tk_widget().grid(row=1, column=2, rowspan=5, columnspan=3)  
    canvas.mpl_connect('button_release_event', onPress)
    canvas.mpl_connect('motion_notify_event', onMotion)    
    circ = mpatches.RegularPolygon((0, 0), 30, 10, color = 'g', alpha=0.5)

    #放置标签、文本框和按钮等部件，并设置文本框的默认值和按钮的事件函数     
    split_label = tkinter.Label(root)
    split_label.grid(row=7, column=0, columnspan=4)
    split_line = '---------------------------------------------------------';
    split_line = split_line + split_line + split_line
    split_label.configure(text=split_line)
    
  
    fur_label = tkinter.Label(root, text='家具类型')
    fur_label.grid(row=8, column=0) 
    '''
    fur_input = tkinter.Entry(root)
    fur_input.grid(row=8, column=1)
    fur_input.insert(0, '-1')'''
    fur_type = tkinter.StringVar()
    fur_option = ttk.Combobox(root, width=12, textvariable=fur_type)
    fur_option['values'] = ('-1', '318-床', '120-移门衣柜','115-榻榻米', '40-儿童床', '301-沙发','323-梳妆台', '310-餐桌' , '330-书桌/工作台','114-书桌','355-坐便器','342-浴室柜','350-卫生间淋浴')
    fur_option.grid(row=8, column=1, sticky=W)
    fur_option.current(0)
    
    x_label = tkinter.Label(root, text='x:')
    x_label.grid(row=9, column=0)
    x_input = tkinter.Entry(root)
    x_input.grid(row=9, column=1, sticky=W)
    
    y_label = tkinter.Label(root, text='y:')
    y_label.grid(row=10, column=0)
    y_input = tkinter.Entry(root)
    y_input.grid(row=10, column=1, sticky=W)
    
    z_label = tkinter.Label(root, text='z:')
    z_label.grid(row=11, column=0)
    z_input = tkinter.Entry(root)
    z_input.grid(row=11, column=1, sticky=W)
    z_input.insert(0, '0')
    
    rotation_label = tkinter.Label(root, text='rotation:')
    rotation_label.grid(row=12, column=0)
    rotation_input = tkinter.Entry(root)
    rotation_input.grid(row=12, column=1, sticky=W)
    rotation_input.insert(0, '0')    

    page_idx_label = tkinter.Label(root, text='请求页编号：')
    page_idx_label.grid(row=8, column=2, sticky=E)
    page_idx_entry = tkinter.Entry(root)
    page_idx_entry.grid(row=8, column=3, sticky=W)
    page_idx_entry.insert(0, '1')
    
    page_size_label = tkinter.Label(root, text='单页记录数量：')
    page_size_label.grid(row=9, column=2, sticky=E)
    page_size_entry = tkinter.Entry(root)
    page_size_entry.grid(row=9, column=3, sticky=W)
    page_size_entry.insert(0, '20')
    
    '''
    #下拉菜单https://blog.csdn.net/u010159842/article/details/53287325
    v = IntVar()
    v.set(1)
    b1 = tkinter.Radiobutton(root, text='直径1米', variable=v, value=1)
    b1.grid(row=8, column=4)
    b2 = tkinter.Radiobutton(root, text='直径2米', variable=v, value=2)
    b2.grid(row=9, column=4)
    b3 = tkinter.Radiobutton(root, text='直径3米', variable=v, value=3)
    b3.grid(row=10,column=4)            
    '''
    
    cursor_size_label = tkinter.Label(root, text='光标尺寸：')
    cursor_size_label.grid(row=10, column=2, sticky=E)
    d_radius = tkinter.StringVar()
    d_radius_option = ttk.Combobox(root, width=12, textvariable=d_radius)
    d_radius_option['values'] = ('直径0.5米', '直径1米', '直径1.5米', '直径2米', '直径2.5米','直径3米')
    d_radius_option.grid(row=10, column=3, sticky=W)
    d_radius_option.current(1)
    
    ip_label = tkinter.Label(root, text='服务端IP')
    ip_label.grid(row=12, column=2, sticky=E)
    host_ip = tkinter.Entry(root)
    host_ip.grid(row=12,column=3, sticky=W)
    host_ip.insert(0, '192.168.23.43:8088')
    
    split_label = tkinter.Label(root)
    split_label.grid(row=13, column=0, columnspan=4)
    split_label.configure(text=split_line)
    '''
    feedback_pos = {}
    for i in range(len(myList)):
        feedback_pos[myList[i]] = ''
        
    '''
    
    
    room_fb_flag={}   #记录某个room是否反馈过
    response_text = {}
        
    

    #启动事件循环
    root.mainloop()