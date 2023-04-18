from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
import random
from django.db.models import Q
import json
from django.http import JsonResponse
from Project.models import *


class Projectcreate:
    def __init__(self, user, name, mood):
        self.user = user
        self.name = name
        self.mood = mood
        self.result = True

    def create(self):
        try:
            project = ProjectInfo.objects.get(Q(user=self.user)&Q(name=self.name))
            self.result = False
        except Exception as e:
            ProjectInfo.objects.create(
                user=self.user,
                name=self.name,
                mood=self.mood
            )


class Answer:
    def __init__(self):
        self.count=0
        self.project_names=[]
        self.project_modes=[]


class Projectget:
    def __init__(self, user):
        self.user=user
        self.answer = Answer()

    def getproject(self):
        projects = ProjectInfo.objects.filter(user = self.user)
        self.answer.count = projects.count()
        for project in projects:
            self.answer.project_names.append(project.name)
            self.answer.project_modes.append(project.mood)


class Projectedit:
    def __init__(self, user, oldname, newname, newmood):
        self.user = user
        self.oldname = oldname
        self.newname = newname
        self.newmood = newmood
        self.result = True

    def edit(self):
        try:
            project = ProjectInfo.objects.get(Q(user=self.user)&Q(name=self.oldname))
            Etyedit = Entityedit(self.user, self.oldname, "null")
            Etyedit.edit1(self.newname)
            project.name = self.newname
            project.mood = self.newmood
            project.save()
        except Exception as e:
            self.result = False


class Projectdelete:
    def __init__(self,user,name):
        self.user = user
        self.name = name
        self.result = True

    def delete(self):
        try:
            project = ProjectInfo.objects.get(Q(user=self.user)&Q(name=self.name))
            project.delete()
            Etydelete = Entitydelete(self.user, self.name, "null")
            Etydelete.delete1()
        except Exception as e:
            self.result = False


class Entitycreate:
    def __init__(self, user, project, name, description):
        self.user = user
        self.project = project
        self.name = name
        self.description = description
        self.result = True
    def create(self):
        try:
            entity = EntityInfo.objects.get(Q(user_project=self.user+"_"+self.project)&Q(name=self.name))
            self.result = False
        except Exception as e:
            EntityInfo.objects.create(
                user_project=self.user+"_"+self.project,
                name=self.name,
                discription=self.description
            )


class EntityAnswer:
    def __init__(self):
        self.count = 0
        self.entity_names = []
        self.entity_descriptions = []


class Entityget:
    def __init__(self, user, project):
        self.user = user
        self.project = project
        self.answer = EntityAnswer()

    def get(self):
        entities = EntityInfo.objects.filter(user_project=self.user+"_"+self.project)
        self.answer.count = entities.count()
        for entity in entities:
            self.answer.entity_names.append(entity.name)
            self.answer.entity_descriptions.append(entity.discription)


class Entityedit:
    def __init__(self, user, project, name):
        self.user = user
        self.project = project
        self.name = name
        self.result = True

    def edit1(self, newproject):
        entities = EntityInfo.objects.filter(user_project=self.user + "_" + self.project)
        for entity in entities:
            entity.user_project = self.user+"_"+newproject
            entity.save()

    def edit2(self, newname, newdescription):
        try:
            entity = EntityInfo.objects.get(Q(user_project=self.user+"_"+self.project)&Q(name=self.name))
            entity.name = newname
            entity.discription = newdescription
            try:
                entitynew = EntityInfo.objects.get(Q(user_project=self.user + "_" + self.project) & Q(name=newname))
                entity.delete()
                self.result = False
            except Exception as e:
                entity.save()
        except Exception as e:
            self.result = False


class Entitydelete:
    def __init__(self, user, project, name):
        self.user = user
        self.project = project
        self.name = name
        self.result = True

    def delete1(self):
        entities = EntityInfo.objects.filter(user_project=self.user + "_" + self.project)
        for entity in entities:
            entity.delete()

    def delete2(self):
        try:
            entity = EntityInfo.objects.get(Q(user_project=self.user + "_" + self.project) & Q(name=self.name))
            entity.delete()
        except Exception as e:
            self.result = False


class Datacreate:
    def __init__(self, user, project, name, type, description, text):
        self.user = user
        self.project = project
        self.name = name
        self.description = description
        self.type = type
        self.text = text
        self.result = True

    def create(self):
        try:
            data = DataInfo.objects.get(Q(user_project=self.user+"_"+self.project)&Q(name=self.name))
            self.result = False
        except Exception as e:
            DataInfo.objects.create(
                user_project=self.user+"_"+self.project,
                name=self.name,
                type=self.type,
                discription=self.description,
                text=self.text
            )


class DataAnswer:
    def __init__(self):
        self.count = 0
        self.data_names = []
        self.data_descriptions = []
        self.data_types = []
        self.data_contents = []


class Dataget:
    def __init__(self, user, project):
        self.user = user
        self.project = project
        self.answer = DataAnswer()

    def get(self):
        datas = DataInfo.objects.filter(user_project=self.user+"_"+self.project)
        self.answer.count = datas.count()
        for data in datas:
            self.answer.data_names.append(data.name)
            self.answer.data_descriptions.append(data.discription)
            self.answer.data_types.append(data.type)
            self.answer.data_contents.append(data.text)


class Relcreate:
    def __init__(self, user, project, name, description, obj, sub):
        self.user = user
        self.project = project
        self.name = name
        self.description = description
        self.obj = obj
        self.sub = sub
        self.result = True

    def create(self):
        try:
            rel = RelInfo.objects.get(Q(user_project=self.user + "_" + self.project) & Q(name=self.name) & Q(obj=self.obj) & Q(sub=self.sub))
            self.result = False
        except Exception as e:
            RelInfo.objects.create(
                user_project=self.user + "_" + self.project,
                name=self.name,
                discription=self.description,
                obj=self.obj,
                sub=self.sub,
            )

class RelAnswer:
    def __init__(self):
        self.count = 0
        self.rel_names = []
        self.rel_descriptions = []
        self.rel_objs = []
        self.rel_subs = []

class Relget:
    def __init__(self, user, project):
        self.user = user
        self.project = project
        self.answer = RelAnswer()

    def get(self):
        rels = RelInfo.objects.filter(user_project=self.user + "_" + self.project)
        self.answer.count = rels.count()
        for rel in rels:
            self.answer.rel_names.append(rel.name)
            self.answer.rel_descriptions.append(rel.discription)
            self.answer.rel_subs.append(rel.sub)
            self.answer.rel_objs.append(rel.obj)


class Reledit:
    def __init__(self, user, project, name, obj, sub):
        self.user = user
        self.project = project
        self.name = name
        self.result = True
        self.obj = obj
        self.sub = sub

    def edit1(self, entity, newentity):
        rels = RelInfo.objects.filter(Q(user_project=self.user + "_" + self.project) & Q(obj=entity))
        for rel in rels:
            rel.obj = newentity
            rel.save()
        rels = RelInfo.objects.filter(Q(user_project=self.user + "_" + self.project) & Q(sub=entity))
        for rel in rels:
            rel.sub = newentity
            rel.save()

    def edit2(self, newname, newdescription, newobj, newsub):
        try:
            rel = RelInfo.objects.get(Q(user_project=self.user + "_" + self.project) & Q(name=self.name) & Q(obj=self.obj) & Q(sub=self.sub))
            rel.name = newname
            rel.discription = newdescription
            rel.obj = newobj
            rel.sub = newsub
            rel.save()
        except Exception as e:
            self.result = False

class Reldelete:
    def __init__(self, user, project, name, obj, sub):
        self.user = user
        self.project = project
        self.name = name
        self.obj = obj
        self.sub = sub
        self.result = True

    def delete(self):
        try:
            rel = RelInfo.objects.get(Q(user_project=self.user + "_" + self.project) & Q(name=self.name) & Q(obj=self.obj) & Q(sub=self.sub))
            rel.delete()
        except Exception as e:
            self.result = False


@csrf_exempt
def projectcreate(request):
    Procreate = Projectcreate(request.POST.get("user"), request.POST.get("project_name"), request.POST.get("project_model"))
    Procreate.create()
    return HttpResponse(Procreate.result)


@csrf_exempt
def projectget(request):
    Proget = Projectget(request.POST.get("username"))
    Proget.getproject()
    data = {
        'count': Proget.answer.count,
        'names': Proget.answer.project_names,
        'moods': Proget.answer.project_modes
    }
    j_data = json.dumps(data)
    return HttpResponse(j_data)


@csrf_exempt
def projectedit(request):
    Proedit = Projectedit(request.POST.get("user"), request.POST.get("old_name"), request.POST.get("new_name"), request.POST.get("new_model"))
    Proedit.edit()
    return HttpResponse(Proedit.result)


@csrf_exempt
def projectdelete(request):
    Prodelete = Projectdelete(request.POST.get("user"),request.POST.get("name"))
    Prodelete.delete()
    return HttpResponse(Prodelete.result)


@csrf_exempt
def entitycreate(request):
    Etycreate = Entitycreate(request.POST.get("user"), request.POST.get("project"), request.POST.get("entity_name"), request.POST.get("entity_description"))
    Etycreate.create()
    return HttpResponse(Etycreate.result)


@csrf_exempt
def entityget(request):
    Etyget = Entityget(request.POST.get("username"), request.POST.get("project"))
    Etyget.get()
    data = {
        'count': Etyget.answer.count,
        'names': Etyget.answer.entity_names,
        'descriptions': Etyget.answer.entity_descriptions
    }
    j_data = json.dumps(data)
    return HttpResponse(j_data)


@csrf_exempt
def entityedit(request):
    Etyedit = Entityedit(request.POST.get("user"), request.POST.get("project"), request.POST.get("entity_pastname"))
    Etyedit.edit2(request.POST.get("entity_newname"), request.POST.get("entity_newdescription"))
    Rledit = Reledit(request.POST.get("user"), request.POST.get("project"), '', '', '')
    Rledit.edit1(request.POST.get("entity_pastname"), request.POST.get("entity_newname"))
    return HttpResponse(Etyedit.result)


@csrf_exempt
def entitydelete(request):
    Etydelete = Entitydelete(request.POST.get("user"), request.POST.get("project"), request.POST.get("entity_name"))
    Etydelete.delete2()
    return HttpResponse(Etydelete.result)


@csrf_exempt
def datacreate(request):
    dtcreate = Datacreate(request.POST.get("username"), request.POST.get("project"), request.POST.get("name"),request.POST.get("type"),request.POST.get("description"), request.POST.get("content"))
    print(request.POST.get("content"))
    dtcreate.create()
    return HttpResponse(dtcreate.result)


@csrf_exempt
def dataget(request):
    Dtget = Dataget(request.POST.get("username"), request.POST.get("project"))
    Dtget.get()
    data = {
        'count': Dtget.answer.count,
        'names': Dtget.answer.data_names,
        'descriptions': Dtget.answer.data_descriptions,
        'types':Dtget.answer.data_types,
        'texts': Dtget.answer.data_contents
    }
    j_data = json.dumps(data)
    return HttpResponse(j_data)


@csrf_exempt
def relcreate(request):
    Rlcreate = Relcreate(request.POST.get('user'), request.POST.get('project'), request.POST.get('relation_name'), request.POST.get('relation_description'), request.POST.get('obj'), request.POST.get('sub'))
    Rlcreate.create()
    return HttpResponse(Rlcreate.result)


@csrf_exempt
def relget(request):
    Rlget = Relget(request.POST.get("username"), request.POST.get('project'))
    Rlget.get()
    data = {
        'count': Rlget.answer.count,
        'names': Rlget.answer.rel_names,
        'descriptions': Rlget.answer.rel_descriptions,
        'objs':Rlget.answer.rel_objs,
        'subs':Rlget.answer.rel_subs,
    }
    j_data = json.dumps(data)
    return HttpResponse(j_data)


@csrf_exempt
def reledit(request):
    reledit = Reledit(request.POST.get('user'), request.POST.get('project'), request.POST.get('save_name'), request.POST.get('save_obj'), request.POST.get('save_sub') )
    reledit.edit2(request.POST.get('relation_name'), request.POST.get('relation_description'), request.POST.get('obj'), request.POST.get('sub'))
    return HttpResponse(reledit.result)


@csrf_exempt
def reldelete(request):
    rldelete = Reldelete(request.POST.get('user'), request.POST.get('project'), request.POST.get('name'), request.POST.get('obj'), request.POST.get('sub'))
    rldelete.delete()
    return HttpResponse(rldelete.result)