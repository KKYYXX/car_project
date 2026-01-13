import requests
from lxml import etree
import csv
import os
import time
import json
import pandas as pd
import re
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','car_project.settings')
django.setup()
from myApp.models import CarInfo


class spider(object):
    def __init__(self):
        self.spiderUrl = ('https://www.dongchedi.com/motor/pc/car/rank_data?aid=1839&app_name=auto_web_pc&offset={offset}&count=12&rank_data_type=11')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0'
        }

    def init(self):
        if not os.path.exists('./temp.csv'):
            with open('./temp.csv', 'a', newline='', encoding='utf-8') as wf:
                write = csv.writer(wf)
                write.writerow(['brand', 'carName', 'carImg', 'saleVolume', 'price', 'manufacturer', 'rank', 'carModel',
                                'energyType', 'marketTime', 'insure'])

    def get_page(self):
        #获取offset的值
        with open('./spiderPage.txt', 'r') as r_f:
            return r_f.readlines()[-1].strip()

    def set_page(self,newPage):
        #使offset的值增加或减少
        with open('./spiderPage.txt', 'a') as a_f:
            a_f.write('\n'+str(newPage))

    def main(self):
        count = self.get_page()
        # 请求时用count的值替换URL中的{offset}
        url = self.spiderUrl.format(offset=int(count))
        print(f'数据从{int(count) + 1}开始爬!')
        # 使用格式化后的URL发送请求
        pageJson = requests.get(url, headers=self.headers).json()
        pageJson = pageJson['data']['list']
        try:
            for index, car in enumerate(pageJson):
                cardata = []
                print('正在爬取第%d' % (index + 1) + '数据')
                # 品牌名
                cardata.append(car['brand_name'])
                # 车名
                cardata.append(car['series_name'])
                # 图片链接
                cardata.append(car['image'])
                # 销量
                cardata.append(car['count'])
                # 价格
                price = []
                price.append(car['min_price'])  # 最低价
                price.append(car['max_price'])  # 最高价
                cardata.append(price)
                # 厂商
                cardata.append(car['sub_brand_name'])
                # 排名
                cardata.append(car['rank'])
                # 车型页面
                carNumber = car['series_id']
                infohtml = requests.get("https://www.dongchedi.com/auto/params-carIds-x-%s" % carNumber,
                                        headers=self.headers)
                infohtmlPath = etree.HTML(infohtml.text)
                # 车型
                carModel = infohtmlPath.xpath("//div[@data-row-anchor='jb']/div[2]/div/text()")[0]
                cardata.append(carModel)
                # 能源类型
                energyType = infohtmlPath.xpath("//div[@data-row-anchor='fuel_form']/div[2]/div/text()")[0]
                cardata.append(energyType)
                # 上市时间
                marketTime = infohtmlPath.xpath("//div[@data-row-anchor='market_time']/div[2]/div/text()")[0]
                cardata.append(marketTime)
                # 保修期限
                insure = infohtmlPath.xpath("//div[@data-row-anchor='period']/div[2]/div/text()")[0]
                cardata.append(insure)
                print(cardata)
                self.save_to_csv(cardata)
        except:
            pass

        #print(pageJson)
        self.set_page(int(count)+10)
        self.main()

    def save_to_csv(self,resultData):
        with open('./temp.csv','a',newline='',encoding='utf-8') as f:
            writer=csv.writer(f)
            writer.writerow(resultData)

    # 数据清洗
    def clear_csv(self):
        df=pd.read_csv('temp.csv')
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        print("总数量为%d"%df.shape[0])
        return df.values

    # 保存到数据库
    def save_to_db(self):
        data=self.clear_csv()
        for car in data:
            CarInfo.objects.create(
                brand=car[0],
                carName=car[1],
                carImg=car[2],
                saleVolume=car[3],
                price=car[4],
                manufacturer=car[5],
                rank=car[6],
                carModel=car[7],
                energyType=car[8],
                marketTime=car[9],
                insure=car[10]
            )


if __name__ == '__main__':
    spiderObj = spider()
    #spiderObj.init()
    #spiderObj.main()
    spiderObj.save_to_db()
