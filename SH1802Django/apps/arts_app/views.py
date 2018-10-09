from django.shortcuts import render, HttpResponse
import json
# Create your views here.


def test_param(request, art_pk):
	result = dict(
		data = int(art_pk) + 100,
		msg = 'ok',
		status = 200
	)

	return HttpResponse(json.dumps(result))