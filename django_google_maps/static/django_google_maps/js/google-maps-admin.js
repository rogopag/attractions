
/*
Integration for Google Maps in the django admin.

How it works:

You have an address field on the page.
Enter an address and an on change event will update the map
with the address. A marker will be placed at the address.
If the user needs to move the marker, they can and the geolocation
field will be updated.

Only one marker will remain present on the map at a time.

This script expects:

<input type="text" name="address" id="id_address" />
<input type="text" name="geolocation" id="id_geolocation" />

<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>

*/
var ajaxurl = '/ajax';

django.jQuery(document).ready(function($) {
	var googlemap = googleMapAdmin();
	googlemap.initialize();
});

function googleMapAdmin() {

	var geocoder = new google.maps.Geocoder(), map, marker, overlays = new Array();

	var self = {
		coordsData : null,
		name : null,
		initialize: function() {
			var lat = 0;
			var lng = 0;
			var zoom = 2;
			// set up initial map to be world view. also, add change
			// event so changing address will update the map
			existinglocation = self.getExistingLocation();
			if (existinglocation) {
				lat = existinglocation[0];
				lng = existinglocation[1];
				zoom = 12;
			}

			var latlng = new google.maps.LatLng(lat,lng);
			var myOptions = {
				zoom: zoom,
				center: latlng,
				mapTypeId: google.maps.MapTypeId.ROADMAP
			};
			map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
			if (existinglocation) {
				self.setMarker(latlng);
			}

			if( this.getExistingBounds() )
			{
				var box = this.getExistingBounds();
				this.drawBounds( box );
				this.placeVertexToBox( box );
				this.coordsData = {'sw':[box.sw.lat(), box.sw.lng()], 'ne':[box.ne.lat(), box.ne.lng()], 'distance' : $('input[name="distance"]').val()};
			}

			$("#id_address").change(function() {
				console.log( "Changed "+$(this).val() );
				self.codeAddress();
			});

			this.doBoundingBox();
			this.sendBoxCoordinatesToServer();
			this.stopCollecting();
		},

		getExistingLocation: function() {
			var geolocation = $("#id_geolocation").val();
			if (geolocation) {
				return geolocation.split(',');
			}
		},
		getExistingBounds: function()
		{
			if( $('#id_bound_sw').val() && $('#id_bound_ne').val() )
			{
				return {'sw' : new google.maps.LatLng( $('#id_bound_sw').val().split(',')[0], $('#id_bound_sw').val().split(',')[1] ), 'ne' :new google.maps.LatLng( $('#id_bound_ne').val().split(',')[0], $('#id_bound_ne').val().split(',')[1] ) };
			}
			else
			{
				return false;
			}

		},
		codeAddress: function() {
			var address = $("#id_address").val();
			geocoder.geocode({'address': address}, function(results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					var latlng = results[0].geometry.location;
					map.setCenter(latlng);
					map.setZoom(18);

					self.setMarker(latlng);
					self.updateGeolocation(latlng);
				} else {
					alert("Geocode was not successful for the following reason: " + status);
				}
			});
		},

		setMarker: function(latlng) {
			if (marker) {
				self.updateMarker(latlng);
			} else {
				self.addMarker({'latlng': latlng, 'draggable': true});
			}
		},

		addMarker: function(Options) {
			marker = new google.maps.Marker({
				map: map,
				position: Options.latlng
			});

			var draggable = Options.draggable || false;
			if (draggable) {
				self.addMarkerDrag(marker);
			}
		},

		addMarkerDrag: function() {
			marker.setDraggable(true);
			google.maps.event.addListener(marker, 'dragend', function(new_location) {
				self.updateGeolocation(new_location.latLng);
			});
		},

		updateMarker: function(latlng) {
			marker.setPosition(latlng);
		},

		updateGeolocation: function(latlng) {
			$("#id_geolocation").val(latlng.lat() + "," + latlng.lng());
		},
		bounds: function(lat, lon, distance)
		{
			/// declare vars 
			var distance = parseFloat(distance), radius = 3963.1, north = 0, south = 180, east = 90, west = 270, lat_r = parseFloat(lat).radians(), lon_r = parseFloat(lon).radians(), northmost, southmost, eastmost, westmost, lat1, lat2, lon1, lon2, box;

			northmost = ( Math.asin( Math.sin(lat_r) * Math.cos( distance / radius ) + Math.cos(lat_r) * Math.sin( distance / radius ) * Math.cos(north) ) ).degrees();
			southmost = ( Math.asin( Math.sin(lat_r) * Math.cos( distance / radius ) + Math.cos(lat_r) * Math.sin( distance / radius ) * Math.cos(south) ) ).degrees();

			eastmost = ( lon_r + Math.atan2( Math.sin(east) * Math.sin( distance / radius ) * Math.cos(lat_r), Math.cos( distance / radius ) - Math.sin(lat_r) * Math.sin(lat_r) ) ).degrees();
			westmost = ( lon_r + Math.atan2( Math.sin(west) * Math.sin( distance / radius ) * Math.cos(lat_r), Math.cos( distance / radius ) - Math.sin(lat_r) * Math.sin(lat_r) ) ).degrees();

			if( northmost > southmost)
			{
				lat1 = southmost;
				lat2 = northmost;
			}
			else
			{
				lat1 = northmost;
				lat2 = southmost;
			}
			if( eastmost > westmost )
			{
				lon1 = westmost;
				lon2 = eastmost;
			}
			else
			{
				lon1 = eastmost;
				lon2 = westmost;
			}	
			box = {'sw' : new google.maps.LatLng(lat1, lon1), 'ne' :new google.maps.LatLng(lat2, lon2) };

			//for debug purposes check the bounds visually on the map


			this.coordsData = {'sw':[lat1, lon1], 'ne':[lat2, lon2], 'distance' : $('input[name="distance"]').val()};

			///Useful for polygon drawing
			this.drawBounds( box );

		},
		placeVertexToBox: function(box)
		{
			for(var c in box)
			{
				var marker = new google.maps.Marker({
					position: box[c],
					map: map,
					title: box[c].toString()
				});
			}
		},
		drawBounds: function( box )
		{
			var bounds, boundingBoxPoints, boundingBox;

			bounds = new google.maps.LatLngBounds(box.sw, box.ne);

			boundingBoxPoints = [
			box.ne, new google.maps.LatLng(box.ne.lat(), box.sw.lng()),
			box.sw, new google.maps.LatLng(box.sw.lat(), box.ne.lng()), box.ne
			];

			/// we're using a simple rectangle so we just need sw and ne coords
			boundingBox = new google.maps.Polyline({
				path: boundingBoxPoints,
				strokeColor: '#FF3311',
				strokeOpacity: 0.8,
				strokeWeight: 3,
				editable:false
			});

			overlays.push( boundingBox );

			map.fitBounds( bounds );

			boundingBox.setMap(map);
		},
		hasOverlays: function()
		{
			return overlays.length;
		},
		doBoundingBox: function()
		{
			$('div#build-bounds').bind('mouseup', function(event){

				self.clearOverlays();

				args = {
					'lat':$('#id_geolocation').val().split(',')[0],
					'lon':$('#id_geolocation').val().split(',')[1],
					'distance':$('#id_distance').val()
				};

				self.bounds( args.lat, args.lon, args.distance );

				$('#id_bound_sw').val( self.coordsData.sw );
				$('#id_bound_ne').val( self.coordsData.ne );

			});
		},
		clearOverlays: function()
		{
			if(this.hasOverlays)
			{
				while( overlays[0] ) overlays.pop().setMap(null) ;
			}
		},
		stopCollecting: function()
		{
			$('div#stop-collecting').bind('mouseup', function(){
				
				var st = $('input[name="sample_task"]').val();
				
				if( !st || st  == '' )
				{
					alert("No task running");
					return false;
				}
				else
				{
					self.coordsData.stop = 'stop';
					self.coordsData.name = $('input[name="bound_name"]').val();
					self.coordsData.sample_task = st;
					if( !self.coordsData.name )
					{
						alert('Give your search a name before stopping');
						return false;
					}
					$.ajax({  
						type: 'post',  
						url: ajaxurl,  
						data: {command: JSON.stringify( self.coordsData ) },
						dataType: 'json',
						error: function(XMLHttpRequest, textStatus, errorThrown)
						{  
							console.log( textStatus, errorThrown );
						},
						beforeSend: function(XMLHttpRequest) 
						{ 
							if (XMLHttpRequest && XMLHttpRequest.overrideMimeType) 
							{
								XMLHttpRequest.overrideMimeType("application/j-son;charset=UTF-8");
							}
						}, 
						success: function( data, textStatus, jqXHR ){
							//console.log( XMLHttpRequest, textStatus, jqXHR );
							console.log( data );
							$('input[name="sample_task"]').val('');
							delete self.coordsData.stop;
							delete self.coordsData.sample_task;
						},
						complete: function( data, textStatus )
						{
							//console.log( data, textStatus );
						}  
					});
				}
			});
		},
		sendBoxCoordinatesToServer : function()
		{
			$('div#send-bounds').bind('mouseup', function(){
				
				var st = $('input[name="sample_task"]').val();
				
				if( ( !st || '' == st ) && self.coordsData )
				{
					self.coordsData.name = $('input[name="bound_name"]').val();
					
					if( !self.coordsData.name )
					{
						alert('Give your search a name before submitting to worker');
						return false;
					}
					$.ajax({  
						type: 'post',  
						url: ajaxurl,  
						data: {command: JSON.stringify(self.coordsData) },
						dataType: 'json',
						error: function(XMLHttpRequest, textStatus, errorThrown)
						{  
							console.log( textStatus, errorThrown );
						},
						beforeSend: function(XMLHttpRequest) 
						{ 
							if (XMLHttpRequest && XMLHttpRequest.overrideMimeType) 
							{
								XMLHttpRequest.overrideMimeType("application/j-son;charset=UTF-8");
							}
						}, 
						success: function( data, textStatus, jqXHR ){
							//console.log( XMLHttpRequest, textStatus, jqXHR );
							console.log( data );
							$('input[name="sample_task"]').val(data.sample_task);
						},
						complete: function( data, textStatus )
						{
							//console.log( data, textStatus );
						}  
					});
				}
				else
				{
					alert('Task already running')
				}
			});
		}
	}

	return self;
};
Number.prototype.radians = function()
{
	return this * Math.PI / 180;
};
Number.prototype.degrees = function()
{
	return this * 180 / Math.PI;
};
// A function hooked to ajaxSend event to send nonce on POST request
$(document).ajaxSend(function(event, xhr, settings) {
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	};
	function sameOrigin(url) {
		// url could be relative or scheme relative or absolute
		var host = document.location.host; // host + port
		var protocol = document.location.protocol;
		var sr_origin = '//' + host;
		var origin = protocol + sr_origin;
		// Allow absolute or scheme relative URLs to same origin
		return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
		(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
		// or any other URL that isn't scheme relative or absolute i.e relative.
		!(/^(\/\/|http:|https:).*/.test(url));
	};
	function safeMethod(method) {
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	};

	if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
		xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	}
});