# from django.shortcuts import render
# from Project.models import *
from py2neo import Graph, Node, NodeMatcher, Relationship
# from openpyxl import load_workbook
# from django.shortcuts import render,HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.db.models import Q
# import json
graph = Graph('http://localhost:7474', user="neo4j", password="12345678", name="neo4j")


# class Graph_Construction:
#     def __init__(self, user, project):
#         self.node_matcher = NodeMatcher(self.graph)
#         self.user = ''.join(str(i) for i in user)
#         self.project = project
#     def Construct(self):
#         entities = EntityInfo.objects.filter(user_project=self.user + "_" + self.project)
#         for entity in entities:
#             node = Node(entity.discription, name=entity.name, belong_to=self.user + "_" + self.project)
#             graph.create(node)
#         relations = RelInfo.objects.filter(user_project=self.user + "_" + self.project)
#         for rel in relations:
#             nodeobj = self.node_matcher.match(name=rel.obj, user_project=self.user + "_" + self.project)
#             print(nodeobj)
#
# Gh = Graph_Construction('谢秉书', 'display_周杰伦')
# Gh.Construct()
node_matcher = NodeMatcher(graph)
condition = {"belong_to": "谢秉书_display_周杰伦", "name": "爱奇艺"}
nodeobj = node_matcher.match(**condition)
print(nodeobj.first())






