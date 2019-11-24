

function print_console(text){
	document.getElementById("status").value = text;
}

function aread()
{    
    print_console("Запрос инициирован...");
    
    var request = new XMLHttpRequest();
    request.open('GET',document.location.origin+'/status',true);
    request.addEventListener('readystatechange', function() {     
        
        if(request.readyState == 4)
        {
        	if(request.status==200)
        	{
	            print_console("Обмен с веб-сервером завершен успешно.");
				
				var pars = request.responseText.split(";");
				
				try
				{
					for (var i = 0; i < 12; i++) {
						var num = i+1
						document.getElementById("pv"+num.toString()).value = pars[i]+" С";
						document.getElementById("sp"+num.toString()).value = pars[i+12]+" С";
						if (pars[24+i]=="True")
						{
							document.getElementById("pv"+num.toString()).className = "w3-input w3-border w3-round-large";
							document.getElementById("plate"+num.toString()).className = "w3-container w3-card-4 " + " w3-green";
						}
						else
						{
							document.getElementById("pv"+num.toString()).className = "w3-input w3-border w3-round-large";
							document.getElementById("plate"+num.toString()).className = "w3-container w3-card-4 " + " w3-light-gray";
						}
					}
					
					var index = parseInt(document.getElementById("unitn").value, 10);
					document.getElementById("write_sp").value = pars[11+index]; //request.responseText;
					if (pars[23+index]=="True")
					{
						document.getElementById("CmdOn").className = "w3-button w3-green";
						document.getElementById("CmdOff").className = "w3-button w3-green";
					}
					else
					{
						document.getElementById("CmdOn").className = "w3-button w3-black";
						document.getElementById("CmdOff").className = "w3-button w3-black";
					}
					
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
