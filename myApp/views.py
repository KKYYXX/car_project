from django.shortcuts import render
from django.http import JsonResponse,HttpResponse

from myApp.utils import getCenterRightData
from .utils import getCenterData
from .utils import getPublicData
from .models import CarInfo
from .utils import getCenterLeftData
from .utils import getBottomLeftData
from .utils import getCenterChangeData
from .utils import getBottomRightData


def center(request):
    if request.method== "GET":
        sumCar,highVolume,topCar,mostModel,mostBrand,averagePrice=getCenterData.getBaseData()
        lastSortList=getCenterData.getRollData()
        oilRate,electricRate,mixRate=getCenterData.getTypeRate()
        return JsonResponse({
            'sumCar':sumCar,
            'highVolume':highVolume,
            'topCar':topCar,
            'mostModel':mostModel,
            'mostBrand':mostBrand,
            'averagePrice':averagePrice,
            'lastSortList':lastSortList,
            'oilRate':oilRate,
            'electricRate':electricRate,
            'mixRate':mixRate
        })

def car_list(request):
    """
    返回所有车辆列表
    GET /myApp/cars/
    """
    if request.method == "GET":
        cars = CarInfo.objects.all().values('id', 'carName', 'brand', 'price')
        data = [
            [str(c['id']), c['carName'], c['brand'], c['price']]
            for c in cars
        ]
        return JsonResponse({'data': data}, safe=False)

def centerLeft(request):
    if request.method == "GET":
        lastPieList = getCenterLeftData.getPieBrandData()
        return JsonResponse({
            'lastPieList': lastPieList
        })

def bottomLeft(request):
    if request.method == "GET":
        brandList,volumeList,priceList = getBottomLeftData.getSquareData()
        return JsonResponse({
            'brandList':brandList,
            'volumeList':volumeList,
            'priceList':priceList
        })

def centerRight(request):
    if request.method == "GET":
        realData=getCenterRightData.getPriceSortData()

        return JsonResponse({
           'realData':realData 
        })

def centerRightChange(request,energyType):
    if request.method == "GET":
        oilData,electricData=getCenterChangeData.getCircleData()
        realData=[]
        if energyType==1:
            realData=oilData
        else:
            realData=electricData
        return JsonResponse({
            'realData':realData
        })

def bottomRight(request):
    if request.method == "GET":
        carData=getBottomRightData.getRankData()
        return JsonResponse({
            'carData':carData
        })