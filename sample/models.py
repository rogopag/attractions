from django.db import models
from django_google_maps.fields import AddressField, GeoLocationField, DistanceField, GeolocationBounds, NameField
import datetime

# Create your models here.
class SampleModel(models.Model):
	bound_name = NameField(max_length=50)
	address = AddressField(max_length=100)
	distance = DistanceField(null=True, blank=True, max_length=6)
	geolocation = GeoLocationField(blank=True)
	bound_sw = GeolocationBounds(blank=True)
	bound_ne = GeolocationBounds(blank=True)
	
