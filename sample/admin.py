
from django.contrib import admin
from django.forms.widgets import TextInput

from django_google_maps.widgets import GoogleMapsAddressWidget, GeocodedAddressWidget, DistanceFieldWidget, GeolocationBoundsWidget
from django_google_maps.fields import AddressField, GeoLocationField, DistanceField, GeolocationBounds

from sample import models

class SampleModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        AddressField: {'widget': GoogleMapsAddressWidget},
        GeoLocationField: {'widget': GeocodedAddressWidget(attrs={'readonly': 'readonly'})},
		DistanceField: {'widget': DistanceFieldWidget},
		GeolocationBounds: {'widget' : GeolocationBoundsWidget}
    }
    list_display = ('address', 'geolocation', 'distance')

admin.site.register(models.SampleModel, SampleModelAdmin)