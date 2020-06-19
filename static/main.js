var glob_auth = false

function onload() {
	let token = localStorage.getItem("token")
	// let token = true
	if (glob_auth) {
	// if (token) {
		document.getElementById("auth").style.display = "none"
		document.getElementById("panel").style.display = "block"
		get_state()
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


// REQUESTS
function auth() {
	username = document.getElementById("auth_username").value
	password = document.getElementById("auth_password").value

	send_http("login", {
		username: username,
		password: password,
		token: ""
	}, (data) => {
		if (data.result) {
			glob_auth = true
			localStorage.setItem("token", data.result.token)
			document.getElementById("auth").style.display = "none"
			document.getElementById("panel").style.display = "block"
			get_state()
		}
	})
}

function get_state() {
	send_ws("state", {})
	console.log("get_state() SEND")

	// if (localStorage.getItem("token")) {
	if (glob_auth) {
		showBusyTank();
		setTimeout(get_state, 1000)
	} else {
		//setTimeout(get_state, 1000)
		document.getElementById("auth").style.display = "block"
		document.getElementById("panel").style.display = "none"
	}
}

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
		setCookie("show_busy_tank","true",10);
	} else 
	{
		setCookie("show_busy_tank","false",10);
	}
}

function showBusyTank()
{
	let show = getCookie("show_busy_tank")
	if (show == "true")
	{
		document.getElementById('busyTank').checked = true;
		Ach = document.getElementsByClassName("w3-light-grey");
		for (i = 0; i < Ach.length; i++) Ach[i].parentNode.parentNode.parentNode.parentNode.parentNode.style.display = 'none';
		Ach = document.getElementsByClassName("w3-green");
		for (i = 0; i < Ach.length; i++) Ach[i].parentNode.parentNode.parentNode.parentNode.parentNode.style.display = '';
	} else {	
		document.getElementById('busyTank').checked = false;	
		Ach1 = document.getElementsByClassName("w3-light-grey");
		for (i = 0; i < Ach1.length; i++) Ach1[i].parentNode.parentNode.parentNode.parentNode.parentNode.style.display = '';

		Ach = document.getElementsByClassName("w3-green");
		for (i = 0; i < Ach.length; i++) Ach[i].parentNode.parentNode.parentNode.parentNode.parentNode.style.display = '';
	}
}

function send_description() {
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


function handler_ws(event) {
	let pars = JSON.parse(event.data).result
	console.log(pars)
	// console.log("GET MESSAGE: " + event.data)
	// Логика обновления данных

	// try {
	if (pars != null)
	{
		if (pars.hasOwnProperty("CKT"))
		{
			let pv_html = new Array(12)
			let sp_html = new Array(12)
			let is_reg_on_html = new Array(12)
			let is_pv_fault_html = new Array(12)
			let is_reg_alarm_html = new Array(12)
			let plc_client_wdt = 0
			// parsing
			pars.CKT.forEach(element => {
				let ckt_num = element.id - 1
				pv_html[ckt_num] = parseFloat(element.pv)
				sp_html[ckt_num] = parseFloat(element.sp)
				is_reg_on_html[ckt_num] = element.is_reg_on
				is_pv_fault_html[ckt_num] = element.is_pv_fault
				is_reg_alarm_html[ckt_num] = element.is_reg_alarm
			});
			// for (var i = 0; i < 12; i++) {
			// for (var i = 0; i < 1; i++) {
			// 	pv_html[i] = parseFloat(pars.CKT[i].pv)
			// 	sp_html[i] = parseFloat(pars.CKT[i].sp)
			// 	is_reg_on_html[i] = pars.CKT[i].is_reg_on
			// 	is_pv_fault_html[i] = pars.CKT[i].is_pv_fault
			// 	is_reg_alarm_html[i] = pars.CKT[i].is_reg_alarm
			// }
			plc_client_wdt = pars.plc_client_wdt
			
			//console.log(pars)

			// for (var i = 0; i < 12; i++) {
			for (var i = 0; i < 1; i++) {
				var num = i+1

				document.getElementById("description_plate"+num.toString()).value = pars.CKT[i].description //
				
				document.getElementById("pv"+num.toString()).value = pv_html[i].toFixed(1);
				document.getElementById("sp"+num.toString()).value = sp_html[i].toFixed(1);
				if (is_reg_on_html[i]==true)
				{
					document.getElementById("plate"+num.toString()).className = "w3-container w3-card-4 " + " w3-green";
				}
				else
				{
					document.getElementById("plate"+num.toString()).className = "w3-container w3-card-4 " + " w3-light-grey";
				}
				if (is_pv_fault_html[i]==true)
				{
					document.getElementById("pv"+num.toString()).className = "w3-input w3-border w3-round-large" + " w3-black";
				}
				else
				{
					if (is_reg_alarm_html[i]==true)
					{
						document.getElementById("pv"+num.toString()).className = "w3-input w3-border w3-round-large" + " w3-red";
					}
					else
					{
						document.getElementById("pv"+num.toString()).className = "w3-input w3-border w3-round-large";
					}
				}
			}
			// TODO: tempereture fault analyse
			var index = parseInt(document.getElementById("unitn").value, 10)-1;
			// document.getElementById("write_sp").value = sp_html[index].toFixed(1); //request.responseText;
			if (is_reg_on_html[index]==true)
			{
				document.getElementById("CmdOn").className = "w3-button w3-green";
				document.getElementById("CmdOff").className = "w3-button w3-green";
			}
			else
			{
				document.getElementById("CmdOn").className = "w3-button w3-black";
				document.getElementById("CmdOff").className = "w3-button w3-black";
			}
			
			print_console(plc_client_wdt + ": посылок от контроллера");
		}
	}
// } catch(exception) {
	// 	document.getElementById("write_sp").value = "exception";
	// };
}