from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
import random
from Mission.models import *
from django.db.models import Q
import json
from django.http import JsonResponse
from Mission.process import *
from Project.models import DataInfo


class Missioncreate:
    def __init__(self, user, project, name, description, text):
        self.user = user
        self.project = project
        self.name = name
        self.description = description
        self.text = text
        self.result = True
        self.entity_name = []
        self.entity_type = []
        self.relation_sub = []
        self.relation_obj = []
        self.relation_type = []

    def create(self):
        try:
            mission = Missions.objects.get(Q(user_project=self.user+"_"+self.project)&Q(name=self.name))
            self.result = False
        except Exception as e:
            Missions.objects.create(
                user_project=self.user+"_"+self.project,
                name=self.name,
                discription=self.description,
                text=self.text
            )
            (self.entity_name, self.entity_type, self.relation_sub, self.relation_type, self.relation_obj) = process(self.text)


class MissionAnswer:
    def __init__(self):
        self.count = 0
        self.mission_names = []
        self.mission_descriptions = []
        self.mission_texts = []


class Missionget:
    def __init__(self, user, project):
        self.user = user
        self.project = project
        self.answer = MissionAnswer()

    def get(self):
        missions = Missions.objects.filter(user_project=self.user+"_"+self.project)
        self.answer.count = missions.count()
        for mission in missions:
            self.answer.mission_names.append(mission.name)
            self.answer.mission_descriptions.append(mission.discription)
            self.answer.mission_texts.append(mission.text)


@csrf_exempt
def missioncreate(request):
    user = request.POST.get("user")
    project = request.POST.get("project")
    data = request.POST.get("data")
    text = DataInfo.objects.get(Q(user_project=user + "_" + project) & Q(name=data)).text
    Mscreate = Missioncreate(request.POST.get("user"), request.POST.get("project"), request.POST.get("mission_name"), request.POST.get("mission_description"), text)
    Mscreate.create()
    data = {
        'result': Mscreate.result,
        'entity_names': Mscreate.entity_name,
        'entity_types': Mscreate.entity_type,
        'rel_subs': Mscreate.relation_sub,
        'rel_types': Mscreate.relation_type,
        'rel_objs': Mscreate.relation_obj,
    }
    j_data = json.dumps(data)
    return HttpResponse(j_data)


@csrf_exempt
def missionget(request):
    Msget = Missionget(request.POST.get("username"), request.POST.get("project"))
    Msget.get()
    data = {
        'count': Msget.answer.count,
        'names': Msget.answer.mission_names,
        'descriptions': Msget.answer.mission_descriptions,
        'texts': Msget.answer.mission_texts
    }
    j_data = json.dumps(data)
    return HttpResponse(j_data)




