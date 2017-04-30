/*!
 * IP Address geocoding API for Google Maps
 * http://lab.abhinayrathore.com/ipmapper/
 * Last Updated: June 13, 2012
 */
var IPMapper = {
	map: null,
	mapTypeId: google.maps.MapTypeId.ROADMAP,
	latlngbound: null,
	infowindow: null,
	baseUrl: "https://geoip.nekudo.com/api/",
	initializeMap: function(mapId){
		IPMapper.latlngbound = new google.maps.LatLngBounds();
		var latlng = new google.maps.LatLng(0, 0);
		//set Map options
		var mapOptions = {
			zoom: 17,
			center: latlng,
			mapTypeId: IPMapper.mapTypeId
		}
		//init Map
		IPMapper.map = new google.maps.Map(document.getElementById(mapId), mapOptions);
		//init info window
		IPMapper.infowindow = new google.maps.InfoWindow();
		//info window close event
		google.maps.event.addListener(IPMapper.infowindow, 'closeclick', function() {
			//IPMapper.map.fitBounds(IPMapper.latlngbound);
			IPMapper.map.panToBounds(IPMapper.latlngbound);
		});
	},
	addIPArray: function(ipArray){
		ipArray = IPMapper.uniqueArray(ipArray); //get unique array elements
		//add Map Marker for each IP
		for (var i = 0; i < ipArray.length; i++){
			IPMapper.addIPMarker(ipArray[i]);
		}
	},
	addIPMarker: function(ip){
		ipRegex = /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/;
		if($.trim(ip) != '' && ipRegex.test(ip)){ //validate IP Address format
			var url = encodeURI(IPMapper.baseUrl + ip + "?callback=?"); //geocoding url
			$.getJSON(url, function(data) { //get Geocoded JSONP data
				if($.trim(data.location.latitude) != '' && data.location.latitude != '0' && !isNaN(data.location.latitude)){ //Geocoding successfull
					var latitude = data.location.latitude;
					var longitude = data.location.longitude;
					var contentString = "";

					if(data.city){
						contentString += '<b>CITY: </b>' + data.city + '<br />';
					}
					contentString += '<b>COUNTRY: </b>' + data.country.name + '<br />' +
													 '<b>TIME ZONE: </b>' + data.location.time_zone + '<br />' +
														'<b>IP: </b>' + data.ip + '<br />';
					var latlng = new google.maps.LatLng(latitude, longitude);
					var marker = new google.maps.Marker({ //create Map Marker
						map: IPMapper.map,
						draggable: false,
						position: latlng
					});
					IPMapper.placeIPMarker(marker, latlng, contentString); //place Marker on Map
				} else {
					IPMapper.logError('IP Address geocoding failed!');
					$.error('IP Address geocoding failed!');
				}
			});
		} else {
			IPMapper.logError('Invalid IP Address!');
			$.error('Invalid IP Address!');
		}
	},
	placeIPMarker: function(marker, latlng, contentString){ //place Marker on Map
		marker.setPosition(latlng);

		// add click callback
		google.maps.event.addListener(marker, 'click', function() {
			IPMapper.getIPInfoWindowEvent(marker, contentString);
		});

		// trigger click to open details by default
		google.maps.event.trigger(marker, 'click');

		IPMapper.latlngbound.extend(latlng);
		IPMapper.map.setCenter(IPMapper.latlngbound.getCenter());
		//IPMapper.map.fitBounds(IPMapper.latlngbound);
		IPMapper.map.setZoom(17);
	},
	getIPInfoWindowEvent: function(marker, contentString){ //open Marker Info Window
		IPMapper.infowindow.close()
		IPMapper.infowindow.setContent(contentString);
		IPMapper.infowindow.open(IPMapper.map, marker);
	},
	uniqueArray: function(inputArray){ //return unique elements from Array
		var a = [];
		for(var i=0; i<inputArray.length; i++) {
			for(var j=i+1; j<inputArray.length; j++) {
				if (inputArray[i] === inputArray[j]) j = ++i;
			}
			a.push(inputArray[i]);
		}
		return a;
	},
	logError: function(error){
		if (typeof console == 'object') { console.error(error); }
	}
}
