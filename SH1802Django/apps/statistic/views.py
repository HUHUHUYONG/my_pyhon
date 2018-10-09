from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from SH1802Django.utils import check_user_login

@check_user_login
def IndexHandler(request):
	return render(request, "static_handler.html")


def HistogramHandler(request):
	import json
	myjson = {
      'type': 'column',
      'colorByPoint': 'true',
      'data': [29.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4],
      'showInLegend': 'true'
    }
	data = json.dumps(myjson)
	return render(request, "art_statics.html", locals())

