
var glob_socket = null
var glob_request_id = 0
var requests = {}
var ws_handlers = {}

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
	requests[glob_request_id] = method
	return JSON.stringify(data)
}

function get_ws(event) {
	let data = JSON.parse(event.data)
	handler = ws_handlers[requests[data["id"]]]
	if (handler) {
		handler(data)
	}
}

function send_ws(method, params) {
	if (!glob_socket || glob_socket.readyState > 1) {
		glob_socket = new WebSocket("ws://"+window.location.host+"/ws/client")
		glob_socket.onmessage = get_ws
	}
	if (glob_socket.readyState == WebSocket.CONNECTING) {
		glob_socket.onopen = function() {
			glob_socket.send(jsonrpc(method, params))
		}
	} else {
		glob_socket.send(jsonrpc(method, params))
	}
}

function send_http(method, params, handler) {
	fetch("http://"+window.location.host+"/api/client", { 
		method: "POST",
		body: jsonrpc(method, params),
	})
	.then(response => response.json())
	.then(data => {handler(data)})
}

// WS
function ws_get_state() {
	send_ws("state", {})

	if (localStorage.getItem("token")) {
		setTimeout(ws_get_state, 1000)
	} else {
		document.getElementById("auth").style.display = "block"
		document.getElementById("panel").style.display = "none"
	}
}

function ws_handle_get_state(data) {
	data = data.result
	let pv_html = new Array(12)
	let sp_html = new Array(12)
	let descriptions = new Array(12)
	let is_reg_on_html = new Array(12)
	let is_pv_fault_html = new Array(12)
	let is_reg_alarm_html = new Array(12)
	let plc_client_wdt = 0

	for (let i = 0; i < 12; i++) {
		pv_html[data.CKT[i].id - 1] = parseFloat(data.CKT[i].pv)
		sp_html[data.CKT[i].id - 1] = parseFloat(data.CKT[i].sp)
		descriptions[data.CKT[i].id - 1] = data.CKT[i].description
		is_reg_on_html[data.CKT[i].id - 1] = data.CKT[i].is_reg_on
		is_pv_fault_html[data.CKT[i].id - 1] = data.CKT[i].is_pv_fault
		is_reg_alarm_html[data.CKT[i].id - 1] = data.CKT[i].is_reg_alarm
	}
	plc_client_wdt = data.plc_client_wdt
		
	for (let i = 0; i < 12; i++) {
		let num = i+1

		document.getElementById("description_plate"+num.toString()).value = descriptions[i]

		document.getElementById("pv"+num.toString()).value = pv_html[i].toFixed(2);
		document.getElementById("sp"+num.toString()).value = sp_html[i].toFixed(2);
		if (is_reg_on_html[i]) {
			document.getElementById("plate"+num.toString()).className = "w3-container w3-card-4 " + " w3-green";
		} else {
			document.getElementById("plate"+num.toString()).className = "w3-container w3-card-4 " + " w3-light-grey";
		}
		if (is_pv_fault_html[i]) {
			document.getElementById("pv"+num.toString()).className = "w3-input w3-border w3-round-large" + " w3-black";
		} else if (is_reg_alarm_html[i]) {
			document.getElementById("pv"+num.toString()).className = "w3-input w3-border w3-round-large" + " w3-red";
		} else {
			document.getElementById("pv"+num.toString()).className = "w3-input w3-border w3-round-large"
		}
	}
		
	let index = parseInt(document.getElementById("unitn").value, 10)-1;
	// document.getElementById("write_sp").value = sp_html[index].toFixed(2); //request.responseText;
	if (is_reg_on_html[index]) {
		document.getElementById("CmdOn").className = "w3-button w3-green";
		document.getElementById("CmdOff").className = "w3-button w3-green";
	} else {
		document.getElementById("CmdOn").className = "w3-button w3-black";
		document.getElementById("CmdOff").className = "w3-button w3-black";
	}
	
	print_console(plc_client_wdt + ": посылок от контроллера");
	// } catch(exception) {
	// 	document.getElementById("write_sp").value = "exception";
	// };
}

function ws_set_description() {
	//var socket = new WebSocket("ws://"+window.location.host+"/ws/client")
	
	pack = {
		"method": "set_description",
		"params": {
			"id": parseInt(document.getElementById("unitn_desc").value, 10),
			"description": document.getElementById("ckt_description").value, 
		},
	}
	//console.log(pack)
	//glob_socket.send(JSON.stringify(pack))
	send_ws("set_description", {
			"id": parseInt(document.getElementById("unitn_desc").value, 10),
			"description": document.getElementById("ckt_description").value, 
		})
}

function ws_handle_set_description(data) {

}

// REQUESTS
function auth() {
	username = document.getElementById("auth_username").value
	password = document.getElementById("auth_password").value

	send_http("login", {
		username: username,
		password: password,
	}, (data) => {
		if (data.result) {
			localStorage.setItem("token", data.result.token)
			document.getElementById("auth").style.display = "none"
			document.getElementById("panel").style.display = "block"
			ws_get_state()
		}
	})
}

// OTHER
function print_console(text){
	document.getElementById("status").value = text;
}

function check_real(str)
{
    let result = str.match(/^[+-]?\d+(\.\d+)?$/);

    return result != null;
}

function dbclickfield()
{
    set_editable(true);
}

function set_editable(val)
{
    if (val)
    {
        document.getElementById("write_sp").readOnly = "";
        document.getElementById("iseditable").value = "1";
        painterror();
    }
    else
    {
        document.getElementById("write_sp").readOnly = "readonly";
        document.getElementById("iseditable").value = "0";
        document.getElementById("write_sp").className = "monitor";
    }
}

function painterror()
{
    if (check_real(document.getElementById("write_sp").value))
        document.getElementById("write_sp").className = "edit";
    else
        document.getElementById("write_sp").className = "error";
}

function keypressfield(key)
{
    if (key == "Enter")
    {
        if (check_real(document.getElementById("write_sp").value))
        {
            awrite();
            set_editable(false);
        }
        else
        {
            alert("Неверный формат числа");
        }
    }
    else if(key == "Escape")
    {
        set_editable(false);
    }
    else
    {
        if (document.getElementById("iseditable").value == "1")
            painterror();
    }
}

function cmdon()
{
	send_ws("command", {
		"id": parseInt(document.getElementById("unitn").value, 10),
		"switch": "YOn"
	})
}

function cmdoff()
{
	send_ws("command", {
		"id": parseInt(document.getElementById("unitn").value, 10),
		"switch": "YOff"
	})
}

function awrite()
{
    send_ws("set_point", {
		"id": parseInt(document.getElementById("unitn").value, 10),
		"set_point": document.getElementById("write_sp").value
	})
}


function setunit(unit)
{
	document.getElementById("unitn").value=unit;
	
	document.getElementById("write_sp").value = "...";
	
	let i = 1;
	var uniti = parseInt(unit,10);
	// while (i <= 12) 
	// { 
	// 	if(i==uniti)
	// 		document.getElementById("pv"+i).style.color = white;//.className = "selected";
	// 	else
	// 		document.getElementById("pv"+i).style.color = red;//.className = "monitor";
	// 	i++;
	// }
}

function checkBoxEvent() {
	if (document.getElementById('busyTank').checked)
	{

		Ach = document.getElementsByClassName("w3-light-grey");
		for (i = 0; i < Ach.length; i++) Ach[i].parentNode.parentNode.parentNode.parentNode.parentNode.style.display = 'none';
		Ach = document.getElementsByClassName("w3-green");
		for (i = 0; i < Ach.length; i++) Ach[i].parentNode.parentNode.parentNode.parentNode.parentNode.style.display = '';
	} else {

		Ach1 = document.getElementsByClassName("w3-light-grey");
		for (i = 0; i < Ach1.length; i++) Ach1[i].parentNode.parentNode.parentNode.parentNode.parentNode.style.display = '';

		Ach = document.getElementsByClassName("w3-green");
		for (i = 0; i < Ach.length; i++) Ach[i].parentNode.parentNode.parentNode.parentNode.parentNode.style.display = '';
	}
}

function onload() {
	ws_handlers["state"] = ws_handle_get_state
	ws_handlers["set_description"] = ws_handle_set_description

	let token = localStorage.getItem("token")
	if (token) {
		document.getElementById("auth").style.display = "none"
		document.getElementById("panel").style.display = "block"
		ws_get_state()
	} else {
		document.getElementById("auth").style.display = "block"
		document.getElementById("panel").style.display = "none"
	}

	// function send() {
	// 	if (document.getElementById("iseditable").value == "0") {
	// 		socket.send(JSON.stringify({"method": "state"}))
	// 		setTimeout(send, 1000)
	// 	}
	// }
}