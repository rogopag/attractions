
from django.contrib import admin
from django.forms.widgets import TextInput

from django_google_maps.widgets import GoogleMapsAddressWidget, GeocodedAddressWidget, DistanceFieldWidget, GeolocationBoundsWidget, NameFieldWidget
from django_google_maps.fields import AddressField, GeoLocationField, DistanceField, GeolocationBounds, NameField

from sample import models

class SampleModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
		NameField:{'widget':NameFieldWidget(attrs={'class':'bounds-name'})},
        AddressField: {'widget': GoogleMapsAddressWidget},
        GeoLocationField: {'widget': GeocodedAddressWidget(attrs={'readonly': 'readonly'})},
		DistanceField: {'widget': DistanceFieldWidget},
		GeolocationBounds: {'widget' : GeolocationBoundsWidget(attrs={'visibility':'hidden'})}
    }
    list_display = ('bound_name', 'address', 'geolocation', 'distance')

admin.site.register(models.SampleModel, SampleModelAdmin)