# Create your views here.
import os
from django.http import HttpResponse
from django.utils import simplejson as json
from sample.tasks.stream import StreamTask
from django.views.generic import View
from celery.contrib.abortable import AbortableAsyncResult
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
			pprint( SampleModel.objects.get(id='4f3154b34a69092c30000001') )
			try:
				action = data['stop']
				result = task.apply_async(args=[data])
				abortable_async_result = AbortableAsyncResult(result.task_id)
				abortable_async_result.abort()
			except KeyError, e:		
				result = task.apply_async(args=[data])
				print "task id should be %s" % result.task_id
			result.wait()
			r = result.get()
			print "result value should be %s" % r
			response = {'value' : r}
		else:
			message = "No XHR"
		return HttpResponse( json.dumps(response), 'application/json' )
		