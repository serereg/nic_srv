
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
					document.getElementById("pv1").value = pars[0];
					document.getElementById("pv2").value = pars[1];
					document.getElementById("pv3").value = pars[2];
					document.getElementById("pv4").value = pars[3];
					document.getElementById("pv5").value = pars[4];
					document.getElementById("pv6").value = pars[5];
					document.getElementById("pv7").value = pars[6];
					document.getElementById("pv8").value = pars[7];
					document.getElementById("pv9").value = pars[8];
					document.getElementById("pv10").value = pars[9];
					document.getElementById("pv11").value = pars[10];
					document.getElementById("pv12").value = pars[11];
					document.getElementById("pv13").value = pars[12];
					
					var index = parseInt(document.getElementById("unitn").value, 10);
					document.getElementById("writedt").value = pars[2+index]; //request.responseText;
				}catch(exception)
				{
					document.getElementById("writedt").value = "jopa";
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
        document.getElementById("writedt").readOnly = "";
        document.getElementById("iseditable").value = "1";
        painterror();
    }
    else
    {
        document.getElementById("writedt").readOnly = "readonly";
        document.getElementById("iseditable").value = "0";
        document.getElementById("writedt").className = "monitor";
    }
}

function painterror()
{
    if (check_real(document.getElementById("writedt").value))
        document.getElementById("writedt").className = "edit";
    else
        document.getElementById("writedt").className = "error";
}

function keypressfield(key)
{
    if (key == "Enter")
    {
        if (check_real(document.getElementById("writedt").value))
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

function awrite()
{
    print_console("Запрос инициирован...");
    
    var params = "?val"+document.getElementById("unitn").value+"=" + document.getElementById("writedt").value;
    
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
	
	document.getElementById("writedt").value = "...";
	
	let i = 1;
	var uniti = parseInt(unit,10);
	while (i <= 12) 
	{ 
		if(i==uniti)
			document.getElementById("pv"+i).className = "selected";
		else
			document.getElementById("pv"+i).className = "monitor";
		i++;
	}
}
