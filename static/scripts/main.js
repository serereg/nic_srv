
let pars__ = 
{
	CKT:[ 
		{id: 1, description: "БЛАНШ-13.5%↵15.07.20-ГБ", pv: 0.2, sp: 0.1, is_reg_on: false, is_pv_fault: false, is_reg_alarm: false},
		{id: 2, description: "Бланш- Готов↵", pv: 0.229, sp: 0, is_reg_on: true, is_pv_fault: false, is_reg_alarm: false},
		{id: 3, description: "Бланш Россия 23.07.20↵-НП-13.5%.↵ГБ на 22°с", pv: 0.667, sp: 0, is_reg_on: true, is_pv_fault: false, is_reg_alarm: true},
		{id: 4, description: "ЛАГЕР-25.03.20↵НП-12.5%-КП-3%", pv: 0.398, sp: 0, is_reg_on: false, is_pv_fault: true, is_reg_alarm: true},
		{id: 5, description: "Lager↵19.03↵19.04↵13%-3.5%↵4.8alk", pv: 0.09, sp: 0.009, is_reg_on: false, is_pv_fault: false, is_reg_alarm: true},
		{id: 6, description: " ИПА-Готовая", pv: -0.09, sp: 0, is_reg_on: false, is_pv_fault: true, is_reg_alarm: false},
		{id: 7, description: " ИПА-Тонна/14.07.20↵ -НП-15%_ГБ-22", pv: 0.292, sp: 0, is_reg_on: true, is_pv_fault: false, is_reg_alarm: true},
		{id: 8, description: "ПУСТАЯ Чистая", pv: 15.125, sp: 0, is_reg_on: false, is_pv_fault: false, is_reg_alarm: true},
		{id: 9, description: " ", pv: 848.0, sp: 5.51, is_reg_on: false, is_pv_fault: false, is_reg_alarm: true},
		{id: 10, description: " ", pv: 848.0, sp: 10.5, is_reg_on: false, is_pv_fault: false, is_reg_alarm: true},
		{id: 11, description: " ", pv: 848.0, sp: 11, is_reg_on: false, is_pv_fault: false, is_reg_alarm: true},
		{id: 12, description: " ", pv: 848.0, sp: 12, is_reg_on: false, is_pv_fault: false, is_reg_alarm: true} 
	],
	plc_client_wdt: 7474
}

var glob_auth = false

// REQUESTS
function auth() {
	username = document.getElementById("auth_username").value
	password = document.getElementById("auth_password").value

/*		// TODO: delete
 	if(username == "Igor")
	{
		glob_auth = true
		document.getElementById("auth").style.display = "none"
		document.getElementById("panel").style.display = "block"
		get_state()
	}	
*/	 
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
	send_ws("state", {}, handler_ws)
	handler_ws() //
	console.log("get_state() SEND")
	// if (localStorage.getItem("token")) {
	if (glob_auth) {
		
		setTimeout(get_state, 1000)
	} else {
		document.getElementById("auth").style.display = "block"
		document.getElementById("panel").style.display = "none"
	}
}

function cmd_on()
{
	send_ws("command", {
		"id": app.curent_cooler_for_editing,
		"switch": "YOn"
	})
}

function cmd_off()
{
	send_ws("command", {
		"id": app.curent_cooler_for_editing,
		"switch": "YOff"
	})
}

function send_description() {
	pack = {
		"method": "set_description",
		"params": {
			"id": app.curent_cooler_for_editing,
			"description": app.coolers[app.curent_cooler_for_editing-1].description,
		},
	}
	send_ws("set_description", {
			"id": app.curent_cooler_for_editing,
			"description": app.coolers[app.curent_cooler_for_editing-1].description,
		})
}

function handler_ws(event) {
	let pars = pars__//JSON.parse(event.data).result
	console.log(pars)
	// console.log("GET MESSAGE: " + event.data)
	// Логика обновления данных
	if (pars != null)
	{
		if (pars.hasOwnProperty("CKT"))
		{
			pars.CKT.forEach(element => {
				app.coolers[element.id-1].pv = element.pv
				app.coolers[element.id-1].sp = element.sp
				app.coolers[element.id-1].is_reg_on = element.is_reg_on
				app.coolers[element.id-1].is_pv_fault = element.is_pv_fault
				app.coolers[element.id-1].is_reg_alarm = element.is_reg_alarm
				app.coolers[element.id-1].description = element.description
			});
		}
		app.connection_watchdog = pars.plc_client_wdt
	}
}