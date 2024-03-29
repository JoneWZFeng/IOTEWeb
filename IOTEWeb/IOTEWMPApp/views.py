#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from IOTEWMPApp.models import *
from django.contrib.auth import  authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import logging
from struct_data import receiveExe
# Create your views here.

def managePage(request):
    username = "用户"
    return render(request, 'ManagementPlatform.html', {'username':username})

def my_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                #重定向到成功页面
            else:
                #提示错误信息
                warning1 = "登陆失败！"
                return render(request, 'login.html', {'warning': warning1})
        else:
            #提示错误信息
            warning2 = "用户不存在或密码错误！"
            return render(request, 'login.html', {'warning': warning2})
        return render(request, 'ManagementPlatform.html', {'username': username})

def my_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

######################################亮度处理#####################################################
#共用的亮度sensor数据处理函数
@login_required()
def floodlightMonitor(request):
    result = {}

    #读取传感器数据
    if request.method == "GET":
        #来自传感器模拟的读请求,返回工作中的传感器
        if "sensorRead" == request.GET['read']:
            #filter方法：匹配到数据时返回一个列表，不可以对查询到的数据进行修改(没有.save()方法)。没有匹配到数据时会返回一个空列表[].
            workingSensors = FloodlightSensor.objects.filter(deviceStatus = True)
            workingSensorsJSONArray = []
            for item in workingSensors:
                temp = {"id": item.id,"num":item.num, "name": item.name, "deviceStatus":item.deviceStatus, "luminance":item.luminance,"updata":item.updata,"downdata":item.downdata}
                workingSensorsJSONArray.append(temp)
            result={"workingSensorsJSON":workingSensorsJSONArray}
        # 来自监视器网页的读请求
        else:
            allSensors = FloodlightSensor.objects.all()
            allSensorsJSONArray = []
            for item in allSensors:
                temp = {"id": item.id,"num":item.num, "name": item.name, "deviceStatus": item.deviceStatus,"luminance": item.luminance,"updata":item.updata,"downdata":item.downdata}
                allSensorsJSONArray.append(temp)
            result = {"allSensorsJSON": allSensorsJSONArray}
    #传感器和web端更新传感器数据的操作
    else:
        id = request.POST['id']
        oldSensor = FloodlightSensor.objects.get(id=id)
        if "sensorWrite" == request.POST['writeType']:
            oldSensor.luminance = request.POST['luminance']
            oldSensor.save(update_fields=['luminance'])
    return JsonResponse(result)

@login_required()
def floodlightWork(request):
    result ={}
    id = request.POST['id']
    oldSensor = FloodlightSensor.objects.get(id = id)
    if request.method == "POST":
        oldSensor.deviceStatus = request.POST['deviceStatus']
        oldSensor.save(update_fields=['deviceStatus'])
        result["editStatus"] = "修改状态成功！"
    return JsonResponse(result)

#修改传感器
@login_required()
def floodlightRenew(request):
    result = {}
    id = request.POST['id']
    oldSensor = FloodlightSensor.objects.get(id=id)
    if request.method == "POST":
        sensorNum = request.POST['sensorNum']
        oldSensor.name = request.POST['sensorName']
        oldSensor.updata = request.POST['sensorUpdata']
        oldSensor.downdata = request.POST['sensorDowndata']
        if sensorNum != oldSensor.num:
            result["renewStatus"] = "设备号不能修改"
        else:
            oldSensor.save(update_fields=['name'])
            oldSensor.save(update_fields=['updata'])
            oldSensor.save(update_fields=['downdata'])
            #oldSensor.save()
            result["renewStatus"] = "修改成功"
    return JsonResponse(result)



#增加，删除亮度传感器
@login_required()
def floodlightSensor(request):
    result = {}
    #新增传感器
    if request.method == "POST":
        sensorNum = request.POST['sensorNum']
        sensorName = request.POST['sensorName']
        sensorUpdata = request.POST['sensorUpdata']
        sensorDowndata = request.POST['sensorDowndata']

        if len(FloodlightSensor.objects.filter(name=sensorName)):
            result["addStatus"]="名称已存在！"
        elif len(FloodlightSensor.objects.filter(num=sensorNum)):
            result["addStatus"]="设备号已存在！"
        else:
            result["addStatus"] = "添加成功！"
            aSensor = FloodlightSensor(num=sensorNum,name=sensorName, deviceStatus=True, luminance=350.64, updata=sensorUpdata,downdata=sensorDowndata)
            aSensor.save()
    #删除传感器
    else:
        sensorId = request.GET['sensorId']
        FloodlightSensor.objects.get(id=sensorId).delete()
    return JsonResponse(result)



######################################温度处理#####################################################
#共用的sensor数据处理函数
@login_required()
def temperatureMonitor(request):
    result = {}
    #receiveExe()
    #读取传感器数据
    if request.method == "GET":
        #来自传感器模拟的读请求,返回工作中的传感器
        if "sensorRead" == request.GET['read']:
            #filter方法：匹配到数据时返回一个列表，不可以对查询到的数据进行修改(没有.save()方法)。没有匹配到数据时会返回一个空列表[].
            workingSensors = TemperatureSensor.objects.filter(deviceStatus = True)
            workingSensorsJSONArray = []
            for item in workingSensors:
                temp = {"id": item.id,"num":item.num, "name": item.name, "deviceStatus":item.deviceStatus, "temperature":item.temperature,"updata":item.updata,"downdata":item.downdata}
                workingSensorsJSONArray.append(temp)
            result={"workingSensorsJSON":workingSensorsJSONArray}
        # 来自监视器网页的读请求
        else:
            allSensors = TemperatureSensor.objects.all()
            allSensorsJSONArray = []
            for item in allSensors:
                temp = {"id": item.id,"num":item.num, "name": item.name, "deviceStatus": item.deviceStatus,"temperature": item.temperature,"updata":item.updata,"downdata":item.downdata}
                allSensorsJSONArray.append(temp)
            result = {"allSensorsJSON": allSensorsJSONArray}
    #传感器和web端更新传感器数据的操作
    else:
        id = request.POST['id']
        oldSensor = TemperatureSensor.objects.get(id=id)
        if "sensorWrite" == request.POST['writeType']:
            oldSensor.temperature = request.POST['temperature']
            oldSensor.save(update_fields=['temperature'])
    return JsonResponse(result)

@login_required()
def temperatureWork(request):
    result ={}
    id = request.POST['id']
    oldSensor = TemperatureSensor.objects.get(id = id)
    if request.method == "POST":
        oldSensor.deviceStatus = request.POST['deviceStatus']
        oldSensor.save(update_fields=['deviceStatus'])
        result["editStatus"] = "修改状态成功！"
    return JsonResponse(result)

#修改传感器
@login_required()
def temperatureRenew(request):
    result = {}
    id = request.POST['id']
    oldSensor = TemperatureSensor.objects.get(id=id)
    if request.method == "POST":
        sensorNum = request.POST['sensorNum']
        oldSensor.name = request.POST['sensorName']
        oldSensor.updata = request.POST['sensorUpdata']
        oldSensor.downdata = request.POST['sensorDowndata']
        if sensorNum != oldSensor.num:
            result["renewStatus"] = "设备号不能修改"
        else:
            oldSensor.save(update_fields=['name'])
            oldSensor.save(update_fields=['updata'])
            oldSensor.save(update_fields=['downdata'])
            #oldSensor.save()
            result["renewStatus"] = "修改成功"
    return JsonResponse(result)

#增加，删除传感器
@login_required()
def temperatureSensor(request):
    result = {}
    #新增传感器
    if request.method == "POST":
        sensorNum = request.POST['sensorNum']
        sensorName = request.POST['sensorName']
        sensorUpdata = request.POST['sensorUpdata']
        sensorDowndata = request.POST['sensorDowndata']

        if len(TemperatureSensor.objects.filter(name=sensorName)):
            result["addStatus"]="名称已存在！"
        elif len(TemperatureSensor.objects.filter(num = sensorNum)):
            result['addStatus']="设备号已存在！"
        else:
            result["addStatus"] = "添加成功！"
            aSensor = TemperatureSensor(num= sensorNum,name=sensorName, deviceStatus=True, temperature=45.52, updata = sensorUpdata, downdata = sensorDowndata)
            aSensor.save()
    #删除传感器
    else:
        sensorId = request.GET['sensorId']
        TemperatureSensor.objects.get(id=sensorId).delete()
    return JsonResponse(result)

######################################湿度处理#####################################################
#共用的湿度sensor数据处理函数
@login_required()
def humidityMonitor(request):
    result = {}
    #读取传感器数据
    if request.method == "GET":
        #来自传感器模拟的读请求,返回工作中的传感器
        if "sensorRead" == request.GET['read']:
            #filter方法：匹配到数据时返回一个列表，不可以对查询到的数据进行修改(没有.save()方法)。没有匹配到数据时会返回一个空列表[].
            workingSensors = HumiditySensor.objects.filter(deviceStatus = True)
            workingSensorsJSONArray = []
            for item in workingSensors:
                temp = {"id": item.id,"num" : item.num, "name": item.name, "deviceStatus":item.deviceStatus, "humidity":item.humidity,"updata":item.updata,"downdata":item.downdata}
                workingSensorsJSONArray.append(temp)
            result={"workingSensorsJSON":workingSensorsJSONArray}
        # 来自监视器网页的读请求
        else:
            allSensors = HumiditySensor.objects.all()
            allSensorsJSONArray = []
            for item in allSensors:
                temp = {"id": item.id,"num":item.num, "name": item.name, "deviceStatus": item.deviceStatus,"humidity": item.humidity,"updata":item.updata,"downdata":item.downdata}
                #print (temp)
                allSensorsJSONArray.append(temp)
            result = {"allSensorsJSON": allSensorsJSONArray}
    #传感器和web端更新传感器数据的操作
    else:
        id = request.POST['id']
        oldSensor = HumiditySensor.objects.get(id=id)
        if "sensorWrite" == request.POST['writeType']:
            oldSensor.humidity = request.POST['humidity']
            oldSensor.save(update_fields=['humidity'])
    return JsonResponse(result)

#修改工作状态
@login_required()
def humidityWork(request):
    result = {}
    id = request.POST['id']
    oldSensor = HumiditySensor.objects.get(id=id)
    if request.method == "POST":
        oldSensor.deviceStatus = request.POST['deviceStatus']
        oldSensor.save(update_fields=['deviceStatus'])
        result["editStatus"] = "修改状态成功！"
    return JsonResponse(result)

#修改传感器
@login_required()
def humidityRenew(request):
    result = {}
    id = request.POST['id']
    oldSensor = HumiditySensor.objects.get(id=id)
    if request.method == "POST":
        sensorNum = request.POST['sensorNum']
        oldSensor.name = request.POST['sensorName']
        oldSensor.updata = request.POST['sensorUpdata']
        oldSensor.downdata = request.POST['sensorDowndata']
        if sensorNum != oldSensor.num:
            result["renewStatus"] = "设备号不能修改"
        else:
            oldSensor.save(update_fields=['name'])
            oldSensor.save(update_fields=['updata'])
            oldSensor.save(update_fields=['downdata'])
            #oldSensor.save()
            result["renewStatus"] = "修改成功"
    return JsonResponse(result)




#增加，删除湿度传感器
@login_required()
def humiditySensor(request):
    result = {}
    #新增传感器
    if request.method == "POST":
        sensorNum = request.POST['sensorNum']
        sensorName = request.POST['sensorName']
        sensorUpdata = request.POST['sensorUpdata']
        sensorDowndata = request.POST['sensorDowndata']

        if len(HumiditySensor.objects.filter(name=sensorName)):
            result["addStatus"]="名称已存在！"
        elif len(HumiditySensor.objects.filter(num=sensorNum)):
            result["addStatus"] = "设备号已存在！"
        else:
            result["addStatus"] = "添加成功！"
            aSensor = HumiditySensor(num=sensorNum,name=sensorName, deviceStatus=True, humidity=50.64, updata=sensorUpdata, downdata=sensorDowndata)
            aSensor.save()
    #删除传感器
    else:
        sensorId = request.GET['sensorId']
        HumiditySensor.objects.get(id=sensorId).delete()
    return JsonResponse(result)
