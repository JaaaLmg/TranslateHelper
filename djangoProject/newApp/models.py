from django.db import models

#用户信息表
class UserInfo(models.Model):
    username=models.CharField(verbose_name='用户名',max_length=32)
    password=models.CharField(verbose_name='密码',max_length=32)

#用户项目表
class ProjectInfo(models.Model):
    projectId=models.IntegerField(verbose_name='项目编号')
    type=models.CharField(verbose_name='翻译类型',max_length=16)
    projectname=models.CharField(verbose_name='项目名称',max_length=32)
    description=models.CharField(verbose_name='项目描述',max_length=256,default='')
    user=models.ForeignKey(verbose_name='关联用户',to=UserInfo,on_delete=models.CASCADE)

#项目内容表
class ContentInfo(models.Model):
    paragraphId=models.IntegerField(verbose_name='段号')
    type=models.CharField(verbose_name='翻译类型',max_length=16)
    origin=models.CharField(verbose_name='原文',max_length=1000)
    target=models.CharField(verbose_name='译文',max_length=1000,default='')
    description=models.CharField(verbose_name='备注',max_length=256,default='')
    project=models.ForeignKey(verbose_name='关联项目',to=ProjectInfo,on_delete=models.CASCADE)

#翻译记忆库
class MemoryInfo(models.Model):
    origin = models.CharField(verbose_name='原文', max_length=1000)
    target = models.CharField(verbose_name='译文', max_length=1000)
    project=models.ForeignKey(verbose_name='关联项目',to=ProjectInfo,on_delete=models.CASCADE)

#翻译术语库
class TerminologyInfo(models.Model):
    origin = models.CharField(verbose_name='原文', max_length=1000)
    target = models.CharField(verbose_name='译文', max_length=1000)
    description=models.CharField(verbose_name='注释',max_length=256,default='')
    project = models.ForeignKey(verbose_name='关联项目', to=ProjectInfo, on_delete=models.CASCADE)