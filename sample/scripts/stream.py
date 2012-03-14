# -*- coding: utf-8 -*-
import os, sys; sys.path.insert(0, os.path.join("..", ".."))
import httplib
import threading
import urllib
import tweepy
from time import sleep
from socket import timeout
from pprint import pprint
from tweepy.utils import import_simplejson
from django.db import models
from sample.models import TweetStatuses
#from tweepy.api import API

json = import_simplejson()

# Query terms

try:
	Q = sys.argv[1:]
except:
	Q = ''

# Locations

# Get these values from your application settings.

CONSUMER_KEY = '1ckG8hFdjy27kheXpjnYgA'
CONSUMER_SECRET = 'VBneTvwGqGFt72pvIf8wTT1QlDe4dCQiLzKN4ZOp0zQ'

# Get these values from the "My Access Token" link located in the
# margin of your application details, or perform the full OAuth
# dance.

ACCESS_TOKEN = '119013910-LVbsanppOgHqVre9SVmwSc0XBKBihgw2LJBSwzS5'
ACCESS_TOKEN_SECRET = '6xd9YsFa3j8PscHSWa7wFki2plu66duMWqk91O0GFc'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Note: Had you wanted to perform the full OAuth dance instead of using
# an access key and access secret, you could have uses the following 
# four lines of code instead of the previous line that manually set the
# access token via auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET).
# 
# auth_url = auth.get_authorization_url(signin_with_twitter=True)
# webbrowser.open(auth_url)
# verifier = raw_input('PIN: ').strip()
# auth.get_access_token(verifier)

# A Custom thread to run our Looop
class thread_looper(threading.Thread):
	def __init__ (self, interval, function, args=[], kwargs={}):
		threading.Thread.__init__(self)
		self.interval = interval
		self.function = function
		self.args = args
		self.kwargs = kwargs
		self.finished = threading.Event()
	def stop (self):
		self.finished.set()
		self.join()
	def run (self):
		while not self.finished.isSet():
			self.finished.wait(self.interval)
			self.function(*self.args, **self.kwargs)

class TweetStream(tweepy.streaming.Stream):
	thread = None
	
	def __init__(self, auth, listener, **options):
		self.thread = thread_looper( 0.8, self._run )
		super(TweetStream, self).__init__(auth, listener, **options)
	
	def _start(self, async):
		self.running = True
		if async:
			self.thread.start()
		else:
			self._run()
			
	def stop(self):
		self.running = False
		try:
			self.thread.stop()
		except AttributeError, e:
			print "Exeption raised %s" % e

class CustomStreamListener(tweepy.StreamListener):
	
	#results = []
	bounds_id = None
	
	def __init__(self, bounds_id):
		self.bounds_id = bounds_id
		super(CustomStreamListener, self).__init__()
		
		
	def on_status(self, status):
		
		# We'll simply print some values in a tab-delimited format
		# suitable for capturing to a flat file but you could opt 
		# store them elsewhere, retweet select statuses, etc.
		try:
			#self.results.append([status.id, status.user.screen_name, status.text, status.created_at, status.user.location, status.user.name, status.user.time_zone, status.place])
			ts =  TweetStatuses()
			ts.tweet_id = status.id
			ts.tweet_screen_name = status.user.screen_name
			ts.tweet_text = status.text
			ts.tweet_created_at = status.created_at
			ts.tweet_location = status.user.location
			ts.tweet_user_name = status.user.name
			ts.tweet_user_timezone = status.user.time_zone
			ts.tweet_user_place = status.place
			ts.tweet_bounds = self.bounds_id
			ts.save()
			StreamManage.counter += 1
			print >> "Executed Call to twitter number %s" % StreamManage.counter
			return StreamManage.counter
		except Exception, e:
			print >> sys.stderr, 'Encountered Exception:', e
			pass

	def on_error(self, status_code):
		print >> sys.stderr, 'Encountered error with status code:', status_code
		return True # Don't kill the stream

	def on_timeout(self):
		print >> sys.stderr, 'Timeout...'
		return True # Don't kill the stream

class StreamManage(object):
	
	streaming_api = None
	
	def __init__(self, bounds_id = None):
		# Create a streaming API and set a timeout value of 60 seconds.
		if( self.streaming_api == None ):
			StreamManage.counter = 0
			self.streaming_api = TweetStream(auth, CustomStreamListener(bounds_id), timeout=120)
			print >> "StreamManage ::: Instantiated obj for first time " + str( self.streaming_api )
		else:
			pass
			#print "Obj already instantiated " + str( self.streaming_api )
		
	
	def stream( self, coords = {}, obj = None ):
		try:
			stop = coords['stop']
			print >> "StreamManage ::: Stop collecting obj %s" % obj + " type %s" % type(obj)
			obj.stop()
			return self.streaming_api
		except KeyError, e:			
			print >> sys.stderr,  'StreamManage ::: Start collecting exception on key %s' % e
		try:
			LOCATIONS = coords['sw'][1], coords['sw'][0], coords['ne'][1], coords['ne'][0]
		except:
			#default to Turin area 15miles radius
			LOCATIONS = 7.40888682759915, 44.806386501450021, 8.0660042459720618, 45.50071940788586
			#8print LOCATIONS

			# Optionally filter the statuses you want to track by providing a list
			# of users to "follow".

		#print >> sys.stderr, 'Filtering the public timeline for "%s"' % (' '.join(sys.argv[1:]),
		self.streaming_api.filter( follow=None, track=Q, async=True, locations=LOCATIONS)
		return self.streaming_api