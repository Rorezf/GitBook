#coding: utf-8
import sys, json
reload(sys)
sys.setdefaultencoding("utf8")
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
	return render(request, "index.html")

@csrf_exempt
def jsonData2(request):
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

@csrf_exempt
def tableIndex(request):
	return render(request, 'table.html')

@csrf_exempt
def jsonData(request):
	context = {
		"data": [
			 [
		      "Tiger Nixon",
		      "System Architect",
		      "Edinburgh",
		      "5421",
		      "2011/04/25",
		      "$320,800"
		    ],
		    [
		      "Garrett Winters",
		      "Accountant",
		      "Tokyo",
		      "8422",
		      "2011/07/25",
		      "$170,750"
		    ],
		    [
		      "Ashton Cox",
		      "Junior Technical Author",
		      "San Francisco",
		      "1562",
		      "2009/01/12",
		      "$86,000"
		    ],
		    [
		      "Cedric Kelly",
		      "Senior Javascript Developer",
		      "Edinburgh",
		      "6224",
		      "2012/03/29",
		      "$433,060"
		    ],
		    [
		      "Airi Satou",
		      "Accountant",
		      "Tokyo",
		      "5407",
		      "2008/11/28",
		      "$162,700"
		    ],
		    [
		      "Brielle Williamson",
		      "Integration Specialist",
		      "New York",
		      "4804",
		      "2012/12/02",
		      "$372,000"
		    ],
		    [
		      "Herrod Chandler",
		      "Sales Assistant",
		      "San Francisco",
		      "9608",
		      "2012/08/06",
		      "$137,500"
		    ],
		    [
		      "Rhona Davidson",
		      "Integration Specialist",
		      "Tokyo",
		      "6200",
		      "2010/10/14",
		      "$327,900"
		    ]
		]
	}
	return HttpResponse(json.dumps(context), content_type="application/json")
