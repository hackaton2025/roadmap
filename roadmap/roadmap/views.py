from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
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

def dis(request):
    return render(request, 'graph_dis.html', {})

def graph_rest(request):
    return HttpResponse(json.dumps(
    {
  "nodes": [
    {
      "count": 1000,
      "name": "s11 1000",
      "display": "\u015amier\u0107",
      "display_en": "Начертательная геометрия",
      "color": "forestgreen"
    },
    {
      "count": 600,
      "name": "kobieta",
      "display": "s12",
      "display_en": "Инженерная графика 1",
      "color": "forestgreen"
    },
    {
      "count": 600,
      "name": "kobieta",
      "display": "s21",
      "display_en": "Инженерная графика 1",
      "color": "indianred"
    },
    {
      "count": 1000,
      "name": "s22",
      "display": "Mi\u0142o\u015b\u0107",
      "display_en": "Инженерная графика 2",
      "color": "indianred"
    },
    {
      "count": 1000,
      "name": "s23",
      "display": "\u015amier\u0107",
      "display_en": "Основы конструирования приборов",
      "color": "indianred"
    },
    {
      "count": 400,
      "name": "s31",
      "display": "\u015amier\u0107",
      "display_en": "Инженерная графика 1",
      "color": "darkcyan"
    },
    {
      "count": 200,
      "name": "s32 6",
      "display": "\u015amier\u0107",
      "display_en": "Инженерная графика 2",
      "color": "darkcyan"
    },
    {
      "count": 200,
      "name": "s33 7",
      "display": "\u015amier\u0107",
      "display_en": "Материаловедение",
      "color": "darkcyan"
    },
    {
      "count": 1000,
      "name": "s33 8",
      "display": "\u015amier\u0107",
      "display_en": "Основы конструирования приборов",
      "color": "darkcyan"
    }


  ],
  "links": [
    {
      "count": 800,
      "source": 0,
      "strength": 4,
      "target": 1
    },
    {
      "count": 600,
      "source": 2,
      "strength": 4,
      "target": 3
    },
    {
      "count": 600,
      "source": 3,
      "strength": 4,
      "target": 4
    },
    {
      "count": 600,
      "source": 5,
      "strength": 4,
      "target": 6
    },
    {
      "count": 600,
      "source": 6,
      "strength": 4,
      "target": 7
    },
    {
      "count": 600,
      "source": 7,
      "strength": 4,
      "target": 8
    },
    {
      "count": 600,
      "source": 0,
      "strength": 2,
      "target": 2
    },
    {
      "count": 600,
      "source": 0,
      "strength": 2,
      "target": 2
    }

  ]
}
), content_type="application/json")


# GET
def matrix(request, specialty_id):
    data = db.specialties.find().skip(int(specialty_id)+1)
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
