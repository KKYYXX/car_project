from typing import Any
import re

import json
import time
from .getPublicData import *

def getSquareData():
    cars=list(getAllCars())
    carsVolume={}
    for i in cars:
        if carsVolume.get(i.carName, -1) == -1:
            carsVolume[i.carName] = int(i.saleVolume)
        else:
            carsVolume[i.carName] += int(i.saleVolume)
    carsSortVolume=sorted(carsVolume.items(),key=lambda x:x[1],reverse=True)[:16]
    brandList=[]
    volumeList=[]
    priceList=[]

    for i in carsSortVolume:
        brandList.append(i[0])
        volumeList.append(i[1])
    for brand in brandList:
        rep = next((c for c in cars if c.carName == brand), None)
        avg_price = 0.0
        if rep:
            raw_price = getattr(rep, 'price', '')
            
            try:
                parsed = json.loads(raw_price)
                if isinstance(parsed, (list, tuple)) and len(parsed) >= 2:
                    avg_price = (float(parsed[0]) + float(parsed[1])) / 2.0
                elif isinstance(parsed, (int, float)):
                    avg_price = float(parsed)
            except Exception:
                m = re.findall(r'\d+\.\d+|\d+', str(raw_price))
                if m:
                    avg_price = float(m[0])
        priceList.append(round(avg_price, 2))

    return brandList,volumeList,priceList

