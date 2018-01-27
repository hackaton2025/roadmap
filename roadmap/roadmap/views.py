from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from pymongo import MongoClient

connection = MongoClient("mongodb://localhost:27017")

db = connection.test


# POST GET
def create_skill(request):
    pass


# POST GET
def create_course(request):
    pass


# GET
def skill(request, skill_id):
    course = db.courses.find({"_id": skill_id})


# GET
def course(request, specialty_id):
    course = db.specialties.find({"_id": specialty_id})


# GET
def graph(request, specialty_id):
    course = db.specialties.find({"_id": specialty_id})

# GET
def matrix(request, course_id):
    data = db.specialties.find().skip(1)
    data = data[0]
    for idx in range(len(data["skills"])):
        data["skills"][idx]["links"] = [0 for i in range(len(data["courses"]))]
        for c_idx in range(len(data["courses"])):
            for m in data["courses"][c_idx]["modules"]:
                for s in m["skills"]:
                    if data["skills"][idx]["id"] == s["id"]:
                        data["skills"][idx]["links"][c_idx] += s["exp"]
    return render(request, 'matrix.html',{
        "specialty":data
    })

# GET
def index(request):
    courses = db.courses.find()
