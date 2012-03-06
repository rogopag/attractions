# -*- coding: utf-8 -*-
import os, sys; sys.path.insert(0, os.path.join("..", ".."))
import httplib
from socket import timeout
import threading
from time import sleep
import urllib
import tweepy
from pprint import pprint
from tweepy.utils import import_simplejson

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
	conn = None
	thread = None
	
	def _start(self, async):
		self.running = True
		if async:
			self.thread = thread_looper( 0.1, self._run )
			self.thread.start()
		else:
			self._run()
			
	def stop(self):
		self.running = False
		self.thread.stop()
		return False
		
	def _run(self):
		url = "%s://%s%s" % (self.scheme, self.host, self.url)
		print "Triggered start " + str(url)
		error_counter = 0
		exception = None
		print "foooo "+str(self.running)
		while self.running:
			if self.retry_count is not None and error_counter > self.retry_count:
				# quit if error count greater than retry count
				break
			try:
				print "now you should connect with " + str( self.scheme )
				if self.scheme == "http":
					self.conn = httplib.HTTPConnection(self.host)
				else:
					self.conn = httplib.HTTPSConnection(self.host)
				self.auth.apply_auth(url, 'POST', self.headers, self.parameters)
				self.conn.connect()
				self.conn.sock.settimeout(self.timeout)
				self.conn.request('POST', self.url, self.body, headers=self.headers)
				resp = self.conn.getresponse()
				if resp.status != 200:
					if self.listener.on_error(resp.status) is False:
						break
					error_counter += 1
					sleep(self.retry_time)
				else:
					error_counter = 0
					self._read_loop(resp)
			except timeout:
				if self.listener.on_timeout() == False:
					break
				if self.running is False:
					break
				self.conn.close()
				sleep(self.snooze_time)
			except Exception, exception:
				# any other exception is fatal, so kill loop
				break
		# cleanup
		  	self.running = False
		  	if self.conn:
				self.conn.close()
		  	if exception:
				raise			

class CustomStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		
		# We'll simply print some values in a tab-delimited format
		# suitable for capturing to a flat file but you could opt 
		# store them elsewhere, retweet select statuses, etc.
		try:
			StreamManage.results.append([status.id, status.user.screen_name, status.text, status.created_at, status.user.screen_name, status.user.location, status.user.name, status.user.time_zone, status.created_at, status.place])
			print StreamManage.results
			return StreamManage.results
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
	results = []
	streaming_api = None
	
	def stream( self, coords = {} ):
		# Create a streaming API and set a timeout value of 60 seconds.

		if( StreamManage.streaming_api == None ):
			StreamManage.streaming_api = TweetStream(auth, CustomStreamListener(), timeout=120)
			print "Instantiated obj for first time " + str( StreamManage.streaming_api )
		else:
			print "Obj already instantiated " + str( StreamManage.streaming_api )

		try:
			stop = coords['stop']
			print "Stop collecting"
			StreamManage.streaming_api.stop()
			return "Collected " + str( len( StreamManage.results ) )
		except KeyError:
			print  'Start collecting'

		try:
			LOCATIONS = coords['sw'][1], coords['sw'][0], coords['ne'][1], coords['ne'][0]
		except:
			#default to Turin area 15miles radius
			LOCATIONS = 7.40888682759915, 44.806386501450021, 8.0660042459720618, 45.50071940788586
			#8print LOCATIONS

			# Optionally filter the statuses you want to track by providing a list
			# of users to "follow".

		#print >> sys.stderr, 'Filtering the public timeline for "%s"' % (' '.join(sys.argv[1:]),
		StreamManage.streaming_api.filter( follow=None, track=Q, async=True, locations=LOCATIONS)
		return "start"