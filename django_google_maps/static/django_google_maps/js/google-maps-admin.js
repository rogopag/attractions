
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

function googleMapAdmin() {

    var geocoder = new google.maps.Geocoder();
    var map;
    var marker;

    var self = {
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
                zoom = 18;
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
			map.fitBounds( bounds );
			boundingBoxPoints = [
	            box.ne, new google.maps.LatLng(box.ne.lat(), box.sw.lng()),
	            box.sw, new google.maps.LatLng(box.sw.lat(), box.ne.lng()), box.ne
	         ];
			boundingBox = new google.maps.Polyline({
	            path: boundingBoxPoints,
	            strokeColor: '#FF0000',
	            strokeOpacity: 1.0,
	            strokeWeight: 2
	         });

	         boundingBox.setMap(map);
		},
		doBoundingBox: function()
		{
			$('div.build-box').bind('mouseup', function(event){

				args = {
					'lat':$('#id_geolocation').val().split(',')[0],
					'lon':$('#id_geolocation').val().split(',')[1],
					'distance':$('#id_distance').val()
				};
				
				self.bounds( args.lat, args.lon, args.distance );

			});
		}
    }

    return self;
}

$(document).ready(function() {
    var googlemap = googleMapAdmin();
    googlemap.initialize();
	googlemap.doBoundingBox();
});
Number.prototype.radians = function()
{
	return this * Math.PI / 180;
};
Number.prototype.degrees = function()
{
	return this * 180 / Math.PI;
};