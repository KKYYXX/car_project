import json
import time
from .getPublicData import *

def getPieBrandData():
    cars=list(getAllCars())
    carsVolume={}
    for i in cars:
        if carsVolume.get(i.brand,-1)==-1:
            carsVolume[str(i.brand)]=int(i.saleVolume)
        else:
            carsVolume[str(i.brand)]+=int(i.saleVolume)
    carsVolume=sorted(carsVolume.items(),key=lambda x:x[1],reverse=True)
    sortDict={i[0]:i[1] for i in carsVolume}
    lastPieList=[]
    for k,v in sortDict.items():
        lastPieList.append({
            'name':k,
            'value':v
        })
    return lastPieList[:10]