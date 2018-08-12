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
import MyRoom


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
        err_msg = "请求Room列表失败！检查IP地址。"
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


def resetForRoomDetail():
    #重置家具类型和坐标信息
    fur_option.current(0)
    fur_option.current(0)
    x_input.delete(0, tkinter.END)
    x_input.insert(0, '0')
    y_input.delete(0, tkinter.END)
    y_input.insert(0, '0')
    z_input.delete(0, tkinter.END)
    z_input.insert(0, '0')
    rotation_input.delete(0, tkinter.END)
    rotation_input.insert(0, '0')
    
    
    feedback_list.clear()


'''获取选中的Room的详细信息 ''' 
def getRoomInfo():
    global response_text
    if isRoomListSelected(room_lb) == False:
        msgbox.showerror("Error", "请批量导入Room列表并选中一个Room!")
    else:        
        try: 
            #请求数据
            cur_id = room_lb.get(room_lb.curselection())
            my_url = 'http://'+ host_ip.get() + '/ai/room/feedback/detail?id='+str(cur_id)
            
            resp = requests.get(my_url)
            response_text = json.loads(resp.text)
            if RoomResponse.isResponseOK(response_text) == False:
                err_code = "Code[%d]" % response_text["code"]
                err_msg = "请求["+my_url+"]失败！"+err_code+" 请检查IP地址，确保服务端已启动！"
                msgbox.showerror("Error", err_msg)
                return 
            
            #解析数据
            show_text = RoomResponse.getRoomDetailShowInfo(response_text)
            cur_room_info_label.configure(text=show_text)
            drawDNA(response_text)
                        
            #重置位置信息
            #resetForRoomDetail()
            
            #msgbox.showinfo("Info", "获取Room详细信息成功!")
        except:
            err_msg = "获取Room详细信息异常！"
            msgbox.showerror("Error", err_msg)

def isObjCategoryFeedbacked(obj_name):
    global feedback_list
    for i in range(len(feedback_list)):
        cur_feedback = feedback_list[i]
        if cur_feedback["name"] == obj_name:
            return i
    return -1
    
def prepareFeedback():
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
    if fur_direction_option.get() == '-1':
            msgbox.showerror("Error", "请选择正确的家具正方向!")
            return
        
    if  fur_option.get() == '-1':
        msgbox.showerror("Error", "请选择正确的家具类型ID!")
        return
    else:  
            
        try:
            cur_id = RoomResponse.getIdFromShowText(cur_room_info_label["text"])       
            cur_id_num = int(cur_id[3:])
            msg = cur_id + '反馈位置： [category'  + fur_option.get() +'] '
            postition = '(x:' + x_input.get() + ', y:' + y_input.get() + ', z:' + z_input.get() + ', rotation:' + rotation_input.get() + ')'
            msg = msg + postition + ' success!'
            #feedback_pos[fur_input.get()] = postition      
            room_fb_flag[cur_id_num] = True
                  
            prepareFeedback()               
            
            my_url = 'http://'+ host_ip.get() + '/ai/room/feedback/update/' + RoomResponse.getRidFromResp(response_text)    #e099ce62b9ef4d5f8b08027c14be4157'        
            headers={'content-type':'application/json'}
            my_data = json.dumps(feedback_list)
            post_r = requests.post(my_url,headers=headers, data=my_data)
            
            
            '''记录到本地文件中'''
            filename = 'feedback_record.txt'
            with open(filename, 'a') as f:
                record_list = []
                record_list.append(response_text)
                record_list.append(feedback_list)
                record_str = json.dumps(record_list)
                f.write(record_str)
                f.write('\n')
                f.close()
            fur_option.current(0)
            fur_direction_option.current(0)
            msgbox.showinfo("Info", msg)  
            
        except:
            fur_option.current(0)
            fur_direction_option.current(0)
            msgbox.showerror("Error", "反馈过程出现异常，重新获取该room详细信息可确认反馈是否成功!")    
        
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
    print(feedback_list)
    msgbox.showinfo("Info", feedback_list)

def pointRectGrow():
    return
    
def onPress(event):
    #print("my pos:", event.button, event.xdata, event.ydata)
    x_input.delete(0,tkinter.END)
    x_input.insert(0,str(event.xdata))
    
    y_input.delete(0,tkinter.END)
    y_input.insert(0,str(event.ydata))
    
    dna_plt=fig.add_subplot(111)
    dna_plt.plot(event.xdata, event.ydata, '*')
    
    
    if fur_direction_option.get() == '上':
        rotation_input.delete(0, END)
        rotation_input.insert(0, '0')
    elif fur_direction_option.get() == '右':
        rotation_input.delete(0, END)
        rotation_input.insert(0, '90')
    elif fur_direction_option.get() == '下':
        rotation_input.delete(0, END)
        rotation_input.insert(0, '180')
    elif fur_direction_option.get() == '左':
        rotation_input.delete(0, END)
        rotation_input.insert(0, '-90')    
    
    canvas.show()
  

def onMotion(event):
    if event.inaxes is None:        
        return
    else: 
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
    

    '''画图'''
    #清空图像，以使得前后两次绘制的图像不会重叠
    #plt.style.use('ggplot')      
    dna_plt.clear()      
        
    dna_plt.plot(shape_pos['x'], shape_pos['y'], linewidth='0.5', color='k')  
    dna_plt.plot(wall_pos['x'], wall_pos['y'], linewidth='0.5', color='b')   
    
    for i in range(window_num):
        
        dna_plt.plot(window_pos['x'][i], window_pos['y'][i], alpha=0.7, color='g', linewidth='0.8', solid_capstyle='round', zorder=2)
    for i in range(door_num):           
        dna_plt.plot(door_pos['x'][i], door_pos['y'][i], alpha=0.7, color='r', linewidth='0.8', solid_capstyle='round', zorder=2)
   
    dna_plt.add_patch(polygon)
    dna_plt.xaxis.set_major_locator(plt.MultipleLocator(500))#设置x主坐标间隔 1
    dna_plt.xaxis.set_minor_locator(plt.MultipleLocator(50))#设置x从坐标间隔 0.1
    dna_plt.yaxis.set_major_locator(plt.MultipleLocator(500))#设置y主坐标间隔 1
    dna_plt.yaxis.set_minor_locator(plt.MultipleLocator(50))#设置y从坐标间隔 0.1
    dna_plt.grid(which='major', axis='x', linewidth=0.75, linestyle='--', color='0.75')#由每个x主坐标出发对x主坐标画垂直于x轴的线段
    dna_plt.grid(which='minor', axis='x', linewidth=0.25, linestyle='--', color='0.75')#由每个x主坐标出发对x主坐标画垂直于x轴的线段
    dna_plt.grid(which='major', axis='y', linewidth=0.75, linestyle='--', color='0.75')
    dna_plt.grid(which='minor', axis='y', linewidth=0.25, linestyle='--', color='0.75')
    
    canvas.show() 
    
    ''' 异形区域检测调试 '''   
    '''
    PatternLearning.identifySpecialRect(shape_point_num, shape_pos, wall_num, wall_pos)
    start_x = float(x_input.get())
    start_y = float(y_input.get())    
    left, right, top, bottom = PatternLearning.rectGrow(start_x, start_y, wall_num, wall_pos)
    print(start_x, start_y, left, right, top, bottom)
    rect = mpatches.Rectangle((left, bottom), right-left, top-bottom, color='b',alpha=0.3)
    dna_plt.add_patch(rect)
    #dna_plt.grid(linestyle='--', color='dimgray', alpha = 0.5)
    '''
    
    
    ''' 卧室主家具位置热度图预测 '''
    if RoomResponse.isBedroom(response_text):
        #x_range, y_range = RoomResponse.getShapeRange(shape_point_num, shape_pos)
        room_meta = MyRoom.RoomMeta(shape_point_num, shape_pos, wall_num, wall_pos, door_num, door_pos, window_num, window_pos)
        x_range = room_meta.getShapeDx();
        y_range = room_meta.getShapeDy();
        
        pos_exp = RoomResponse.getExpList(response_text)
        pos = RoomResponse.recoverPositionPoint(pos_exp, x_range, y_range)
        print(pos)
        
        
        '''不同类型家具已有反馈位置的点图'''
        obj_color=['b','r','magenta','g']
        obj_marker=['+', '.', 'x', 'o']
        idx = 0
        for i_key, i_value in pos.items():
            cur_color = obj_color[idx % len(obj_color)]
            cur_marker = obj_marker[idx % len(obj_marker)]
            idx += 1
            x = []
            y = []
            for i in range(len(i_value)):
                x.append(i_value[i]['x'])
                y.append(i_value[i]['y'])
            dna_plt.scatter(x, y, marker=cur_marker, color=cur_color, label=str(i_key))  
        
        handles, labels = dna_plt.get_legend_handles_labels()
        dna_plt.legend(handles[::-1], labels[::-1], loc = 1)
            
        
        
        #家具位置预测       
        room_meta.generatePointByPrediction()
        objPositon = room_meta.getObjPosition()
        #print(objPositon)
        if 318 in objPositon:    #床
            dna_plt.plot(objPositon[318]['x'], objPositon[318]['y'], linewidth='3.0', color='orange')
            
        if 120 in objPositon:    #衣柜
            dna_plt.plot(objPositon[120]['x'], objPositon[120]['y'], linewidth='3.0', color='hotpink')
        
        


if __name__ == '__main__':   
    matplotlib.use('TkAgg')

    root = tkinter.Tk()  
    
    #room列表部件
    tkinter.Label(root, text='Room列表:').grid(row=0,column=0)
    room_list = []
    room_lb = tkinter.Listbox(root, selectmode = tkinter.SINGLE, height=35 )
    #lb.configure(yscrollcommand=scrolly.set)
    for item in room_list:
        room_lb.insert(tkinter.END,item)    
    room_lb.select_set(0)    
    room_lb.grid(row=1,column=0, rowspan=5)

    
    #请求按钮
    tkinter.Button(root,text='请求Room列表',command=requestRoomList).grid(row=1,column=1, sticky=E+W)   
    tkinter.Button(root,text='获取选中Room信息',command=getRoomInfo).grid(row=2,column=1, sticky=E+W)
    #tkinter.Button(root,text='绘制选中Room',command=drawDNA).grid(row=3,column=1, sticky=E+W)   
    tkinter.Button(root,text='反馈家具位置',command=feedBack).grid(row=3,column=1, sticky=E+W)
    tkinter.Button(root,text='查看已反馈的Room', command=showFeedBackList).grid(row=4,column=1,sticky=E+W)
    tkinter.Button(root,text='区域生长', command=pointRectGrow).grid(row=5,column=1,sticky=E+W)
    cur_room_label = tkinter.Label(root, text='当前处理的Room：')
    cur_room_label.grid(row=6, column=0, sticky=E+W)
    cur_room_info_label = tkinter.Label(root, text='')
    cur_room_info_label.grid(row=6, column=1, columnspan=4, sticky=W)
    

    #在Tk的GUI上放置一个画布，并用.grid()来调整布局
    fig = Figure(figsize=(8,6), dpi=100) 
    dna_plt = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=root)  
    canvas.show() 
    canvas.get_tk_widget().grid(row=1, column=2, rowspan=6, columnspan=3)  
    canvas.mpl_connect('button_release_event', onPress)
    canvas.mpl_connect('motion_notify_event', onMotion)    
    #circ = mpatches.RegularPolygon((0, 0), 30, 10, color = 'g', alpha=0.5)
    polygon = mpatches.Polygon([[150, 150], [350, 400], [200, 600]], facecolor='g', alpha=0.5)
    #rotate_arrow = mpatches.Arrow(100, 110, 11, 12, width=200, color='r')

    #放置标签、文本框和按钮等部件，并设置文本框的默认值和按钮的事件函数     
    split_label = tkinter.Label(root)
    split_label.grid(row=7, column=0, columnspan=5)
    split_line = '---------------------------------------------------------';
    split_line = split_line + split_line + split_line
    split_label.configure(text=split_line)
    
  
    fur_label = tkinter.Label(root, text='家具类型：')
    fur_label.grid(row=8, column=0, sticky=E) 

    fur_type = tkinter.StringVar()
    fur_option = ttk.Combobox(root, width=12, textvariable=fur_type)
    fur_option['values'] = ('-1', '318-床', '120-移门衣柜','115-榻榻米', '40-儿童床', '301-沙发','323-梳妆台', '310-餐桌' , '330-书桌/工作台','114-书桌','355-坐便器','342-浴室柜','350-卫生间淋浴')
    fur_option.grid(row=8, column=1, sticky=W)
    fur_option.current(0)
    
    fur_direction_label = tkinter.Label(root, text='家具正方向：')
    fur_direction_label.grid(row=8, column=2, sticky=E) 
    fur_direction = tkinter.StringVar()
    fur_direction_option = ttk.Combobox(root, width=12, textvariable=fur_direction)
    fur_direction_option['values'] = ('-1', '上','下', '左', '右')
    fur_direction_option.grid(row=8, column=3, sticky=W)
    fur_direction_option.current(0)
    
    x_label = tkinter.Label(root, text='x：')
    x_label.grid(row=9, column=0, sticky=E)
    x_input = tkinter.Entry(root)
    x_input.grid(row=9, column=1, sticky=W)
    x_input.insert(0, '0')
    
    y_label = tkinter.Label(root, text='y：')
    y_label.grid(row=10, column=0, sticky=E)
    y_input = tkinter.Entry(root)
    y_input.grid(row=10, column=1, sticky=W)
    y_input.insert(0, '0')
    
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
    page_idx_label.grid(row=9, column=2, sticky=E)
    page_idx_entry = tkinter.Entry(root)
    page_idx_entry.grid(row=9, column=3, sticky=W)
    page_idx_entry.insert(0, '1')
    
    page_size_label = tkinter.Label(root, text='单页记录数量：')
    page_size_label.grid(row=10, column=2, sticky=E)
    page_size_entry = tkinter.Entry(root)
    page_size_entry.grid(row=10, column=3, sticky=W)
    page_size_entry.insert(0, '35')    
    
    obj_dx_label = tkinter.Label(root, text='反馈家具尺寸Dx：')
    obj_dx_label.grid(row=13, column=0, sticky=E)
    obj_dy_label = tkinter.Label(root, text='反馈家具尺寸Dy：')
    obj_dy_label.grid(row=14, column=0, sticky=E)

    dx_scale = tkinter.Scale(root, from_ = 100, to = 5000, orient=tkinter.HORIZONTAL, resolution=50)
    dx_scale.grid(row=13, column=1, sticky=W)
    dx_scale.set(1000)    
    
    dy_scale = tkinter.Scale(root, from_ = 100, to = 5000, orient=tkinter.HORIZONTAL, resolution=50)
    dy_scale.grid(row=14, column=1, sticky=W)    
    dy_scale.set(1000)
    
    ip_label = tkinter.Label(root, text='服务端IP：')
    ip_label.grid(row=11, column=2, sticky=E)
    host_ip = tkinter.Entry(root)
    host_ip.grid(row=11,column=3, sticky=W)
    host_ip.insert(0, '192.168.22.124:8088')
    host_info = tkinter.Label(root, text="启动服务端并输入正确的IP地址和端口号！", fg='red')
    host_info.grid(row=10, column=4,sticky=W)
    
    split_label = tkinter.Label(root)
    split_label.grid(row=15, column=0, columnspan=5)
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