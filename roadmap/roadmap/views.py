from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
#from django.core.urlresolvers import reverse
from pymongo import MongoClient
from django.shortcuts import redirect
import json


connection = MongoClient("mongodb://localhost:27017")

db = connection.test


# POST GET
def create(request):
    if request.method == 'POST':
        data = json.loads(request.POST['data'])
        print(data)
        db.specialties.insert_one(data)
        n = db.specialties.count()
        return redirect("/{}/matrix".format(n))
        #
    else:
        return render(request, 'create.html', {})

# GET
def course(request, specialty_id):
    course = db.specialties.find({"_id": specialty_id})


# GET
def graph(request, specialty_id):
    return render(request, 'graph.html', {})

def graph_rest(request):
    return HttpResponse(json.dumps(
    { "nodes": [
    {
      "count": 500,
      "name": "kobieta",
      "display": "Kobieta",
      "display_en": "Woman"
    },
    {
      "count": 1000,
      "name": "milosc",
      "display": "Mi\u0142o\u015b\u0107",
      "display_en": "Love"
    },
    {
      "count": 1500,
      "name": "smierc",
      "display": "\u015amier\u0107",
      "display_en": "Death"
    }
  ],
  "links": [
    {
      "count": 400,
      "source": 1,
      "strength": 5.5563465441023085,
      "target": 2
    },
    {
      "count": 400,
      "source": 0,
      "strength": 1.200,
      "target": 1
    }
  ]
}), content_type="application/json")


# GET
def matrix(request, specialty_id):
    data = db.specialties.find().skip(int(specialty_id)-1)
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
    return render(request, 'index.html', {})
