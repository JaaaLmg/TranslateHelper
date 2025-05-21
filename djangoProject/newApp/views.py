from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.conf import settings
import json
import os
from newApp.fileProcess import *
from newApp.models import *


textNow=[]

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
        projectId = data['projectId']

        userid = request.session.get('info').get('id')
        userproject = ProjectInfo.objects.filter(user_id=userid).filter(projectId=projectId).first()
        targetPrjId = userproject.id
        content = ContentInfo.objects.filter(project_id=targetPrjId).filter(paragraphId=rowIndex).first()

        #更新数据库
        content.target=data.get('target')
        content.description=data.get('notes')
        content.save()

        return JsonResponse({'message':'修改成功！'})
        # newtext=responseDict['text']
        # newtext[rowIndex-1]=data
        # responseDict['text']=newtext

    elif request.method == "GET":
        responseDict = {'message': '', 'text': []}

        projectId=request.GET.get('projectId')
        userid=request.session.get('info').get('id')
        print(userid)
        userproject=ProjectInfo.objects.filter(user_id=userid).filter(projectId=projectId).first()
        targetPrjId=userproject.id
        contentSet=ContentInfo.objects.filter(project_id=targetPrjId).order_by('paragraphId')
        contentList=[]

        for content in contentSet:
            para_dict = {}
            para_dict['id'] = content.paragraphId
            para_dict['direction'] = content.type
            para_dict['origin'] = content.origin
            para_dict['target'] = content.target
            para_dict['notes'] = content.description
            contentList.append(para_dict)

        responseDict['message']="修改成功！"
        responseDict['text']=contentList
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
        global textNow
        textNow=processFile(uploaded_file.name,upload_path)

        #response = HttpResponse("ok")
        # responseDict['message']='File uploaded successfully'
        # responseDict['text']=text
        # global textNow
        # textNow=text
        # time.sleep(1)

    return HttpResponse('ok')

def createproject(request):
    global textNow
    if request.method == "POST":
        newProject = json.loads(request.body)
        userid = request.session.get('info').get('id')

        if(newProject.get('type')=='delete'):
            #数据库中删除项目
            prjId=newProject.get('id')
            targetProject=ProjectInfo.objects.filter(user_id=userid).get(projectId=prjId)
            targetProject.delete()
            #修改其他项目编号
            prjSet=ProjectInfo.objects.filter(user_id=userid)
            for prj in prjSet:
                if prj.projectId>prjId:
                    prj.projectId=prj.projectId-1
                    prj.save()

        else:
            #数据库中添加项目
            ProjectInfo.objects.create(projectId=newProject.get('id'),type=newProject.get('type'),projectname=newProject.get('name'),description=newProject.get('description'),user_id=userid)
            newProjectId=ProjectInfo.objects.filter(user_id=userid).filter(projectId=newProject.get('id')).first().id
            for paragraph in textNow:
                ContentInfo.objects.create(paragraphId=paragraph.get('id'),type=newProject.get('type'),origin=paragraph.get('origin'),target=paragraph.get('target'),description='',project_id=newProjectId)

        response = HttpResponse("ok")
        return response

    elif request.method == "GET":
        responseInfo = {'username':'', 'projectList':[]}  #返回值

        username = request.session.get('info').get('username')
        userid=request.session.get('info').get('id')
        projectSet=ProjectInfo.objects.filter(user_id=userid).order_by('projectId')
        projectList=[]
        for project in projectSet:
            projectDict={}
            projectDict['id']=project.projectId
            projectDict['type']=project.type
            projectDict['name']=project.projectname
            projectDict['description']=project.description
            projectList.append(projectDict)

        responseInfo['username']=username
        responseInfo['projectList']=projectList
        return JsonResponse(responseInfo)


def searchMemory(request):
    if request.method == "POST":
        data=json.loads(request.body)
        projectId = data.get('projectId')
        origin = data.get('origin')
        target = data.get('target')
        userid = request.session.get('info').get('id')
        userproject = ProjectInfo.objects.filter(user_id=userid).filter(projectId=projectId).first()
        targetPrjId = userproject.id

        pair=MemoryInfo.objects.filter(project_id=targetPrjId).filter(origin=origin).first()
        if pair:
            # 更新数据库
            pair.target = target
            pair.save()
        else:
            #在数据库总添加
            MemoryInfo.objects.create(origin=origin,target=target,project_id=targetPrjId)
        return JsonResponse({'message':'存储成功！'})

    elif request.method == "GET":
        responseDict = {'message': '', 'memoryData': []}

        projectId = request.GET.get('projectId')
        origin = request.GET.get('origin')
        userid = request.session.get('info').get('id')
        userproject = ProjectInfo.objects.filter(user_id=userid).filter(projectId=projectId).first()
        targetPrjId = userproject.id
        memorySet=MemoryInfo.objects.filter(project_id=targetPrjId).filter(origin=origin).order_by('-id')

        print(targetPrjId)

        memoryList=[]
        for memory in memorySet:
            memoryDict={}
            memoryDict['origin']=memory.origin
            memoryDict['target']=memory.target
            memoryList.append(memoryDict)

        responseDict['memoryData']=memoryList
        responseDict['message']="检索完成"
        return JsonResponse(responseDict)

def searchTerm(request):
    if request.method == "POST":
        data=json.loads(request.body)
        projectId = data.get('projectId')
        origin = data.get('origin')
        target = data.get('target')
        description=data.get('description')
        userid = request.session.get('info').get('id')
        userproject = ProjectInfo.objects.filter(user_id=userid).filter(projectId=projectId).first()
        targetPrjId = userproject.id

        pair=TerminologyInfo.objects.filter(project_id=targetPrjId).filter(origin=origin).first()
        if pair:
            # 更新数据库
            pair.target = target
            pair.description = description
            pair.save()
        else:
            #在数据库总添加
            TerminologyInfo.objects.create(origin=origin,target=target,description=description,project_id=targetPrjId)
        return JsonResponse({'message':'存储成功！'})

    elif request.method == "GET":
        responseDict = {'message': '', 'termData': []}

        projectId = request.GET.get('projectId')
        origin = request.GET.get('origin')
        userid = request.session.get('info').get('id')
        userproject = ProjectInfo.objects.filter(user_id=userid).filter(projectId=projectId).first()
        targetPrjId = userproject.id
        termSet=TerminologyInfo.objects.filter(project_id=targetPrjId).filter(origin=origin).order_by('-id')

        termList=[]
        for term in termSet:
            termDict={}
            termDict['origin']=term.origin
            termDict['target']=term.target
            termDict['description']=term.description
            termList.append(termDict)

        responseDict['termData']=termList
        responseDict['message']="检索完成"
        return JsonResponse(responseDict)