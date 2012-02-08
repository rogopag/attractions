from django.conf import settings
from django.forms import widgets
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.util import flatatt

class GoogleMapsAddressWidget(widgets.TextInput):
	"a widget that will place a google map right after the #id_address field"
	
	class Media:
		css = {'all': (settings.STATIC_URL + 'django_google_maps/css/google-maps-admin.css',),}
		js = (
			'https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js',
			'http://maps.google.com/maps/api/js?sensor=true',
			settings.STATIC_URL + 'django_google_maps/js/google-maps-admin.js',
		)

	def render(self, name, value, attrs=None):
		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
		if value != '':
			# Only add the 'value' attribute if a value is non-empty.
			final_attrs['value'] = force_unicode(self._format_value(value))
		return mark_safe(u'<input%s /><div class="map_canvas_wrapper"><div id="map_canvas"></div></div>' % flatatt(final_attrs))

class GeocodedAddressWidget(widgets.TextInput):
	class Media:
		js = (settings.STATIC_URL + 'django_google_maps/js/build_box.js',
		)
	def render(self, name, value, attrs=None):
		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
		if value != '':
			# Only add the 'value' attribute if a value is non-empty.
			final_attrs['value'] = force_unicode(self._format_value(value))
		return mark_safe(u'<input%s /><div id="build-bounds" class="build-box">BUILD BOX</div><div id="send-bounds" class="build-box">SEND BOUNDS</div>' % flatatt(final_attrs))

class DistanceFieldWidget(widgets.TextInput):
	def render(self, name, value, attrs=None):
		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name, value=10)
		if value != '':
			# Only add the 'value' attribute if a value is non-empty.
			final_attrs['value'] = force_unicode(self._format_value(value))
		return mark_safe( u'<input%s >' % flatatt(final_attrs) )
		
class GeolocationBoundsWidget(widgets.HiddenInput):
	def render(self, name, value, attrs=None):
		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
		if value != '':
			# Only add the 'value' attribute if a value is non-empty.
			final_attrs['value'] = force_unicode(self._format_value(value))
		return mark_safe( u'<input%s >' % flatatt(final_attrs) )
		