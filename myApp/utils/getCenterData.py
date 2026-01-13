import json
import time
from .getPublicData import *


# 获取六个板块的数据
def getBaseData():
    cars=list(getAllCars())
    sumCar=len(cars) # 排行榜上的车辆总数
    highVolume=cars[0].saleVolume # 最高销量
    topCar=cars[0].carName # 销量最高的车

    #排行榜上最多的车型
    carModels={}
    maxModel=0
    mostModel=''
    for i in cars:
        if carModels.get(i.carModel,-1) == -1:
            carModels[str(i.carModel)]=1
        else:
            carModels[str(i.carModel)]+=1

    carModels=sorted(carModels.items(),key=lambda x:x[1],reverse=True)
    mostModel=carModels[0][0]

    #排行榜上最多的品牌
    carBrands={}
    maxBrand=0
    mostBrand=''
    for i in cars:
        if carBrands.get(i.brand,-1) == -1:
            carBrands[str(i.brand)]=1
        else:
            carBrands[str(i.brand)]+=1
    for k,v in carBrands.items():
        if v>maxBrand:
            maxBrand=v
            mostBrand=k

    #排行榜车辆的平均价格
    averagePrice=0
    carPrice={}
    sumPrice=0
    for i in cars:
        x= json.loads(i.price)[0] + json.loads(i.price)[1] #获取最低价和最高价的总和
        sumPrice+=x
    averagePrice=sumPrice/(sumCar*2)
    averagePrice=round(averagePrice,2) # 保留两位小数

    # 返回车辆总数、最高销量、销量最高的车、最多的车型、最多的品牌、平均价格
    return sumCar,highVolume,topCar,mostModel,mostBrand,averagePrice


# 获取轮播图数据
def getRollData():
    cars=list(getAllCars())
    # 品牌
    carBrands={}
    for i in cars:
        if carBrands.get(i.brand,-1)==-1:
            carBrands[str(i.brand)]=1
        else:
            carBrands[str(i.brand)]+=1
    brandList=[(value,key)for key,value in carBrands.items()]
    brandList=sorted(brandList,reverse=True)[:10]
    sortDict={i[1]:i[0] for i in brandList}
    lastSortList=[]
    for k,v in sortDict.items():
        lastSortList.append({
            'name':k,
            'value':v
        })
    return lastSortList

def getTypeRate():
    cars=list(getAllCars())
    # 能源类型
    carTypes={}
    for i in cars:
        if carTypes.get(i.energyType,-1)==-1:
            carTypes[str(i.energyType)]=1
        else:
            carTypes[str(i.energyType)]+=1
    oilRate=round(carTypes['汽油']/1000*100,2)  # 油车占比
    electricRate = round(carTypes['纯电动'] / 1000 * 100, 2)  # 电车占比
    mixRate=round(100-oilRate-electricRate,2)  # 其他能源占比
    return oilRate,electricRate,mixRate







