# -*- coding: utf-8 -*-
import os, sys; sys.path.insert(0, os.path.join("..", ".."))
import tweepy
import webbrowser
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
results = []

class CustomStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		
		# We'll simply print some values in a tab-delimited format
		# suitable for capturing to a flat file but you could opt 
		# store them elsewhere, retweet select statuses, etc.
		try:
			results.append([status.id, status.user.screen_name, status.text, status.created_at, status.user.screen_name, status.user.location, status.user.name, status.user.time_zone, status.created_at, status.place])
			return results
		except Exception, e:
			print >> sys.stderr, 'Encountered Exception:', e
			pass

	def on_error(self, status_code):
		print >> sys.stderr, 'Encountered error with status code:', status_code
		return True # Don't kill the stream
# -*- coding: utf-8 -*-
import os, sys; sys.path.insert(0, os.path.join("..", ".."))
import tweepy
import webbrowser
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

class CustomStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		
		# We'll simply print some values in a tab-delimited format
		# suitable for capturing to a flat file but you could opt 
		# store them elsewhere, retweet select statuses, etc.
		try:
			stream.results.append([status.id, status.user.screen_name, status.text, status.created_at, status.user.screen_name, status.user.location, status.user.name, status.user.time_zone, status.created_at, status.place])
			print stream.results
			return stream.results
		except Exception, e:
			print >> sys.stderr, 'Encountered Exception:', e
			pass

	def on_error(self, status_code):
		print >> sys.stderr, 'Encountered error with status code:', status_code
		return True # Don't kill the stream

	def on_timeout(self):
		print >> sys.stderr, 'Timeout...'
		return True # Don't kill the stream

def stream( coords = {} ):
	# Create a streaming API and set a timeout value of 60 seconds.
	stream.streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout=120)
	
	try:
		stop = coords['stop']
		tweepy.streaming.Stream.disconnect(stream.streaming_api)
		print "Stop collecting"
		return stream.results
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
	stream.streaming_api.filter( follow=None, track=Q, async=True, locations=LOCATIONS)
	return stream.results
	
stream.results = []
stream.streaming_api = object()