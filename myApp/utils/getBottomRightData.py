import json
import re
import time
from .getPublicData import *

def getRankData():
    cars=list(getAllCars())
    carData=[]
    for i in cars:
        i.price=re.findall(r'\d+\.\d+|\d+',i.price)
        i.price='-'.join(i.price)
        carData.append({
            'brand':i.brand,
            'rank':i.rank,
            'carName':i.carName,
            'carImg':i.carImg,
            'manufacturer':i.manufacturer,
            'carModel':i.carModel,
            'price':i.price,
            'saleVolume':i.saleVolume,
            'marketTime':i.marketTime,
            'insure':i.insure,
        })
    return carData
