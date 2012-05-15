from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import ListField, DictField
from django_google_maps.fields import AddressField, GeoLocationField, DistanceField, GeolocationBounds, NameField, SampleTaskField
import datetime

# Create your models here.
class SampleModel(models.Model):
	bound_name = NameField(max_length=50, unique=True)
	address = AddressField(max_length=100)
	distance = DistanceField(null=True, blank=True, max_length=6)
	geolocation = GeoLocationField(blank=True)
	bound_sw = GeolocationBounds(blank=True)
	bound_ne = GeolocationBounds(blank=True)
	sample_task = SampleTaskField(null=True, blank=True, max_length=50)
	owner = models.ForeignKey(User, null=True)
	
	def __unicode__(self):
		return unicode(self.id)
		
class TweetStatuses(models.Model):
	tweet_id = models.CharField(max_length=50)
	tweet_screen_name = models.CharField(max_length=35)
	tweet_text = models.TextField(max_length=140)
	tweet_created_at = models.DateTimeField(null=True, blank=True)
	tweet_location = DictField()
	tweet_user_name = models.CharField(max_length=35)
	tweet_user_timezone = models.CharField(max_length=20, null=True, blank=True)
	tweet_user_place = models.CharField(max_length=35, null=True, blank=True)
	tweet_bounds = models.ForeignKey(SampleModel, null=True)