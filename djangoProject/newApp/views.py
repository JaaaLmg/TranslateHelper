from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.conf import settings
import json
import os
from newApp.fileProcess import *
from newApp.models import *

responseDict={'message':'','text':[]}
def login(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        username = data['username']
        password = data['password']

        #在数据库中校验
        userobject=UserInfo.objects.filter(username=username,password=password).first()
        if userobject:
        #登录成功
            #设置cookie和session
            request.session['info']={'username':username,'id':userobject.id}
            response=HttpResponse("ok")
            return response
        else:
            response = HttpResponse(json.dumps({"error": "用户名或密码错误"}))
            response.status_code = 444
            return response

        # if username=='ja' and password=='123':
        #     print("right")
        #     response = HttpResponse("ok")
        #     return response
        # else:
        #     response=HttpResponse(json.dumps({"error":"用户名或密码错误"}))
        #     response.status_code=444
        #     return response

def register(request):
    if request.method == "POST":
        response = HttpResponse("ok")
        return response

def startnow(request):
    return render(request,"home.html")

def translate(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        rowIndex=data['id']
        newtext=responseDict['text']
        newtext[rowIndex-1]=data
        responseDict['text']=newtext

    responseDict['message']="修改成功！"
    return JsonResponse(responseDict)

def uploadfile(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get('file')
        #设置保存路径
        upload_path=os.path.join(settings.BASE_DIR,'newApp','static','uploadfiles',uploaded_file.name)
        #将文件保存到指定路径
        with open(upload_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
        #处理文件
        text=processFile(uploaded_file.name,upload_path)

        responseDict['message']='File uploaded successfully'
        responseDict['text']=text

    return JsonResponse(responseDict)


def createproject(request):
    if request.method == "POST":
        response = HttpResponse("ok")
        return response
    elif request.method == "GET":
        username = request.session.get('info').get('username')
        #print(username)
        responseInfo={'username':username}
        return JsonResponse(responseInfo)
# Create your views here.
