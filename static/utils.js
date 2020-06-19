
var glob_socket = null
var glob_request_id = 0
// var requests = {}


// UTILS
function jsonrpc(method, params) {
	let token = localStorage.getItem("token")
	if (token != null) {
		params.token = token
	}
	if (++glob_request_id < 0) {
		glob_request_id = 1
	}
	let data = {
		jsonrpc: "2.0",
		method: method,
		id: glob_request_id,
		params: {},
	}
	for (key in params) {
		data.params[key] = params[key]
    }
    console.log(JSON.stringify(data))
	return JSON.stringify(data)
}

function send_http(method, params, handler) {
	fetch("http://"+window.location.host+"/api/client", { 
		method: "POST",
		body: jsonrpc(method, params),
	})
	.then(response => response.json())
	.then(data => {handler(data)})
}


function send_ws(method, params) {
	if (!glob_socket || glob_socket.readyState > 1) {
		glob_socket = new WebSocket("ws://"+window.location.host+"/ws/client")
		glob_socket.onmessage = handler_ws
	}
	if (glob_socket.readyState == WebSocket.CONNECTING) {
		glob_socket.onopen = function() {
			glob_socket.send(jsonrpc(method, params))
		}
	} else {
		glob_socket.send(jsonrpc(method, params))
	}
}

//
function setCookie(cname, cvalue, exdays) {
	var d = new Date();
	d.setTime(d.getTime() + (exdays*24*60*60*1000));
	var expires = "expires="+ d.toUTCString();
	document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
	var name = cname + "=";
	var decodedCookie = decodeURIComponent(document.cookie);
	var ca = decodedCookie.split(';');
	for(var i = 0; i <ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
}