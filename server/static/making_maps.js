"use strict";

/* ===========================================================
 * XmlHttpRequest functions
 * -----------------------------------------------------------
*/

function generate_map() {
	var url = "/generatemap";
	var request = new XMLHttpRequest();
	request.onload = function() {
		if (request.status == 200) {
			var response = JSON.parse(request.responseText);
			if (response['meta']['status'] == 'ok') {
				addmap(response['content']);
			} else {
				alert('Map could not be generated: ' + response['meta']['reason']);
			}
		} else {
			alert('Server error');
		}
	}
	request.open("GET", url);
	request.send();
}

/* ===========================================================
 * Functions that manipulated the DOM
 * -----------------------------------------------------------
*/

function addmap(response) {
    var datacontainer = document.getElementById('datacontainer');
	var mapdata = document.getElementById('mapdata');

    var new_mapdata = document.createElement('div');
    new_mapdata.setAttribute('id', 'mapdata');

	var image = document.createElement('img');
	image.setAttribute('alt', 'The New Map');
    var response_nocache = response + "#" + new Date().getTime();
	image.setAttribute('src', response_nocache);

    new_mapdata.appendChild(image);

    datacontainer.replaceChild(new_mapdata, mapdata);
}
