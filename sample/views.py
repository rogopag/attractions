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
			obj = SampleModel.objects.get(bound_name=data['name'])
			pprint(data)
			#print "object id is %s" % str( obj.sample_task ) 
			try:
				action = data['stop']
				sample_task = data['sample_task']
				print "ok got the stop key foo"
				return HttpResponse( json.dumps({'fuck':'bar'}), 'application/json' )	
				result = task.apply_async(args=[data])
				abortable_async_result = AbortableAsyncResult(sample_task)
				abortable_async_result.abort()
				obj.sample_task = u''
				obj.save()
			except KeyError, e:
				print "Key not present "
				return HttpResponse( json.dumps({'fuck':'foo'}), 'application/json' )		
				result = task.apply_async(args=[data])
				obj.sample_task = result.task_id
				obj.save()
				print "task id should be %s" % result.task_id
			result.wait()
			r = result.get()
			print "type of r is %s " % type(r)
			print "result value should be %s" % r
			response = {'value' : r, 'sample_task' : obj.sample_task}
		else:
			message = "No XHR"
		return HttpResponse( json.dumps(response), 'application/json' )
		