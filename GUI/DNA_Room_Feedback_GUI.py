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
import PatternLearning


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
        #msgbox.showinfo("Info", "Room请求成功!")
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
            
            print(response_text)
            
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

def isObjCategoryFeedbacked(obj_name):
    global feedback_list
    for i in range(len(feedback_list)):
        cur_feedback = feedback_list[i]
        if cur_feedback["name"] == obj_name:
            return i
    return -1
    
def packFeedback():
    global feedback_list
    
    obj_name = fur_option.get()
    obj_name_list = obj_name.split('-')
    obj_name = obj_name_list[1]
    
    search_idx = isObjCategoryFeedbacked(obj_name)
    if search_idx != -1:
        aijia_feedback = feedback_list[search_idx]
    else:
        aijia_feedback = {}
    aijia_feedback["name"] = obj_name          #物品名称
    #物品旋转信息
    aijia_feedback["rotate"] = {}
    aijia_feedback["rotate"]["xAxis"] = 0.0
    aijia_feedback["rotate"]["yAxis"] = 0.0
    aijia_feedback["rotate"]["zAxis"] = 0 - float(rotation_input.get())
    
    #物品底部中心点位置
    aijia_feedback["location"] = {}
    aijia_feedback["location"]["x"] = float(x_input.get())
    aijia_feedback["location"]["y"] = float(y_input.get())
    aijia_feedback["location"]["z"] = float(z_input.get())
    aijia_feedback["locationInHouse"] = {}
    aijia_feedback["locationInHouse"]["x"] = 0.0
    aijia_feedback["locationInHouse"]["y"] = 0.0
    aijia_feedback["locationInHouse"]["z"] = 0.0
    
    #物品缩放信息
    '''
    aijia_feedback["scale"] = {}
    aijia_feedback["scale"]["x"] = 1.0
    aijia_feedback["scale"]["y"] = 1.0
    aijia_feedback["scale"]["z"] = 1.0
    '''
    aijia_feedback["axisScale"] = {}
    aijia_feedback["axisScale"]["x"] = 1.0
    aijia_feedback["axisScale"]["y"] = 1.0
    aijia_feedback["axisScale"]["z"] = 1.0
    
    #物品变换前的长宽高
    aijia_feedback["size"] = {}
    aijia_feedback["size"]["dx"] = dx_scale.get()
    aijia_feedback["size"]["dy"] = dy_scale.get()
    aijia_feedback["size"]["dz"] = 0.0
    
    aijia_feedback["skuId"] = 1
    aijia_feedback["modelCode"] = 0
    aijia_feedback["categoryId"] = int(obj_name_list[0])
    
    #修正移动
    aijia_feedback["fixedMove"] = {}
    aijia_feedback["fixedMove"]["x"] = 0.0
    aijia_feedback["fixedMove"]["y"] = 0.0
    aijia_feedback["fixedMove"]["z"] = 0.0
    
    #修正旋转
    aijia_feedback["fixedRotate"] = {}
    aijia_feedback["fixedRotate"]["xAxis"] = 0.0
    aijia_feedback["fixedRotate"]["yAxis"] = 0.0
    aijia_feedback["fixedRotate"]["zAxis"] = 0.0
    
    aijia_feedback["mark"] = 0
    
    if search_idx == -1:
        feedback_list.append(aijia_feedback)
        
    
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
       
        msgbox.showinfo("Info", msg)
        
        packFeedback()
        
        print(feedback_list)
        
        
        my_url = 'http://'+ host_ip.get() + '/ai/room/feedback/update/' + RoomResponse.getRidFromResp(response_text)    #e099ce62b9ef4d5f8b08027c14be4157'        
        
        headers={'content-type':'application/json'}
        my_data = json.dumps(feedback_list)
        #print(my_data)
        post_r = requests.post(my_url,headers=headers, data=my_data)
        print("post_r=",post_r)
        #print("post_r.text=", post_r.text)
        
        
        
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
        
        '''
        cur_str = d_radius_option.get()        
        start_idx = cur_str.find("直径") + len("直径")
        end_idx = cur_str.find("米")
        number = float(cur_str[start_idx:end_idx])
        circ._set_radius(number * 500)
        circ._set_xy([event.xdata, event.ydata])
        '''
        dx = dx_scale.get() / 2.0
        dy = dy_scale.get() / 2.0
        x = [event.xdata - dx, event.xdata + dx, event.xdata + dx, event.xdata - dx]
        y = [event.ydata - dy, event.ydata - dy, event.ydata + dy, event.ydata + dy]

        polygon.set_xy(list(zip(x,y)))        
        event.canvas.draw()        
        return
    
def drawDNA(response_text):
    try:      
        door_num, door_pos = RoomResponse.getDoorInfoFromRoom(response_text)
        shape_point_num, shape_pos = RoomResponse.getWallShapeInfoFromRoom(response_text, "shapes")
        wall_num, wall_pos = RoomResponse.getWallShapeInfoFromRoom(response_text, "walls")
        window_num, window_pos = RoomResponse.getWindowInfoFromRoom(response_text)
        
    except:
        msgbox.showerror("Error", "绘图失败!")
        return       
    

    #清空图像，以使得前后两次绘制的图像不会重叠
    plt.style.use('ggplot')      
    dna_plt.clear()      
        
    dna_plt.plot(shape_pos['x'], shape_pos['y'], linewidth='0.5', color='k')  
    dna_plt.plot(wall_pos['x'], wall_pos['y'], linewidth='0.5', color='b')   
    
    for i in range(window_num):
        #print(window_pos['x'][i])
        dna_plt.plot(window_pos['x'][i], window_pos['y'][i], alpha=0.7, color='g', linewidth='0.8', solid_capstyle='round', zorder=2)
    for i in range(door_num):           
        dna_plt.plot(door_pos['x'][i], door_pos['y'][i], alpha=0.7, color='r', linewidth='0.8', solid_capstyle='round', zorder=2)
   
    #dna_plt.xlim((-5000, 5000))
    #dna_plt.ylim((-5000, 5000))    
    dna_plt.add_patch(polygon)
    #dna_plt.add_patch(rotate_arrow)
    #print("hello2", fig.axes, fig.axes[0].patches)
    #dna_plt.remove(circ)    
    #cursor = Cursor(dna_plt, useblit=True, color='r', linewidth=2)
    canvas.show() 
    
    
    if RoomResponse.isBedroom(response_text):
        x_range, y_range = RoomResponse.getShapeRange(shape_point_num, shape_pos)
        pattern, door_size_ratio, window_size_ratio = PatternLearning.generateRoomParttern(door_num, door_pos, window_num, window_pos, x_range, y_range)
        free_wall, align = PatternLearning.predictObjPostitionByPattern(pattern, door_size_ratio, window_size_ratio)
        print(pattern, free_wall, align)
        pos_exp = RoomResponse.getExpList(response_text)
        pos = RoomResponse.recoverPositionPoint(pos_exp, x_range, y_range)
        print(pos)
        
        
        '''不同类型家具已有反馈位置的点图'''
        obj_color=['b','r','y','g']
        obj_marker=['+', '.', ',']
        idx = 0
        for i_key, i_value in pos.items():
            cur_color = obj_color[idx % len(obj_color)]
            cur_marker = obj_marker[idx % len(obj_marker)]
            idx += 1
            for i in range(len(i_value)):
                x = i_value[i]['x']
                y = i_value[i]['y']
                dna_plt.plot(x, y, marker=cur_marker, color=cur_color)            
            
        
        
        if len(free_wall) > 0:
            objPositon = PatternLearning.generatePointByPrediction(shape_point_num, shape_pos, wall_num, wall_pos,free_wall[0], align)
            print(objPositon)
            if 318 in objPositon:
                dna_plt.plot(objPositon[318]['x'], objPositon[318]['y'], linewidth='3.0', color='r')


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
    #circ = mpatches.RegularPolygon((0, 0), 30, 10, color = 'g', alpha=0.5)
    polygon = mpatches.Polygon([[150, 150], [350, 400], [200, 600]], facecolor='g', alpha=0.5)
    #rotate_arrow = mpatches.Arrow(100, 110, 11, 12, width=200, color='r')

    #放置标签、文本框和按钮等部件，并设置文本框的默认值和按钮的事件函数     
    split_label = tkinter.Label(root)
    split_label.grid(row=7, column=0, columnspan=4)
    split_line = '---------------------------------------------------------';
    split_line = split_line + split_line + split_line
    split_label.configure(text=split_line)
    
  
    fur_label = tkinter.Label(root, text='家具类型：')
    fur_label.grid(row=8, column=0, sticky=E) 
    '''
    fur_input = tkinter.Entry(root)
    fur_input.grid(row=8, column=1)
    fur_input.insert(0, '-1')'''
    fur_type = tkinter.StringVar()
    fur_option = ttk.Combobox(root, width=12, textvariable=fur_type)
    fur_option['values'] = ('-1', '318-床', '120-移门衣柜','115-榻榻米', '40-儿童床', '301-沙发','323-梳妆台', '310-餐桌' , '330-书桌/工作台','114-书桌','355-坐便器','342-浴室柜','350-卫生间淋浴')
    fur_option.grid(row=8, column=1, sticky=W)
    fur_option.current(0)
    
    x_label = tkinter.Label(root, text='x：')
    x_label.grid(row=9, column=0, sticky=E)
    x_input = tkinter.Entry(root)
    x_input.grid(row=9, column=1, sticky=W)
    
    y_label = tkinter.Label(root, text='y：')
    y_label.grid(row=10, column=0, sticky=E)
    y_input = tkinter.Entry(root)
    y_input.grid(row=10, column=1, sticky=W)
    
    z_label = tkinter.Label(root, text='z：')
    z_label.grid(row=11, column=0, sticky=E)
    z_input = tkinter.Entry(root)
    z_input.grid(row=11, column=1, sticky=W)
    z_input.insert(0, '0')
    
    rotation_label = tkinter.Label(root, text='rotation：')
    rotation_label.grid(row=12, column=0, sticky=E)
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
    
    obj_dx_label = tkinter.Label(root, text='反馈家具尺寸Dx：')
    obj_dx_label.grid(row=13, column=0, sticky=E)
    obj_dy_label = tkinter.Label(root, text='反馈家具尺寸Dy：')
    obj_dy_label.grid(row=14, column=0, sticky=E)
    '''
    d_radius = tkinter.StringVar()
    d_radius_option = ttk.Combobox(root, width=12, textvariable=d_radius)
    d_radius_option['values'] = ('直径0.5米', '直径1米', '直径1.5米', '直径2米', '直径2.5米','直径3米')
    d_radius_option.grid(row=10, column=3, sticky=W)
    d_radius_option.current(1)
    '''
    
    dx_scale = Scale(root, from_ = 0, to = 5000, orient=HORIZONTAL, resolution=5)
    dx_scale.grid(row=13, column=1, sticky=W)
    dx_scale.set(1000)
    
    dy_scale = Scale(root, from_ = 0, to = 5000, orient=HORIZONTAL, resolution=5)
    dy_scale.grid(row=14, column=1, sticky=W)    
    dy_scale.set(1000)
    
    ip_label = tkinter.Label(root, text='服务端IP：')
    ip_label.grid(row=10, column=2, sticky=E)
    host_ip = tkinter.Entry(root)
    host_ip.grid(row=10,column=3, sticky=W)
    host_ip.insert(0, '192.168.23.59:8088')
    
    split_label = tkinter.Label(root)
    split_label.grid(row=15, column=0, columnspan=4)
    split_label.configure(text=split_line)
    '''
    feedback_pos = {}
    for i in range(len(myList)):
        feedback_pos[myList[i]] = ''
        
    '''
    
    
    room_fb_flag={}     #记录某个room是否反馈过
    response_text = {}  #记录当前room的详细信息
    feedback_list = []
        
    

    #启动事件循环
    root.mainloop()