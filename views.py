# Create your views here.
from django.http import HttpResponse
from django.utils import simplejson as json
from pprint import pprint
import urllib2

def home(request):
	URL = 'http://pipes.yahoo.com/pipes/pipe.run?_id=58dd05a516b4692ed1f280a32f563f0c&_render=json'
	try:
		s = urllib2.urlopen(urllib2.Request(url=URL))
	except urllib2.HTTPError, e:
		print "Problems loading the url " + str(e)
	s = s.read()
	s = json.JSONDecoder().decode( s )
	for item in s['value']['items']:
		pprint(item['title'])
	return HttpResponse(str(s))