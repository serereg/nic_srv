

function print_console(text){
	document.getElementById("status").value = text;
}

function aread()
{    
    print_console("Запрос инициирован...");
    
    var request = new XMLHttpRequest();
    request.open('GET',document.location.origin+'/ahandler.htm',true);
    request.addEventListener('readystatechange', function() {     
        
        if(request.readyState == 4)
        {
        	if(request.status==200)
        	{
	            print_console("Обмен завершен успешно.");
				
				var pars = request.responseText.split(";");
				
				try
				{
					for (var i = 0; i < 12; i++) {
						var num = i+1
						document.getElementById("pv"+num.toString()).value = "T= "+pars[i]+" С;    Зд= "+pars[i+12];
						if (pars[24+i]=="True")
						{
							document.getElementById("pv"+num.toString()).className = "button_is_on";
						}
						else
						{
							document.getElementById("pv"+num.toString()).className = "button_is_off";
						}
					}
					
					var index = parseInt(document.getElementById("unitn").value, 10);
					document.getElementById("write_sp").value = pars[11+index]; //request.responseText;
					if (pars[23+index]=="True")
					{
						document.getElementById("CmdOn").className = "button_is_on";
						document.getElementById("CmdOff").className = "button_is_on";
					}
					else
					{
						document.getElementById("CmdOn").className = "button_is_off";
						document.getElementById("CmdOff").className = "button_is_off";
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
    request.open('GET',document.location.origin+'/ahandler.htm'+params,true);
	request.setRequestHeader("Pragma", "no-cache");
	request.setRequestHeader("Cache-Control", "no-cache");
	request.send("");
}

function cmdoff()
{
    var params = "?cmd"+document.getElementById("unitn").value+"=YOff";
	var request = new XMLHttpRequest();
    request.open('GET',document.location.origin+'/ahandler.htm'+params,true);
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
    request.open('GET',document.location.origin+'/ahandler.htm'+params,true);
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
