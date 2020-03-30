

function print_console(text){
	document.getElementById("status").value = text;
}

function aread()
{    
    print_console("Запрос инициирован...");
    
    var request = new XMLHttpRequest();
    request.open('GET',document.location.origin+'/states',true);
    request.addEventListener('readystatechange', function() {     
        
        if(request.readyState == 4)
        {
        	if(request.status==200)
        	{
				
				var ts2 = request.responseText;

				var pars = JSON.parse(ts2);

				try
				{
					let pv_html = new Array(12)
					let sp_html = new Array(12)
					let is_reg_on_html = new Array(12)
					let is_pv_fault_html = new Array(12)
					let is_reg_alarm_html = new Array(12)
					let plc_client_wdt = 0
					// parsing
					for (var i = 0; i < 7; i++) {
						pv_html[i] = parseFloat(pars.CKT[i].pv)
						sp_html[i] = parseFloat(pars.CKT[i].sp)
						is_reg_on_html[i] = pars.CKT[i].is_reg_on
						is_pv_fault_html[i] = pars.CKT[i].is_pv_fault
						is_reg_alarm_html[i] = pars.CKT[i].is_reg_alarm
					}
					plc_client_wdt = pars.plc_client_wdt
					
					for (var i = 0; i < 7; i++) {
						var num = i+1
						document.getElementById("pv"+num.toString()).value = pv_html[i].toFixed(2);
						document.getElementById("sp"+num.toString()).value = sp_html[i].toFixed(2);
						if (is_reg_on_html[i]=="True")
						{
							document.getElementById("plate"+num.toString()).className = "w3-container w3-card-4 " + " w3-green";
						}
						else
						{
							document.getElementById("plate"+num.toString()).className = "w3-container w3-card-4 " + " w3-light-grey";
						}
						if (is_pv_fault_html[i]=="True")
						{
							document.getElementById("pv"+num.toString()).className = "w3-input w3-border w3-round-large" + " w3-black";
						}
						else
						{
							if (is_reg_alarm_html[i]=="True")
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
					document.getElementById("write_sp").value = sp_html[index].toFixed(2); //request.responseText;
					if (is_reg_on_html[index]=="True")
					{
						document.getElementById("CmdOn").className = "w3-button w3-green";
						document.getElementById("CmdOff").className = "w3-button w3-green";
					}
					else
					{
						document.getElementById("CmdOn").className = "w3-button w3-black";
						document.getElementById("CmdOff").className = "w3-button w3-black";
					}
					
					print_console("Обмен c контроллером (количество посылок): "+plc_client_wdt);
				}catch(exception)
				{
					document.getElementById("write_sp").value = "exception";
				};
        	}
        	else
        	{
	            print_console("Ошибка:" + request.status);
        	}
        }

       });
   	request.setRequestHeader("Pragma", "no-cache");
	request.setRequestHeader("Cache-Control", "no-cache");

    request.send("");

}

function readval_t()
{
    if (document.getElementById("iseditable").value == "0")
        aread();
    setTimeout(readval_t, 1000);

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
    var params = "?cmd"+document.getElementById("unitn").value+"=YOn";
	var request = new XMLHttpRequest();
    request.open('GET',document.location.origin+'/command'+params,true);
	request.setRequestHeader("Pragma", "no-cache");
	request.setRequestHeader("Cache-Control", "no-cache");
	request.send("");
}

function cmdoff()
{
    var params = "?cmd"+document.getElementById("unitn").value+"=YOff";
	var request = new XMLHttpRequest();
    request.open('GET',document.location.origin+'/command'+params,true);
	request.setRequestHeader("Pragma", "no-cache");
	request.setRequestHeader("Cache-Control", "no-cache");
	request.send("");
}

function awrite()
{
    print_console("Запрос инициирован...");
    
    var params = "?val"+document.getElementById("unitn").value+"=" + document.getElementById("write_sp").value;
    
	//alert(params);
	
    var request = new XMLHttpRequest();
    request.open('GET',document.location.origin+'/command'+params,true);
    request.addEventListener('readystatechange', function() {   	        
        
        if(request.readyState == 4)
        {
        	if(request.status==200)
        	{
	            print_console("Обмен завершен успешно.");
        	}
        	else
        	{
	            print_console("Ошибка:" + request.status);
        	}
        }

       });
   	request.setRequestHeader("Pragma", "no-cache");
	request.setRequestHeader("Cache-Control", "no-cache");

    request.send("");
}


function setunit(unit)
{
	document.getElementById("unitn").value=unit;
	
	document.getElementById("write_sp").value = "...";
	
	let i = 1;
	var uniti = parseInt(unit,10);
	while (i <= 12) 
	{ 
		if(i==uniti)
			document.getElementById("pv"+i).style.color = white;//.className = "selected";
		else
			document.getElementById("pv"+i).style.color = red;//.className = "monitor";
		i++;
	}
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
