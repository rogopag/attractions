# Create your views here.
import os
from django.http import HttpResponse
from django.utils import simplejson as json
from sample.tasks.stream import StreamTask
from django.views.generic import View
from celery.contrib.abortable import AbortableAsyncResult
from celery.task.control import revoke 
from sample.models import SampleModel
from pprint import pprint


class AjaxView(View):
	
	def get(self, request):
		return HttpResponse( json.dumps({'foo' : 'bar'}), 'application/json' )
		
	def post(self, request):
		if request.is_ajax():
			# Here we can access the POST data
			data = json.JSONDecoder().decode( request.POST['command'] )
			task = StreamTask()
			obj = SampleModel.objects.get(bound_name=data['name'])
			data['bounds_id'] = obj
			try:
				action = data['stop']
				sample_task = data['sample_task']
				result = task.apply_async(args=[data])
				result.wait()
				r = result.get()
				result.revoke()
				obj.sample_task = u''
				obj.save()
			except KeyError, e:		
				result = task.apply_async(args=[data])
				obj.sample_task = result.task_id
				obj.save()
				result.wait()
				r = result.get()
				print "task id should be %s" % result.task_id
			response = {'value' : r, 'sample_task' : obj.sample_task}
		else:
			message = "No XHR"
		return HttpResponse( json.dumps(response), 'application/json' )
		