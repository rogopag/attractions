# Create your views here.
import os
from django.http import HttpResponse
from django.utils import simplejson as json
from scripts.stream import stream
from pprint import pprint

def ajax(request):
	if request.is_ajax():
		if request.method == 'GET':
			message = "This is an XHR GET request"
		elif request.method == 'POST':
			# Here we can access the POST data
			data = json.JSONDecoder().decode( request.POST['command'] )
			stream( data )
			response = {'value' : 'response from view'}
		else:
			message = "No XHR"
		return HttpResponse( json.dumps(response), 'application/json' )