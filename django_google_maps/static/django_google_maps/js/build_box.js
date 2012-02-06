var ajaxurl = '/ajax';

$(function(){
	doBoundingBox();
});

function doBoundingBox()
{
	$('div.build-box').bind('mouseup', function(event){
	
		args = {
			'lat':$('#id_geolocation').val().split(',')[0],
			'lon':$('#id_geolocation').val().split(',')[1],
			'distance':$('#id_distance').val()
		};
		//console.log( bounds( args.lat, args.lon, args.distance ) );
		return;
		
	});
};
function bounds(lat, lon, distance)
{
	var distance = parseFloat(distance), radius = 3963.1, north = 0, south = 180, east = 90, west = 270, lat_r = parseFloat(lat).radians(), lon_r = parseFloat(lon).radians(), northmost, southmost, eastmost, westmost, lat1, lat2, lon1, lon2, box, bounds;
	
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
	box = {'nw' : new google.maps.LatLng(lat1, lon1), 'se' :new google.maps.LatLng(lat2, lon2) };
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