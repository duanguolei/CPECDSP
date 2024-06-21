
import time
import tkinter as tk
from tkinter import ttk
import threading
import pandas as pd
from tkintertable import TableCanvas,TableModel
from analyze_show import analyze_show
import os
from tkinter.messagebox import showinfo

#加载地级市名称列表
with open('cities.txt','r',encoding='utf-8')as f:
    cities=[i.strip() for i in f.readlines()]


#建立标签索引
fators={
    '城市代码':'city',
    '年度标识':'year',
    '城市名称':'Ctnm',
    "城市类别":'Cttyp',
    "生产总值(亿元)":'GDP',
    "第一产业占GDP比重(%)":"Gdpct01",
    "第二产业占GDP比重(%)":"Gdpct02",
    "第三产业占GDP比重(%)":"Gdpct03",
    "人均地区生产总值(元)":"GDP_PerCapita",
    "第一产业生产总值(万元)":"GDP_PrimInd",
    "第二产业生产总值(万元)":"GDP_SecInd",
    "第三产业生产总值(万元)":"GDP_TerInd",
    "人口密度(人/平方公里)":"Eect04",
    "从业人员(万人)":"Eect05",
    "城镇个体劳动者(万人)":'Eect06',
    "第一产业从业人员比重(%)":"Eect08",
    "第二产业从业人员比重(%)":"Eect09",
    "第三产业从业人员比重(%)":"Eect10",
    "全部职工年均人数(万人)":"Eect11",
    "全部职工工资总额(万元)":"Eect12",
    "职工平均工资总额(万元)":'wage',
    "全市户籍人口(万人)":'hpopu',
    '城镇化率':'urban',
    '夜间灯光强度':'nightLight'
}


class GUI:
    def __init__(self):
        self.df=pd.read_csv('数据.csv')

        self.root = tk.Tk()

        self.root.title('中国地级市经济数据统计平台')

        self.root.attributes('-alpha', 0.95)
        # self.root.config(background='#d4dde1')
        self.height=800
        self.weight=1000

        self.root.geometry(f"{self.weight}x{self.height}+350+80")

        self.create_title_frame()#创建标题
        self.create_query_frame()#创建参数选择框架

        self.root.mainloop()

    def get_df_date(self,selectfactors):

        # 获取时间线和城市
        self.begin_date =int(self.date_begin.get())
        self.end_date = int(self.date_end.get())
        self.city = self.city_combobox.get()

        #获取标签对应的数据
        df=pd.DataFrame(self.df,columns=selectfactors)


        if self.city!='全部':
            self.fillerter_data=df[(df['year']>=self.begin_date)&(df['year']<=self.end_date)&(df['Ctnm']==self.city)]

            return self.fillerter_data

        else:
            self.fillerter_data=df[(df['year']>=self.begin_date)&(df['year']<=self.end_date)]

            return self.fillerter_data


    def save_data(self):
        #保存pd数据

        if not os.path.exists('data'):
            os.makedirs('data')

        try:
            self.fillerter_data.to_csv(f'./data/{time.time()}.csv',index=False)
            showinfo('suceess',f'./data/{time.time()}.csv 导出成功')
        except Exception as e:
            showinfo('fail',e)



    def thread_it(self, fun, *args):
        """
        进程
        :param fun:
        :param args:
        :return:
        """
        p = threading.Thread(target=fun, args=(args))
        p.daemon = True
        p.start()

    def create_title_frame(self):
        #标题
        title_frame = ttk.Frame(self.root,width=self.weight,height=50)
        title_frame.place(relx=0,rely=0)
        title_label = ttk.Label(title_frame, text="中国地级市经济数据统计平台",background='#C9C9C9', font=("微软雅黑", 30), anchor='center')
        title_label.place(relx=0,rely=0,width=self.weight)




    def create_data_display_frame(self):
        """
        创建数据展示表
        :return:
        """
        self.show_fram = ttk.LabelFrame(text='数据查询结果',width=self.weight*0.98, height=self.height * 0.54)
        self.show_fram.place(relx=0, rely=0.44)

        selected_opeions=[]#保存索引
        select_factors=[]#保存标签

        for option,var in self.options.items():
            if var.get()==1:
                if option=='全部':
                    selected_opeions=list(fators.keys())
                    select_factors=list(fators.values())
                    break
                else:
                    selected_opeions.append(option)
                    select_factors.append(fators[option])


        if selected_opeions:
            data_dict={}
            data = self.get_df_date(select_factors).values
            for i,v in enumerate(data):
                data_dict[f'rec{i+1}']=dict(zip(selected_opeions,v))
            #创建表格
            # print(data_dict)
            table = TableCanvas(self.show_fram, data=data_dict,width=self.weight*0.93,height=self.height*0.48)
            table.show()







    def create_query_frame(self):
        self.search_fram=ttk.LabelFrame(self.root,text='参数选择',height=self.height*0.38,width=self.weight)
        self.search_fram.place(relx=0,rely=50/self.height)
        #创建日期选择
        date_label=ttk.Label(self.search_fram,text='日期：')
        date_label.place(relx=0,rely=0.01)

        self.date_begin=ttk.Combobox(self.search_fram,
                                     values=[2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
                                     )
        self.date_begin.set(2006)
        self.date_begin.place(relx=0.1,rely=0.01)

        self.begin_label=ttk.Label(self.search_fram,text='开始日期:').place(relx=0.04,rely=0.01)
        self.end_label=ttk.Label(self.search_fram,text='结束日期:').place(relx=0.27,rely=0.01)

        end_values=[2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006]

        self.date_end=ttk.Combobox(self.search_fram,
                                   values=end_values
                                   )
        self.date_end.set(2019)
        self.date_end.place(relx=0.33,rely=0.01)



        #创建城市选项
        city_lable=ttk.Label(self.search_fram,text='城市:')
        city_lable.place(relx=0,rely=0.13)
        self.city_combobox=ttk.Combobox(self.search_fram,values=['全部']+cities)
        self.city_combobox.set('全部')

        self.city_combobox.place(relx=0.05,rely=0.13)


        #创建标签缩影选项
        factors_label=ttk.LabelFrame(self.search_fram,text='标签选择:',
                                     width=self.weight,height=self.height*0.2)
        factors_label.place(relx=0,rely=0.25)
        fators_list=["全部"]+list(fators.keys())

        self.options={}
        for i in fators_list:
            self.options[i]=tk.IntVar()
            if i == '年度标识':
                self.options[i].set(1)
            if i=='城市名称':
                self.options[i].set(1)

        n=0
        rely = 0
        for option,var in self.options.items():
            relx=n*0.16
            #复选按钮
            checkbox=tk.Checkbutton(factors_label,text=option,variable=var)
            checkbox.place(relx=relx,rely=rely)
            n+=1
            if relx >= 0.80:
                n = 0
                rely += 0.2


        button_from=ttk.LabelFrame(self.search_fram,text='操作',width=self.weight,height=80)
        button_from.place(relx=0,rely=0.8)
        #查询按钮
        search_button=ttk.Button(button_from,text='查询',command=self.create_data_display_frame)
        search_button.place(relx=0,rely=0,width=80,height=40)
        #导出数据按钮
        output_button=ttk.Button(button_from,text='导出',command=self.save_data)
        output_button.place(relx=0.1,rely=0,width=80,height=40)

        #可视化分析按钮
        ananlyze_button=ttk.Button(button_from,text='可视化大屏',command=lambda : analyze_show(self.root))
        ananlyze_button.place(relx=0.9,rely=0,width=80,height=40)




if __name__ == "__main__":
     GUI()

