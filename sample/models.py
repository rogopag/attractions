from django.db import models
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
	
	def __unicode__(self):
		return unicode(self.id)
	
