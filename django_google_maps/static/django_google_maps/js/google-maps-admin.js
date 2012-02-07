
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

            $("#id_address").change(function() {
					console.log( "Changed "+$(this).val() );
					self.codeAddress();
				});
				
			this.doBoundingBox();
			this.sendBoxCoordinatesToServer();
        },

        getExistingLocation: function() {
            var geolocation = $("#id_geolocation").val();
            if (geolocation) {
                return geolocation.split(',');
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
			var distance = parseFloat(distance), radius = 3963.1, north = 0, south = 180, east = 90, west = 270, lat_r = parseFloat(lat).radians(), lon_r = parseFloat(lon).radians(), northmost, southmost, eastmost, westmost, lat1, lat2, lon1, lon2, box, bounds, boundingBoxPoints, boundingBox;
			
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
			bounds = new google.maps.LatLngBounds(box.sw, box.ne);
			
			this.coordsData = {'sw':[lat1, lon1], 'ne':[lat2, lon2], 'distance' : $('input[name="distance"]').val()};
			
			///Useful for polygon drawing
			
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

			});
		},
		clearOverlays: function()
		{
			if(this.hasOverlays)
			{
				while( overlays[0] ) overlays.pop().setMap(null) ;
			}
		},
		sendBoxCoordinatesToServer : function()
		{
			$('div#send-bounds').bind('mouseup', function(){
				if( self.coordsData )
				{
					$.ajax({  
							type: 'post',  
							url: ajaxurl,  
							data: self.coordsData,
							dataType: 'text',
							error: function(XMLHttpRequest, textStatus, errorThrown)
							{  
								console.log( XMLHttpRequest, textStatus, errorThrown );
							},
							beforeSend: function(XMLHttpRequest) 
							{ 
								console.log( XMLHttpRequest );
							}, 
							success: function( data, textStatus, jqXHR ){
								//console.log( XMLHttpRequest, textStatus, jqXHR );
								console.log( data );
							},
							complete: function( data, textStatus )
							{
								console.log( XMLHttpRequest, textStatus );
							}  
						});
				}
				else
				{
					console.log('build bounds first then submit request')
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
    }
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
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});