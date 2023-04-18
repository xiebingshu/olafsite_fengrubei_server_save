from django.shortcuts import render
from Project.models import *
from py2neo import Graph, Node, NodeMatcher, Relationship
from openpyxl import load_workbook
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
graph = Graph('http://localhost:7474', user="neo4j", password="12345678", name="neo4j")


class Graph_Construction:
    def __init__(self, user, project):
        self.node_matcher = NodeMatcher(graph)
        self.user = ''.join(str(i) for i in user)
        self.project = project
    def Construct(self):
        entities = EntityInfo.objects.filter(user_project=self.user + "_" + self.project)
        for entity in entities:
            node = Node(entity.discription, name=entity.name, belong_to=self.user + "_" + self.project)
            graph.create(node)
        relations = RelInfo.objects.filter(user_project=self.user + "_" + self.project)
        for rel in relations:
            condition_obj = {"belong_to": self.user + "_" + self.project, "name": rel.obj}
            condition_sub = {"belong_to": self.user + "_" + self.project, "name": rel.sub}
            nodeobj = self.node_matcher.match(**condition_obj).first()
            nodesub = self.node_matcher.match(**condition_sub).first()
            if nodeobj is not None and nodesub is not None:
                relation = Relationship(nodeobj, rel.name, nodesub)
                graph.create(relation)



@csrf_exempt
def graphConstruction(request):
    Gh = Graph_Construction(request.POST.get('username'), request.POST.get('project'))
    Gh.Construct()
    return HttpResponse('True')


