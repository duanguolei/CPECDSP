"""
code speace
@Time    : 2023/5/20 14:56
@Author  : 泪懿:dgl
@File    : create_analyze.py
"""
import matplotlib.pyplot as plt
import mplcyberpunk
plt.style.use('cyberpunk')
import seaborn as sns
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import pandas as pd
import io
import base64
from PIL import Image


class create_analyze:
    def __init__(self):
        self.df=pd.read_csv('数据.csv')
        
    def run(self,city):

        self.imgs_list=[]

        self.df_Ctnm = self.df[self.df['Ctnm'] == city].sort_index(ascending=False)
        self.crete_1()
        self.create_3()
        self.create_5()
        self.create_6()
        self.crete_4()
        self.create_2()



        return self.imgs_list

    def crete_1(self):
        # 人均生产总值，职工增长总额增长曲线
        plt.plot(self.df_Ctnm['year'].values, self.df_Ctnm['GDP_PerCapita'].values, 'ro-', label='人均地区生产总值')

        plt.plot(self.df_Ctnm['year'].values, self.df_Ctnm['wage'].values, 'ko-', label='职工平均工资总额')

        plt.legend()
        plt.title('人均地区生产总值,工资增长曲线')

        # 将图片转换为字节形式
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        # 读取字节数据
        img_bytes = buf.read()

        self.imgs_list.append(img_bytes)
        plt.close()

        
    def create_2(self):
        # 第一，二，三产业占GDP比重，增长曲线
        plt.plot(self.df_Ctnm['year'].values, self.df_Ctnm['Gdpct01'].values, 'o-')
        plt.plot(self.df_Ctnm['year'].values, self.df_Ctnm['Gdpct02'].values, 'o--')
        plt.plot(self.df_Ctnm['year'].values, self.df_Ctnm['Gdpct03'].values, '-')
        mplcyberpunk.add_underglow()
        plt.legend(['第一产业', '第二产业', '第三产业'])
        plt.title('第一，二，三产业占GDP比重，增长曲线')

        # 将图片转换为字节形式
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        # 读取字节数据
        img_bytes = buf.read()
        self.imgs_list.append(img_bytes)

        plt.close()
        
    def create_3(self):
        # 第一，二，三产业比重占比饼状图
        gdp_01 = self.df_Ctnm.GDP_PerCapita.mean()
        gdp_02 = self.df_Ctnm.GDP_SecInd.mean()
        gfp_03 = self.df_Ctnm.GDP_TerInd.mean()

        plt.pie([gdp_01, gdp_02, gfp_03], labels=['第一产业', '第二产业', '第三产业'], explode=[0.02, 0.02, 0.02])
        plt.legend()
        plt.title('第一，二，三产业比重占比饼状图')

        # 将图片转换为字节形式
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        # 读取字节数据
        img_bytes = buf.read()
        self.imgs_list.append(img_bytes)
        plt.close()
    def crete_4(self):
        # 相关系数图
        hot_data = self.df_Ctnm[['GDP', "Eect04", "GDP_PerCapita", 'urban', 'nightLight']]

        sns.heatmap(hot_data.corr())

        plt.title('地区生产总值,人均生产总值，城镇化率等相关系数图')

        # 将图片转换为字节形式
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        # 读取字节数据
        img_bytes = buf.read()
        self.imgs_list.append(img_bytes)
        plt.close()
    def create_5(self):
        # 地区生产总值柱状图

        plt.bar(self.df_Ctnm['year'].values, self.df_Ctnm['GDP'].values)
        plt.plot(self.df_Ctnm['year'].values, self.df_Ctnm['GDP'].values, 'ro-')

        plt.title('地区生产总值柱状图')

        # 将图片转换为字节形式
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        # 读取字节数据
        img_bytes = buf.read()
        self.imgs_list.append(img_bytes)
        plt.close()

    def create_6(self):


        plt.bar(self.df_Ctnm['year'].values, [i for i in self.df_Ctnm['Eect06'].values], label='城镇个体劳动者(万人)', alpha=0.7)
        plt.bar(self.df_Ctnm['year'].values, self.df_Ctnm['Eect05'].values, label='从业人员(万人)', alpha=0.4)

        plt.legend()

        plt.title('城镇个体劳动者,从业人员数量对比图')
        for i, v in enumerate([i for i in self.df_Ctnm['Eect06'].values]):
            plt.text(self.df_Ctnm['year'].values[i], v, str(v))

         # 将图片转换为字节形式
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        # 读取字节数据
        img_bytes = buf.read()
        self.imgs_list.append(img_bytes)

        plt.close()

        
