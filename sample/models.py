from django.db import models
from django_google_maps.fields import AddressField, GeoLocationField, DistanceField
import datetime

# Create your models here.
class SampleModel(models.Model):
	address = AddressField(max_length=100)
	distance = DistanceField(null=True, blank=True, max_length=6)
	geolocation = GeoLocationField(blank=True)
	location = ListField(mod)
	
