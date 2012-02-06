
from django.contrib import admin
from django.forms.widgets import TextInput

from django_google_maps.widgets import GoogleMapsAddressWidget, GeocodedAddressWidget, DistanceFieldWidget
from django_google_maps.fields import AddressField, GeoLocationField, DistanceField

from sample import models

class SampleModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        AddressField: {'widget': GoogleMapsAddressWidget},
        GeoLocationField: {'widget': GeocodedAddressWidget(attrs={'readonly': 'readonly'})},
		DistanceField: {'widget': DistanceFieldWidget}
    }
    list_display = ('address', 'geolocation', 'distance')

admin.site.register(models.SampleModel, SampleModelAdmin)