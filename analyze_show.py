"""
code speace
@Time    : 2023/5/19 20:56
@Author  : 泪懿:dgl
@File    : analyze_show.py
"""
import time
import tkinter as tk
from tkinter import ttk

import threading
import pandas as pd
import io
from PIL import Image,ImageTk
from create_analyze import create_analyze

with open('cities.txt','r',encoding='utf-8')as f:
    cities=[i.strip() for i in f.readlines()]



class analyze_show():
    def __init__(self,parent_window):
        parent_window.destroy()
        self.root=tk.Tk()
        self.root.title('中国地级市经济数据统计平台')

        self.root.attributes('-alpha', 1)
        self.root.config(background='#212946')
        self.height = 800
        self.weight = 1000

        self.root.geometry(f"{self.weight}x{self.height}+350+80")

        #导入数据分析模块
        self.nanlyze=create_analyze()

        self.create_title_frame()
        self.create_quear_fram()


        self.root.mainloop()

    def create_title_frame(self):

        #创建标题
        title_frame = ttk.Frame(self.root,width=self.weight,height=50,)
        title_frame.place(relx=0,rely=0)
        title_label = ttk.Label(title_frame,foreground='white',text="中国地级市经济数据可视化大屏",background='#212946', font=("微软雅黑", 30,), anchor='center')
        title_label.place(relx=0,rely=0,width=self.weight)

    def back(self):
        from demo import GUI
        self.root.destroy()#销毁当前界面
        GUI()#返回主界面

    def create_quear_fram(self):
        #创建城市选项
        quer_fram=ttk.LabelFrame(self.root,text='城市选择',width=self.weight,height=50,)
        quer_fram.place(relx=0,rely=0.07)

        city_lable = ttk.Label(quer_fram, text='城市:')
        city_lable.place(relx=0, rely=0.13)
        self.city_combobox = ttk.Combobox(quer_fram, values=cities)
        self.city_combobox.set('三亚市')
        self.city_combobox.place(relx=0.05, rely=0.13)

        ananlyze_button = ttk.Button(quer_fram, text='开始分析',command=self.create_imgs_show)
        ananlyze_button.place(relx=0.24, rely=0, width=80, height=30)

        back_button=ttk.Button(quer_fram,text='返回',command=self.back)
        back_button.place(relx=0.90, rely=0, width=80, height=30)

        #创建图片展示模块
        self.img_label_fram = ttk.LabelFrame(width=self.weight, height=self.height * 0.87,)
        self.img_label_fram.place(relx=0, rely=0.13)

    def resize_img(self,img):
        """
        更改生成图片大小，适应容易
        :return:
        """

        X=int(self.weight/3)
        y=int(self.height*0.87/2)

        img=Image.open(io.BytesIO(img))
        new_img=img.resize((X,y))

        new_img = new_img.convert('RGB')

        # 将重新定义尺寸后的图像保存到字节数据
        output_bytes = io.BytesIO()
        new_img.save(output_bytes, format='JPEG')
        output_bytes.seek(0)
        output_image_bytes = output_bytes.read()

        return output_image_bytes


    def create_imgs_show(self):
        """
        根据选择城市，生成分析图片字节列表

        :return:
        """
        city=self.city_combobox.get()
        img_list=self.nanlyze.run(city)
        relx=0
        rely=0
        n=0

        for i,v in enumerate(img_list):
            #生成每个图片容器，添加到主容器里面
            pand=ttk.Panedwindow(self.img_label_fram)
            v=self.resize_img(v)
            pand.img=ImageTk.PhotoImage(data=v)
            img_label=ttk.Label(self.img_label_fram)
            img_label.config(image=pand.img)
            img_label.place(relx=relx,rely=rely,width=int(self.weight/3),height=int(self.height*0.87/2))
            n+=1
            if relx>=0.66:
                n=0
                rely+=0.5
            relx = n * 0.33



