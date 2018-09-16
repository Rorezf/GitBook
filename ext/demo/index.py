#coding: utf-8
import sys, json
reload(sys)
sys.setdefaultencoding("utf8")
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
	return render(request, "index.html")

@csrf_exempt
def jsonData(request):
	contextTemp = []
	context = {
		"task": "Rel7.2.5.5",
		"status": "(22,14,5,3,0)",
		"expanded": True,
		'children': []
	}
	t = {
		"task": "Smoking Test",
        "status": "(22,14,5,3,0)",
        "leaf": True,
	}
	context['children'].append(t)
	contextTemp.append(context)

	return HttpResponse(json.dumps(contextTemp), content_type="application/json")